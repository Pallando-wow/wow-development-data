# Pallando WoW Development Data

Public, machine-readable World of Warcraft development data for addon tooling.

The repository is designed as a stable data source for **Pallando's WoW Addon Studio** and other addon-development tools. It stores technical facts, identifiers, relationships and observations that are useful during addon development.

## Scope

Initial data includes:

- WoW client versions
- build numbers
- TOC Interface numbers
- source/provenance information

The data model also defines collection and publication formats for:

- API and event availability
- quests
- spells
- items
- NPCs
- maps and zones
- factions
- achievements
- professions
- hunter pet families, abilities and trainer relationships

The goal is **not** to mirror Wowhead or redistribute Blizzard game content. Large copyrighted texts, textures, models, sounds and other game assets are intentionally out of scope.

## Files

- `catalog.json` — stable entry point for clients and available datasets
- `catalog.schema.json` — JSON Schema for the catalog
- `schemas/collector-export.schema.json` — normalized collector interchange format
- `schemas/datasets/` — schemas for published datasets
- `data/` — development datasets referenced by the catalog
- `examples/` — schema examples used by CI
- `docs/` — data policy, provenance and collector documentation

## Data collection

A future `PallandoDataCollector` WoW addon can collect development-relevant observations through the normal WoW addon API and store them in SavedVariables. Pallando's WoW Addon Studio then validates, normalizes and aggregates those observations before publication here.

Player-identifying and social data is out of scope. The collector must not publish character names, Battle.net identities, guild names, friend lists, whispers, chat logs, machine identifiers or persistent user identifiers.

See `docs/dataset-model.md` for the initial observation, versioning and provenance model.

## Provenance

Published records retain source and evidence information. Sources can include upstream version mirrors, collector observations and manually verified corrections.

## License

The factual dataset in this repository is released under CC0-1.0. Third-party names and trademarks remain the property of their respective owners.

World of Warcraft and Blizzard Entertainment are trademarks or registered trademarks of Blizzard Entertainment, Inc. This project is not affiliated with or endorsed by Blizzard Entertainment.
