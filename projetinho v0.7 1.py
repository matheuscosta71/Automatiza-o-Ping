import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

def ping_ip(location, ip):
    # Executa o comando ping via subprocesso
    process = subprocess.Popen(['ping', '-n', '4', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output, _ = process.communicate()

    # Verifica se houve timeout ou TTL expirado na saída
    error_indicators = ["Esgotado o tempo limite do pedido", "TTL expirado", "expirou em trânsito"]
    is_failure = any(indicator in output for indicator in error_indicators)
    success = process.returncode == 0 and not is_failure  # Verifica se o processo retornou com código de saída zero e não houve erros indicados

    return location, ip, success, output

# Dicionário que mapeia IPs para localidades
ip_locations = { 
                
'201.60.28.774' : 'CIE 79881',
'201.60.48.635' : 'CIE 9660',
'201.60.13.857' : 'CIE 903401',
    
}

# Listas para armazenar os resultados dos pings bem-sucedidos e falhados
successful_pings = []
failed_pings = []

# Usar ThreadPoolExecutor para realizar os pings em paralelo
with ThreadPoolExecutor(max_workers=100) as executor:  # Ajuste max_workers conforme necessário
    futures = {executor.submit(ping_ip, location, ip): (location, ip) for ip, location in ip_locations.items()}
    for future in as_completed(futures):
        location, ip = futures[future]
        try:
            result = future.result()
            if result[2]:  # Se o ping foi bem-sucedido
                successful_pings.append(result)
            else:
                failed_pings.append(result)
        except Exception as e:
            print(f"Ping para {location} ({ip}) falhou com exceção: {e}")
            failed_pings.append((location, ip, False, str(e)))

# Imprime os resultados dos pings bem-sucedidos
print("Pings bem-sucedidos:")
for location, ip, success, output in successful_pings:
    print(f"Output for {location} ({ip}):\n{output}")

# Imprime os resultados dos pings falhados
print("\nPings que falharam:")
for location, ip, success, output in failed_pings:
    print(f"Output for {location} ({ip}):\n{output}")
