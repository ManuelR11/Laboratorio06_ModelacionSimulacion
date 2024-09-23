import numpy as np

# Constantes
SIMULATION_TIME = 3600 
LAMBDA = 40
SERVICE_RATE_PROVIDER1 = 100
SERVICE_RATE_PROVIDER2 = 10

# Función para generar llegadas según proceso de Poisson
def generate_arrivals(lambd, time):
    arrivals = []
    current_time = 0
    while current_time < time:
        inter_arrival_time = np.random.exponential(1/lambd)
        current_time += inter_arrival_time
        arrivals.append(current_time)
    return np.array(arrivals)

# Función para generar tiempos de servicio según distribución exponencial
def generate_service_times(mu, num_services):
    return np.random.exponential(1/mu, num_services)

# Simular el comportamiento de un sistema de servidor único (Proveedor 1)
def simulate_single_server(lambd, mu, sim_time):
    arrivals = generate_arrivals(lambd, sim_time)
    num_arrivals = len(arrivals)
    service_times = generate_service_times(mu, num_arrivals)
    
    departure_times = np.zeros(num_arrivals)
    server_busy_time = 0
    total_queue_time = 0
    queue_lengths = []

    for i in range(num_arrivals):
        if i == 0:
            departure_times[i] = arrivals[i] + service_times[i]
        else:
            if arrivals[i] > departure_times[i-1]:
                departure_times[i] = arrivals[i] + service_times[i]
            else:
                total_queue_time += (departure_times[i-1] - arrivals[i])
                departure_times[i] = departure_times[i-1] + service_times[i]
        server_busy_time += service_times[i]
        queue_lengths.append(max(0, departure_times[i-1] - arrivals[i]))

    server_idle_time = sim_time - server_busy_time
    total_time_in_queue = total_queue_time
    avg_time_in_queue = total_queue_time / num_arrivals
    avg_queue_length = np.mean(queue_lengths)
    last_departure = departure_times[-1]

    return {
        "Solicitudes atendidas": num_arrivals,
        "Tiempo ocupado": server_busy_time,
        "Tiempo desocupado": server_idle_time,
        "Tiempo total en cola": total_time_in_queue,
        "Promedio tiempo en cola": avg_time_in_queue,
        "Promedio solicitudes en cola por segundo": avg_queue_length,
        "Momento de la última salida": last_departure
    }

# Simular el comportamiento del sistema con múltiples servidores (Proveedor 2)
def simulate_multiple_servers(lambd, mu, sim_time, server_capacity):
    arrivals = generate_arrivals(lambd, sim_time)
    num_arrivals = len(arrivals)
    service_times = generate_service_times(mu, num_arrivals)
    
    servers = [0] * server_capacity
    server_busy_time = [0] * server_capacity
    total_queue_time = 0
    queue_lengths = []

    for i in range(num_arrivals):
        earliest_server = np.argmin(servers)
        if arrivals[i] > servers[earliest_server]:
            servers[earliest_server] = arrivals[i] + service_times[i]
        else:
            total_queue_time += (servers[earliest_server] - arrivals[i])
            servers[earliest_server] += service_times[i]
        server_busy_time[earliest_server] += service_times[i]
        queue_lengths.append(max(0, servers[earliest_server] - arrivals[i]))

    server_idle_time = [sim_time - busy for busy in server_busy_time]
    total_time_in_queue = total_queue_time
    avg_time_in_queue = total_queue_time / num_arrivals
    avg_queue_length = np.mean(queue_lengths)
    last_departure = max(servers)

    return {
        "Solicitudes atendidas": num_arrivals,
        "Tiempo ocupado por servidor": server_busy_time,
        "Tiempo desocupado por servidor": server_idle_time,
        "Tiempo total en cola": total_time_in_queue,
        "Promedio tiempo en cola": avg_time_in_queue,
        "Promedio solicitudes en cola por segundo": avg_queue_length,
        "Momento de la última salida": last_departure
    }

# Búsqueda empírica del número mínimo de servidores necesarios
def find_min_servers(lambd, mu, sim_time):
    num_servers = 1
    while True:
        total_queue_time = simulate_multiple_servers(lambd, mu, sim_time, num_servers)["Tiempo total en cola"]
        if total_queue_time == 0:
            return num_servers
        num_servers += 1

# Simulación para Proveedor 1 (Mountain Mega Computing)
result_provider1 = simulate_single_server(LAMBDA, SERVICE_RATE_PROVIDER1, SIMULATION_TIME)
print("Resultados de Mountain Mega Computing:")
for key, value in result_provider1.items():
    print(f"{key}: {value}")

# Simulación para Proveedor 2 (Pizzita Computing), con capacidad dinámica de servidores
num_servers = 10
result_provider2 = simulate_multiple_servers(LAMBDA, SERVICE_RATE_PROVIDER2, SIMULATION_TIME, num_servers)
print("\nResultados de Pizzita Computing:")
for key, value in result_provider2.items():
    print(f"{key}: {value}")

# Encontrar el número mínimo de servidores para Pizzita Computing
min_servers = find_min_servers(LAMBDA, SERVICE_RATE_PROVIDER2, SIMULATION_TIME)
print(f"\nNúmero mínimo de servidores necesarios en Pizzita Computing para evitar colas: {min_servers}")
