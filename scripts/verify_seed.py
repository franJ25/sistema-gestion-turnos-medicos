"""
Script para verificar los datos insertados en la base de datos
"""

from app.backend.db.db import SessionLocal
from app.backend.models.models import (
    Sucursal, Consultorio, Especialidad, Medico, Paciente,
    Estado, AgendaRegular, Turno, User, Role
)

db = SessionLocal()

print("\n" + "="*60)
print("📊 VERIFICACIÓN DE DATOS EN LA BASE DE DATOS")
print("="*60 + "\n")

# Contar registros
roles_count = db.query(Role).count()
users_count = db.query(User).count()
sucursales_count = db.query(Sucursal).count()
consultorios_count = db.query(Consultorio).count()
especialidades_count = db.query(Especialidad).count()
medicos_count = db.query(Medico).count()
pacientes_count = db.query(Paciente).count()
estados_count = db.query(Estado).count()
agendas_count = db.query(AgendaRegular).count()
turnos_count = db.query(Turno).count()

print(f"👥 Roles:              {roles_count}")
print(f"👤 Usuarios:           {users_count}")
print(f"🏥 Sucursales:         {sucursales_count}")
print(f"🚪 Consultorios:       {consultorios_count}")
print(f"⚕️  Especialidades:     {especialidades_count}")
print(f"👨‍⚕️ Médicos:            {medicos_count}")
print(f"🧑 Pacientes:          {pacientes_count}")
print(f"📊 Estados:            {estados_count}")
print(f"📅 Agendas regulares:  {agendas_count}")
print(f"🗓️  Turnos:             {turnos_count}")

print("\n" + "="*60)
print("✅ VERIFICACIÓN COMPLETADA")
print("="*60 + "\n")

# Mostrar algunos ejemplos
print("📋 EJEMPLOS DE DATOS INSERTADOS:\n")

print("👨‍⚕️ Primeros 3 médicos:")
medicos = db.query(Medico).limit(3).all()
for m in medicos:
    print(f"   - {m.Nombre} {m.Apellido} (Matrícula: {m.Matricula})")

print("\n🧑 Primeros 3 pacientes:")
pacientes = db.query(Paciente).limit(3).all()
for p in pacientes:
    print(f"   - {p.Nombre} {p.Apellido} (Email: {p.Email})")

print("\n🗓️  Primeros 3 turnos:")
turnos = db.query(Turno).limit(3).all()
for t in turnos:
    print(f"   - Fecha: {t.Fecha}, Hora: {t.Hora}, Paciente ID: {t.Paciente_nroPaciente}")

db.close()
