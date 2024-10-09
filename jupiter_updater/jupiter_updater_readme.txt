Jupiter Swap API Updater
This script automatically downloads the latest version of the Jupiter Swap API, extracts it, and updates the configuration file jupiter-config.toml with the new path to the downloaded executable.

Features
    Downloads the latest Jupiter Swap API ZIP file.
    Extracts the contents to the current directory.
    Updates the jupiter-config.toml file to reflect the new path of the downloaded executable, regardless of its location in the NotArb folder.

Instructions
	Prerequisites
		Python 3.x
		requests library (install using pip install requests if not already installed)

How to Use
    Place the Script:
        Save the Python script in the "libs" folder within the NotArb folder, or wherever you want to download and extract the Jupiter Swap API ZIP file.

    Run the Script:
        Open a terminal or command prompt.

        Navigate to the directory where the script is located.

        Run the script using the command:

        python jupup.py

How It Works
    The script first downloads the ZIP file from the specified URL.
    It then extracts the contents of the ZIP file to the current directory.
    The script retrieves the name of the extracted file and constructs the full path.
    It searches for the jupiter-config.toml file in the NotArb folder and its subdirectories.
    The script updates the jupiter_path in the configuration file to point to the newly extracted file.

Important Note
    Ensure that the jupiter-config.toml file is accessible within the NotArb folder or its subdirectories.

Troubleshooting
    If the script reports that the jupiter-config.toml file is not found, ensure it is correctly placed within the NotArb folder or its subdirectories.
    If you encounter any issues downloading the file, verify your internet connection and the URL used in the script.