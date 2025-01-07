# Liferay Version Detector

Liferay Version Detector is a sophisticated tool for identifying Liferay portal versions. This tool can check a single domain or a list of domains for indications of Liferay versions. It detects Liferay versions using multiple strategies such as HTTP headers, meta tags, common endpoints, HTML comments, JSP files, and JavaScript variables. The script provides detailed logging for each check, supports checking both HTTP and HTTPS versions of the URLs, and saves detected versions to a results file.

## Requirements

Python 3.x and the following Python libraries: requests, beautifulsoup4, pyfiglet, and colorama. 

## Installation

Clone the repository: `git clone https://github.com/yourusername/liferay-version-detector.git`, change into the project directory: `cd liferay-version-detector`, and install the required Python libraries: `pip install -r requirements.txt`.

## Usage

To check a single domain, use the `-u` or `--url` option followed by the domain: `python get_liferay_version_advanced.py -u example.com`. To check a list of domains from a file, use the `-f` or `--file` option followed by the path to the file: `python get_liferay_version_advanced.py -f domains.txt`. Additional options include `--timeout` to set the request timeout in seconds (default is 5 seconds) and `--results` to set the path to the results file (default is `results.txt`).

## Example

For checking a single domain: `python get_liferay_version_advanced.py -u example.com`. For checking a list of domains, create a file called `domains.txt` with each domain on a new line, then run: `python get_liferay_version_advanced.py -f domains.txt`.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

