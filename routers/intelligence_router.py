from sqlalchemy import text
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from models.user import User
from core.db import get_db
from core.dependencies import get_user_object
router=APIRouter(prefix="/intelligence",tags=["Pharmacy Intelligenc"])
@router.get("/")
def pharmacy_intelligence(db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    hospital_id=current_user.hospital_id
    inventory_query=text("""
                         SELECT
                         d.name,
                         d.quantity_in_stock,
                         d.buying_price,
                         COALESCE(
                         SUM(ps.quantity),0) AS monthly_sales,
                         CASE
                         WHEN COALESCE(SUM(ps.quantity),0)=0
                         THEN 999
                         ELSE
                         ROUND(d.quantity_in_stock::numeric /(SUM(ps.quantity)/30.0),1)
                         END AS inventory_days
                         FROM drugs d
                         LEFT JOIN pharmacy_sales ps
                         ON ps.drug_id=d.drug_id
                         AND ps.sold_at >= NOW() - INTERVAL '30 days'
                         WHERE d.hospital_id=:hospital_id
                         GROUP BY d.drug_id
                         """)
    inventory_data=db.execute(inventory_query,{
        "hospital_id":hospital_id
    }).fetchall()
    overstocked=[]
    excess_value=0
    for row in inventory_data:
        inventory_days=float(row[4] or 0)
        if inventory_days > 90:
            excess_stock=row[1]
            value=excess_stock * float(row[2] or 0)
            excess_value += value
            overstocked.append({
                "drug":row[0],
                "stock":row[1],
                "monthly_sales":row[3],
                "inventory_days":inventory_days,
                "value":value
            })
    expiry_query=text("""
                      SELECT
                      name,
                      quantity_in_stock,
                      buying_price,
                      expiry_date,
                      (quantity_in_stock * buying_price) AS risk_value
                      FROM drugs
                      WHERE hospital_id=:hospital_id
                      AND quantity_in_stock > 0
                      AND expiry_date BETWEEN
                      CURRENT_DATE
                      AND CURRENT_DATE + INTERVAL '45 days'
                      ORDER BY risk_value DESC
                      """)
    expiry_data=db.execute(expiry_query,{
        "hospital_id":hospital_id
    }).fetchall()
    expiry_total=sum(float(row[4] or 0)
                     for row in expiry_data)
    top_expiry=None
    if expiry_data:
        top_expiry={
            "drug":expiry_data[0][0],
            "risk_value":float(expiry_data[0][4])
        }
    leakage_query=text("""
                       SELECT
                       d.name,d.buying_price,d.selling_price,
                       SUM(ps.quantity) AS units_sold,
                       (d.selling_price - d.buying_price) AS margin
                       FROM drugs d
                       JOIN pharmacy_sales ps
                       ON ps.drug_id=d.drug_id
                       WHERE d.hospital_id=:hospital_id
                       GROUP BY d.drug_id
                       HAVING SUM(ps.quantity) >= 5
                       """)
    leakage_data=db.execute(leakage_query,{
        "hospital_id":hospital_id
    }).fetchall()
    leakage=[]
    leakage_loss=0
    for row in leakage_data:
        margin=float(row[4] or 0)
        selling=float(row[2] or 0)
        if selling > 0:
            margin_pct=(margin/selling)*100
        else:
            margin_pct=0
        if margin_pct < 15:
            units=int(row[3] or 0)
            estimated_loss=units * (selling*0.15-margin)
            leakage_loss += estimated_loss
            leakage.append({
                "drug":row[0],
                "units_sold":units,
                "margin_pct":round(margin_pct,1),
                "estimated_loss":round(estimated_loss,2)
            })
    stockout_query=text("""
                        SELECT
                        d.name,d.quantity_in_stock,
                        AVG(daily_sales.qty) AS daily_velocity
                        FROM drugs d
                        JOIN(
                        SELECT
                        drug_id,
                        DATE(sold_at) AS day,
                        SUM(quantity) AS qty
                        FROM pharmacy_sales
                        GROUP BY 
                        drug_id,
                        DATE(sold_at)
                        )daily_sales
                        ON daily_sales.drug_id=d.drug_id
                        WHERE d.hospital_id=:hospital_id
                        GROUP BY d.drug_id
                        """)
    stockout_data=db.execute(stockout_query,{
        "hospital_id":hospital_id
    }).fetchall()
    stockouts=[]
    for row in stockout_data:
        stock=float(row[1] or 0)
        velocity=float(row[2] or 0)
        if velocity <= 0:
            continue
        days_left=stock/velocity
        if days_left <= 7:
            stockouts.append({
                "drug":row[0],
                "days_left":round(days_left,1),
                "stock":stock,
                "daily_velocity":round(velocity,1)
            })
    return {
        "inventory_loss_risk":{
            "count":len(overstocked),
            "financial_exposure":round(excess_value,2),
            "items":overstocked[:5],
            "recommended_action":"Reduce future orders or redistribute stock to minimize expiry risk"
        },
        "expiry_exposure":{
            "financial_exposure":round(expiry_total,2),
            "count":len(expiry_data),
            "top_risk":top_expiry,
            "recommended_action":"Prioritize sales even at buying price and reduce reorders"
        },
        "revenue_leakage":{
            "count":len(leakage),
            "estimated_loss":round(leakage_loss,2),
            "items":leakage[:5],
            "recommended_action":"Adjust pricing or renegotiate suppliers"
        },
        "stockout_predictions":{
            "count":len(stockouts),
            "items":stockouts[:5],
            "recommended_action":"Reorder high-demand drugs early"
        }
    }