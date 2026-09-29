# Data policy

## Purpose

This repository contains machine-readable facts and observations that are useful for World of Warcraft addon development.

The project is intentionally narrower than a game database. It does not aim to reproduce Wowhead or redistribute Blizzard game content.

## Allowed data

Suitable records include:

- client versions, build numbers and TOC Interface values
- numeric game identifiers
- API and event availability
- technical constants and enum values
- relationships observed through the normal addon API
- quest, spell, item, NPC, map, faction, achievement and profession identifiers
- hunter pet family, ability and trainer relationships
- observation counts and client/build provenance

## Excluded data

Do not publish:

- large bodies of Blizzard-authored text
- quest or NPC dialogue archives
- textures, icons, models, sounds, music or other game assets
- authentication material or account identifiers
- character names or player GUIDs
- Battle.net identities
- guild or friend lists
- whispers, chat logs or other social communication
- information intended to identify or profile players

If context such as player class, race or level is required to interpret an observation, it should be stored without a player identifier.

## Corrections

Collector output is an observation, not automatically authoritative truth. Data should be validated and normalized before publication. Manually verified corrections are allowed and should retain provenance where practical.
