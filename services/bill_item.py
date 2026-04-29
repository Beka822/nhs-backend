from models.bill import Bill
from models.services import Service
from models.bill_item import BillItem
import uuid
from models.user import User
def add_bill_item(bill_id:str,data,db,current_user:User):
    bill=db.query(Bill).filter(Bill.bill_id==bill_id,Bill.hospital_id==current_user.hospital_id).first()
    if not bill:
        raise ValueError("Bill not found")
    if data.service_id:
        service=db.query(Service).filter(Service.service_id==data.service_id,Service.hospital_id==current_user.hospital_id,Service.is_active==True).first()
        if not service:
            raise ValueError("Service not found")
        description=service.name
        unit_price=service.price
    else:
        description=data.description
        unit_price=data.unit_price
    quantity=data.quantity
    total_price=quantity * unit_price
    item=BillItem(bill_id=bill_id,service_id=data.service_id if data.service_id else None,description=description,quantity=quantity,unit_price=unit_price,total_price=total_price)
    db.add(item)
    bill.total_amount = (bill.total_amount or 0) + total_price
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