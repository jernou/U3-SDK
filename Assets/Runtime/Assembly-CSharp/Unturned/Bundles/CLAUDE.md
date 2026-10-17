# Bundles — assets (`.dat` → C# classes)

Every piece of game content (item, vehicle, effect, NPC, spawn table...) is an `Asset` subclass filled from a
`.dat` text file. The `.dat` files themselves are **not in this repo** (they ship with the game / mods).

## Key files

- `Asset.cs` — base class, `PopulateAsset(in PopulateAssetParameters p)`; identity = `GUID` (+ legacy `ushort id`).
- `Assets.cs` — loading, lookup (`Assets.find<T>(Guid)`, `Assets.find(EAssetType, ushort)`), error reporting.
- `Unturned/UnturnedNexus.cs` — **registration**: `Assets.assetTypes.addType("Gun", typeof(ItemGunAsset))`
  maps the `.dat` `Type` value to a class; `Assets.useableTypes.addType(...)` maps `Useable` to a `Useable*` class.
- `ItemAsset.cs` → `ItemWeaponAsset.cs` → `ItemGunAsset.cs`, ... — item hierarchy.
- `NPC*Condition.cs`, `NPC*Reward.cs`, `INPCCondition.cs`, `INPCReward.cs` — quest/dialogue logic blocks.
- `MasterBundle*.cs`, `Bundle.cs` — Unity asset bundle loading.

## Adding a `.dat` property

```
public override void PopulateAsset(in PopulateAssetParameters p)
{
	base.PopulateAsset(in p);
	strength = p.data.ParseFloat("Strength", 1f);   // default keeps old content working
	isLight  = p.data.ContainsKey("Light");          // flag-style keys
}
```

- Use `p.data.Parse*` (`ParseFloat`, `ParseBool`, `ParseUInt8`, `ParseEnum`, `ParseGuidOrLegacyId`, `ParseStruct`).
- Always give a default that preserves behaviour of existing mods — thousands of workshop `.dat` files exist.
- Report bad content with `Assets.ReportError(this, "...")`, don't throw.
- Document the property in the official modding docs if it's user-facing (see `README.md` links).

## Adding a new asset type

1. `FooAsset : Asset` (or `ItemAsset`) here, override `PopulateAsset`.
2. Register in `Unturned/UnturnedNexus.cs`. 3. If it's an item with behaviour, add a `Useable*`
   (see `Unturned/Useable/CLAUDE.md`). 4. `.meta` for each new file.

## Pitfalls

- Asset references: prefer `Guid` / `AssetReference<T>`; legacy `ushort` IDs collide between mods.
- Threads: `AssetsWorker.cs` only reads and parses `.dat` files on a background thread; `PopulateAsset` itself
  is called on the main thread from `Assets.LoadFile` and may load objects from `p.bundle`.
- `Assets.cs` loading order matters: master bundles are loaded before the assets that reference them.
