# Interactable — things the player can use in the world

Components on barricades, level objects and vehicles. Base: `Interactable.cs`
(`checkInteractable`, `checkUseable`, `checkHint`, `checkHighlight`, `use`, `updateState(Asset, byte[] state)`).
`Interactable2*.cs` — newer, smaller variant for salvage/HP display.

| Kind | Files |
|---|---|
| Placeable barricades | `InteractableDoor`, `InteractableStorage`, `InteractableSign`, `InteractableFarm`, `InteractableGenerator`, `InteractableSentry`, `InteractableBed`, `InteractableClaim`, ... |
| Level objects | `InteractableObject*.cs` (binary state, NPC, quest, dropper, resource, note, rubble) |
| Vehicles | `InteractableVehicle.cs` (~6.4k lines), `Passenger.cs`, `Wheel.cs`, `Buoyancy.cs`, engine sound controllers |

## Rules

- State is a `byte[]` saved by `BarricadeManager`/`ObjectManager` and replicated to clients; its layout is a
  save-format contract (plugins also read it). Rebuild via `rebuildState()` + `BarricadeManager.updateState(...)`.
- `updateState` may be called before `Start` and more than once (plugins) — keep it idempotent.
- `use()` on a client sends a request; the server validates distance/ownership before changing state.
- Vehicles: read `InteractableVehicle.cs` by range; vehicle spawning/saving is in `Unturned/Managers/VehicleManager.cs`.
