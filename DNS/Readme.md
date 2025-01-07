# Subdomain Finder & Web Service Checker

## Description

This script uses the assetfinder tool to discover subdomains for a given domain, validates which subdomains are live, and identifies those with active web services. Results are saved into organized output files for easy reference.

## Key Features:

> - **Subdomain Discovery: Enumerates subdomains using the powerful assetfinder tool.**

> - **Live Subdomain Validation: Checks if discovered subdomains are live by attempting to resolve them.**

> - **Web Service Detection: Tests live subdomains for active HTTP/HTTPS services.**

> - **Organized Output: Results are saved into separate files for all subdomains, live subdomains, and subdomains with active web services.**

## Requirements

Prerequisites:

Python 3.7+

Assetfinder: Installable via Go:

go install github.com/tomnomnom/assetfinder@latest

Python Libraries: Install the required Python packages:

pip install requests termcolor

Usage

Script Arguments:

-d, --domain (required): Target domain (e.g., example.com)

-o, --output (required): Output file to save all discovered subdomains.

-l, --live_output (required): Output file to save live subdomains.

-w, --web_output (required): Output file to save subdomains with web services.

-t, --timeout: Timeout for web service check (default: 10 seconds).

Example Command:

python subdomain_web_checker.py -d example.com -o all_subdomains.txt -l live_subdomains.txt -w web_services.txt -t 15

Output Files

All Subdomains (-o):

Contains all subdomains discovered by the assetfinder tool.

Live Subdomains (-l):

Lists subdomains that are live and resolvable.

Subdomains with Web Services (-w):

Includes URLs of subdomains with active HTTP/HTTPS services.

Script Workflow

Subdomain Discovery:

Executes assetfinder to find subdomains.

Filters results to include only subdomains belonging to the specified domain.

Saves all discovered subdomains to the file specified by -o.

Live Subdomain Validation:

Checks each subdomain to see if it resolves.

Saves live subdomains to the file specified by -l.

Web Service Detection:

Tests live subdomains for HTTP/HTTPS services.

Saves subdomains with active web services to the file specified by -w.

Example Output

Command:

python subdomain_web_checker.py -d example.com -o all_subdomains.txt -l live_subdomains.txt -w web_services.txt -t 15

Output Files:

all_subdomains.txt:

sub1.example.com
sub2.example.com
sub3.example.com

live_subdomains.txt:

sub1.example.com
sub2.example.com

web_services.txt:

http://sub1.example.com
https://sub2.example.com

Contributing

Feel free to fork this repository and submit pull requests for improvements or new features. Ensure your code adheres to best practices and is thoroughly tested.

License

This project is licensed under the MIT License. See the LICENSE file for details.

Disclaimer

This tool is for educational purposes and authorized use only. The author is not responsible for any misuse of this tool.

