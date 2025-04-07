import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_http_access(location, ip):
    urls = [f"http://{ip}", f"https://{ip}"]
    accessible = False

    for url in urls:
        try:
            response = requests.get(url, timeout=3)  # Tempo limite de 3 segundos
            if response.status_code == 200:
                accessible = True
                break  # Se uma das portas funcionar, já consideramos acessível
        except requests.RequestException:
            pass  # Ignora erros de conexão

    return location, ip, accessible

# Dicionário que mapeia IPs para localidades
ip_locations = {

'10.117.89.156' : 'CIE 921130',
'10.115.227.259' : 'CIE 24703',
'10.172.196.429' : 'CIE 48975',
'10.172.196.630' : 'CIE 48975',
}

# Listas para armazenar os resultados
accessible_ips = []
inaccessible_ips = []

# Executar verificações em paralelo
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(check_http_access, location, ip): (location, ip) for ip, location in ip_locations.items()}
    
    for future in as_completed(futures):
        location, ip = futures[future]
        try:
            location, ip, success = future.result()
            if success:
                accessible_ips.append((location, ip))
            else:
                inaccessible_ips.append((location, ip))
        except Exception as e:
            print(f"Erro ao verificar {location} ({ip}): {e}")
            inaccessible_ips.append((location, ip))

# Salvar os resultados em um arquivo de texto
with open('resultados_http.txt', 'w', encoding='utf-8') as file:
    file.write("===== IPs que acessam via HTTP/HTTPS =====\n")
    for location, ip in accessible_ips:
        file.write(f"{location}: {ip} - Acessível\n")

    file.write("\n===== IPs que NÃO acessam via HTTP/HTTPS =====\n")
    for location, ip in inaccessible_ips:
        file.write(f"{location}: {ip} - Inacessível\n")

print("Resultados salvos no arquivo 'resultados_http.txt'.")
