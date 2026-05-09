from sqlalchemy.orm import Session
from models.pharmacy import Drug
from sqlalchemy import text
from models.pharmacysale import PharmacySale
from models.user import User
from datetime import datetime,timedelta
from schemas.pharmacy import DrugCreate,DrugUpdate
from utils.date_range import get_period_range
def create_drug(db:Session,current_user:User,data):
    drug=Drug(hospital_id=current_user.hospital_id,name=data.name,category=data.category,unit=data.unit,buying_price=data.buying_price,selling_price=data.selling_price,quantity_in_stock=data.quantity_in_stock,reorder_level=data.reorder_level)
    db.add(drug)
    db.commit()
    db.refresh(drug)
    return drug
def update_drug(db:Session,drug_id:int,current_user:User,data):
    drug=db.query(Drug).filter(Drug.drug_id==drug_id,Drug.hospital_id==current_user.hospital_id).first()
    if not drug:
        raise ValueError("Drug not found")
    for key,value in data.dict(exclude_unset=True).items():
        setattr(drug,key,value)
    db.commit()
    db.refresh(drug)
    return drug
def get_drugs(db:Session,current_user:User):
    return db.query(Drug).filter(Drug.hospital_id==current_user.hospital_id).all()
def dispense_drug(db:Session,current_user:User,data):
    drug=db.query(Drug).filter(Drug.hospital_id==current_user.hospital_id).first()
    if not drug:
        raise ValueError("Drug not found")
    if drug.quantity_in_stock < data.quantity:
        raise ValueError("Insufficient stock")
    total_price=float(drug.selling_price)*data.quantity
    sale=PharmacySale(hospital_id=current_user.hospital_id,drug_id=data.drug_id,quantity=data.quantity,total_price=total_price,payment_method=data.payment_method.lower())
    drug.quantity_in_stock -= data.quantity
    db.add(sale)
    db.commit()
    db.refresh(sale)
    return sale
def pharmacy_sales_summary(db:Session,current_user:User,period:str):
    start,end=get_period_range(period)
    query=text("""SELECT
    COUNT(*) AS total_sales,
               COALESCE(SUM(total_price),0)AS revenue
               FROM pharmacy_sales
               WHERE hospital_id=:hospital_id
               AND sold_at::date=CURRENT_DATE
               """)
    data=db.execute(query,{
                "hospital_id":current_user.hospital_id,
                "start":start,
                "end":end
               }).fetchone()
    inventory_query=text("""
                         SELECT
                         COALESCE(
                         SUM(
                         quantity_in_stock * buying_price),0)
                         FROM drugs
                         WHERE hospital_id=:hospital_id
                         """)
    inventory=db.execute(
        inventory_query,
        {
            "hospital_id":current_user.hospital_id
        }
    ).fetchone()
    profit=pharmcy_profit_summary(db,current_user,period)
    return {
        "total_sales":data[0],
        "revenue":float(data[1] or 0),
        "inventory_value":float(inventory[0] or 0),
        "profit":profit["profit"]
    }
def top_selling_drugs(db:Session,current_user:User):
    query=text("""SELECT
               d.name,
               SUM(ps.quantity) AS quantity_sold,
               SUM(ps.total_price) AS revenue
               FROM pharmacy_sales ps
               JOIN drugs d
               ON d.drug_id=ps.drug_id
               WHERE ps.hospital_id=:hospital_id
               GROUP BY d.name
               ORDER BY quantity_sold DESC
               LIMIT 5
               """)
    data=db.execute(query,{
        "hospital_id":current_user.hospital_id
    }).fetchall()
    return [
        {
            "name":row[0],
            "quantity_sold":row[1],
            "revenue":float(row[2] or 0)
        }
        for row in data
    ]
def low_stock_drugs(db:Session,current_user:User):
    return db.query(Drug).filter(Drug.hospital_id==current_user.hospital_id,Drug.quantity_in_stock <=Drug.reorder_level).all()
def pharmacy_payment_distribution(db:Session,current_user:User,period:str):
    start,end=get_period_range(period)
    query=text("""
               SELECT
               CASE
               WHEN
               LOWER(TRIM(payment_method))='cash'
               THEN 'Cash'
               WHEN REPLACE(
               LOWER(TRIM(payment_method)),
               '_',
               '')='mpesa'
               THEN 'M-Pesa'
               WHEN LOWER(TRIM(payment_method))='insurance'
               THEN 'Insurance'
               ELSE 'Other'
               END AS method,
               SUM(total_price) AS amount
               FROM pharmacy_sales
               WHERE hospital_id=:hospital_id
               AND sold_at BETWEEN :start AND :end
               GROUP BY method
               ORDER BY amount DESC
               """)
    data=db.execute(query,{
        "hospital_id":current_user.hospital_id,
        "start":start,
        "end":end
    }).fetchall()
    return [
        {
            "method":row[0],
            "amount":float(row[1] or 0)
        }
        for row in data
    ]
def pharmacy_revenue_trend(db:Session,current_user:User,period:str):
    start,end=get_period_range(period)
    query=text("""
               SELECT
               sold_at::date AS date,
               SUM(total_price) AS revenue
               FROM pharmacy_sales
               WHERE hospital_id=:hospital_id
               AND sold_at BETWEEN :start AND :end
               GROUP BY sold_at::date
               ORDER BY sold_at::date
               """)
    data=db.execute(
        query,{
            "hospital_id":current_user.hospital_id,
            "start":start,
            "end":end
        }
    ).fetchall()
    return [
        {
            "date":str(row[0]),
            "revenue":float(row[1] or 0)
        }
        for row in data
    ]
def pharmcy_profit_summary(db:Session,current_user:User,period:str):
    start,end=get_period_range(period)
    query=text("""
               SELECT
               COALESCE(
               SUM((
               d.selling_price - d.buying_price)*ps.quantity),0) AS profit
               FROM pharmacy_sales ps
               JOIN drugs d
               ON d.drug_id=ps.drug_id
               WHERE ps.hospital_id=:hospital_id
               AND ps.sold_at BETWEEN :start AND :end
               """)
    data=db.execute(query,{
        "hospital_id":current_user.hospital_id,
        "start":start,
        "end":end
    }).fetchone()
    return{
        "profit":float(data[0] or 0)
    }
def pharmacy_profit_trend(db:Session,current_user:User,period:str):
    start,end=get_period_range(period)
    query=text("""
               SELECT
               ps.sold_at::date AS date,
               SUM((
               d.selling_price - d.buying_price)*ps.quantity) AS profit
               FROM pharmacy_sales ps
               JOIN drugs d
               ON d.drug_id=ps.drug_id
               WHERE ps.hospital_id=:hospital_id
               AND ps.sold_at BETWEEN :start AND :end
               GROUP BY ps.sold_at::date
               ORDER BY ps.sold_at::date
               """)
    data=db.execute(query,
                    {
                        "hospital_id":current_user.hospital_id,
                        "start":start,
                        "end":end
                    }).fetchall()
    return [
        {
            "date":str(row[0]),
            "profit":float(row[1] or 0)
        }
        for row in data
    ]