"""
Script para insertar datos de prueba en la base de datos del sistema de turnos médicos
"""

from sqlalchemy.orm import Session
from app.backend.db.db import engine, Base, SessionLocal
from app.backend.models.models import (
    Sucursal,
    Consultorio,
    Especialidad,
    Medico,
    Paciente,
    Estado,
    AgendaRegular,
    Turno,
    User,
    Role,
    MedicoEspecialidad,
)
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Contexto para hashear contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def clear_database(db: Session):
    """Limpia todas las tablas de la base de datos"""
    print("🗑️  Limpiando base de datos...")

    # Orden importante para respetar las FK
    db.query(Turno).delete()
    db.query(AgendaRegular).delete()
    db.query(MedicoEspecialidad).delete()
    db.query(Medico).delete()
    db.query(Paciente).delete()
    db.query(User).delete()
    db.query(Role).delete()
    db.query(Estado).delete()
    db.query(Especialidad).delete()
    db.query(Consultorio).delete()
    db.query(Sucursal).delete()

    db.commit()
    print("✅ Base de datos limpiada")


def seed_roles(db: Session):
    """Crea los roles del sistema"""
    print("👥 Creando roles...")

    roles = [
        Role(Id=1, Nombre="Admin"),
        Role(Id=2, Nombre="Medico"),
        Role(Id=3, Nombre="Paciente"),
        Role(Id=4, Nombre="Secretaria"),
    ]

    db.add_all(roles)
    db.commit()
    print(f"✅ {len(roles)} roles creados")


def seed_estados(db: Session):
    """Crea los estados de los turnos"""
    print("📊 Creando estados...")

    estados = [
        Estado(Id=1, Descripcion="Pendiente"),
        Estado(Id=2, Descripcion="Confirmado"),
        Estado(Id=3, Descripcion="Cancelado"),
        Estado(Id=4, Descripcion="Atendido"),
        Estado(Id=5, Descripcion="Finalizado"),
        Estado(Id=6, Descripcion="Ausente"),
        Estado(Id=7, Descripcion="Anunciado"),
    ]

    db.add_all(estados)
    db.commit()
    print(f"✅ {len(estados)} estados creados")


def seed_sucursales(db: Session):
    """Crea sucursales"""
    print("🏥 Creando sucursales...")

    sucursales = [
        Sucursal(Id=1, Nombre="Sede Central", Direccion="Av. Libertador 1000, CABA"),
        Sucursal(Id=2, Nombre="Sede Norte", Direccion="Av. Cabildo 2500, CABA"),
        Sucursal(Id=3, Nombre="Sede Sur", Direccion="Av. Rivadavia 5000, CABA"),
        Sucursal(Id=4, Nombre="Sede Oeste", Direccion="Av. Gaona 3000, CABA"),
    ]

    db.add_all(sucursales)
    db.commit()
    print(f"✅ {len(sucursales)} sucursales creadas")


def seed_consultorios(db: Session):
    """Crea consultorios para cada sucursal"""
    print("🚪 Creando consultorios...")

    consultorios = []

    # 5 consultorios por sucursal
    for sucursal_id in range(1, 5):
        for numero in range(1, 6):
            consultorios.append(Consultorio(Numero=numero, Sucursal_Id=sucursal_id))

    db.add_all(consultorios)
    db.commit()
    print(f"✅ {len(consultorios)} consultorios creados")


def seed_especialidades(db: Session):
    """Crea especialidades médicas"""
    print("⚕️  Creando especialidades...")

    especialidades = [
        Especialidad(Id_especialidad=1, descripcion="Cardiología"),
        Especialidad(Id_especialidad=2, descripcion="Dermatología"),
        Especialidad(Id_especialidad=3, descripcion="Pediatría"),
        Especialidad(Id_especialidad=4, descripcion="Traumatología"),
        Especialidad(Id_especialidad=5, descripcion="Oftalmología"),
        Especialidad(Id_especialidad=6, descripcion="Neurología"),
        Especialidad(Id_especialidad=7, descripcion="Ginecología"),
        Especialidad(Id_especialidad=8, descripcion="Psiquiatría"),
        Especialidad(Id_especialidad=9, descripcion="Odontología"),
        Especialidad(Id_especialidad=10, descripcion="Clínica Médica"),
    ]

    db.add_all(especialidades)
    db.commit()
    print(f"✅ {len(especialidades)} especialidades creadas")


