# run.py - Ejecutar simulación por consola

from model_hospital import HospitalModel

# Inicializar el modelo con una planta 5x5 y algunos agentes
model = HospitalModel(
    width=6,
    height=6,
    n_pacientes=5,
    n_medicos=2,
    n_enfermeros=2,
    n_limpieza=1,
    n_recepcionistas=1
)

# Simular desde las 08:00 hasta las 21:00
for i in range(14):
    print(f"\n🕒 Hora: {model.current_hour}:00")
    model.step()
    for agent in model.schedule.agents:
        print(f"{agent.__class__.__name__} {agent.unique_id} está en {agent.pos}")