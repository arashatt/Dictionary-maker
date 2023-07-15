import subprocess
def get_file_path():
    try:
        # Launch the file selection dialog
        result = subprocess.run(['zenity', '--file-selection'], capture_output=True, text=True, check=True)
        file_path = result.stdout.strip()
    
        if file_path:
            return file_path
        else:
            print("No file selected.")
            return None
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            print("User canceled the window.")
        else:
            print("An error occurred:", e.stderr)

