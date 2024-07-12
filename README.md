## Technical Documentation for Data Shipping Tool

### Overview
This tool, authored by Hud Seidu Daannaa, is designed to ship data to specified memcache servers as listed in the `settings.ini` file. The data is sent in parallel to ensure high availability and redundancy. During its operation, the tool creates a tracking folder to save the application state. If this folder is absent, the application will treat it as a new start. The application accepts JSON files as input, shipping the data contained within to the memcache servers.

### Features
- Parallel data shipping to multiple memcache servers.
- High availability and redundancy through parallel processing.
- Application state tracking through a directory.
- JSON input for key-value pairs.
- Support for various operational commands through command-line arguments.

### Requirements
- Python 2.x
- `pymemcache` library (installable via pip)

### Installation
1. Ensure Python 2.x is installed on your system.
2. Install the required `pymemcache` library:
    ```sh
    pip install pymemcache
    ```

### Usage
1. Make the script executable:
    ```sh
    chmod +x x1.py
    ```
2. Run the script:
    ```sh
    ./x1.py
    ```
    Or
    ```sh
    python ./x1.py
    ```

### Command-Line Arguments
- `-f --file`: Specify a file to ship data from.
- `-d --dir`: Specify a directory containing multiple files to ship data from.
- `-X --flush`: Flush will reset the application logs and registry/memfile.
- `-R --readme`: Display the README information.
- `-g --get`: Specify a key to retrieve a value stored in memcache.

### Configuration
The tool uses a `settings.ini` file for configuration. Below is an example configuration:

```ini
[Memcache_config]
address=192.168.1.15:4200, 192.168.1.15:4300

[Application]
primary_key=indicator, last_updated, published_date
memdir=rf987dsdsds7
document_key_field=indicator
```

### Detailed Functionality

#### Signal Handling
The tool handles `SIGINT` (CTRL+C) signals gracefully, displaying a termination message and exiting cleanly.

#### Utility Functions
- **`touch(fname, times=None)`**: Creates an empty file or updates the timestamp of an existing file.
- **`install(package)`**: Installs a specified package using pip.
- **`writer(data, file_)`**: Appends data to a specified file.
- **`reader(file_)`**: Reads lines from a specified file.
- **`log(datax, log_path='application.log')`**: Writes logs with timestamps to a specified log file.
- **`make_key(keyd, data)`**: Generates a unique key based on specified fields in the data.
- **`hashfile(file_)`**: Computes the SHA-256 hash of a specified file.

#### Core Functions
- **`fcn_v1(address, memory_dir_name, file__)`**: Ships data from a single file to a specified memcache server.
- **`fcn_v2(address, memory_dir_name, intel_dir)`**: Ships data from multiple files in a specified directory to a specified memcache server.

#### Main Function
- **`main_hud()`**: The main function that handles argument parsing, configuration reading, and initiates the data shipping process based on specified arguments.

### Example Workflow
1. **Sending Data from a Single File**:
    ```sh
    python ./x1.py -f data.json
    ```
2. **Sending Data from a Directory**:
    ```sh
    python ./x1.py -d data_directory
    ```
3. **Retrieving a Value from Memcache**:
    ```sh
    python ./x1.py -g some_key
    ```
4. **Flushing Logs and Registry**:
    ```sh
    python ./x1.py -X
    ```
5. **Displaying README Information**:
    ```sh
    python ./x1.py -R
    ```

### Threat Modeling
- **Assets**:
  - Memcache Servers
  - Data Files
  - Application Logs
  - Configuration Files

- **Threats**:
  - Unauthorized access to memcache servers.
  - Data corruption during transmission.
  - Application failure or crash.
  - Loss of application state.

- **Mitigations**:
  - Use secure channels (e.g., TLS) for communication with memcache servers.
  - Implement data validation and integrity checks.
  - Ensure robust error handling and logging.
  - Regularly back up the application state directory.

### Security Mechanisms
- **User Authentication**: Ensure only authorized users can run the script by implementing access controls.
- **Enhanced Logging**: Detailed logging for monitoring and debugging.
- **File Encryption**: Encrypt sensitive data files before transmission.
- **File Name Encoding**: Use encoded file names to prevent unauthorized access or tampering.
- **File Upload Limit**: Set limits on the size of files that can be uploaded to prevent resource exhaustion attacks.
- **File Type Restrictions**: Allow only specific file types to be processed to prevent malicious file uploads.


This tool provides a robust mechanism for shipping data to multiple memcache servers, ensuring high availability and redundancy. Proper configuration and usage of the tool, along with implementing the recommended security mechanisms, will ensure secure and efficient data handling.

For any issues or contributions, please refer to the project repository or contact the author, Hud Seidu Daannaa.
