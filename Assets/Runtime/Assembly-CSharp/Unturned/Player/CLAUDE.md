# Player — the player entity and its components

`Player.cs` is the root `MonoBehaviour`; each aspect is a separate component deriving from `PlayerCaller`
(which is a `SteamCaller` → has `channel` and RPCs). Access them as `player.life`, `player.inventory`,
`player.equipment`, `player.movement`, `player.stance`, `player.look`, `player.skills`, `player.crafting`,
`player.quests`, `player.clothing`, `player.interact`, `player.animator`, `player.voice`, `player.workzone`.

| Component | Responsibility |
|---|---|
| `PlayerLife.cs` | health, food, water, virus, oxygen, bleeding, broken legs, death/respawn |
| `PlayerInventory.cs` | item pages (hands, backpack, storage...), add/remove/drag |
| `PlayerEquipment.cs` | what is held; creates the `Useable` (see `Unturned/Useable`) |
| `PlayerMovement.cs`, `PlayerStance.cs`, `PlayerLook.cs` | physics movement, crouch/prone/sprint, camera |
| `PlayerInput.cs` | client input packets, server simulation ticks, client-side prediction & resimulation |
| `PlayerQuests.cs` | NPC flags, quests, groups |
| `PlayerUI.cs` | client HUD root (client only) |

## Lookups

- Local player (client): `Player.player`. By id on server: `PlayerTool.getPlayer(steamID)` (`Unturned/Tools/PlayerTool.cs`).
- Connection info, name, admin flag: `SteamPlayer` (`player.channel.owner`), `Unturned/Provider/SteamPlayer.cs`.

## Lifecycle (in `Player.cs`)

`InitializePlayer()` calls each component's `InitializePlayer()` in a fixed order — add new components there.
`SendInitialPlayerState(...)` sends each component's state to a newly connected client — add yours if it has
replicated state. Save/load: each component has `save()` / `load()` using `PlayerSavedata` files.

## Rules

- Mutating methods run on the server; clients receive results via `Client*Method` RPCs
  (see `Assets/Runtime/Assembly-CSharp/NetInvokable/CLAUDE.md`).
- Typical guards: `Provider.isServer` (authoritative logic), `channel.IsLocalPlayer` (owner-only visuals/UI),
  `Dedicator.IsDedicatedServer` (skip client work on dedicated).
- Static events (`PlayerLife.onPlayerDied`, `OnPreDeath`, ...) and instance delegates (`onHealthUpdated`, ...)
  are used by plugins and UI — keep them and their signatures.
- Savedata files are versioned (`SAVEDATA_VERSION*`); keep backward-compatible reads.
