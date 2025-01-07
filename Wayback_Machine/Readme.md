# Wayback Sensitive Info Detector

Wayback Sensitive Info Detector is a sophisticated tool for identifying sensitive information in archived URLs. This tool can check a single domain or a list of domains for indications of sensitive information using the Wayback Machine and `getallurls` tool.

## Features

- Checks archived URLs for sensitive information such as passwords, credentials, admin pages, and more.
- Can process a single domain or a list of domains.
- Saves results in a structured format, with each domain's results saved in a separate folder.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/wayback-sensitive-info-detector.git
    cd wayback-sensitive-info-detector
    ```

2. **Install the required dependencies:**

    - Python 3.x
    - `requests`, `pyfiglet`, `colorama`
    - `getallurls` tool

    ```bash
    pip install requests pyfiglet colorama
    go install github.com/lc/gau/v2/cmd/gau@latest
    ```

## Usage

1. **Check a single domain:**

    ```bash
    python wayback_sensitive_info.py -u example.com
    ```

2. **Check a list of domains from a file:**

    ```bash
    python wayback_sensitive_info.py -f domains.txt
    ```

## Options

- `-u`, `--url`: Check a single domain.
- `-f`, `--file`: Path to the file containing the list of domains.

## Example

1. **Single Domain:**

    ```bash
    python wayback_sensitive_info.py -u example.com
    ```

    Output will be saved in a folder named `example_com` with a file `example_com.txt` containing the results.

2. **Multiple Domains:**

    ```bash
    python wayback_sensitive_info.py -f domains.txt
    ```

    Each domain's results will be saved in separate folders named after the domain.

## Sensitive Keywords

The tool searches for a wide range of sensitive keywords in the URLs, including:

- Authentication and authorization terms: `password`, `token`, `auth`, `session`, etc.
- User and account-related terms: `username`, `user`, `account`, `root`, etc.
- Financial terms: `payment`, `credit`, `card`, `billing`, `invoice`, `purchase`, `order`, etc.
- Data and database terms: `db`, `database`, `backup`, etc.
- Security terms: `secure`, `ssl`, `cert`, `certificate`, etc.
- Miscellaneous terms that often indicate sensitive or internal information: `config`, `confidential`, `private`, `hidden`, `internal`, `sensitive`, etc.
- Environment and stage-related terms: `test`, `development`, `dev`, `stage`, `staging`, `uat`, `prod`, `production`, etc.
- Debug and log-related terms: `debug`, `trace`, `error`, `bug`, `logs`, `log`, `dump`, etc.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or suggestions.

## License

This project is licensed under the MIT License.

