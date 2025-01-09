import requests
from bs4 import BeautifulSoup
import argparse
import re
import time

def print_banner():
    banner = """
    ##############################################
    #                                            #
    #           CVE PoC Search Tool             #
    #       Find CVEs and GitHub PoCs           #
    #                                            #
    ##############################################
    """
    print(banner)

class CVEPOCSearcher:
    def __init__(self, keyword, github_token):
        self.keyword = keyword
        self.github_token = github_token
        self.cve_details = []

    def search_cves_mitre(self):
        print("Searching for CVEs on MITRE...")
        cve_url = f'https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword={self.keyword}'
        response = requests.get(cve_url)

        if response.status_code == 200:
            # Explicitly set encoding
            response.encoding = 'utf-8'

            soup = BeautifulSoup(response.text, 'xml')  # Switch to XML parsing
            tables = soup.find_all('table')  # List all tables

            print(f"Found {len(tables)} tables. Debugging table content...")

            # Find the table with "Name" and "Description" headers
            for index, table in enumerate(tables):
                headers = table.find('thead')
                if headers and "Name" in headers.get_text() and "Description" in headers.get_text():
                    print(f"\nTable {index + 1} is identified as the CVE table.")
                    self.parse_cve_table(table)
                    break
            else:
                print("CVE table not found on MITRE. Verify the HTML/XML structure of the page.")
        else:
            print(f"Failed to fetch CVEs from MITRE. Status code: {response.status_code}")

    def parse_cve_table(self, table):
        rows = table.find_all('tr')[1:]  # Skip header row
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 2:
                cve_id = cols[0].get_text(strip=True)
                description = cols[1].get_text(strip=True)
                self.cve_details.append({"id": cve_id, "description": description})

    def filter_rce_cves(self):
        print("Filtering CVEs for potential RCE vulnerabilities...")
        rce_keywords = ["remote code execution", "RCE", "arbitrary code execution"]
        self.cve_details = [
            cve for cve in self.cve_details
            if any(keyword.lower() in cve['description'].lower() for keyword in rce_keywords)
        ]

    def check_rate_limit(self):
        print("\nChecking GitHub API rate limit...")
        headers = {'Authorization': f'token {self.github_token}'}
        response = requests.get('https://api.github.com/rate_limit', headers=headers)

        if response.status_code == 200:
            rate_limit = response.json()
            remaining = rate_limit['rate']['remaining']
            reset_time = rate_limit['rate']['reset']
            print(f"Remaining API calls: {remaining}")
            print(f"Rate limit resets at: {reset_time}")
            if remaining == 0:
                print("Rate limit exceeded. Please wait for the reset time.")
                return False
            return True
        else:
            print(f"Failed to fetch rate limit status. Status code: {response.status_code}")
            return False

    def search_pocs(self):
        print("\nSearching for PoCs on GitHub...")
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': f'token {self.github_token}'
        }

        for cve in self.cve_details:
            print(f"Processing CVE: {cve['id']}")
            time.sleep(2)  # Introduce a delay between requests to prevent rate limit issues
            cve_id = cve['id']
            github_url = f'https://api.github.com/search/repositories?q={cve_id}+exploit'
            response = requests.get(github_url, headers=headers)

            if response.status_code == 200:
                repos = response.json().get('items', [])
                if repos:
                    cve['pocs'] = []
                    for repo in repos:
                        cve['pocs'].append({
                            "name": repo.get("name"),
                            "url": repo.get("html_url"),
                            "description": repo.get("description", "No description available")
                        })
                else:
                    cve['pocs'] = "No PoCs found"
            else:
                print(f"Failed to fetch PoCs for {cve_id}. Status code: {response.status_code}")
                print(f"Response: {response.json()}")  # Print error details

    def display_results(self):
        if not self.cve_details:
            print("No CVEs found.")
        else:
            for cve in self.cve_details:
                print(f"CVE ID: {cve['id']}")
                print(f"Description: {cve['description']}")
                if 'pocs' in cve:
                    if isinstance(cve['pocs'], str):
                        print(f"PoCs: {cve['pocs']}")
                    else:
                        print("PoCs:")
                        for poc in cve['pocs']:
                            print(f"  - Name: {poc['name']}")
                            print(f"    URL: {poc['url']}")
                            print(f"    Description: {poc['description']}")
                print("-" * 50)

if __name__ == "__main__":
    print_banner()

    parser = argparse.ArgumentParser(description="Search for CVEs and their descriptions using a keyword and find associated PoCs.")
    parser.add_argument("--keyword", required=True, help="Keyword to search for CVEs")
    parser.add_argument("--github_token", required=True, help="GitHub Personal Access Token for authentication")
    args = parser.parse_args()

    searcher = CVEPOCSearcher(args.keyword, args.github_token)
    searcher.search_cves_mitre()
    searcher.filter_rce_cves()
    searcher.search_pocs()
    searcher.display_results()

