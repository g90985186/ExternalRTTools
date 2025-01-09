import argparse
import requests
import csv
import time
from colorama import Fore, Style, init

# Initialize colorama for cross-platform support
init()

def display_title():
    title = """
    ==========================================
         Censys Open Ports Search Script
    ==========================================
    """
    print(Fore.CYAN + title + Style.RESET_ALL)

def censys_search(api_id, api_secret, target, output_file=None):
    url = "https://search.censys.io/api/v2/hosts/search"
    headers = {
        "Accept": "application/json",
    }

    if "/" in target:
        # IP range query
        query = f"ip:{target}"
    elif target.replace(".", "").isdigit():
        # Single IP address
        query = f"ip:{target}"
    else:
        # Domain name
        query = f"domain:{target}"

    payload = {
        "q": query
    }

    try:
        # Add rate limiting: 0.4 actions per second for search
        time.sleep(2.5)  # Delay to comply with the 0.4 actions/second limit

        response = requests.post(url, headers=headers, json=payload, auth=(api_id, api_secret))
        if response.status_code == 200:
            results = response.json()
            print(Fore.GREEN + f"Search results for target '{target}':" + Style.RESET_ALL)

            # Output processing
            results_list = results.get("result", {}).get("hits", [])
            aggregated_data = {}

            if results_list:
                for result in results_list:
                    ip = result.get("ip", "N/A")
                    services = result.get("services", [])
                    for service in services:
                        port = service.get('port', 'N/A')
                        service_name = service.get('service_name', 'N/A')
                        if ip not in aggregated_data:
                            aggregated_data[ip] = {"ports": [], "services": []}
                        aggregated_data[ip]["ports"].append(port)
                        aggregated_data[ip]["services"].append(service_name)

                if output_file:
                    with open(output_file, "w", newline="") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(["IP Address", "Open Ports", "Services"])
                        for ip, data in aggregated_data.items():
                            ports_str = ", ".join(map(str, data["ports"]))
                            services_str = ", ".join(data["services"])
                            print(Fore.GREEN + f"IP: {ip} - Ports: {ports_str} - Services: {services_str}" + Style.RESET_ALL)
                            writer.writerow([ip, ports_str, services_str])
                    print(Fore.BLUE + f"Results saved to {output_file}" + Style.RESET_ALL)
                else:
                    for ip, data in aggregated_data.items():
                        ports_str = ", ".join(map(str, data["ports"]))
                        services_str = ", ".join(data["services"])
                        print(Fore.GREEN + f"IP: {ip} - Ports: {ports_str} - Services: {services_str}" + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + "No results found." + Style.RESET_ALL)
        elif response.status_code == 401:
            print(Fore.RED + "Unauthorized: Invalid API credentials." + Style.RESET_ALL)
        elif response.status_code == 429:
            print(Fore.RED + "Rate limit exceeded. Retrying after delay..." + Style.RESET_ALL)
            time.sleep(60)  # Delay for retry to comply with rate limits
            censys_search(api_id, api_secret, target, output_file)
        else:
            print(Fore.RED + f"Error: {response.status_code} - {response.text}" + Style.RESET_ALL)
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Request failed: {e}" + Style.RESET_ALL)

def main():
    display_title()

    parser = argparse.ArgumentParser(description="Search Censys API for open ports associated with an IP range, IP address, or domain.")
    parser.add_argument("--api-id", required=True, help="Your Censys API ID.")
    parser.add_argument("--api-secret", required=True, help="Your Censys API Secret.")
    parser.add_argument("--target", required=True, help="IP range, single IP address, or domain to search.")
    parser.add_argument("-o", "--output", help="CSV file to save the output.")

    args = parser.parse_args()

    censys_search(args.api_id, args.api_secret, args.target, args.output)

if __name__ == "__main__":
    main()

