import csv
import json
from pathlib import Path
from utils import is_debug_mode, activate_debug


IDS_MAPPING_PATH = Path("data/raw/IDS_mapping.csv")
RAW_SCHEMA_PATH = Path("schema/raw_schema.json")
MODEL_SCHEMA_PATH = Path("schema/model_schema.json")


def extract_id_values(mapping_path: Path) -> dict:
    """Parse IDS_mapping.csv into {field_name: sorted list of int ids}."""
    text = mapping_path.read_text().splitlines()
    sections = {}
    current = None
    for line in text:
        if not line.strip():
            current = None
            continue
        if line.endswith(",description"):
            current = line.split(",")[0]
            sections[current] = []
            continue
        if current:
            parts = next(csv.reader([line]))
            if not parts:
                continue
            id_str = parts[0].strip()
            if not id_str or id_str.lower() in {"nan", "null"}:
                continue
            try:
                sections[current].append(int(id_str))
            except ValueError:
                # Skip non-numeric ids (shouldn't occur in this mapping)
                continue

    # Deduplicate + sort for stable ordering in schema files
    return {k: sorted(set(v)) for k, v in sections.items()}


def update_schema(schema_path: Path, id_values: dict, dry_run: bool = True) -> None:
    """Update allowed_values in a schema JSON using id_values mapping."""
    schema = json.loads(schema_path.read_text())
    for feature in schema.get("features", []):
        name = feature.get("name")
        if name in id_values:
            feature["allowed_values"] = id_values[name]

    if dry_run:
        print(f"[DRY RUN] Would update: {schema_path}")
        for name, values in id_values.items():
            print(f"  - {name}: {values}")
        return

    schema_path.write_text(json.dumps(schema, indent=2) + "\n")
    print(f"Updated: {schema_path}")


def main() -> None:
    activate_debug()
    id_values = extract_id_values(IDS_MAPPING_PATH)

    # Dry-run to show what would be updated
    if is_debug_mode():
        update_schema(RAW_SCHEMA_PATH, id_values, dry_run=True)
        update_schema(MODEL_SCHEMA_PATH, id_values, dry_run=True)
    else: 
        update_schema(RAW_SCHEMA_PATH, id_values, dry_run=False)
        update_schema(MODEL_SCHEMA_PATH, id_values, dry_run=False)


if __name__ == "__main__":
    main()
