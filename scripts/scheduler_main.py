from apscheduler.schedulers.background import BackgroundScheduler
from app.backend.services.notification_service import NotificationService
from app.backend.services.turno_repository import TurnoRepository
from app.backend.db.db import SessionLocal
import time
import atexit 

def run_notification_job():
    """Función que se llama periódicamente para ejecutar el servicio."""
    db_session = SessionLocal()
    turno_repo = TurnoRepository(db_session)
    notification_service = NotificationService(turno_repo)
    
    notification_service.check_and_notify() 
    db_session.close() 

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    
    scheduler.add_job(run_notification_job, 'interval', minutes=1)
    
    # Iniciar el scheduler
    scheduler.start()
    print('Scheduler iniciado. La verificación de notificaciones se ejecutará cada 2 minutos.')
    # Asegurarse de que el scheduler se detenga cuando la aplicación Python finalice
    atexit.register(lambda: scheduler.shutdown())

    # Mantener el hilo principal vivo
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        pass