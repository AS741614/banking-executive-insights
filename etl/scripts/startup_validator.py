import os
import sys
from typing import List

class ETLStartupValidator:
    """
    Institutional ETL Startup Validator.
    Ensures source data integrity and directory readiness.
    """

    def __init__(self, raw_data_dir: str = "data/raw"):
        self.raw_data_dir = raw_data_dir
        self.required_files = [
            "accounts.csv",
            "branches.csv",
            "customers.csv",
            "products.csv",
            "transactions.csv"
        ]

    def validate_source_files(self) -> bool:
        print("--- ETL Source Data Validation ---")
        missing_files = []
        for file in self.required_files:
            file_path = os.path.join(self.raw_data_dir, file)
            if not os.path.exists(file_path):
                missing_files.append(file)
                print(f"[FAIL] Missing source file: {file_path}")
            else:
                size_kb = os.path.getsize(file_path) / 1024
                print(f"[OK] Source file: {file} ({size_kb:.2f} KB)")
        
        if missing_files:
            print(f"\n[WARN] Total missing files: {len(missing_files)}")
            return False
        return True

    def validate_output_directories(self) -> bool:
        # Check for tableau export dirs etc
        dirs = ["tableau/exports"]
        for d in dirs:
            if not os.path.exists(d):
                os.makedirs(d, exist_ok=True)
                print(f"[INFO] Created directory: {d}")
        return True

if __name__ == "__main__":
    validator = ETLStartupValidator()
    # Source files might not exist if they haven't been generated yet, 
    # but we should warn the operator.
    validator.validate_source_files()
    validator.validate_output_directories()
    print("\n[INFO] ETL environment validation complete.")
