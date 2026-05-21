import sys
import os
import importlib

REQUIRED_PACKAGES = [
    "fastapi",
    "uvicorn",
    "pydantic",
    "pydantic_settings",
    "psutil",
    "jose",
    "passlib",
    "bcrypt",
    "requests",
    "plotly",
    "streamlit"
]

REQUIRED_ENV_VARS = [
    "SECRET_KEY"
]

def validate_runtime():
    print("--- ESOTERIC Platform Runtime Validation ---")
    missing_packages = []
    
    for package in REQUIRED_PACKAGES:
        try:
            importlib.import_module(package)
            print(f"[OK] Package: {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"[FAIL] Package: {package}")

    missing_envs = []
    for env in REQUIRED_ENV_VARS:
        if env not in os.environ:
            missing_envs.append(env)
            print(f"[WARN] Env Var: {env} (Using default if available)")
        else:
            print(f"[OK] Env Var: {env}")

    if missing_packages:
        print("\nCRITICAL: Missing required packages. Run: pip install " + " ".join(missing_packages))
        sys.exit(1)
    
    print("\n[SUCCESS] Institutional runtime validation passed.")

if __name__ == "__main__":
    validate_runtime()