def seed_users_and_medicos(db: Session):
    """Crea usuarios médicos y sus perfiles"""
    print("👨‍⚕️ Creando médicos y usuarios...")

    medicos_data = [
        {
            "matricula": "M-12345",
            "nombre": "Juan",
            "apellido": "Pérez",
            "email": "juan.perez@hospital.com",
            "especialidades": [1, 10],  # Cardiología y Clínica Médica
        },
        {
            "matricula": "M-23456",
            "nombre": "María",
            "apellido": "González",
            "email": "maria.gonzalez@hospital.com",
            "especialidades": [2],  # Dermatología
        },
        {
            "matricula": "M-34567",
            "nombre": "Carlos",
            "apellido": "Rodríguez",
            "email": "carlos.rodriguez@hospital.com",
            "especialidades": [3],  # Pediatría
        },
        {
            "matricula": "M-45678",
            "nombre": "Ana",
            "apellido": "Martínez",
            "email": "ana.martinez@hospital.com",
            "especialidades": [4],  # Traumatología
        },
        {
            "matricula": "M-56789",
            "nombre": "Luis",
            "apellido": "López",
            "email": "luis.lopez@hospital.com",
            "especialidades": [5],  # Oftalmología
        },
        {
            "matricula": "M-67890",
            "nombre": "Laura",
            "apellido": "Fernández",
            "email": "laura.fernandez@hospital.com",
            "especialidades": [6],  # Neurología
        },
        {
            "matricula": "M-78901",
            "nombre": "Diego",
            "apellido": "Sánchez",
            "email": "diego.sanchez@hospital.com",
            "especialidades": [7],  # Ginecología
        },
        {
            "matricula": "M-89012",
            "nombre": "Patricia",
            "apellido": "Ramírez",
            "email": "patricia.ramirez@hospital.com",
            "especialidades": [8],  # Psiquiatría
        },
        {
            "matricula": "M-90123",
            "nombre": "Roberto",
            "apellido": "Torres",
            "email": "roberto.torres@hospital.com",
            "especialidades": [9],  # Odontología
        },
        {
            "matricula": "M-01234",
            "nombre": "Gabriela",
            "apellido": "Díaz",
            "email": "gabriela.diaz@hospital.com",
            "especialidades": [10],  # Clínica Médica
        },
    ]

    medicos = []
    medico_especialidades = []

    for i, data in enumerate(medicos_data, start=1):
        # Crear usuario
        user = User(
            Email=data["email"],
            Password_Hash=pwd_context.hash("medico123"),  # Contraseña por defecto
            Role_Id=2,  # Rol Medico
        )
        db.add(user)
        db.flush()  # Para obtener el User_Id

        # Crear médico
        medico = Medico(
            Matricula=data["matricula"],
            Nombre=data["nombre"],
            Apellido=data["apellido"],
            User_Id=user.Id,
        )
        medicos.append(medico)

        # Asociar especialidades
        for esp_id in data["especialidades"]:
            medico_especialidades.append(
                MedicoEspecialidad(
                    Medico_Matricula=data["matricula"],
                    Especialidad_Id=esp_id,
                )
            )

    db.add_all(medicos)
    db.add_all(medico_especialidades)
    db.commit()
    print(f"✅ {len(medicos)} médicos creados con sus usuarios")


