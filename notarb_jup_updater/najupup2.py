import requests
import os
import zipfile
from tqdm import tqdm

# Global variable to track actions and their statuses
action_summary = []

# Notarb Updater Functions
def get_latest_jar_info():
    url = "https://api.github.com/repos/NotArb/Jupiter/releases/latest"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        for asset in data['assets']:
            if asset['name'].endswith('.jar'):
                return asset['browser_download_url'], asset['name']
    return None, None

def download_jar(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        filename = url.split('/')[-1]
        total_size = int(response.headers.get('content-length', 0))
        
        with open(filename, 'wb') as file, tqdm(
            desc=filename,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                bar.update(len(chunk))
        
        print(f"Downloaded: {filename}")
        action_summary.append(f"Downloaded: {filename} - Success")
        return filename
    else:
        print("Failed to download the JAR file.")
        action_summary.append("Downloaded JAR file - Failed")
        return None

def update_notarb_java_sh(jar_filename):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    notarb_sh_path = os.path.join(script_dir, "notarb_java.sh")
    
    if not os.path.isfile(notarb_sh_path):
        print("notarb_java.sh file not found.")
        action_summary.append("Updated notarb_java.sh - Failed (file not found)")
        return False
    
    with open(notarb_sh_path, 'r') as file:
        lines = file.readlines()

    updated = False
    with open(notarb_sh_path, 'w') as file:
        for line in lines:
            if line.startswith('bot_path="$libs_path/'):
                line = f'bot_path="$libs_path/{jar_filename}"\n'
                updated = True
            file.write(line)

    if updated:
        print(f"Updated notarb_java.sh with the new jar filename: {jar_filename}")
        action_summary.append(f"Updated notarb_java.sh - Success")
    else:
        print("No updates made to notarb_java.sh.")
        action_summary.append("Updated notarb_java.sh - No updates made")

    return updated

def check_current_version():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    notarb_sh_path = os.path.join(script_dir, "notarb_java.sh")
    
    if not os.path.isfile(notarb_sh_path):
        print("notarb_java.sh file not found.")
        return None
    
    with open(notarb_sh_path, 'r') as file:
        for line in file:
            if line.startswith('bot_path="$libs_path/'):
                return line.split('/')[-1].strip().strip('"')
    return None

def check_jar_exists(filename):
    if os.path.isfile(filename):
        print(f"JAR file exists: {filename}")
        action_summary.append(f"Checked existence of {filename} - Exists")
        return True
    else:
        print(f"JAR file does not exist: {filename}")
        action_summary.append(f"Checked existence of {filename} - Does not exist")
        return False

# Jupiter Updater Functions
def download_file(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        filename = url.split('/')[-1]
        total_size = int(response.headers.get('content-length', 0))
        
        with open(filename, 'wb') as file, tqdm(
            desc=filename,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                bar.update(len(chunk))
        
        print(f"Downloaded: {filename}")
        action_summary.append(f"Downloaded: {filename} - Success")
        return filename
    else:
        print("Failed to download the file.")
        action_summary.append("Downloaded file - Failed")
        return None

def unzip_file(zip_filename):
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        total_files = len(zip_ref.namelist())
        with tqdm(total=total_files, desc="Extracting files", unit="file") as bar:
            for file in zip_ref.namelist():
                zip_ref.extract(file)
                bar.update(1)
    print(f"Extracted: {zip_filename}")
    action_summary.append(f"Extracted: {zip_filename} - Success")

def get_extracted_filename(zip_filename):
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        return zip_ref.namelist()[0]

def update_jupiter_config(extracted_filename):
    current_path = os.path.abspath(extracted_filename)
    jupiter_path = current_path
    
    # Check for jupiter-config.toml in the current directory
    config_path_current = os.path.join(os.getcwd(), "jupiter-config.toml")
    
    updated = False
    if os.path.isfile(config_path_current):
        with open(config_path_current, 'r') as file:
            lines = file.readlines()
        
        with open(config_path_current, 'w') as file:
            for line in lines:
                if line.startswith('jupiter_path='):
                    line = f'jupiter_path="{jupiter_path}"\n'
                    updated = True
                file.write(line)
        
        print(f"Updated jupiter-config.toml in the current directory with the new jupiter_path: {jupiter_path}")
        action_summary.append(f"Updated jupiter-config.toml (current) - Success")
    else:
        action_summary.append("Updated jupiter-config.toml (current) - Failed (file not found)")

    # Navigate one folder back to find jupiter-config.toml
    config_path_parent = os.path.join(os.path.dirname(os.getcwd()), "jupiter-config.toml")
    
    if os.path.isfile(config_path_parent):
        with open(config_path_parent, 'r') as file:
            lines = file.readlines()
        
        with open(config_path_parent, 'w') as file:
            for line in lines:
                if line.startswith('jupiter_path='):
                    line = f'jupiter_path="{jupiter_path}"\n'
                    updated = True
                file.write(line)
        
        print(f"Updated jupiter-config.toml in the parent directory with the new jupiter_path: {jupiter_path}")
        action_summary.append(f"Updated jupiter-config.toml (parent) - Success")
    else:
        action_summary.append("Updated jupiter-config.toml (parent) - Failed (file not found)")

    return updated

# Main Function
def main():
    # Notarb Updater
    print("Starting Notarb Updater...")
    latest_jar_url, latest_jar_filename = get_latest_jar_info()
    if latest_jar_url and latest_jar_filename:
        print(f"Latest JAR file URL: {latest_jar_url}")
        current_version = check_current_version()
        
        if current_version == latest_jar_filename and check_jar_exists(current_version):
            print("The current version is already up-to-date and exists in the folder. Skipping download and update.")
            action_summary.append("Checked current version - Up-to-date and exists")
        else:
            if not check_jar_exists(latest_jar_filename):
                downloaded_filename = download_jar(latest_jar_url)
                if downloaded_filename:
                    updated = update_notarb_java_sh(downloaded_filename)
                    if updated:
                        print(f"Updated notarb_java.sh with the new jar filename: {downloaded_filename}")
                    else:
                        print("No updates made to notarb_java.sh.")
            else:
                print(f"The specified JAR file already exists: {latest_jar_filename}")

    else:
        print("Failed to retrieve the latest JAR file URL.")
        action_summary.append("Checked for latest JAR - Failed")

    # Jupiter Updater
    print("\nStarting Jupiter Updater...")
    jupiter_url = "https://github.com/jup-ag/jupiter-swap-api/releases/download/v6.0.29/jupiter-swap-api-x86_64-unknown-linux-gnu.zip"
    zip_filename = download_file(jupiter_url)
    if zip_filename:
        unzip_file(zip_filename)
        extracted_filename = get_extracted_filename(zip_filename)
        updated = update_jupiter_config(extracted_filename)
        
        if updated:
            print("Updated jupiter-config.toml with the new jupiter_path.")
        else:
            print("No updates made to jupiter-config.toml.")

    print("\nAll actions completed successfully.")

    # Print the overview of actions taken
    print("\n--- Overview of Actions Taken ---")
    for action in action_summary:
        print(action)

if __name__ == "__main__":
    main()
