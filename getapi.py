import requests

# Dynatrace configuration
DYNATRACE_URL = "https://<YOUR_ENV>.live.dynatrace.com"
API_TOKEN = "<YOUR_API_TOKEN>"
HEADERS = {
    "Authorization": f"Api-Token {API_TOKEN}",
    "Content-Type": "application/json"
}

def get_hosts():
    """Fetches all monitored hosts"""
    url = f"{DYNATRACE_URL}/api/v1/entity/infrastructure/hosts"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_host_details(entity_id):
    """Fetches detailed information for a single host"""
    url = f"{DYNATRACE_URL}/api/v1/entity/infrastructure/hosts/{entity_id}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def main():
    hosts_data = get_hosts()
    results = []

    for host in hosts_data:
        details = get_host_details(host['entityId'])
        host_info = {
            "hostname": host.get("displayName"),
            "cpu_cores": host.get("cpuCores"),
            "memory_total_mb": host.get("memoryTotal"),
            "disk_total_mb": details.get("diskTotal")
        }
        results.append(host_info)

    for item in results:
        print(item)

if __name__ == "__main__":
    main()
