# Pallando WoW Development Data

Public, machine-readable World of Warcraft development data for addon tooling.

The repository is designed as a stable data source for **Pallando's WoW Addon Studio** and other addon-development tools. It stores technical facts, identifiers, relationships and observations that are useful during addon development.

## Scope

Initial data focuses on:

- WoW client versions
- build numbers
- TOC Interface numbers
- source/provenance information

Planned datasets include:

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
- `data/` — development datasets referenced by the catalog
- `docs/` — data policy, provenance and collector documentation

## Data collection

A future `PallandoDataCollector` WoW addon can collect development-relevant observations through the normal WoW addon API and store them in SavedVariables. Pallando's WoW Addon Studio can then validate and normalize those observations before publication here.

Player-identifying and social data is out of scope. The collector must not publish character names, Battle.net identities, guild names, friend lists, whispers, chat logs or other player-identifying data.

## Provenance

Published records should retain source and observation information whenever practical. Sources can include upstream version mirrors, collector observations and manually verified corrections.

## License

The factual dataset in this repository is intended to be released under CC0-1.0. Third-party names and trademarks remain the property of their respective owners.

World of Warcraft and Blizzard Entertainment are trademarks or registered trademarks of Blizzard Entertainment, Inc. This project is not affiliated with or endorsed by Blizzard Entertainment.
