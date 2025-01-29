import subprocess
import platform

def check_ollama():
    if platform.system() == "Windows":
        try:
            # Use 'where' command to check if ollama.exe exists in any directory
            output = subprocess.check_output('where ollama', shell=True, text=True)
            return True  # Ollama is installed if the command returns a path
        except subprocess.CalledProcessError:
            # If 'where' command returns an error (file not found), return False
            return False
    else:
        try:
            # Use 'which' command to check if ollama exists in Unix systems
            subprocess.check_output(['which', 'ollama'], stderr=subprocess.STDOUT)
            return True  # Ollama is installed if the command succeeds
        except subprocess.CalledProcessError:
            return False

if check_ollama():
    print("You have Ollama installed")
else:
    print("You don't have Ollama installed")
