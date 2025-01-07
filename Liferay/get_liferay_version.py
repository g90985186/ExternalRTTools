import argparse
import requests
from requests.exceptions import RequestException, Timeout
from urllib.parse import urlparse
import pyfiglet
from colorama import init, Fore, Style
from bs4 import BeautifulSoup, Comment
import re

def print_title():
    """Print the script title and description."""
    title = pyfiglet.figlet_format("Liferay Version Detector")
    description = """
    Liferay Version Detector - A sophisticated tool for identifying Liferay portal versions.
    This tool can check a single domain or a list of domains for indications of Liferay versions.
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

def save_result(domain, version, results_file):
    """Save the detected domain and version to the results file."""
    with open(results_file, 'a') as file:
        file.write(f"{domain}: {version}\n")

def get_liferay_version(url, timeout=5):
    """Determine the Liferay version for a given URL."""
    strategies = [
        check_headers,
        check_meta_tags,
        check_common_endpoints,
        check_comments,
        check_jsp_files,
        check_js_variables
    ]
    for strategy in strategies:
        version = strategy(url, timeout)
        if version:
            return version
    return "Liferay version not found"

def check_headers(url, timeout):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        log_check("HTTP headers")
        if 'Liferay-Portal' in response.headers:
            version = response.headers['Liferay-Portal']
            log_check("HTTP headers", "Detected")
            return version
        log_check("HTTP headers", "Not detected")
    except RequestException as e:
        print(f"{Fore.RED}Headers check failed: {e}{Style.RESET_ALL}")
    return None

def check_meta_tags(url, timeout):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        log_check("Meta tags")
        soup = BeautifulSoup(response.content, 'html.parser')
        meta_generator = soup.find('meta', attrs={'name': 'generator'})
        if meta_generator and 'Liferay' in meta_generator['content']:
            log_check("Meta tags", "Detected")
            return meta_generator['content']
        log_check("Meta tags", "Not detected")
    except RequestException as e:
        print(f"{Fore.RED}Meta tags check failed: {e}{Style.RESET_ALL}")
    return None

def check_common_endpoints(url, timeout):
    endpoints = [
        '/html/portal/update_available.html',
        '/api/jsonws',
        '/c/portal/update_available',
        '/c/portal/license',
        '/c/portal/login',
        '/api/jsonws/invoke',
        '/group/control_panel/manage',
        '/web/guest/home'
    ]
    for endpoint in endpoints:
        full_url = url + endpoint
        try:
            response = requests.get(full_url, timeout=timeout)
            if response.status_code == 200:
                version = extract_version_from_text(response.text)
                if version:
                    log_check(f"Endpoint {endpoint}", "Detected")
                    return version
            log_check(f"Endpoint {endpoint}", "Not detected")
        except RequestException as e:
            print(f"{Fore.RED}Endpoint {endpoint} check failed: {e}{Style.RESET_ALL}")
    return None

def check_comments(url, timeout):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        log_check("HTML comments")
        soup = BeautifulSoup(response.content, 'html.parser')
        comments = soup.findAll(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            version = extract_version_from_text(comment)
            if version:
                log_check("HTML comments", "Detected")
                return version
        log_check("HTML comments", "Not detected")
    except RequestException as e:
        print(f"{Fore.RED}Comments check failed: {e}{Style.RESET_ALL}")
    return None

def check_jsp_files(url, timeout):
    jsp_files = [
        '/html/common/themes/top.jsp',
        '/html/common/themes/bottom.jsp',
        '/html/portal/update_available.jsp',
        '/html/portal/setup_wizard.jsp'
    ]
    for jsp_file in jsp_files:
        full_url = url + jsp_file
        try:
            response = requests.get(full_url, timeout=timeout)
            if response.status_code == 200:
                version = extract_version_from_text(response.text)
                if version:
                    log_check(f"JSP file {jsp_file}", "Detected")
                    return version
            log_check(f"JSP file {jsp_file}", "Not detected")
        except RequestException as e:
            print(f"{Fore.RED}JSP file {jsp_file} check failed: {e}{Style.RESET_ALL}")
    return None

def check_js_variables(url, timeout):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        log_check("JavaScript variables")
        js_variables = re.findall(r'Liferay\.version\s*=\s*"(\d+\.\d+\.\d+)"', response.text)
        if js_variables:
            log_check("JavaScript variables", "Detected")
            return js_variables[0]
        log_check("JavaScript variables", "Not detected")
    except RequestException as e:
        print(f"{Fore.RED}JavaScript variables check failed: {e}{Style.RESET_ALL}")
    return None

def extract_version_from_text(text):
    version_patterns = [
        re.compile(r'Liferay Portal (\d+\.\d+\.\d+)'),
        re.compile(r'Liferay (\d+\.\d+\.\d+)'),
        re.compile(r'Version (\d+\.\d+\.\d+)'),
        re.compile(r'Liferay Version (\d+\.\d+\.\d+)'),
        re.compile(r'liferayVersion\s*=\s*"(\d+\.\d+\.\d+)"'),
        re.compile(r'Liferay\.version = "(\d+\.\d+\.\d+)"')
    ]
    for pattern in version_patterns:
        match = pattern.search(text)
        if match:
            return match.group(1)
    return None

def process_domains(domains, timeout, results_file):
    """Process a list of domains to check for Liferay version."""
    for domain in domains:
        url = f'http://{domain}'
        print(f"\nChecking {url}...")
        version = get_liferay_version(url, timeout)
        if version and version != "Liferay version not found":
            print(f"{Fore.GREEN}+ {domain}: {version}{Style.RESET_ALL}")
            save_result(domain, version, results_file)
        else:
            url = f'https://{domain}'
            print(f"\nChecking {url}...")
            version = get_liferay_version(url, timeout)
            if version and version != "Liferay version not found":
                print(f"{Fore.GREEN}+ {domain}: {version}{Style.RESET_ALL}")
                save_result(domain, version, results_file)
            else:
                print(f"{Fore.RED}- {domain}: Liferay version not found{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(description="Check if domains are running on Liferay and identify the version.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', '--url', type=str, help="Check a single domain.")
    group.add_argument('-f', '--file', type=str, help="Path to the file containing the list of domains.")
    parser.add_argument('--timeout', type=int, default=5, help="Request timeout in seconds. Default is 5 seconds.")
    parser.add_argument('--results', type=str, default='results.txt', help="Path to the results file. Default is results.txt.")
    args = parser.parse_args()

    init(autoreset=True)
    print_title()

    if args.url:
        domains = [args.url]
    elif args.file:
        domains = read_domains(args.file)

    process_domains(domains, timeout=args.timeout, results_file=args.results)

if __name__ == "__main__":
    main()

