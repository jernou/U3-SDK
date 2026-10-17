# Managers — world state

Mostly static facades (`*Manager : SteamCaller`) that own world entities and replicate them:
`ItemManager` (items on ground), `BarricadeManager`, `StructureManager`, `VehicleManager`, `ZombieManager`,
`AnimalManager`, `ObjectManager` (level objects), `ResourceManager` (trees/rocks), `EffectManager`,
`ChatManager`, `SaveManager`, `LightingManager`, `LevelManager` (arena mode), `GroupManager`,
`ClaimManager`, `SafezoneManager`, `TemperatureManager`, `OxygenManager`.

## Region model

The world is a grid (`Unturned/Regions/Regions.cs`); entities are stored per region (`ItemRegion`,
`BarricadeRegion`, `StructureRegion`, ...) addressed by `(x, y)`. Barricades also have `plant`
(`ushort.MaxValue` = on ground, otherwise vehicle index). Replication is sent only to players near
the region — use `Regions.tryGetCoordinate` / `tryGetRegion` helpers rather than linear searches.

## Instance data

- `*Drop` (`BarricadeDrop`, `StructureDrop`, `ItemDrop`) = live object + RPCs, addressed by `NetId`.
- `*Data` (`BarricadeData`, `StructureData`, `ItemData`) = serializable state.
- Barricade/structure RPCs moved from static to `*Drop` instance methods; old static methods throw
  `NotSupportedException` — don't revive them.

## Rules

- Creation/destruction/damage only on server; manager methods early-return on clients.
- Many public static methods and events are used by plugins (`onDamageBarricadeRequested`, ...) — keep signatures.
- Save/load: each manager has `save()` called from `SaveManager.save()`; formats are versioned.
- `BarricadeManager.cs`, `VehicleManager.cs` are ~3.5k lines: grep first.