def seed_users_and_pacientes(db: Session):
    """Crea usuarios pacientes y sus perfiles"""
    print("👤 Creando pacientes y usuarios...")

    pacientes_data = [
        {
            "nombre": "Pedro",
            "apellido": "Gómez",
            "telefono": "11-2345-6789",
            "email": "pedro.gomez@email.com",
        },
        {
            "nombre": "Sofía",
            "apellido": "López",
            "telefono": "11-3456-7890",
            "email": "sofia.lopez@email.com",
        },
        {
            "nombre": "Martín",
            "apellido": "Álvarez",
            "telefono": "11-4567-8901",
            "email": "martin.alvarez@email.com",
        },
        {
            "nombre": "Valeria",
            "apellido": "Ruiz",
            "telefono": "11-5678-9012",
            "email": "valeria.ruiz@email.com",
        },
        {
            "nombre": "Lucas",
            "apellido": "Moreno",
            "telefono": "11-6789-0123",
            "email": "lucas.moreno@email.com",
        },
        {
            "nombre": "Camila",
            "apellido": "Castro",
            "telefono": "11-7890-1234",
            "email": "camila.castro@email.com",
        },
        {
            "nombre": "Federico",
            "apellido": "Silva",
            "telefono": "11-8901-2345",
            "email": "federico.silva@email.com",
        },
        {
            "nombre": "Valentina",
            "apellido": "Romero",
            "telefono": "11-9012-3456",
            "email": "valentina.romero@email.com",
        },
        {
            "nombre": "Agustín",
            "apellido": "Benítez",
            "telefono": "11-0123-4567",
            "email": "agustin.benitez@email.com",
        },
        {
            "nombre": "Florencia",
            "apellido": "Vargas",
            "telefono": "11-1234-5678",
            "email": "florencia.vargas@email.com",
        },
        {
            "nombre": "Matías",
            "apellido": "Ojeda",
            "telefono": "11-2345-6780",
            "email": "matias.ojeda@email.com",
        },
        {
            "nombre": "Catalina",
            "apellido": "Navarro",
            "telefono": "11-3456-7891",
            "email": "catalina.navarro@email.com",
        },
        {
            "nombre": "Nicolás",
            "apellido": "Pereyra",
            "telefono": "11-4567-8902",
            "email": "nicolas.pereyra@email.com",
        },
        {
            "nombre": "Milagros",
            "apellido": "Vega",
            "telefono": "11-5678-9013",
            "email": "milagros.vega@email.com",
        },
        {
            "nombre": "Tomás",
            "apellido": "Medina",
            "telefono": "11-6789-0124",
            "email": "tomas.medina@email.com",
        },
        {
            "nombre": "Francisco",
            "apellido": "Jalile",
            "telefono": "11-7890-1235",
            "email": "francisco.jalile@email.com",
        },
    ]

    pacientes = []

    for data in pacientes_data:
        # Crear usuario
        user = User(
            Email=data["email"],
            Password_Hash=pwd_context.hash("paciente123"),  # Contraseña por defecto
            Role_Id=3,  # Rol Paciente
        )
        db.add(user)
        db.flush()

        # Crear paciente
        paciente = Paciente(
            Nombre=data["nombre"],
            Apellido=data["apellido"],
            Telefono=data["telefono"],
            Email=data["email"],
            User_Id=user.Id,
        )
        pacientes.append(paciente)

    db.add_all(pacientes)
    db.commit()
    print(f"✅ {len(pacientes)} pacientes creados con sus usuarios")


def seed_agendas_regulares(db: Session):
    """Crea agendas regulares para los médicos"""
    print("📅 Creando agendas regulares...")

    # Obtener todos los médicos
    medicos = db.query(Medico).all()

    agendas = []

    for medico in medicos:
        # Obtener especialidades del médico
        especialidades = (
            db.query(MedicoEspecialidad)
            .filter(MedicoEspecialidad.Medico_Matricula == medico.Matricula)
            .all()
        )

        for esp in especialidades:
            # Lunes a Viernes (1-5)
            for dia in range(1, 6):
                # Turno mañana: 8:00 - 12:00
                agendas.append(
                    AgendaRegular(
                        Medico_Matricula=medico.Matricula,
                        Especialidad_Id=esp.Especialidad_Id,
                        Dia_de_semana=dia,
                        Hora_inicio="08:00",
                        Hora_fin="12:00",
                        Duracion=30,  # 30 minutos por turno
                        Sucursal_Id=(dia % 4) + 1,  # Rotar entre sucursales
                    )
                )

                # Turno tarde: 14:00 - 18:00
                agendas.append(
                    AgendaRegular(
                        Medico_Matricula=medico.Matricula,
                        Especialidad_Id=esp.Especialidad_Id,
                        Dia_de_semana=dia,
                        Hora_inicio="14:00",
                        Hora_fin="18:00",
                        Duracion=30,
                        Sucursal_Id=(dia % 4) + 1,
                    )
                )

    db.add_all(agendas)
    db.commit()
    print(f"✅ {len(agendas)} agendas regulares creadas")


