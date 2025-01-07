# Credential Searcher 

Credential Searcher is a Python script that searches for breached credentials across multiple platforms, including Dehashed, Have I Been Pwned (HIBP), and LeakCheck. The script can query these platforms using email addresses or domain names and provides a user-friendly interface with options to save the results to a file.  <!-- Credential Searcher is a Python script that searches for breached credentials across multiple platforms, including Dehashed, Have I Been Pwned (HIBP), and LeakCheck. The script can query these platforms using email addresses or domain names and provides a user-friendly interface with options to save the results to a file. -->

## Features 
- **Search for leaked credentials on:**
  - Dehashed  <!-- - Dehashed -->
  - Have I Been Pwned  <!-- - Have I Been Pwned -->
  - LeakCheck  <!-- - LeakCheck -->
- **Query using:**  <!-- - **Query using:** -->
  - Email addresses  <!-- - Email addresses -->
  - Domain names  <!-- - Domain names -->
  - Email lists from a file  <!-- - Email lists from a file -->
- **Save results to a file for further analysis.**  <!-- - **Save results to a file for further analysis.** -->
- **Handle rate limits and API-specific requirements gracefully.**  <!-- - **Handle rate limits and API-specific requirements gracefully.** -->

## Prerequisites  

### Dependencies 

- **Python 3.7+** 
- **Required Python libraries:** 
  ##### pip install requests colorama  

## Installation 

Install the required libraries using pip: 

##### pip install requests colorama 


## Usage

### Command-line Arguments

| Argument               | Description                                                                 |  <!-- | Argument               | Description                                                                 | -->
|------------------------|-----------------------------------------------------------------------------|  <!-- |------------------------|-----------------------------------------------------------------------------| -->
| `--username`           | Your Dehashed username (email). Required for Dehashed searches.             |  <!-- | `--username`           | Your Dehashed username (email). Required for Dehashed searches.             | -->
| `--dehashed-api-key`   | Your Dehashed API key. Required for Dehashed searches.                       |  <!-- | `--dehashed-api-key`   | Your Dehashed API key. Required for Dehashed searches.                       | -->
| `--hibp-api-key`       | Your Have I Been Pwned API key. Required for HIBP searches.                 |  <!-- | `--hibp-api-key`       | Your Have I Been Pwned API key. Required for HIBP searches.                 | -->
| `--leakcheck-api-key`  | Your LeakCheck API key. Required for LeakCheck searches.                    |  <!-- | `--leakcheck-api-key`  | Your LeakCheck API key. Required for LeakCheck searches.                    | -->
| `--domain`             | The domain name to search for.                                              |  <!-- | `--domain`             | The domain name to search for.                                              | -->
| `--email`              | A single email address to search for.                                       |  <!-- | `--email`              | A single email address to search for.                                       | -->
| `--email-file`         | Path to a text file containing a list of email addresses to search.         |  <!-- | `--email-file`         | Path to a text file containing a list of email addresses to search.         | -->
| `-o, --output`         | Path to save the output.                                                    |  <!-- | `-o, --output`         | Path to save the output.                                                    | -->
| `--search-platform`    | Choose the platform to search: dehashed, hibp, leakcheck, both, or all. Default: all. |  <!-- | `--search-platform`    | Choose the platform to search: dehashed, hibp, leakcheck, both, or all. Default: all. | -->

## Examples 

### Search for a Single Email 

> `python credential_searcher.py --email example@example.com --search-platform hibp --hibp-api-key YOUR_HIBP_API_KEY  <!-- python credential_searcher.py --email example@example.com --search-platform hibp --hibp-api-key YOUR_HIBP_API_KEY`

### Search for Emails from a File on LeakCheck 

> `python credential_searcher.py --email-file emails.txt --search-platform leakcheck --leakcheck-api-key YOUR_LEAKCHECK_API_KEY  <!-- python credential_searcher.py --email-file emails.txt --search-platform leakcheck --leakcheck-api-key YOUR_LEAKCHECK_API_KEY`


### Search for a Domain on Dehashed 

> `python credential_searcher.py --domain example.com --search-platform dehashed --username YOUR_EMAIL --dehashed-api-key YOUR_DEHASHED_API_KEY  <!-- python credential_searcher.py --domain example.com --search-platform dehashed --username YOUR_EMAIL --dehashed-api-key YOUR_DEHASHED_API_KEY`


### Save Results to a File  


> `python credential_searcher.py --email example@example.com --output results.txt --search-platform all --hibp-api-key YOUR_HIBP_API_KEY --dehashed-api-key YOUR_DEHASHED_API_KEY --leakcheck-api-key YOUR_LEAKCHECK_API_KEY  <!-- python credential_searcher.py --email example@example.com --output results.txt --search-platform all --hibp-api-key YOUR_HIBP_API_KEY --dehashed-api-key YOUR_DEHASHED_API_KEY --leakcheck-api-key YOUR_LEAKCHECK_API_KEY`


## API Key Setup 

### Dehashed  

1. Sign up at [Dehashed](https://www.dehashed.com).  <!-- 1. Sign up at [Dehashed](https://www.dehashed.com). -->
2. Obtain your username and API key from the user dashboard.  <!-- 2. Obtain your username and API key from the user dashboard. -->

### Have I Been Pwned  

1. Sign up at [HIBP](https://haveibeenpwned.com).  <!-- 1. Sign up at [HIBP](https://haveibeenpwned.com). -->
2. Obtain your API key from the user dashboard.  <!-- 2. Obtain your API key from the user dashboard. -->

### LeakCheck 

1. Sign up at [LeakCheck](https://leakcheck.net).  <!-- 1. Sign up at [LeakCheck](https://leakcheck.net). -->
2. Obtain your API key from the user dashboard.  <!-- 2. Obtain your API key from the user dashboard. -->

## Error Handling 

- **401 Unauthorized:** Ensure the provided API key is valid and corresponds to the selected platform.  <!-- - **401 Unauthorized:** Ensure the provided API key is valid and corresponds to the selected platform. -->
- **429 Too Many Requests:** The script handles rate limits by retrying after a delay. If the issue persists, reduce the query rate.  <!-- - **429 Too Many Requests:** The script handles rate limits by retrying after a delay. If the issue persists, reduce the query rate. -->

## License 

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.  <!-- This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. -->

## Contributing 

Contributions are welcome! Feel free to submit issues or pull requests to enhance the functionality or fix bugs.  <!-- Contributions are welcome! Feel free to submit issues or pull requests to enhance the functionality or fix bugs. -->

## Contact 

For questions or support, please contact [Your Name or Email].  <!-- For questions or support, please contact [Your Name or Email]. -->
