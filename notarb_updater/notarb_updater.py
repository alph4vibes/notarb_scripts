import requests
import os
import platform

def get_latest_jar_info():
    # GitHub API URL for the latest release
    url = "https://api.github.com/repos/NotArb/Jupiter/releases/latest"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # Find the .jar asset
        for asset in data['assets']:
            if asset['name'].endswith('.jar'):
                return asset['browser_download_url'], asset['name']
    
    return None, None

def download_jar(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        # Get the filename from the URL
        filename = url.split('/')[-1]
        # Write the file to the current directory
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded: {filename}")
        return filename
    else:
        print("Failed to download the JAR file.")
        return None

def update_notarb_java_sh(jar_filename):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    notarb_sh_path = os.path.join(script_dir, "notarb_java.sh")
    
    if not os.path.isfile(notarb_sh_path):
        print("notarb_java.sh file not found.")
        return
    
    with open(notarb_sh_path, 'r') as file:
        lines = file.readlines()

    # Update the line with the new jar filename
    with open(notarb_sh_path, 'w') as file:
        for line in lines:
            if line.startswith('bot_path="$libs_path/'):
                # Replace the old jar filename with the new one
                line = f'bot_path="$libs_path/{jar_filename}"\n'
            file.write(line)

    print(f"Updated notarb_java.sh with the new jar filename: {jar_filename}")

def check_current_version():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    notarb_sh_path = os.path.join(script_dir, "notarb_java.sh")
    
    if not os.path.isfile(notarb_sh_path):
        print("notarb_java.sh file not found.")
        return None
    
    with open(notarb_sh_path, 'r') as file:
        for line in file:
            if line.startswith('bot_path="$libs_path/'):
                # Extract the current jar filename
                return line.split('/')[-1].strip().strip('"')
    
    return None

def main():
    latest_jar_url, latest_jar_filename = get_latest_jar_info()
    if latest_jar_url and latest_jar_filename:
        print(f"Latest JAR file URL: {latest_jar_url}")
        current_version = check_current_version()
        
        if current_version == latest_jar_filename:
            print("The current version is already up-to-date. Skipping download and update.")
        else:
            downloaded_filename = download_jar(latest_jar_url)
            if downloaded_filename:
                update_notarb_java_sh(downloaded_filename)
    else:
        print("Failed to retrieve the latest JAR file URL.")

if __name__ == "__main__":
    main()
