# Tomcat Detector

Tomcat Detector is a sophisticated tool designed to identify Apache Tomcat servers. This tool can check a single domain or a list of domains for indications of Apache Tomcat, by inspecting multiple ports and various HTTP response headers, content, and other indicators.

## Features

- Checks for Apache Tomcat on multiple ports (80, 443, 8080).
- Inspects various HTTP response headers (Server, X-Powered-By).
- Checks for Java JSESSIONID cookie.
- Examines response content for common Tomcat indications.
- Checks for default Tomcat management endpoints.
- Searches for Tomcat-specific error pages.
- Looks for fingerprinting URLs and resources.
- Checks for common Tomcat directories and files.
- Probes HTTP methods behavior.
- Tests for known Tomcat vulnerabilities.
- Saves the results to a specified file when a Tomcat server is detected.

## Installation

First, make sure you have Python installed. Then, install the required libraries using pip:


pip install requests pyfiglet colorama


## Usage

 You can run the script in different ways:
 
 Checking a Single Domain
 To check a single domain, use the -u or --url option:
 

 python check_tomcat.py -u example.com --timeout 10 --results results.txt
 Checking Multiple Domains from a File
 To check multiple domains from a file, use the -f or --file option:
 

 python check_tomcat.py -f domains.txt --timeout 10 --results results.txt
 Options
 -u, --url: Check a single domain.
 -f, --file: Path to the file containing the list of domains.
 --https: Use HTTPS instead of HTTP (by default, both are checked based on the port).
 --timeout: Request timeout in seconds (default is 5 seconds).
 --results: Path to the results file (default is results.txt).
 ## Example
 To check a list of domains in domains.txt with a timeout of 10 seconds, and save the results to results.txt:
 
 
 python check_tomcat.py -f domains.txt --timeout 10 --results results.txt
 Script Details
 The script checks multiple ports (80, 443, and 8080) on each domain to identify Apache Tomcat servers. It uses the following methods:
 
 Server Header: Inspects the Server HTTP response header for indications of Tomcat.
 X-Powered-By Header: Checks the X-Powered-By HTTP response header.
 JSESSIONID Cookie: Looks for the presence of the JSESSIONID cookie.
 Response Content: Searches the response content for keywords like "Apache Tomcat" and "Tomcat/".
 Management Endpoints: Checks default management endpoints like /manager/html and /host-manager/html.
 Error Pages: Looks for Tomcat-specific error pages.
 Fingerprint Resources: Searches for Tomcat-specific URLs and resources.
 Common Directories and Files: Checks for common Tomcat directories and configuration files.
 HTTP Methods: Probes the behavior of certain HTTP methods like OPTIONS, PUT, and DELETE.
 Known Vulnerabilities: Probes for known vulnerabilities, e.g., CVE-2020-1938 (Ghostcat).
 License
 This project is licensed under the MIT License - see the LICENSE file for details.


python check_tomcat.py -f domains.txt --timeout 10 --results results.txt
Options
-u, --url: Check a single domain.
-f, --file: Path to the file containing the list of domains.
--https: Use HTTPS instead of HTTP (by default, both are checked based on the port).
--timeout: Request timeout in seconds (default is 5 seconds).
--results: Path to the results file (default is results.txt).
Example
To check a list of domains in domains.txt with a timeout of 10 seconds, and save the results to results.txt:


python check_tomcat.py -f domains.txt --timeout 10 --results results.txt
Script Details
The script checks multiple ports (80, 443, and 8080) on each domain to identify Apache Tomcat servers. It uses the following methods:

Server Header: Inspects the Server HTTP response header for indications of Tomcat.
X-Powered-By Header: Checks the X-Powered-By HTTP response header.
JSESSIONID Cookie: Looks for the presence of the JSESSIONID cookie.
Response Content: Searches the response content for keywords like "Apache Tomcat" and "Tomcat/".
Management Endpoints: Checks default management endpoints like /manager/html and /host-manager/html.
Error Pages: Looks for Tomcat-specific error pages.
Fingerprint Resources: Searches for Tomcat-specific URLs and resources.
Common Directories and Files: Checks for common Tomcat directories and configuration files.
HTTP Methods: Probes the behavior of certain HTTP methods like OPTIONS, PUT, and DELETE.
Known Vulnerabilities: Probes for known vulnerabilities, e.g., CVE-2020-1938 (Ghostcat).


## License
This project is licensed under the MIT License - see the LICENSE file for details.




## Contributing

Contributions are welcome! Please open an issue or submit a pull request.


