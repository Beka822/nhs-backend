from fastapi import APIRouter,Depends,Query
from datetime import datetime,timedelta
from sqlalchemy.orm import Session
from sqlalchemy import text
from core.db import get_db
from models.user import User
from core.dependencies import get_user_object
router=APIRouter(prefix="/dashboard",tags=["Dashboard"])
@router.get("/patients")
def get_patient_stats(db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    hospital_id=current_user.hospital_id
    today=db.execute(text("""
                          SELECT COUNT(*) FROM mv_patient_visits
                          WHERE hospital_id=:hospital_id
                          AND visit_date=CURRENT_DATE
                          """),{"hospital_id":
                                hospital_id}).scalar()
    week=db.execute(text("""
                         SELECT COUNT(*) FROM mv_patient_visits
                         WHERE hospital_id=:hospital_id
                         AND visit_date >= CURRENT_DATE -
                         INTERVAL '7 days'
                         """),{"hospital_id":
                               hospital_id}).scalar()
    month=db.execute(text("""
                          SELECT COUNT(*) FROM mv_patient_visits
                          WHERE hospital_id=:hospital_id
                          AND date_trunc('month',visit_date)=
                          date_trunc('month',CURRENT_DATE)
                          """),{"hospital_id":
                                hospital_id}).scalar()
    return {
        "today":today,
        "week":week,
        "month":month
    }
@router.get("/visits-trend")
def get_visits_trend(db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    data=db.execute(text("""
                         SELECT visit_date, COUNT(*) as total
                         FROM mv_patient_visits
                         WHERE hospital_id=:hospital_id
                         AND visit_date >= CURRENT_DATE -
                         INTERVAL '30 days'
                         GROUP BY visit_date
                         ORDER BY visit_date
                         """),{"hospital_id":
                               current_user.hospital_id}).fetchall()
    return [
        {"date": row[0], "total": row[1]}
        for row in data
    ]
@router.get("/top-services")
def get_top_services(period:str=Query("month"),db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    hospital_id=current_user.hospital_id
    period=period.lower()
    now=datetime.utcnow()
    if period == "today":
        start=datetime(now.year,now.month,now.day)
        end=start + timedelta(days=1)
    elif period== "week":
        start=now - timedelta(days=7)
        end=now
    elif period== "month":
        start=datetime(now.year,now.month,1)
        if now.month==12:
            end=datetime(now.year+1,1,1)
        else:
            end=datetime(now.year,now.month+1,1)
    elif period=="year":
        start=datetime(now.year,1,1)
        end=datetime(now.year+1,1,1)
    else:
        start=None
        end=None
    query="""SELECT
    s.name,
    COUNT(*) AS usage_count,
    SUM(bi.total_price) AS total_revenue
    FROM bill_items bi
    JOIN services s ON s.service_id=bi.service_id
    JOIN bills b ON bi.bill_id=b.bill_id
    WHERE b.hospital_id=:hospital_id
    """
    params={"hospital_id":hospital_id}
    if start and end:
        query += "AND b.created_at >= :start AND b.created_at <:end"
        params.update({"start":start,"end":end})
    query += """ GROUP BY s.name
    ORDER BY total_revenue DESC
    LIMIT 5
    """
    data=db.execute(text(query),params).fetchall()
    return [
        {
            "name":row[0],
            "usage_count":row[1],
            "revenue":float(row[2] or 0)
        }
        for row in data
    ]
@router.get("/ward-bor-trend")
def get_ward_bor_trend(db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    hospital_id=current_user.hospital_id
    data=db.execute(text("""
                         SELECT ward_name,date,occupancy_rate
                         FROM mv_ward_bor_trend
                         WHERE hospital_id=:hospital_id
                         ORDER BY ward_name,date
                         """),{"hospital_id":
                               hospital_id}).fetchall()
    return [
        {
            "ward": row[0],
            "date": row[1],
            "occupancy_rate": float(row[2])
        }
        for row in data
    ]
@router.get("/admission-discharge-trend")
def get_admission_discharge_trend(db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    hospital_id=current_user.hospital_id
    data=db.execute(text("""
                         SELECT date,admissions,discharges,net_flow
                         FROM mv_admission_discharge_trend
                         WHERE hospital_id=:hospital_id
                         ORDER BY date
                         """),{"hospital_id":
                               hospital_id}).fetchall()
    return [
        {
            "date": row[0],
            "admissions": row[1],
            "discharges": row[2],
            "net_flow": row[3]
        }
        for row in data
    ]
@router.get("/icu-occupancy")
def get_icu_occupancy(db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    hospital_id=current_user.hospital_id
    data=db.execute(text("""
                         SELECT date,occupied_beds,total_beds,occupancy_rate
                         FROM mv_icu_occupancy
                         WHERE hospital_id=:hospital_id
                         ORDER BY date
                         """),{"hospital_id":
                               hospital_id}).fetchall()
    latest=data[-1] if data else None
    occupancy_rate=float(latest[3]) if latest else 0
    return {
        "trend": [
            {
                "date": row[0],
                "occupied_beds": row[1],
                "total_beds": row[2],
                "occupancy_rate": float(row[3])
            }
            for row in data
        ],
        "current":{
            "occupied_beds":latest[1] if latest else 0,
            "total_beds":latest[2] if latest else 0,
            "occupancy_rate":occupancy_rate
        },
        "alert":{
            "level":(
                "CRITICAL" if occupancy_rate >= 90 
                else
                "WARNING" if occupancy_rate >=75
                else
                "NORMAL"
            ),
            "message":(
                "ICU is critically full" if occupancy_rate >= 90 else
                "ICU nearing capacity" if occupancy_rate >=75 else
                "ICU operating normally"
            )
        }
    }
@router.get("/los-analytics")
def get_los_analytics(period:str="month",db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    hospital_id=current_user.hospital_id
    now=datetime.utcnow()
    if period =="today":
        start=datetime(now.year,now.month,now.day)
    elif period=="week":
        start=now-timedelta(days=7)
    elif period=="month":
        start=datetime(now.year,now.month,1)
    elif period=="year":
        start=datetime(now.year,1,1)
    else:
        start=None
    query="""SELECT
    ward_name,service_name,
    AVG(avg_los) as avg_los,
    AVG(median_los) as median_los,
    AVG(discharge_efficiency_score) as
    efficiency
    FROM mv_los_analytics
    WHERE hospital_id=:hospital_id
    """
    params={"hospital_id":hospital_id}
    if start:
        query += "AND date >= :start"
        params["start"]=start

    query += """ GROUP BY ward_name,service_name
    ORDER BY efficiency DESC
    LIMIT 10 
    """
    data=db.execute(text(query),params).fetchall()
    return [
        {
            "ward": row[0],
            "service": row[1],
            "avg_los":float(row[2]),
            "median_los":float(row[3]),
            "efficiency_score":float(row[4])
        }
        for row in data
    ]
@router.get("/top-transfer-reasons")
def get_top_transfer_reasons(year:int,month:int,db:Session=Depends(get_db),current_user:User=Depends(get_user_object)):
    hospital_id=current_user.hospital_id
    start=datetime(year,month,1)
    data=db.execute(text("""
                         WITH monthly_total AS (
                         SELECT SUM(transfer_count) AS total
                         FROM mv_transfer_reason_analysis
                         WHERE hospital_id=:hospital_id
                         AND month=:start)
                         SELECT
                         m.reason,
                         m.transfer_count,
                         ROUND((m.transfer_count*100.0 / NULLIF(mt.total,0)),2)
                         AS percentage
                         FROM mv_transfer_reason_analysis m
                         CROSS JOIN monthly_total mt
                         WHERE m.hospital_id=:hospital_id
                         AND m.month=:start
                         ORDER BY m.transfer_count DESC
                         LIMIT 3
                         """),{
                             "hospital_id":hospital_id,
                             "start":start
                         }).fetchall()
    return [
        {
            "reason": row[0],
            "count": row[1],
            "percentage":float(row[2] or 0)
        }
        for row in data
    ]
@router.get("/payment-analytics")
def get_payment_analytics(
    period:str="month",
    db:Session=Depends(get_db),
    current_user:User=Depends(get_user_object)
):
    hospital_id=current_user.hospital_id
    today=datetime.utcnow().date()
    if period =="today":
        start=today
        end=today + timedelta(days=1)
    elif period=="week":
        start = today - timedelta(days=today.weekday())
        end=start + timedelta(days=7)
    elif period=="month":
        start=today.replace(day=1)
        end=(start + timedelta(days=32)).replace(day=1)
    elif period=="year":
        start=today.replace(month=1,day=1)
        end=start.replace(year=start.year +1)
    else:
        start=today.replace(day=1)
        end=(start + timedelta(days=32)).replace(day=1)
    distribution=db.execute(text("""
                                 SELECT
                                 payment_method,
                                 SUM(total_amount) AS amount
                                 FROM mv_payment_analytics
                                 WHERE hospital_id=:hospital_id
                                 AND date >=:start AND date <:end
                                 GROUP BY payment_method
                                 """),{
                                     "hospital_id":hospital_id,
                                     "start":start,
                                     "end":end
                                 }).fetchall()
    total=sum(row[1] or 0 for row in distribution)
    pie=[
        {
            "method":row[0],
            "amount": float(row[1] or 0),
            "percentage":round((row[1]/total)*100,2) if total else 0
        }
        for row in distribution
    ]
    trend=db.execute(text("""
                          SELECT
                          date,
                          SUM(total_amount) AS revenue
                          FROM mv_payment_analytics
                          WHERE hospital_id=:hospital_id
                          AND date >=:start AND date<:end
                          GROUP BY date
                          ORDER BY date
                          """),{
                              "hospital_id":hospital_id,
                              "start":start,
                              "end":end
                          }).fetchall()
    trend_data=[
        {
            "date":row[0],
            "revenue":float(row[1] or 0)
        }
        for row in trend
    ]
    digital_cash=db.execute(text("""
                                 SELECT
                                 CASE
                                 WHEN payment_method='Cash' THEN 'Cash'
                                 ELSE 'Digital'
                                 END AS category,
                                 SUM(total_amount) AS amount
                                 FROM mv_payment_analytics
                                 WHERE hospital_id=:hospital_id
                                 AND date >=:start AND date < :end
                                 GROUP BY category
                                 """),{
                                    "hospital_id":hospital_id,
                                    "start":start,
                                    "end":end
                                 }).fetchall()
    digital_cash_data=[
        {
            "category": row[0],
            "amount": float(row[1] or 0)
        }
        for row in digital_cash
    ]
    insurance=db.execute(text("""
                              SELECT
                              SUM(total_amount) FILTER (WHERE
                              payment_method='Insurance') AS
                              insurance_amount,
                              SUM(total_amount) AS total_amount
                              FROM mv_payment_analytics
                              WHERE hospital_id=:hospital_id
                              AND date >=:start AND date < :end
                              """),{
                                  "hospital_id":hospital_id,
                                  "start":start,
                                  "end":end
                              }).fetchone()
    insurance_amount=float(insurance[0] or 0)
    total_amount=float(insurance[1] or 0)
    insurance_dependency=round((insurance_amount/total_amount)*100,2) if total_amount else 0
    return{
        "distribution":pie,
        "trend":trend_data,
        "digital_vs_cash":digital_cash_data,
        "insurance_dependency":insurance_dependency
    }