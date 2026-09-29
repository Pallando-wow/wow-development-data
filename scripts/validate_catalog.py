#!/usr/bin/env python3

import json
import re
from datetime import datetime
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog.json"
ID_PATTERN = re.compile(r"^[a-z0-9_]+$")
DATASET_ID_PATTERN = re.compile(r"^[a-z0-9_.-]+$")
VERSION_PATTERN = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def parse_date(value, field):
    require(isinstance(value, str) and value, f"{field} must be a date-time string.")

    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(f"{field} is not a valid ISO date-time: {value!r}") from exc


def expected_interface(version):
    match = VERSION_PATTERN.fullmatch(version)
    require(match is not None, f"Invalid client version: {version!r}")

    major, minor, patch = map(int, match.groups())
    require(minor <= 99 and patch <= 99, f"Cannot derive Interface from {version!r}.")

    return major * 10000 + minor * 100 + patch


def validate_client(client):
    required = {"id", "name", "version", "build", "interface", "source"}
    require(required <= client.keys(), f"Client is missing fields: {required - client.keys()}")

    require(ID_PATTERN.fullmatch(client["id"]) is not None, f"Invalid client id: {client['id']!r}")
    require(isinstance(client["name"], str) and client["name"], f"Invalid name for {client['id']}.")
    require(isinstance(client["build"], int) and client["build"] > 0, f"Invalid build for {client['id']}.")
    require(isinstance(client["interface"], int) and client["interface"] > 0, f"Invalid Interface for {client['id']}.")

    expected = expected_interface(client["version"])
    require(
        client["interface"] == expected,
        f"{client['id']} Interface {client['interface']} does not match version {client['version']} (expected {expected}).",
    )

    source = client["source"]
    for field in ("type", "provider"):
        require(isinstance(source.get(field), str) and source[field], f"Invalid source {field} for {client['id']}.")

    reference = source.get("reference")
    require(reference is None or isinstance(reference, str), f"Invalid source reference for {client['id']}.")
    parse_date(source.get("observedAt"), f"{client['id']}.source.observedAt")


def validate_dataset(dataset, client_ids):
    required = {
        "id",
        "clientId",
        "kind",
        "path",
        "schemaVersion",
        "recordCount",
        "generatedAt",
    }
    require(required <= dataset.keys(), f"Dataset is missing fields: {required - dataset.keys()}")

    require(DATASET_ID_PATTERN.fullmatch(dataset["id"]) is not None, f"Invalid dataset id: {dataset['id']!r}")
    require(dataset["clientId"] in client_ids, f"Unknown dataset clientId: {dataset['clientId']!r}")
    require(isinstance(dataset["kind"], str) and dataset["kind"], f"Invalid kind for dataset {dataset['id']}.")

    path = PurePosixPath(dataset["path"])
    require(not path.is_absolute(), f"Dataset path must be relative: {dataset['path']!r}")
    require(".." not in path.parts, f"Dataset path cannot escape repository: {dataset['path']!r}")

    require(isinstance(dataset["schemaVersion"], int) and dataset["schemaVersion"] > 0, f"Invalid schemaVersion for {dataset['id']}.")
    require(isinstance(dataset["recordCount"], int) and dataset["recordCount"] >= 0, f"Invalid recordCount for {dataset['id']}.")
    parse_date(dataset["generatedAt"], f"{dataset['id']}.generatedAt")


def main():
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

    require(catalog.get("schemaVersion") == 1, "Unsupported catalog schemaVersion.")
    parse_date(catalog.get("generatedAt"), "generatedAt")

    clients = catalog.get("clients")
    datasets = catalog.get("datasets")
    require(isinstance(clients, list), "clients must be an array.")
    require(isinstance(datasets, list), "datasets must be an array.")

    client_ids = set()
    for client in clients:
        validate_client(client)
        require(client["id"] not in client_ids, f"Duplicate client id: {client['id']}")
        client_ids.add(client["id"])

    dataset_ids = set()
    for dataset in datasets:
        validate_dataset(dataset, client_ids)
        require(dataset["id"] not in dataset_ids, f"Duplicate dataset id: {dataset['id']}")
        dataset_ids.add(dataset["id"])

    print(
        f"Catalog valid: {len(clients)} clients, "
        f"{len(datasets)} datasets."
    )


if __name__ == "__main__":
    main()
