Notarb + Jupiter Updater

This script automates the updating process for the Notarb and Jupiter projects. It checks for the latest JAR file for Notarb and downloads the latest Jupiter binary, updating necessary configuration files as required.

Features
    Automatically checks for the latest JAR file from the Notarb GitHub repository.
    Downloads the JAR file if it's not already present in the directory.
    Updates the notarb_java.sh script with the correct JAR filename.
    Downloads and unzips the latest Jupiter binary from the specified release.
    Updates jupiter-config.toml with the new path for the Jupiter binary.
    Provides a summary of all actions taken, including successes and failures.

Requirements
    Python 3.x
    requests library
    tqdm library for progress bars

You can install the required libraries using:

pip install requests tqdm

Usage
    Clone the repository or download the script.
    Ensure you have a valid notarb_java.sh file and a jupiter-config.toml file in your working directory.
    Run the script:

	python najupup.py

	or

	python3 najupup.py

Detailed Functionality

Notarb Updater
    Check for Latest JAR: Retrieves the latest JAR file information from the Notarb GitHub repository.
    Download JAR: Downloads the JAR file if it's not already present in the directory.
    Update notarb_java.sh: Updates the script with the new JAR filename. If the JAR file is already specified and exists, it skips the download.

Jupiter Updater
    Download Jupiter Binary: Downloads the latest Jupiter binary from the specified URL.
    Unzip and Update Config: Unzips the downloaded file and updates jupiter-config.toml with the new binary path.

Summary of Actions
	At the end of the script execution, a summary of all actions taken will be displayed, indicating whether each action was successful or failed.


