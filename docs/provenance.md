# Provenance

Every published client build and, where practical, every future dataset should be traceable to its source.

## Client versions

The initial automated version source is the public `Gethe/wow-ui-source` repository.

For each configured branch, the updater reads `version.txt`, records the source branch and commit SHA, and derives the current TOC Interface value from the three-part client version.

For a client version `major.minor.patch`, the current Interface convention is:

```text
major × 10000 + minor × 100 + patch
```

Examples:

```text
1.60.1  -> 16001
1.15.9  -> 11509
12.1.0  -> 120100
```

The validator rejects catalog entries where the stored Interface value does not match this derivation. If Blizzard changes the convention for a future client, the derivation logic and schema must be reviewed instead of silently accepting a conflicting value.

## Source types

`upstream-derived`
: A factual value was read from an upstream source and one or more additional values were deterministically derived from it.

Future source types may include collector observations and manually verified corrections.

## Collector observations

Future collector datasets should record the WoW client/build and sufficient observation metadata to distinguish:

- first seen
- last seen
- observation count
- collector version

Raw SavedVariables should not be published directly. Pallando's WoW Addon Studio should validate and normalize them first.
