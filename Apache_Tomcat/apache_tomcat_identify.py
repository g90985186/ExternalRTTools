import argparse
import requests
from requests.exceptions import RequestException, Timeout
from urllib.parse import urlparse
import pyfiglet
from colorama import init, Fore, Style

def print_title():
    """Print the script title and description."""
    title = pyfiglet.figlet_format("Tomcat Detector")
    description = """
    Tomcat Detector - A sophisticated tool for identifying Apache Tomcat servers.
    This tool can check a single domain or a list of domains for indications of Apache Tomcat.
    """
    print(title)
    print(description)

def read_domains(file_path):
    """Read domains from a file and return them as a list."""
    with open(file_path, 'r') as file:
        domains = [line.strip() for line in file.readlines()]
    return domains

def log_check(action, result=None):
    """Log the actions taken and the results."""
    if result is not None:
        color = Fore.GREEN if result == "Detected" else Fore.RED
        symbol = "+" if result == "Detected" else "-"
        print(f"{color}{symbol} {action}: {result}{Style.RESET_ALL}")
    else:
        print(f"Checking {action}...")

def save_result(domain, port, results_file):
    """Save the detected domain and port to the results file."""
    with open(results_file, 'a') as file:
        file.write(f"{domain}:{port}\n")

def check_tomcat(domain, port, timeout=5):
    """Check if the given domain is running on Apache Tomcat."""
    scheme = 'https' if port == 443 else 'http'
    url = f'{scheme}://{domain}:{port}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        # Check Server header
        log_check(f"Server header on port {port}")
        server_header = response.headers.get('Server', '')
        if 'tomcat' in server_header.lower():
            log_check(f"Server header on port {port}", "Detected")
            return True
        log_check(f"Server header on port {port}", "Not detected")

        # Check X-Powered-By header
        log_check(f"X-Powered-By header on port {port}")
        x_powered_by = response.headers.get('X-Powered-By', '')
        if 'tomcat' in x_powered_by.lower():
            log_check(f"X-Powered-By header on port {port}", "Detected")
            return True
        log_check(f"X-Powered-By header on port {port}", "Not detected")

        # Check for Java JSESSIONID cookie
        log_check(f"JSESSIONID cookie on port {port}")
        if 'JSESSIONID' in response.cookies:
            log_check(f"JSESSIONID cookie on port {port}", "Detected")
            return True
        log_check(f"JSESSIONID cookie on port {port}", "Not detected")

        # Check response content for common Tomcat indications
        log_check(f"Response content on port {port}")
        if 'Apache Tomcat' in response.text or 'Tomcat/' in response.text:
            log_check(f"Response content on port {port}", "Detected")
            return True
        log_check(f"Response content on port {port}", "Not detected")

        # Check for default Tomcat management endpoints
        if check_tomcat_management_endpoints(domain, scheme, port, headers, timeout):
            return True

        # Check for Tomcat specific error pages
        if check_tomcat_error_pages(domain, scheme, port, headers, timeout):
            return True

        # Check for fingerprinting URLs and resources
        if check_tomcat_fingerprint_resources(domain, scheme, port, headers, timeout):
            return True

        # Check for common Tomcat directories and files
        if check_tomcat_common_directories_files(domain, scheme, port, headers, timeout):
            return True

        # Check HTTP methods behavior
        if check_tomcat_http_methods(domain, scheme, port, headers, timeout):
            return True

        # Probe for known Tomcat vulnerabilities
        if check_tomcat_vulnerabilities(domain, scheme, port, headers, timeout):
            return True

        return False
    except Timeout:
        print(f"{Fore.RED}Error: Timeout occurred while checking {domain}:{port}{Style.RESET_ALL}")
        return False
    except RequestException as e:
        print(f"{Fore.RED}Error checking domain {domain}:{port}: {e}{Style.RESET_ALL}")
        return False

def check_tomcat_management_endpoints(domain, scheme, port, headers, timeout):
    """Check for default Tomcat management endpoints."""
    management_paths = ['/manager/html', '/host-manager/html']
    for path in management_paths:
        log_check(f"Management endpoint {path} on port {port}")
        url = f'{scheme}://{domain}:{port}{path}'
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            if response.status_code == 200 and ('Tomcat Manager' in response.text or 'Tomcat Host Manager' in response.text):
                log_check(f"Management endpoint {path} on port {port}", "Detected")
                return True
        except RequestException:
            log_check(f"Management endpoint {path} on port {port}", "Not detected")
            continue
    return False

