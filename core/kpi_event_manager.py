import time
import threading
from collections import defaultdict
from sqlalchemy import text
class KPIEventManager:
    def __init__(self,session_factory):
        self.session_factory=session_factory
        self.event_buffer=defaultdict(float)
        self.debounce_window=30
        self.lock=threading.Lock()
        self.event_map={
            "admission_created":[
                "mv_admission_discharge_trend",
                "mv_patient_visits",
                "mv_icu_occupancy",
                "mv_ward_bor_trend"
            ],
            "discharge_created":[
                "mv_admission_discharge_trend",
                "mv_los_analytics",
                "mv_icu_occupancy",
                "mv_ward_bor_trend"
            ],
            "visit_created":[
                "mv_patients_visits"
            ],
            "icu_updated":[
                "mv_icu_occupancy"
            ],
            "bed_transfer":[
                "mv_transfer_reason_analysis",
                "mv_ward_bor_trend"
            ],
            "bill_paid":[
                "mv_payment_analytics"
            ]
        }
        self.worker_started=False
    def start_worker(self):
        if self.worker_started:
            return
        self.worker_started=True
        def worker():
            while True:
                time.sleep(10)
                self.process_events()
        thread=threading.Thread(target=worker, daemon=True)
        thread.start()
    def emit_event(self, event_name:str):
        with self.lock:
            self.event_buffer[event_name]=time.time()
            print(f"[EVENT EMITTED] {event_name}")
    def process_events(self):
        with self.lock:
            now=time.time()
            ready_events=[
                event for event, ts in self.event_buffer.items()
                if now - ts >= self.debounce_window
            ]
            if not ready_events:
                return
            views_to_refresh=set()
            for event in ready_events:
                views=self.event_map.get(event, [])
                for v in views:
                    views_to_refresh.add(v)
                del self.event_buffer[event]
        if views_to_refresh:
            self.refresh_views(list(views_to_refresh))
    def refresh_views(self,views):
        db=self.session_factory()
        try:
            for view in views:
                try:
                    db.execute(text(f"REFRESH MATERIALIZED VIEW CONCURRENTLY {view}"))
                    db.commit()
                    print(f"[REFRESHED] {view}")
                except Exception as e:
                    db.rollback()
                    print(f"[ERROR] {view} -> {str(e)}")
        except Exception as e:
            print(f"[DB TRANSACTION ERROR] {e}")
        