import argparse
import subprocess
import os
import pyfiglet
from colorama import init, Fore, Style
import requests
from urllib.parse import urlparse

def print_title():
    """Print the script title and description."""
    title = pyfiglet.figlet_format("Wayback Sensitive Info Detector")
    description = """
    Wayback Sensitive Info Detector - A sophisticated tool for identifying sensitive information in archived URLs.
    This tool can check a single domain or a list of domains for indications of sensitive information.
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

def save_result(domain, results):
    """Save the detected sensitive URLs to a file in a folder named after the domain."""
    folder_name = domain.replace(".", "_")
    os.makedirs(folder_name, exist_ok=True)
    output_file = os.path.join(folder_name, f"{folder_name}.txt")

    with open(output_file, 'w') as file:
        if results:
            file.write("Potential sensitive information found in the following URLs:\n")
            for url in results:
                file.write(url + '\n')
        else:
            file.write("No sensitive information found in the URLs.\n")

    print(f"Results saved in {output_file}")

def check_sensitive_info(url, sensitive_keywords):
    """Check if the URL contains sensitive information."""
    return any(keyword in url.lower() for keyword in sensitive_keywords)

def fetch_urls(domain, sensitive_keywords):
    """Run getallurls tool and fetch URLs, excluding non-interesting files."""
    try:
        # Run the `gau` command to fetch URLs, excluding non-interesting files
        result = subprocess.run(['gau', domain,'--fc','404', '--blacklist', '.jpg,.jpeg,.png,.gif,.svg,.bmp,.ico,.tiff,.webp,.css,.woff,.woff2,.ttf,.otf'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check if the command ran successfully
        if result.returncode != 0:
            print(f"{Fore.RED}Error running gau: {result.stderr}{Style.RESET_ALL}")
            return []

        # Split the output into lines (URLs)
        urls = result.stdout.splitlines()

        # Filter out JavaScript files unless they contain sensitive keywords
        urls = [url for url in urls if not url.endswith(('.js')) or check_sensitive_info(url, sensitive_keywords)]

        return urls

    except Exception as e:
        print(f"{Fore.RED}Exception occurred while fetching URLs for {domain}: {str(e)}{Style.RESET_ALL}")
        return []

def process_domains(domains, sensitive_keywords):
    """Process a list of domains to check for sensitive information."""
    for domain in domains:
        print(f"\nChecking {domain}...")
        urls = fetch_urls(domain, sensitive_keywords)
        if not urls:
            print(f"{Fore.RED}- No URLs found for {domain}.{Style.RESET_ALL}")
            continue

        sensitive_urls = [url for url in urls if check_sensitive_info(url, sensitive_keywords)]
        if sensitive_urls:
            print(f"{Fore.GREEN}+ Sensitive information found in URLs for {domain}.{Style.RESET_ALL}")
            save_result(domain, sensitive_urls)
        else:
            print(f"{Fore.RED}- No sensitive information found in URLs for {domain}.{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(description="Check archived URLs for sensitive information.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-u', '--url', type=str, help="Check a single domain.")
    group.add_argument('-f', '--file', type=str, help="Path to the file containing the list of domains.")
    parser.add_argument('-k', '--keywords', type=str, nargs='+', help="Custom sensitive keywords to search for.")
    args = parser.parse_args()

    init(autoreset=True)
    print_title()

    sensitive_keywords = args.keywords if args.keywords else [
        'password', 'credential', 'admin', 'login', 'secret', 'key', 'config', 'confidential',
        'private', 'token', 'auth', 'session', 'account', 'database', 'root', 'backup',
        'user', 'username', 'access', 'secure', 'payment',
        'credit', 'card', 'billing', 'invoice', 'purchase', 'order', 'customer', 'client',
        'api', 'apikey', 'hidden', 'internal', 'sensitive', 'temp', 'tmp', 'test',
        'development', 'dev', 'stage', 'staging', 'uat', 'prod', 'production', 'debug', 'trace',
        'error', 'bug', 'logs', 'log', 'dump', 'import', 'export', 'upload', 'download'
    ]

    if args.url:
        domains = [args.url]
    elif args.file:
        domains = read_domains(args.file)

    process_domains(domains, sensitive_keywords)

if __name__ == "__main__":
    main()

