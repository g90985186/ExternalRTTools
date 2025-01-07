import argparse
import requests
from colorama import Fore, Style, init
from getpass import getpass
import time

# Initialize colorama for cross-platform support
init()

def display_title():
    title = """
    ============================================
         Credential Searcher - By ChatGPT
    ============================================
    """
    print(Fore.CYAN + title + Style.RESET_ALL)

def search_dehashed(username, api_key, query, output_file=None, is_email=False):
    url = "https://api.dehashed.com/search"
    headers = {
        "Accept": "application/json"
    }
    params = {
        "query": f"{query}" if is_email else f"domain:{query}"
    }

    try:
        response = requests.get(url, headers=headers, params=params, auth=(username, api_key))
        if response.status_code == 200:
            results = response.json().get("entries", [])
            if results:
                seen_entries = set()  # To track unique email:password pairs
                output_lines = []  # To store output for saving to file
                print(Fore.GREEN + "Identified Credentials:" + Style.RESET_ALL)
                for entry in results:
                    email = entry.get("email", "N/A")
                    password = entry.get("password", "")
                    if password:  # Only process entries with a password value
                        credential = f"{email}:{password}"
                        if credential not in seen_entries:
                            seen_entries.add(credential)
                            print(Fore.GREEN + credential + Style.RESET_ALL)
                            output_lines.append(credential)
                if output_file:
                    with open(output_file, "w") as file:
                        file.write("\n".join(output_lines))
                    print(Fore.BLUE + f"Output saved to {output_file}" + Style.RESET_ALL)
            else:
                print(Fore.YELLOW + "No results found for the given query." + Style.RESET_ALL)
        elif response.status_code == 401:
            print(Fore.RED + "Unauthorized: Invalid username or API key." + Style.RESET_ALL)
        else:
            print(Fore.RED + f"Error: {response.status_code} - {response.text}" + Style.RESET_ALL)
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Request failed: {e}" + Style.RESET_ALL)

