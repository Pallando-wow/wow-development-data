# Dataset model

This document defines the data model for development-relevant WoW observations.

The model separates three stages:

```text
WoW
 ↓
PallandoDataCollector
 ↓
collector export / SavedVariables
 ↓
Pallando's WoW Addon Studio
 ↓
validation, normalization and aggregation
 ↓
published datasets
```

Raw collector output is evidence. It is not published as authoritative data without validation.

## Dataset families

The model reserves the following dataset kinds:

- `api`
- `event`
- `quest`
- `spell`
- `item`
- `npc`
- `map`
- `faction`
- `achievement`
- `profession`
- `pet-family`
- `pet-ability`
- `pet-trainer`

Additional kinds can be added when a concrete addon-development use case requires them.

## Collector export

`schemas/collector-export.schema.json` defines the normalized interchange format expected from `PallandoDataCollector`.

A collector export contains:

- collector name and version
- exact WoW client id
- client version
- build number
- TOC Interface number
- locale
- capture timestamp
- optional anonymous player context
- one or more observations

Player context is deliberately limited to:

- class token
- race token
- level

No player name, GUID, account identifier, guild, friend, chat or device identifier is part of the schema.

## Observation identity

An observation is identified by:

```text
kind + entity + client/build context
```

`entity` has exactly one identity field:

- `id` for numeric WoW identifiers such as quest, spell, item, NPC or map ids
- `key` for named technical entities such as API functions and events

Examples:

```json
{ "kind": "spell", "entity": { "id": 12345 } }
{ "kind": "api", "entity": { "key": "GetBuildInfo" } }
{ "kind": "event", "entity": { "key": "QUEST_ACCEPTED" } }
```

This avoids inventing synthetic numeric identifiers for APIs and events.

Relations are represented as factual fields containing other numeric ids. Examples include:

- `parentMapId`
- `factionId`
- `spellIds`
- `trainerNpcIds`

The generic fact format intentionally remains small and machine-readable. Large game-authored text and binary assets remain out of scope.

## Published datasets

Published datasets use `schemas/datasets/entity-observations.schema.json`.

The file convention is:

```text
data/<kind>/<clientId>.json
```

Examples:

```text
data/spell/wow_forever.json
data/quest/wow_forever.json
data/pet-ability/wow_forever.json
```

The root `catalog.json` remains the stable discovery point and references datasets only after they are actually published.

## Record evidence

Every published record contains evidence:

- `firstSeen` — build and timestamp of the earliest retained observation
- `lastSeen` — build and timestamp of the newest retained observation
- `observationCount` — number of normalized observations supporting the record
- `builds` — distinct builds on which the record was observed

This allows a consumer to distinguish a one-off observation from a fact repeatedly seen across builds.

## Provenance

Each record contains one or more source descriptors.

Initial source types are:

- `collector`
- `manual`
- `upstream-derived`

Collector sources include the collector version. Manual corrections should describe their origin in `reference` when practical.

## Versioning

There are four separate version dimensions:

1. `schemaVersion` versions the JSON contract.
2. `collector.version` identifies the collector implementation.
3. client `version`, `build` and `interface` identify the WoW runtime.
4. `generatedAt` identifies when a published dataset was produced.

Collector-export schema version 2 and entity-observation schema version 2 introduce the `entity` object so numeric and named technical identities can share the same model.

A schema change that breaks existing consumers increments `schemaVersion`.

A new WoW build does not require a new schema version.

## Deterministic output

Published files should be stable in Git:

- numeric identities sorted by `entity.id`
- named identities sorted ordinally by `entity.key`
- build lists sorted ascending
- source descriptors sorted deterministically
- UTF-8 without BOM
- LF line endings
- two-space JSON indentation
- one final newline

This keeps diffs reviewable when datasets grow.

## Privacy boundary

The collector and published datasets must not include information intended to identify or profile a player.

Prohibited examples include:

- character names
- player GUIDs
- Battle.net account identifiers
- guild names
- friend lists
- whispers
- chat logs
- machine or installation identifiers
- persistent collector/user ids

If additional context becomes necessary later, it must be reviewed before extending the schema.