def seed_turnos(db: Session):
    print("🗓️  Creando turnos con reglas estrictas de fechas...")

    pacientes = db.query(Paciente).all()
    medicos = db.query(Medico).all()

    # Estados
    ESTADO_PENDIENTE = 1
    ESTADO_CONFIRMADO = 2
    ESTADO_CANCELADO = 3
    ESTADO_ATENDIDO = 4
    ESTADO_FINALIZADO = 5
    ESTADO_AUSENTE = 6

    # Fecha "actual" fija
    FECHA_ACTUAL = datetime(2025, 11, 20)

    horas = ["08:00", "09:00", "10:00", "11:00", "14:00", "15:00", "16:00", "17:00"]

    turnos = []
    idx = 0

    # Helper: obtiene especialidad
    def get_esp(medico):
        return (
            db.query(MedicoEspecialidad)
            .filter(MedicoEspecialidad.Medico_Matricula == medico.Matricula)
            .first()
        )

    # ------------------------------
    # FINALIZADOS (SOLO PASADO)
    # ------------------------------
    fechas_finalizados = [datetime(2025, 11, 10) + timedelta(days=i) for i in range(10)]

    for fecha in fechas_finalizados:
        medico = medicos[idx % len(medicos)]
        paciente = pacientes[idx % len(pacientes)]
        esp = get_esp(medico)

        turnos.append(
            Turno(
                Fecha=fecha.strftime("%Y-%m-%d"),
                Hora=horas[idx % len(horas)],
                Paciente_nroPaciente=paciente.nroPaciente,
                Medico_Matricula=medico.Matricula,
                Especialidad_Id=esp.Especialidad_Id,
                Estado_Id=ESTADO_FINALIZADO,
                Sucursal_Id=(idx % 4) + 1,
                Duracion=30,
                Motivo=f"Finalizado {idx+1}",
            )
        )
        idx += 1

    # ------------------------------
    # ATENDIDOS (SOLO PASADO)
    # ------------------------------
    fechas_atendidos = [datetime(2025, 11, 11) + timedelta(days=i) for i in range(5)]

    for fecha in fechas_atendidos:
        medico = medicos[idx % len(medicos)]
        paciente = pacientes[idx % len(pacientes)]
        esp = get_esp(medico)

        turnos.append(
            Turno(
                Fecha=fecha.strftime("%Y-%m-%d"),
                Hora=horas[idx % len(horas)],
                Paciente_nroPaciente=paciente.nroPaciente,
                Medico_Matricula=medico.Matricula,
                Especialidad_Id=esp.Especialidad_Id,
                Estado_Id=ESTADO_ATENDIDO,
                Sucursal_Id=(idx % 4) + 1,
                Duracion=30,
                Motivo=f"Atendido {idx+1}",
            )
        )
        idx += 1

    # ------------------------------
    # AUSENTES (SOLO PASADO)
    # ------------------------------
    fechas_ausentes = [datetime(2025, 11, 12) + timedelta(days=i) for i in range(7)]

    for fecha in fechas_ausentes:
        medico = medicos[idx % len(medicos)]
        paciente = pacientes[idx % len(pacientes)]
        esp = get_esp(medico)

        turnos.append(
            Turno(
                Fecha=fecha.strftime("%Y-%m-%d"),
                Hora=horas[idx % len(horas)],
                Paciente_nroPaciente=paciente.nroPaciente,
                Medico_Matricula=medico.Matricula,
                Especialidad_Id=esp.Especialidad_Id,
                Estado_Id=ESTADO_AUSENTE,
                Sucursal_Id=(idx % 4) + 1,
                Duracion=30,
                Motivo=f"Ausente {idx+1}",
            )
        )
        idx += 1

    # ------------------------------
    # CANCELADOS (PASADO Y FUTURO)
    # ------------------------------
    fechas_cancelados = [
        datetime(2025, 11, 13),  # pasado
        datetime(2025, 11, 23),  # futuro
    ]

    for fecha in fechas_cancelados:
        medico = medicos[idx % len(medicos)]
        paciente = pacientes[idx % len(pacientes)]
        esp = get_esp(medico)

        turnos.append(
            Turno(
                Fecha=fecha.strftime("%Y-%m-%d"),
                Hora=horas[idx % len(horas)],
                Paciente_nroPaciente=paciente.nroPaciente,
                Medico_Matricula=medico.Matricula,
                Especialidad_Id=esp.Especialidad_Id,
                Estado_Id=ESTADO_CANCELADO,
                Sucursal_Id=(idx % 4) + 1,
                Duracion=30,
                Motivo=f"Cancelado {idx+1}",
            )
        )
        idx += 1

    # ------------------------------
    # PENDIENTES (SOLO FUTURO)
    # ------------------------------
    fechas_pendientes = [datetime(2025, 11, 21) + timedelta(days=i) for i in range(5)]

    for fecha in fechas_pendientes:
        medico = medicos[idx % len(medicos)]
        paciente = pacientes[idx % len(pacientes)]
        esp = get_esp(medico)

        turnos.append(
            Turno(
                Fecha=fecha.strftime("%Y-%m-%d"),
                Hora=horas[idx % len(horas)],
                Paciente_nroPaciente=paciente.nroPaciente,
                Medico_Matricula=medico.Matricula,
                Especialidad_Id=esp.Especialidad_Id,
                Estado_Id=ESTADO_PENDIENTE,
                Sucursal_Id=(idx % 4) + 1,
                Duracion=30,
                Motivo=f"Pendiente {idx+1}",
            )
        )
        idx += 1

    # ------------------------------
    # CONFIRMADOS (SOLO FUTURO)
    # ------------------------------
    fechas_confirmados = [datetime(2025, 11, 22) + timedelta(days=i) for i in range(5)]

    for fecha in fechas_confirmados:
        medico = medicos[idx % len(medicos)]
        paciente = pacientes[idx % len(pacientes)]
        esp = get_esp(medico)

        turnos.append(
            Turno(
                Fecha=fecha.strftime("%Y-%m-%d"),
                Hora=horas[idx % len(horas)],
                Paciente_nroPaciente=paciente.nroPaciente,
                Medico_Matricula=medico.Matricula,
                Especialidad_Id=esp.Especialidad_Id,
                Estado_Id=ESTADO_CONFIRMADO,
                Sucursal_Id=(idx % 4) + 1,
                Duracion=30,
                Motivo=f"Confirmado {idx+1}",
            )
        )
        idx += 1

    db.add_all(turnos)
    db.commit()

    print(f"✅ {len(turnos)} turnos creados con fechas válidas según reglas.")


