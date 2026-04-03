from models.bill import Bill
from models.bill_item import BillItem
import uuid
from models.user import User
def add_bill_item(bill_id:str,data,db,current_user:User):
    bill=db.query(Bill).filter(Bill.bill_id==bill_id,Bill.hospital_id==current_user.hospital_id).first()
    if not bill:
        raise ValueError("Bill not found")
    total_price=data.quantity * data.unit_price
    item=BillItem(bill_id=bill_id,description=data.description,quantity=data.quantity,unit_price=data.unit_price,total_price=total_price)
    db.add(item)
    bill.total_amount += total_price
    db.commit()
    db.refresh(item)
    return {
        "item_id":item.item_id,
        "bill_id":item.bill_id,
        "description":item.description,
        "quantity":item.quantity,
        "unit_price":item.unit_price,
        "total_price":item.total_price

    }
def get_bill_item(db,bill_id:str,current_user:User):
    bill=db.query(Bill).filter(Bill.bill_id==bill_id,Bill.hospital_id==current_user.hospital_id)
    if not bill:
        raise ValueError("Bill not found")
    items=db.query(BillItem).filter(BillItem.bill_id==bill_id).all()
    if not items:
        return []
    result=[
        {
            "item_id":item.item_id,
            "bill_id":item.bill_id,
            "description":item.description,
            "quantity":item.quantity,
            "unit_price":item.unit_price,
            "total_price":item.total_price,
        }
        for item in items
    ]
    return result