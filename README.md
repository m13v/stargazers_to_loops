# stargazers_to_loops

## Project Description

`stargazers_to_loops` is a small project designed to analyze GitHub stargazers data and extract meaningful insights. 

This tool helps open-source project maintainers understand their community better by providing detailed statistics on user engagement.

We gather all stargazers, then request profile for each one to get their e-mail address.
We then add all users with valid email address to loops.so database

## Features

- **Get Records**: Extract specific fields such as `login` and `emails` from JSON data.
- **Statistics**: Calculate and display the total number of records, the number of records with the `loops` field.
- **User-Friendly Output**: Print the filtered data in a readable format in local json and upload to loop.so

## Installation

1. Clone the repository:
````bash
git clone https://github.com/yourusername/stargazers_to_loops.git
````
2. Navigate to the project directory:
````bash
cd stargazers_to_loops
````
3. Install the required dependencies:
````bash
pip install -r requirements.txt
````

## Usage

1. Place your JSON file containing stargazers data in the project directory.
2. Run the script:
````bash
python main.py
````
[optionally] you can run script for a specific user: e.g. 
````bash
python main.py m13v
````

## Example json stats
````bash
python check_json_records.py    
````
````bash
Total records: 514
Records with 'loops' field: 514
Breakdown of 'loops' field:
  added: 138
  no valid email exist: 376
````

## TO-DO

- When getting stargazers don't overwrite existing
- Get stargazer email only if it wasn't already added

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

Special thanks to the open-source community for their continuous support and contributions.