def search_hibp(api_key, email, output_file=None):
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
    headers = {
        "hibp-api-key": api_key,
        "user-agent": "CredentialSearcher"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            breaches = response.json()
            print(Fore.GREEN + f"Breaches found for {email}:" + Style.RESET_ALL)
            output_lines = []
            for breach in breaches:
                breach_name = breach.get("Name", "Unknown")
                print(Fore.GREEN + f"{email} was found in {breach_name}" + Style.RESET_ALL)
                output_lines.append(f"{email} was found in {breach_name}")
            if output_file:
                with open(output_file, "a") as file:
                    file.write("\n".join(output_lines) + "\n")
                print(Fore.BLUE + f"Output saved to {output_file}" + Style.RESET_ALL)
        elif response.status_code == 404:
            print(Fore.YELLOW + f"No breaches found for {email}." + Style.RESET_ALL)
        elif response.status_code == 429:
            print(Fore.RED + f"Rate limit exceeded for {email}. Retrying after delay..." + Style.RESET_ALL)
            time.sleep(5)  # Delay before retrying
            search_hibp(api_key, email, output_file)
        elif response.status_code == 401:
            print(Fore.RED + "Unauthorized: Invalid HIBP API key." + Style.RESET_ALL)
        else:
            print(Fore.RED + f"Error: {response.status_code} - {response.text}" + Style.RESET_ALL)
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Request failed: {e}" + Style.RESET_ALL)

def search_leakcheck(api_key, email, output_file=None):
    url = "https://leakcheck.net/api/v1/check"
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": api_key,
        "query": email,
        "type": "email"  # Specify the type of query
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            results = response.json()
            if results.get("success"):
                data = results.get("result", [])
                if data:
                    print(Fore.GREEN + f"Breaches found for {email}:" + Style.RESET_ALL)
                    output_lines = []
                    for breach in data:
                        password = breach.get("password", "N/A")
                        print(Fore.GREEN + f"{email}:{password}" + Style.RESET_ALL)
                        output_lines.append(f"{email}:{password}")
                    if output_file:
                        with open(output_file, "a") as file:
                            file.write("\n".join(output_lines) + "\n")
                        print(Fore.BLUE + f"Output saved to {output_file}" + Style.RESET_ALL)
                else:
                    print(Fore.YELLOW + f"No passwords found for {email}." + Style.RESET_ALL)
            else:
                print(Fore.RED + f"Error: {results.get('message', 'Unknown error')}." + Style.RESET_ALL)
        elif response.status_code == 401:
            print(Fore.RED + "Unauthorized: Invalid LeakCheck API key." + Style.RESET_ALL)
        elif response.status_code == 429:
            print(Fore.RED + f"Rate limit exceeded for LeakCheck. Retrying after delay..." + Style.RESET_ALL)
            time.sleep(5)
            search_leakcheck(api_key, email, output_file)
        else:
            print(Fore.RED + f"Error: {response.status_code} - {response.text}" + Style.RESET_ALL)
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Request failed: {e}" + Style.RESET_ALL)

def process_email_file(file_path):
    try:
        with open(file_path, "r") as file:
            emails = [line.strip() for line in file if line.strip()]
        return emails
    except FileNotFoundError:
        print(Fore.RED + f"Error: File {file_path} not found." + Style.RESET_ALL)
        return []

def main():
    display_title()

    parser = argparse.ArgumentParser(description="Search a domain or email addresses in Dehashed, Have I Been Pwned, and LeakCheck and print identified credentials.")
    parser.add_argument("--username", help="Your Dehashed username (email). Required for Dehashed.")
    parser.add_argument("--dehashed-api-key", help="Your Dehashed API key. Required for Dehashed.")
    parser.add_argument("--hibp-api-key", help="Your Have I Been Pwned API key. Required for HIBP.")
    parser.add_argument("--leakcheck-api-key", help="Your LeakCheck API key. Required for LeakCheck.")
    parser.add_argument("--domain", help="The domain name to search for.")
    parser.add_argument("--email", help="The email address to search for.")
    parser.add_argument("--email-file", help="Path to a text file containing email addresses to search.")
    parser.add_argument("-o", "--output", help="File to save the output.")
    parser.add_argument("--search-platform", choices=["dehashed", "hibp", "leakcheck", "both", "all"], default="all", help="Choose where to search: Dehashed, HIBP, LeakCheck, both, or all.")

    args = parser.parse_args()

    if args.search_platform in ["dehashed", "both", "all"]:
        if not args.username or not args.dehashed_api_key:
            print(Fore.RED + "Error: --username and --dehashed-api-key are required for Dehashed searches." + Style.RESET_ALL)
            return
        if args.domain:
            search_dehashed(args.username, args.dehashed_api_key, args.domain, args.output)
        elif args.email:
            print(Fore.YELLOW + f"Searching in Dehashed for {args.email}..." + Style.RESET_ALL)
            search_dehashed(args.username, args.dehashed_api_key, args.email, args.output, is_email=True)
        elif args.email_file:
            emails = process_email_file(args.email_file)
            for email in emails:
                print(Fore.YELLOW + f"Searching in Dehashed for {email}..." + Style.RESET_ALL)
                search_dehashed(args.username, args.dehashed_api_key, email, args.output, is_email=True)

    if args.search_platform in ["hibp", "both", "all"]:
        if not args.hibp_api_key:
            print(Fore.RED + "Error: --hibp-api-key is required for HIBP searches." + Style.RESET_ALL)
            return
        if args.email:
            print(Fore.YELLOW + f"Searching in Have I Been Pwned for {args.email}..." + Style.RESET_ALL)
            search_hibp(args.hibp_api_key, args.email, args.output)
        elif args.email_file:
            emails = process_email_file(args.email_file)
            for email in emails:
                print(Fore.YELLOW + f"Searching in Have I Been Pwned for {email}..." + Style.RESET_ALL)
                search_hibp(args.hibp_api_key, email, args.output)

    if args.search_platform in ["leakcheck", "all"]:
        if not args.leakcheck_api_key:
            print(Fore.RED + "Error: --leakcheck-api-key is required for LeakCheck searches." + Style.RESET_ALL)
            return
        if args.email:
            print(Fore.YELLOW + f"Searching in LeakCheck for {args.email}..." + Style.RESET_ALL)
            search_leakcheck(args.leakcheck_api_key, args.email, args.output)
        elif args.email_file:
            emails = process_email_file(args.email_file)
            for email in emails:
                print(Fore.YELLOW + f"Searching in LeakCheck for {email}..." + Style.RESET_ALL)
                search_leakcheck(args.leakcheck_api_key, email, args.output)

    if not (args.domain or args.email or args.email_file):
        print(Fore.RED + "Error: You must specify either --domain, --email, or --email-file." + Style.RESET_ALL)

if __name__ == "__main__":
    main()

