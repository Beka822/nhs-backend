from fastapi import APIRouter,Request,Depends
from sqlalchemy.orm import Session
from models.patient import Patient
from models.visit import Visit
from models.audit_log import AuditLog
from models.pays import Pay
from core.db import get_db
from services.wallet import credit_wallet
router=APIRouter(prefix="/pay",tags=["Pay"])
@router.post("/mpesa/callback")
async def mpesa_callback(request:Request,db:Session=Depends(get_db)):
    data=await request.json()
    print(data)
    stk=data["Body"]["stkCallback"]
    result_code=stk.get("ResultCode")
    checkout_id=stk.get("CheckoutRequestID")
    reference=stk.get("AccountReference")
    payment=db.query(Pay).filter(Pay.checkout_request_id==checkout_id).first()
    if not payment:
        return {"ResultCode": 0, "ResultDesc": "Accepted"}
    #SUCCESS
    if result_code==0:
        #amount=next((item["Value"] for item 
                    #in metadata if item.get("Name")== "Amount"),0)
        #receipt=next((item["Value"] for item in
                    # metadata if item.get("Name")== "MpesaReceiptNumber"),"SIMULATED")
       # phone=next((item["Value"] for item in
                   #metadata if item.get("Name")=="PhoneNumber"),"25400000000")
        #Extract visit_id
        visit_id=payment.reference.split("_")[1]
        #Credit wallet
        visit=db.query(Visit).filter(Visit.visit_id==visit_id).first()
        if visit:
            visit.payment_status="PAID"
            db.add(visit)
            db.commit()
            db.refresh(visit)
        audit=AuditLog(action="MPESA_PAYMENT_SUCCESS",entity="Visit",entity_id=visit.visit_id)
        db.add(audit)
        db.commit()
        metadata=stk.get("CallbackMetadata",{}).get("Item",[])
        amount=next((item["Value"] for item in metadata if item.get("Name")=="Amount"),None)
        receipt=next((item["Value"] for item in metadata if item.get("Name")=="MpesaReceiptNumber"),None)
        phone=next((item["Value"] for item in metadata if item.get("Name")=="PhoneNumber"),None)
        if receipt:
            existing=db.query(Pay).filter(Pay.mpesa_receipt==receipt).first()
            if existing:
                return {"ResultCode":0, "ResultDesc": "Duplicate ignored"}
            payment.mpesa_receipt=receipt
        payment.status="SUCCESS"
        db.commit()
    else:
        payment.status="FAILED"
        db.commit()
    return {"ResultCode": 0, "ResultDesc": "Accepted"}