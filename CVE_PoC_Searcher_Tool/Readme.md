# CVE PoC Search Tool

CVE PoC Search Tool is a Python script designed to help cybersecurity professionals identify Common Vulnerabilities and Exposures (CVEs) with potential Remote Code Execution (RCE) vulnerabilities and locate Proof-of-Concept (PoC) exploits available on GitHub using keywords. The tool fetches CVEs from the MITRE database and identifies potential Proof-of-Concept (PoC) exploits available on GitHub.

## Features

- **Search CVEs**: Retrieves CVE data from the MITRE CVE database using a specified keyword. ⭐
- **Filter by RCE**: Filters CVEs to show only those with potential Remote Code Execution (RCE) vulnerabilities. ⭐
- **Find GitHub PoCs**: Searches GitHub for PoCs related to the identified CVEs. ⭐
- **Rate Limiting**: Implements GitHub API rate limit checking. ⭐
- **Easy-to-Read Output**: Displays CVE details and available PoCs in a user-friendly format. ⭐

## Requirements

### Python Version

- Python 3.8 or higher ⭐

### Python Libraries

- `requests` ⭐
- `beautifulsoup4` ⭐

Install the required libraries using pip:


pip install requests beautifulsoup4 ⭐
## Usage
Running the Script
To run the script, use the following command:

python CVE_PoC_Search.py --keyword "<your_keyword>" --github_token "<your_github_token>" ⭐
Arguments
--keyword: The keyword to search for CVEs (e.g., apache tomcat). ⭐
--github_token: Your GitHub Personal Access Token for API authentication. ⭐
## Example

python CVE_PoC_Search.py --keyword "citrix netscaler" --github_token "ghp_your_personal_access_token" ⭐
Output
The script provides the following:

Filtered CVEs: Displays CVEs related to the keyword, filtered for potential RCE vulnerabilities. ⭐
GitHub PoCs: Shows GitHub repositories with PoCs for the identified CVEs. ⭐
Example output:

`##############################################
#                                            #
#           CVE PoC Search Tool              #
#       Find CVEs and GitHub PoCs            #
#                                            #
##############################################

Searching for CVEs on MITRE...
Found 5 tables. Debugging table content...

Table 3 is identified as the CVE table.
Filtering CVEs for potential RCE vulnerabilities...

Searching for PoCs on GitHub...
Processing CVE: CVE-2020-8299
Processing CVE: CVE-2014-8580
CVE ID: CVE-2020-8299
Description: Citrix ADC and Citrix/NetScaler Gateway 13.0 before 13.0-76.29, suffers from uncontrolled resource consumption.
PoCs: No PoCs found
--------------------------------------------------
CVE ID: CVE-2014-8580
Description: Citrix NetScaler Application Delivery Controller allows remote access to network resources of other users.
PoCs: No PoCs found
`
### Notes
Ensure your GitHub Personal Access Token has appropriate permissions to access the API (public repositories). ⭐
This script currently uses only the MITRE CVE database. Support for the NVD can be added in the future. ⭐
License
This project is licensed under the MIT License. See the LICENSE file for details. ⭐

## Contribution
Feel free to submit issues or pull requests to improve this tool. ⭐

Happy vulnerability hunting! 🎯
