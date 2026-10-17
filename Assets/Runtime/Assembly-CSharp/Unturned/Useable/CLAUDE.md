# Useable — behaviour of the equipped item

When a player equips an item, `PlayerEquipment` adds the `Useable*` component chosen by the item asset's
`Useable` key (mapped in `Unturned/UnturnedNexus.cs` via `Assets.useableTypes.addType(...)`).
Data comes from the matching `Item*Asset` in `Unturned/Bundles`.

## Base class `Useable.cs` — override points

- `equip()` / `dequip()` — set up / tear down (models, UI, events).
- `startPrimary()` / `stopPrimary()`, `startSecondary()` / `stopSecondary()` — input (fire/aim, swing, eat...).
- `simulate(uint simulation, bool inputSteady)` — fixed-tick logic, runs on owner and server (predicted).
- `tick()` — per-frame (visuals, client); `tock(uint clock)` — fixed clock.
- `updateState(byte[] newState)` — item state bytes (ammo, attachments, durability) changed.

## Rules

- Server decides outcomes (hits, damage, ammo); the owning client predicts. Client → server requests are
  `ServerInstanceMethod` with `ONLY_FROM_OWNER` and `ratelimitHz` (see `ReceiveChangeFiremode` in `UseableGun.cs`).
- Damage goes through `Unturned/Tools/DamageTool.cs`, not direct health edits.
- Item state is a `byte[]` whose layout is a save/network contract (e.g. gun attachments). Don't reorder bytes.
- `UseableGun.cs` is ~6.6k lines: grep for the method, read by range.

## Adding a new useable

1. `UseableFoo : Useable` here. 2. Register in `Unturned/UnturnedNexus.cs`. 3. Asset class in `Unturned/Bundles`
(if new fields). 4. New RPCs → regenerate NetGen. 5. `.meta` files.