def check_tomcat_error_pages(domain, scheme, port, headers, timeout):
    """Check for Tomcat specific error pages."""
    log_check(f"Error page on port {port}")
    url = f'{scheme}://{domain}:{port}/nonexistentpage'
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        if response.status_code == 404 and 'Apache Tomcat' in response.text:
            log_check(f"Error page on port {port}", "Detected")
            return True
    except RequestException:
        log_check(f"Error page on port {port}", "Not detected")
    return False

def check_tomcat_fingerprint_resources(domain, scheme, port, headers, timeout):
    """Check for Tomcat-specific URLs and resources."""
    fingerprint_paths = [
        '/docs/', '/examples/', '/host-manager/', '/manager/', '/webapps/', 
        '/favicon.ico', '/index.jsp'
    ]
    for path in fingerprint_paths:
        log_check(f"Fingerprint resource {path} on port {port}")
        url = f'{scheme}://{domain}:{port}{path}'
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            if response.status_code == 200 and ('Apache Tomcat' in response.text or 'Tomcat/' in response.text):
                log_check(f"Fingerprint resource {path} on port {port}", "Detected")
                return True
        except RequestException:
            log_check(f"Fingerprint resource {path} on port {port}", "Not detected")
            continue
    return False

def check_tomcat_common_directories_files(domain, scheme, port, headers, timeout):
    """Check for common Tomcat directories and files."""
    common_paths = [
        '/conf/', '/webapps/', '/logs/', '/conf/server.xml', '/web.xml'
    ]
    for path in common_paths:
        log_check(f"Common directory/file {path} on port {port}")
        url = f'{scheme}://{domain}:{port}{path}'
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            if response.status_code == 200 and ('Apache Tomcat' in response.text or 'Tomcat/' in response.text):
                log_check(f"Common directory/file {path} on port {port}", "Detected")
                return True
        except RequestException:
            log_check(f"Common directory/file {path} on port {port}", "Not detected")
            continue
    return False

def check_tomcat_http_methods(domain, scheme, port, headers, timeout):
    """Check for Tomcat-specific behavior with certain HTTP methods."""
    methods = ['OPTIONS', 'PUT', 'DELETE']
    for method in methods:
        log_check(f"HTTP method {method} on port {port}")
        try:
            response = requests.request(method, f'{scheme}://{domain}:{port}', headers=headers, timeout=timeout)
            if response.status_code == 200 and 'Apache Tomcat' in response.text:
                log_check(f"HTTP method {method} on port {port}", "Detected")
                return True
        except RequestException:
            log_check(f"HTTP method {method} on port {port}", "Not detected")
            continue
    return False

def check_tomcat_vulnerabilities(domain, scheme, port, headers, timeout):
    """Probe for known Tomcat vulnerabilities."""
    known_vulnerabilities = [
        # Example: Check for CVE-2020-1938 (Ghostcat)
        ('/AJP/13', 'Vulnerable to CVE-2020-1938 (Ghostcat)')
    ]
    for path, description in known_vulnerabilities:
        log_check(f"Vulnerability check {path} on port {port}")
        url = f'{scheme}://{domain}:{port}{path}'
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            if response.status_code == 200:
                log_check(f"Vulnerability check {path} on port {port}", f"Detected - {description}")
                return True
        except RequestException:
            log_check(f"Vulnerability check {path} on port {port}", "Not detected")
            continue
    return False

def process_domains(domains, use_https, timeout, results_file):
    """Process a list of domains to check for Apache Tomcat."""
    ports = [80, 443, 8080]
    for domain in domains:
        for port in ports:
            print(f"\nChecking {domain} on port {port}...")
            if check_tomcat(domain, port, timeout):
                print(f"{Fore.GREEN}+ {domain}:{port} is running on Apache Tomcat.{Style.RESET_ALL}")
                save_result(domain, port, results_file)
            else:
                print(f"{Fore.RED}- {domain}:{port} is not running on Apache Tomcat or could not be determined.{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(description="Check if domains are running on Apache Tomcat.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', '--url', type=str, help="Check a single domain.")
    group.add_argument('-f', '--file', type=str, help="Path to the file containing the list of domains.")
    parser.add_argument('--https', action='store_true', help="Use HTTPS instead of HTTP.")
    parser.add_argument('--timeout', type=int, default=5, help="Request timeout in seconds. Default is 5 seconds.")
    parser.add_argument('--results', type=str, default='results.txt', help="Path to the results file. Default is results.txt.")
    args = parser.parse_args()

    init(autoreset=True)
    print_title()

    if args.url:
        domains = [args.url]
    elif args.file:
        domains = read_domains(args.file)

    process_domains(domains, use_https=args.https, timeout=args.timeout, results_file=args.results)

if __name__ == "__main__":
    main()

