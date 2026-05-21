import os
import sys
import subprocess
import logging

logger = logging.getLogger("esoteric_bank.etl.seed_orchestrator")

class SeedOrchestrator:
    """
    Institutional Seed Orchestrator.
    Manages generation of synthetic institutional data and initial ETL loading.
    """

    @staticmethod
    def generate_source_data():
        print("--- Generating Synthetic Source Data ---")
        try:
            # We assume src/generate_source_data.py exists as per session context
            subprocess.run(["python", "src/generate_source_data.py"], check=True)
            print("[OK] Source data generation complete.")
        except Exception as e:
            print(f"[FAIL] Data generation failed: {e}")
            sys.exit(1)

    @staticmethod
    def run_initial_etl():
        print("--- Running Initial ETL Load ---")
        try:
            # We assume src/etl.py exists as per session context
            subprocess.run(["python", "src/etl.py"], check=True)
            print("[OK] Initial ETL load complete.")
        except Exception as e:
            print(f"[FAIL] ETL execution failed: {e}")
            sys.exit(1)

if __name__ == "__main__":
    orchestrator = SeedOrchestrator()
    orchestrator.generate_source_data()
    orchestrator.run_initial_etl()
    print("\n[SUCCESS] Institutional seeding complete.")
