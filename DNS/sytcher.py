import argparse
import requests
import sys
from termcolor import colored
import subprocess

def print_banner():
    banner = """
   ____        _       _                 
  / ___| _   _| |_ ___| |__   ___ _ __   
  \___ \| | | | __/ __| '_ \ / _ \ '__|  
   ___) | |_| | || (__| | | |  __/ |     
  |____/ \__, |\__\___|_| |_|\___|_|     
         |___/                           
    Subdomain Finder & Web Service Checker
    """
    print(colored(banner, 'green'))

def run_assetfinder(domain, output_file):
    """Run the assetfinder command-line tool and save results to a file."""
    try:
        result = subprocess.run(
            ["assetfinder", "--subs-only", domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        if result.returncode == 0:
            subdomains = [line.strip() for line in result.stdout.splitlines() if line.endswith(domain)]
            with open(output_file, 'w') as file:
                file.write("\n".join(subdomains) + "\n")
            return subdomains
        else:
            print(colored(f"[!] Assetfinder error: {result.stderr}", 'red'))
    except FileNotFoundError:
        print(colored("[!] Assetfinder is not installed or not in PATH.", 'red'))
    return []

def is_live(subdomain):
    """Check if the subdomain is live by resolving it."""
    try:
        response = requests.get(f"http://{subdomain}", timeout=5)
        return True
    except requests.RequestException:
        return False

def check_web_service(subdomain, timeout):
    """Check if the subdomain has a web service."""
    urls = [f"http://{subdomain}", f"https://{subdomain}"]
    for url in urls:
        try:
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                return url
        except requests.RequestException:
            continue
    return None

def main():
    print_banner()

    parser = argparse.ArgumentParser(
        description="Find subdomains of a domain and check for web services."
    )
    parser.add_argument(
        "-d", "--domain", required=True, help="Target domain (e.g., test.com)"
    )
    parser.add_argument(
        "-o", "--output", required=True, help="Output file to save all found subdomains"
    )
    parser.add_argument(
        "-l", "--live_output", required=True, help="Output file to save live subdomains"
    )
    parser.add_argument(
        "-w", "--web_output", required=True, help="Output file to save subdomains with web services"
    )
    parser.add_argument(
        "-t", "--timeout", type=int, default=10, help="Timeout for web service check (default: 10 seconds)"
    )

    args = parser.parse_args()

    domain = args.domain
    output_file = args.output
    live_output = args.live_output
    web_output = args.web_output
    timeout = args.timeout

    print(colored(f"[+] Running assetfinder for domain: {domain}\n", 'cyan'))

    subdomains = run_assetfinder(domain, output_file)

    if not subdomains:
        print(colored("[-] No subdomains found.", 'red'))
        sys.exit(1)

    live_subdomains = []
    web_services = []

    print(colored(f"[+] Checking for live subdomains\n", 'cyan'))

    for subdomain in subdomains:
        if is_live(subdomain):
            live_subdomains.append(subdomain)
            with open(live_output, 'a') as live_file:
                live_file.write(subdomain + "\n")

    print(colored(f"[+] Checking for web services on live subdomains\n", 'cyan'))

    for subdomain in live_subdomains:
        service_url = check_web_service(subdomain, timeout)
        if service_url:
            web_services.append(service_url)
            with open(web_output, 'a') as web_file:
                web_file.write(service_url + "\n")
            print(colored(f"[+] Found web service: {service_url}", 'green'))

    print(colored(f"[+] Subdomain discovery and checks completed. Results saved.", 'yellow'))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(colored("\n[!] Script interrupted by user.", 'red'))
        sys.exit(1)

