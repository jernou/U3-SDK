# Level — map loading and level data

`Level.cs` — entry point: `Level.load(LevelInfo, hasAuthority)`, `Level.info`, loading sequence, loading music.
Map files (terrain, objects, nodes) live in the game install / workshop, not in this repo.

| Data | File |
|---|---|
| Map metadata | `LevelInfo.cs`, `LevelAsset` (in `Unturned/Bundles`) |
| Placed objects | `LevelObjects.cs`, `LevelObject.cs` (runtime state: `Unturned/Managers/ObjectManager.cs`) |
| Terrain | `LevelGround.cs` (+ `Framework/Landscapes`) |
| Spawns & tables | `LevelItems.cs` + `ItemSpawnpoint`/`ItemTable`, `LevelZombies.cs`, `LevelVehicles.cs`, `LevelAnimals.cs`, `LevelPlayers.cs` |
| Nodes (legacy) | `LevelNodes.cs`, `*Node.cs` (airdrop, location, safezone, ...) |
| Volumes | `VolumeBase.cs`, `VolumeManagerBase.cs`, `*Volume.cs` + `*VolumeManager.cs` |
| Lighting & weather | `LevelLighting.cs` (~2.8k lines), `WeatherComponentBase.cs`, `CustomWeatherComponent.cs` |
| Roads, navigation | `LevelRoads.cs`, `Road.cs`, `LevelNavigation.cs`, `UnturnedPathfinding.cs` |
| Net ids for level entities | `LevelNetIdRegistry.cs` |

## Rules

- Level data formats are read from existing maps (official + thousands of workshop maps): changes must stay
  backward compatible; new data needs a version bump with the old read path kept.
- New volume type: copy an existing pair (`*Volume` + `*VolumeManager`), it plugs into the Devkit
  (`Framework/Devkit`) for editing.
