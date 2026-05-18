from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent

PROMPT_FILE = ROOT / "ai/prompts/generate_data_dictionary.txt"
SCHEMA_FILE = ROOT / "sql/01_schema.sql"

OUTPUT_DIR = ROOT / "ai/generated"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "esoteric_bank_intelligence_report.md"

prompt = PROMPT_FILE.read_text()
schema = SCHEMA_FILE.read_text()

full_prompt = f"""
{prompt}

POSTGRESQL WAREHOUSE SCHEMA:
==================================================

{schema}
"""

print("======================================")
print("ESOTERIC BANK Cognitive Engine Online")
print("Generating enterprise intelligence report...")
print("======================================")

result = subprocess.run(
    ["gemini", "-p", full_prompt],
    capture_output=True,
    text=True
)

OUTPUT_FILE.write_text(result.stdout)

print(f"\nEnterprise report generated successfully:")
print(OUTPUT_FILE)
