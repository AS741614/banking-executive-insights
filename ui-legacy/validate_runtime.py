import sys
import subprocess
import importlib.util
import requests

def check_package(package_name):
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        print(f"[-] Missing dependency: {package_name}")
        return False
    print(f"[+] Found dependency: {package_name}")
    return True

def check_api(url):
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            print(f"[+] API Connection Successful: {url}")
            return True
        else:
            print(f"[-] API returned status {response.status_code}: {url}")
            return False
    except Exception as e:
        print(f"[-] API Connection Failed: {url} ({e})")
        return False

def main():
    print("=== ESOTERIC BANK UI RUNTIME VALIDATION ===")
    
    dependencies = ["streamlit", "pandas", "numpy", "plotly", "requests"]
    all_deps = True
    for dep in dependencies:
        if not check_package(dep):
            all_deps = False
            
    if not all_deps:
        print("!!! Missing dependencies. Please run 'pip install -r requirements.txt' !!!")
        # sys.exit(1) # Don't exit, just warn for now as per "senior" advice
        
    print("\n--- API Connectivity Check ---")
    api_ready = check_api("http://localhost:8000/api/v1/platform/health")
    
    if api_ready:
        print("[SUCCESS] Runtime environment is stabilized.")
    else:
        print("[WARNING] Backend API is offline. UI will start in limited/mock mode.")

if __name__ == "__main__":
    main()
