from pathlib import Path
import yaml


def load_yaml(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"YAML datoteka ne postoji: {path}")

    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML mora biti dict na vrhu dokumenta: {path}")
    return data

def load_config(path="input/config.yaml"):
    return load_yaml(path)