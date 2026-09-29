#!/usr/bin/env python3

import json
import os
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog.json"
SOURCES_PATH = ROOT / "sources.json"
VERSION_PATTERN = re.compile(r"^(\d+)\.(\d+)\.(\d+)\.(\d+)$")


def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def request_text(url):
    headers = {
        "User-Agent": "Pallando-wow/wow-development-data"
    }

    token = os.environ.get("GITHUB_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        headers["Authorization"] = f"Bearer {token}"
        headers["X-GitHub-Api-Version"] = "2022-11-28"

    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def derive_interface(major, minor, patch):
    if minor > 99 or patch > 99:
        raise ValueError(
            f"Cannot derive Interface safely from version {major}.{minor}.{patch}."
        )

    return major * 10000 + minor * 100 + patch


def read_branch_info(repository, branch):
    url = f"https://api.github.com/repos/{repository}/branches/{branch}"
    payload = json.loads(request_text(url))

    return (
        payload["commit"]["sha"],
        payload["commit"]["commit"]["author"]["date"],
    )


def read_version(repository, branch):
    url = f"https://raw.githubusercontent.com/{repository}/{branch}/version.txt"
    raw = request_text(url).strip()
    match = VERSION_PATTERN.fullmatch(raw)

    if not match:
        raise ValueError(
            f"Unexpected version.txt content for {repository}@{branch}: {raw!r}"
        )

    major, minor, patch, build = map(int, match.groups())

    return (
        f"{major}.{minor}.{patch}",
        build,
        derive_interface(major, minor, patch),
    )


def comparable(client):
    source = client["source"]
    return {
        "id": client["id"],
        "name": client["name"],
        "version": client["version"],
        "build": client["build"],
        "interface": client["interface"],
        "sourceType": source["type"],
        "sourceProvider": source["provider"],
        "sourceReference": source.get("reference"),
    }


def main():
    sources = json.loads(SOURCES_PATH.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    repository = sources["repository"]
    provider = sources["provider"]

    existing = {
        client["id"]: client
        for client in catalog.get("clients", [])
    }

    clients = []
    changed = False

    for source in sources["clients"]:
        version, build, interface = read_version(
            repository,
            source["branch"],
        )
        commit_sha, observed_at = read_branch_info(
            repository,
            source["branch"],
        )

        candidate = {
            "id": source["id"],
            "name": source["name"],
            "version": version,
            "build": build,
            "interface": interface,
            "source": {
                "type": "upstream-derived",
                "provider": provider,
                "reference": f'{source["branch"]}@{commit_sha}',
                "observedAt": observed_at,
            },
        }

        previous = existing.get(source["id"])

        if previous is None or comparable(previous) != comparable(candidate):
            changed = True

        clients.append(candidate)

    if len(existing) != len(clients):
        changed = True

    if not changed:
        print("No client version changes detected.")
        return

    catalog["schemaVersion"] = 1
    catalog["generatedAt"] = utc_now()
    catalog["clients"] = clients
    catalog.setdefault("datasets", [])

    CATALOG_PATH.write_text(
        json.dumps(catalog, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print("catalog.json updated.")


if __name__ == "__main__":
    main()
