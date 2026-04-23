import urllib.request
import urllib.parse
import urllib.error
import json
import datetime
import http.cookiejar

BASE_URL = "http://localhost:8000/api"
EMAIL = "paciente@turnos.com"
PASSWORD = "paciente123"
ADMIN_EMAIL = "admin@turnos.com"
ADMIN_PASSWORD = "admin123"
DOCTOR_MATRICULA = "MED002"

# Setup cookie jar
cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

def request(method, url, data=None, params=None):
    if params:
        url += "?" + urllib.parse.urlencode(params)
    
    req = urllib.request.Request(url, method=method)
    req.add_header('Content-Type', 'application/json')
    
    if data:
        json_data = json.dumps(data).encode('utf-8')
        req.data = json_data
        
    try:
        with opener.open(req) as response:
            if response.status >= 200 and response.status < 300:
                content = response.read().decode('utf-8')
                if content:
                    return json.loads(content)
                return {}
            else:
                print(f"Request failed: {response.status} {response.reason}")
                return None
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} {e.reason}")
        try:
            print(e.read().decode('utf-8'))
        except:
            pass
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def login(email, password):
    print(f"Logging in as {email}...")
    res = request("POST", f"{BASE_URL}/auth/login", data={"email": email, "password": password})
    if res is not None:
        print("Login successful.")
        return True
    return False

def get_user_info():
    # Hardcoded ID for patient
    return 3

def get_all_patients():
    print("Getting all patients...")
    patients = request("GET", f"{BASE_URL}/pacientes/pacientes/")
    if patients:
        print(f"Found {len(patients)} patients.")
        for p in patients:
            print(f" - {p['Nombre']} {p['Apellido']} (ID: {p['nroPaciente']}, Email: {p.get('Email')})")
        return patients
    return []

def get_patient_by_user_id(user_id):
    print(f"Getting patient for user {user_id}...")
    patient = request("GET", f"{BASE_URL}/pacientes/pacientes/user/{user_id}")
    if patient:
        print(f"Patient found: {patient['Nombre']} {patient['Apellido']} (ID: {patient['nroPaciente']})")
        return patient
    return None

def get_doctor(matricula):
    print(f"Getting doctor {matricula}...")
    doctor = request("GET", f"{BASE_URL}/medicos/medicos/{matricula}")
    if doctor:
        print(f"Doctor found: {doctor['Nombre']} {doctor['Apellido']}")
        return doctor
    return None

def create_agenda(matricula, day_of_week):
    print(f"Creating regular agenda for {matricula} on day {day_of_week}...")
    payload = {
        "Especialidad_Id": 1, # Assuming 1 exists (Cardiologia usually)
        "Dia_de_semana": day_of_week,
        "Hora_inicio": "09:00",
        "Hora_fin": "17:00",
        "Duracion": 30,
        "Sucursal_Id": 1 # Assuming 1 exists
    }
    # Note: Double prefix for agendas
    res = request("POST", f"{BASE_URL}/agendas/agendas/medicos/{matricula}/agenda/regular", data=payload)
    if res is not None:
        print("Agenda created successfully.")
        return True
    else:
        print("Failed to create agenda (maybe already exists).")
        return False

def get_available_agenda(matricula, date_str):
    print(f"Getting available agenda for {matricula} on {date_str}...")
    agenda = request("GET", f"{BASE_URL}/agendas/agendas/medicos/{matricula}/agenda/disponible", params={"fecha": date_str})
    if agenda is not None:
        print(f"Found {len(agenda)} available slots.")
        return agenda
    return None

def create_appointment(patient_id, matricula, date_str, time_str, specialty_id):
    print(f"Creating appointment for patient {patient_id} with {matricula} on {date_str} at {time_str}...")
    payload = {
        "Fecha": date_str,
        "Hora": time_str,
        "Paciente_nroPaciente": patient_id,
        "Medico_Matricula": matricula,
        "Especialidad_Id": specialty_id,
        "Motivo": "Test appointment",
        "Duracion": 30
    }
    # Note: Double prefix for turnos?
    # routes.py: router.include_router(turnos_router, prefix="/turnos", tags=["Turnos"])
    # turnos.py: router = APIRouter(prefix="/turnos", tags=["Turnos"])
    # So yes, /api/turnos/turnos/
    res = request("POST", f"{BASE_URL}/turnos/turnos/", data=payload)
    if res is not None:
        print("Appointment created successfully!")
        return res
    return None

def main():
    # 1. Login as Admin to create agenda
    if not login(ADMIN_EMAIL, ADMIN_PASSWORD):
        return
    
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    day_of_week = tomorrow.isoweekday()
    
    create_agenda(DOCTOR_MATRICULA, day_of_week)
    
    # 2. Login as Patient to book appointment
    # Clear cookies first
    cookie_jar.clear()
    
    if not login(EMAIL, PASSWORD):
        return

    user_id = get_user_info()
    patient = get_patient_by_user_id(user_id)
    
    if not patient:
        print("Patient not found by User ID. Listing all patients...")
        get_all_patients()
        return

    if not get_doctor(DOCTOR_MATRICULA):
        print(f"Doctor {DOCTOR_MATRICULA} not found!")
        return

    date_str = tomorrow.strftime("%Y-%m-%d")
    
    # Check agenda
    agenda = get_available_agenda(DOCTOR_MATRICULA, date_str)
    
    if not agenda:
        print("No agenda available. Skipping appointment creation.")
    else:
        slot = agenda[0]
        create_appointment(patient['nroPaciente'], DOCTOR_MATRICULA, date_str, slot['hora'], slot['especialidad_id'])

if __name__ == "__main__":
    main()
