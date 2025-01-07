# Subdomain Finder & Web Service Checker  <!-- # Subdomain Finder & Web Service Checker -->

## Description  <!-- ## Description -->

This script uses the `assetfinder` tool to discover subdomains for a given domain, validates which subdomains are live, and identifies those with active web services. Results are saved into organized output files for easy reference.  <!-- This script uses the `assetfinder` tool to discover subdomains for a given domain, validates which subdomains are live, and identifies those with active web services. Results are saved into organized output files for easy reference. -->

## Key Features  <!-- ## Key Features -->

- **Subdomain Discovery:** Enumerates subdomains using the powerful `assetfinder` tool.  <!-- - **Subdomain Discovery:** Enumerates subdomains using the powerful `assetfinder` tool. -->
- **Live Subdomain Validation:** Checks if discovered subdomains are live by attempting to resolve them.  <!-- - **Live Subdomain Validation:** Checks if discovered subdomains are live by attempting to resolve them. -->
- **Web Service Detection:** Tests live subdomains for active HTTP/HTTPS services.  <!-- - **Web Service Detection:** Tests live subdomains for active HTTP/HTTPS services. -->
- **Organized Output:** Results are saved into separate files for all subdomains, live subdomains, and subdomains with active web services.  <!-- - **Organized Output:** Results are saved into separate files for all subdomains, live subdomains, and subdomains with active web services. -->

## Requirements  <!-- ## Requirements -->

### Prerequisites  <!-- ### Prerequisites -->

- **Python 3.7+**  <!-- - **Python 3.7+** -->
- **Assetfinder**: Installable via Go:  <!-- - **Assetfinder**: Installable via Go: -->
  ```sh  <!-- ```sh -->
  go install github.com/tomnomnom/assetfinder@latest  <!-- go install github.com/tomnomnom/assetfinder@latest -->
  ```  <!-- ``` -->
- **Python Libraries**: Install the required Python packages:  <!-- - **Python Libraries**: Install the required Python packages: -->
  ```sh  <!-- ```sh -->
  pip install requests termcolor  <!-- pip install requests termcolor -->
  ```  <!-- ``` -->

## Usage  <!-- ## Usage -->

### Script Arguments  <!-- ### Script Arguments -->

- `-d`, `--domain` (required): Target domain (e.g., example.com)  <!-- - `-d`, `--domain` (required): Target domain (e.g., example.com) -->
- `-o`, `--output` (required): Output file to save all discovered subdomains.  <!-- - `-o`, `--output` (required): Output file to save all discovered subdomains. -->
- `-l`, `--live_output` (required): Output file to save live subdomains.  <!-- - `-l`, `--live_output` (required): Output file to save live subdomains. -->
- `-w`, `--web_output` (required): Output file to save subdomains with web services.  <!-- - `-w`, `--web_output` (required): Output file to save subdomains with web services. -->
- `-t`, `--timeout`: Timeout for web service check (default: 10 seconds).  <!-- - `-t`, `--timeout`: Timeout for web service check (default: 10 seconds). -->

### Example Command  <!-- ### Example Command -->

```sh  <!-- ```sh -->
python subdomain_web_checker.py -d example.com -o all_subdomains.txt -l live_subdomains.txt -w web_services.txt -t 15  <!-- python subdomain_web_checker.py -d example.com -o all_subdomains.txt -l live_subdomains.txt -w web_services.txt -t 15 -->
```  <!-- ``` -->

### Output Files  <!-- ### Output Files -->

- **All Subdomains (`-o`):** Contains all subdomains discovered by the `assetfinder` tool.  <!-- - **All Subdomains (`-o`):** Contains all subdomains discovered by the `assetfinder` tool. -->
- **Live Subdomains (`-l`):** Lists subdomains that are live and resolvable.  <!-- - **Live Subdomains (`-l`):** Lists subdomains that are live and resolvable. -->
- **Subdomains with Web Services (`-w`):** Includes URLs of subdomains with active HTTP/HTTPS services.  <!-- - **Subdomains with Web Services (`-w`):** Includes URLs of subdomains with active HTTP/HTTPS services. -->

## Script Workflow  <!-- ## Script Workflow -->

### Subdomain Discovery  <!-- ### Subdomain Discovery -->

1. Executes `assetfinder` to find subdomains.  <!-- 1. Executes `assetfinder` to find subdomains. -->
2. Filters results to include only subdomains belonging to the specified domain.  <!-- 2. Filters results to include only subdomains belonging to the specified domain. -->
3. Saves all discovered subdomains to the file specified by `-o`.  <!-- 3. Saves all discovered subdomains to the file specified by `-o`. -->

### Live Subdomain Validation  <!-- ### Live Subdomain Validation -->

1. Checks each subdomain to see if it resolves.  <!-- 1. Checks each subdomain to see if it resolves. -->
2. Saves live subdomains to the file specified by `-l`.  <!-- 2. Saves live subdomains to the file specified by `-l`. -->

### Web Service Detection  <!-- ### Web Service Detection -->

1. Tests live subdomains for HTTP/HTTPS services.  <!-- 1. Tests live subdomains for HTTP/HTTPS services. -->
2. Saves subdomains with active web services to the file specified by `-w`.  <!-- 2. Saves subdomains with active web services to the file specified by `-w`. -->

### Example Output  <!-- ### Example Output -->

**Command:**  <!-- **Command:** -->

```sh  <!-- ```sh -->
python subdomain_web_checker.py -d example.com -o all_subdomains.txt -l live_subdomains.txt -w web_services.txt -t 15  <!-- python subdomain_web_checker.py -d example.com -o all_subdomains.txt -l live_subdomains.txt -w web_services.txt -t 15 -->
```  <!-- ``` -->

**Output Files:**  <!-- **Output Files:** -->

- `all_subdomains.txt`:  <!-- - `all_subdomains.txt`: -->
  ```  <!-- ``` -->
  sub1.example.com  <!-- sub1.example.com -->
  sub2.example.com  <!-- sub2.example.com -->
  sub3.example.com  <!-- sub3.example.com -->
  ```  <!-- ``` -->

- `live_subdomains.txt`:  <!-- - `live_subdomains.txt`: -->
  ```  <!-- ``` -->
  sub1.example.com  <!-- sub1.example.com -->
  sub2.example.com  <!-- sub2.example.com -->
  ```  <!-- ``` -->

- `web_services.txt`:  <!-- - `web_services.txt`: -->
  ```  <!-- ``` -->
  http://sub1.example.com  <!-- http://sub1.example.com -->
  https://sub2.example.com  <!-- https://sub2.example.com -->
  ```  <!-- ``` -->

## Contributing  <!-- ## Contributing -->

Feel free to fork this repository and submit pull requests for improvements or new features. Ensure your code adheres to best practices and is thoroughly tested.  <!-- Feel free to fork this repository and submit pull requests for improvements or new features. Ensure your code adheres to best practices and is thoroughly tested. -->

## License  <!-- ## License -->

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.  <!-- This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. -->

## Disclaimer  <!-- ## Disclaimer -->

This tool is for educational purposes and authorized use only. The author is not responsible for any misuse of this tool.  <!-- This tool is for educational purposes and authorized use only. The author is not responsible for any misuse of this tool. -->
