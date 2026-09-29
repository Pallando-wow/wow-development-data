# Data directory

Large development datasets are stored below this directory and referenced from the root `catalog.json`.

Reserved dataset families currently include:

- `api/`
- `event/`
- `quest/`
- `spell/`
- `item/`
- `npc/`
- `map/`
- `faction/`
- `achievement/`
- `profession/`
- `pet-family/`
- `pet-ability/`
- `pet-trainer/`

The initial published file convention is:

```text
data/<kind>/<clientId>.json
```

A dataset is added to `catalog.json` only when it contains validated records. Empty placeholder JSON files are deliberately avoided.

See `docs/dataset-model.md` for observation, provenance and versioning rules.
