import requests
import os
import zipfile
import shutil
from tqdm import tqdm

def delete_existing_file(filename):
    if os.path.exists(filename):
        try:
            os.remove(filename)
            print(f"Removed existing file: {filename}")
            return True
        except OSError as e:
            print(f"Error removing file: {e}")
            return False
    return True

def download_file(url):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        filename = url.split('/')[-1]
        total_size = int(response.headers.get('content-length', 0))
        block_size = 8192
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=block_size):
                progress_bar.update(len(chunk))
                file.write(chunk)
        progress_bar.close()
        if total_size != 0 and progress_bar.n != total_size:
            print("ERROR, something went wrong")
        else:
            print(f"Downloaded: {filename}")
            return filename
    else:
        print("Failed to download the file.")
        return None

def unzip_file(zip_filename):
    extracted_file = os.path.splitext(zip_filename)[0]  # This will be the name without the zip extension

    # Unzip the file
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        for member in tqdm(zip_ref.infolist(), desc='Extracting '):
            try:
                zip_ref.extract(member)
            except zipfile.error as e:
                print(f"Error extracting file: {e}")
        print(f"Extracted: {zip_filename}")

def get_extracted_filename(zip_filename):
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        return zip_ref.namelist()[0]  # Return the first file in the zip

def update_jupiter_config(extracted_filename):
    current_path = os.path.abspath(extracted_filename)
    jupiter_path = current_path
    
    # Check for jupiter-config.toml in the current directory
    config_path_current = os.path.join(os.getcwd(), "jupiter-config.toml")
    
    if os.path.isfile(config_path_current):
        with open(config_path_current, 'r') as file:
            lines = file.readlines()
        
        with open(config_path_current, 'w') as file:
            for line in lines:
                if line.startswith('jupiter_path='):
                    line = f'jupiter_path="{jupiter_path}"\n'
                file.write(line)
        
        print(f"Updated jupiter-config.toml in the current directory with the new jupiter_path: {jupiter_path}")

    # Navigate one folder back to find jupiter-config.toml
    config_path_parent = os.path.join(os.path.dirname(os.getcwd()), "jupiter-config.toml")
    
    if os.path.isfile(config_path_parent):
        with open(config_path_parent, 'r') as file:
            lines = file.readlines()
        
        with open(config_path_parent, 'w') as file:
            for line in lines:
                if line.startswith('jupiter_path='):
                    line = f'jupiter_path="{jupiter_path}"\n'
                file.write(line)
        
        print(f"Updated jupiter-config.toml in the parent directory with the new jupiter_path: {jupiter_path}")
    else:
        print("jupiter-config.toml file not found in the parent directory.")

def main():
    url = "https://github.com/jup-ag/jupiter-swap-api/releases/download/v6.0.29/jupiter-swap-api-x86_64-unknown-linux-gnu.zip"
    extracted_file = "jupiter-swap-api"

    # Check for the existence of the jupiter-swap-api file and delete it if it exists
    if not delete_existing_file(extracted_file):
        print("Failed to delete the existing file. Exiting.")
        return

    # Verify that the file was deleted
    if os.path.exists(extracted_file):
        print("File still exists after deletion attempt. Exiting.")
        return

    # Download the zip file
    zip_filename = download_file(url)
    if zip_filename:
        unzip_file(zip_filename)
        extracted_filename = get_extracted_filename(zip_filename)
        update_jupiter_config(extracted_filename)

        print("All actions completed successfully.")

if __name__ == "__main__":
    main()