def seed_admin_user(db: Session):
    """Crea un usuario administrador"""
    print("👑 Creando usuario administrador...")

    admin = User(
        Email="admin@hospital.com",
        Password_Hash=pwd_context.hash("admin123"),
        Role_Id=1,  # Rol Admin
    )

    db.add(admin)
    db.commit()
    print("✅ Usuario administrador creado (admin@hospital.com / admin123)")


def main():
    """Función principal"""
    print("\n" + "=" * 60)
    print("🌱 INICIANDO SEED DE BASE DE DATOS")
    print("=" * 60 + "\n")

    # Crear las tablas si no existen
    Base.metadata.create_all(bind=engine)

    # Crear sesión
    db = SessionLocal()

    try:
        # Limpiar base de datos (CUIDADO: Esto borra todos los datos)
        clear_database(db)

        # Insertar datos
        seed_roles(db)
        seed_estados(db)
        seed_sucursales(db)
        seed_consultorios(db)
        seed_especialidades(db)
        seed_users_and_medicos(db)
        seed_users_and_pacientes(db)
        seed_agendas_regulares(db)
        seed_turnos(db)
        seed_admin_user(db)

        print("\n" + "=" * 60)
        print("✅ SEED COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        print("\n📋 CREDENCIALES DE ACCESO:")
        print("-" * 60)
        print("👑 Admin:")
        print("   Email: admin@hospital.com")
        print("   Password: admin123")
        print("\n👨‍⚕️ Médicos (todos tienen password: medico123):")
        print("   juan.perez@hospital.com")
        print("   maria.gonzalez@hospital.com")
        print("   ... y más")
        print("\n👤 Pacientes (todos tienen password: paciente123):")
        print("   pedro.gomez@email.com")
        print("   sofia.lopez@email.com")
        print("   ... y más")
        print("=" * 60 + "\n")

    except Exception as e:
        print(f"❌ Error durante el seed: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
