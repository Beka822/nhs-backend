from fastapi import APIRouter,Request,Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from models.patient import Patient
from datetime import datetime
from models.pays import Pay
from models.user import User
from core.dependencies import get_user_object
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
        payment.amount=amount
        payment.phone_number=str(phone)
        db.commit()
    else:
        payment.status="FAILED"
        db.commit()
    return {"ResultCode": 0, "ResultDesc": "Accepted"}
@router.get("/payout")
def get_revenue(db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    now=datetime.utcnow()
    start_of_month=datetime(now.year,now.month,1)
    if now.month==12:
        end_of_month=datetime(now.year+1,1,1)
    else:
        end_of_month=datetime(now.year,now.month+1,1)
    hospital_id=current_user.hospital_id
    result=db.query(Pay.clinical_id,func.count(Pay.payment_id).label("total_visits"),func.sum(Pay.amount).label("total_revenue"),func.sum(Pay.clinic_share).label("clinic_earnings"),).filter(Pay.clinical_id==hospital_id,Pay.status=="SUCCESS",Pay.created_at>=start_of_month,Pay.created_at<end_of_month).group_by(Pay.clinical_id).first()
    return{
        "hospital_name":current_user.hospital_id,
        "total_visits":result.total_visits,
        "total_revenue":result.total_revenue
        if result else 0,
        "clinic_earnings":result.clinic_earnings if result else 0,
        "month":start_of_month.strftime("%B%Y")
    }