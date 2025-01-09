# Censys Open Ports Search Script

Censys Open Ports Search Script is a Python tool that queries the Censys Search API to retrieve information about open ports and associated services for a given IP address, IP range, or domain.

## Features

- Flexible Target Input: Supports IP ranges, single IP addresses, and domains.

- Aggregated Output: Groups open ports and their services by IP address.

- CSV Export: Saves the results in a CSV file for easy analysis.

- Rate Limiting Compliance: Adheres to Censys API rate limits.

- Retry Logic: Handles rate limit errors (429) with automatic retries.

## Prerequisites

- Dependencies

- Python 3.7+

- Required Python libraries:

- requests

- csv

- colorama

## Installation

Install the required dependencies using pip:

pip install requests colorama

## Usage

Command-Line Arguments

Argument

Description

--api-id

Your Censys API ID. Required.

--api-secret

Your Censys API Secret. Required.

--target

The IP range, IP address, or domain to search for open ports. Required.

-o, --output

(Optional) Path to save the results as a CSV file.

## Examples

Search for a Single IP Address

python censys_search.py --api-id YOUR_API_ID --api-secret YOUR_API_SECRET --target 192.168.1.1

Search for an IP Range and Save Results to CSV

python censys_search.py --api-id YOUR_API_ID --api-secret YOUR_API_SECRET --target 192.168.0.0/24 --output results.csv

Search for a Domain

python censys_search.py --api-id YOUR_API_ID --api-secret YOUR_API_SECRET --target example.com

Output Format

Results will display open ports and their associated services in the format:

IP - 80, 443, 22 - http, https, ssh

When saved to a CSV file, it includes the following columns:

IP Address: The queried IP address.

Open Ports: Comma-separated list of open ports.

Services: Comma-separated list of services associated with the open ports.

Censys API Rate Limits

Type

Limit

api:search

0.4 actions/second (120 per 5 minutes)

The script includes built-in delays and retries to comply with these limits.

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve the script.
