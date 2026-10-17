# Codebase map (catalog for agents)

Use: find the task → open the entry file → if the directory has a `CLAUDE.md`, it holds local rules.
Paths are relative to `Assets/Runtime/Assembly-CSharp/` unless they start with `Assets/` or `docs/`.
(★ = directory has its own `CLAUDE.md`.)

## Task → where to look

| Task | Start here | Also relevant |
|---|---|---|
| Add/change a network call (RPC) | ★ `NetInvokable` | `NetGen/NetInvokable` (generated), `Assets/Editor/Assembly-CSharp-Editor/NetGen` |
| Connect / auth / kick / ban / queue | ★ `Unturned/Provider` → `Provider.cs` | `NetMessaging`, `Unturned/Provider/SteamPending.cs` |
| Player health, food, water, death | ★ `Unturned/Player` → `PlayerLife.cs` | `Unturned/Tools/DamageTool.cs`, `Unturned/Damage` |
| Inventory, item pages, dragging items | `Unturned/Player/PlayerInventory.cs` | `Unturned/Inventory` (`Item`, `ItemJar`, `Items`) |
| Equipped item behaviour (gun, melee, food...) | ★ `Unturned/Useable` | `Unturned/Player/PlayerEquipment.cs`, item asset in ★ `Unturned/Bundles` |
| New item / asset type, `.dat` field | ★ `Unturned/Bundles` | `Unturned/UnturnedNexus.cs` (type registration) |
| Guns: ballistics, attachments, firing | `Unturned/Useable/UseableGun.cs` (large) | `Unturned/Bundles/ItemGunAsset.cs`, `Unturned/Attachments` |
| Damage, explosions, armor | `Unturned/Tools/DamageTool.cs` | `Unturned/Damage`, `Unturned/Bundles/ArmorTier.cs` |
| Barricades / structures (building) | ★ `Unturned/Managers` → `BarricadeManager.cs`, `StructureManager.cs` | `Unturned/Useable/UseableBarricade.cs`, `Unturned/Managers/HousingConnections.cs` |
| Items lying on the ground | `Unturned/Managers/ItemManager.cs` | `Unturned/Level/ItemSpawnpoint.cs`, `Unturned/Level/ItemTable.cs` |
| Vehicles | `Unturned/Interactable/InteractableVehicle.cs` (large) | `Unturned/Managers/VehicleManager.cs`, `Unturned/Bundles/VehicleAsset.cs` |
| Zombies | `Unturned/Zombies/Zombie.cs` | `Unturned/Managers/ZombieManager.cs`, `Unturned/Level/LevelZombies.cs` |
| Animals | `Unturned/Animals/Animal.cs` | `Unturned/Managers/AnimalManager.cs`, `Unturned/Bundles/AnimalAsset.cs` |
| Interactive world objects (doors, storage, signs) | ★ `Unturned/Interactable` | `Unturned/Managers/ObjectManager.cs` |
| Crafting | `Unturned/Player/PlayerCrafting.cs` | `Unturned/Inventory/Blueprint.cs`, `Unturned/Bundles/CraftingAsset.cs` |
| NPC dialogue, quests, vendors, flags | `Unturned/Player/PlayerQuests.cs` | `Unturned/Bundles/NPC*.cs`, `Unturned/Bundles/DialogueAsset.cs`, `Unturned/Bundles/VendorAsset.cs`, `Unturned/Tools/NPCTool.cs` |
| Skills / experience | `Unturned/Player/PlayerSkills.cs` | `Unturned/Player/Skill.cs` |
| Movement, stance, look, input | `Unturned/Player/PlayerMovement.cs`, `PlayerStance.cs`, `PlayerLook.cs`, `PlayerInput.cs` | `Unturned/Settings/ControlsSettings.cs` |
| Chat | `Unturned/Managers/ChatManager.cs` | — |
| Admin / console commands | ★ `Unturned/Command` | `Unturned/Provider/SteamAdminlist.cs` |
| Map loading, level data | ★ `Unturned/Level` → `Level.cs` | `Unturned/Loading`, `Unturned/Managers/LevelManager.cs` |
| Weather, lighting, day/night | `Unturned/Level/LevelLighting.cs` | `Unturned/Bundles/WeatherAsset.cs`, `Unturned/Level/WeatherComponentBase.cs` |
| Volumes (safezone, deadzone, kill, teleport) | `Framework/Devkit` | `Unturned/Level/*Volume*.cs`, `Unturned/Level/VolumeManagerBase.cs` |
| In-game map editor (legacy) | `Unturned/Edit` | `Unturned/UI/Edit` |
| Devkit (new editor tools, hierarchy, undo) | `Framework/Devkit` | `Framework/Devkit/Transactions` |
| Terrain / foliage | `Framework/Landscapes`, `Framework/Foliage` | — |
| UI: menus, HUD, dashboard | ★ `Unturned/UI` | `Unturned/Player/PlayerUI.cs`, `Unturned/Sleek`, `Glazier*` |
| Effects, particles, sounds | `Unturned/Managers/EffectManager.cs` | `Unturned/Bundles/EffectAsset.cs` |
| Saving / loading world & player | `Unturned/Managers/SaveManager.cs` | `Unturned/Files` (`ReadWrite`, `Block`, `*Savedata`) |
| Server gameplay config (`Config.json`) | `Unturned/Settings/PlayConfigData.cs` | `Unturned/Provider/Provider.cs` |
| Client settings (graphics, audio, controls) | `Unturned/Settings` | — |
| Localization strings | `Unturned/Files/Localization.cs`, `Unturned/Files/Local.cs` | (`.dat` texts are in the game install) |
| Workshop / mods download | `Provider/Services/Workshop`, `Unturned/Provider/SteamContent.cs` | `Unturned/Bundles/DedicatedUGC.cs` |
| Cosmetics, economy, item store | `Provider/Services/Economy`, `ItemStore` | `Unturned/Bundles/SkinAsset.cs` |
| Map-maker Unity components (event hooks) | ★ `Unturned/ModHooks` | — |
| Plugin modules (`.module` loading) | `Framework/Modules` | — |
| Server list, curation | `Unturned/UI/Menu/Play`, `Unturned/ServerListCuration` | `Unturned/Provider/SteamServerAdvertisement.cs` |
| Region grid (world split into cells) | `Unturned/Regions/Regions.cs` | used by all `*Manager` classes |
| Binary serialization for net | `Assets/Runtime/SDG.NetPak` | `NetPak` |
| `.dat` text format parser | `Assets/Runtime/UnturnedDat` | `Assets/Tests/UnturnedDat` |
| Transports (Steam sockets, UDP, loopback) | `Assets/Runtime/SDG.NetTransport`, `NetTransport_*` | `Unturned/Provider/NetTransportFactory.cs` |
| Build pipeline, editor utilities | `Assets/Editor/Assembly-CSharp-Editor/Tools` | `Assets/Editor/Jenkins` |
| Unit tests | `Assets/Tests`, `Assets/Editor/Assembly-CSharp-Editor/Tests` | run via Unity Test Runner (not available to agents) |
| Mod content security (UnityEvents in bundles) | `Unturned/Bundles/StaticUnityEventPrevention.cs` | `Unturned/Command/Commander.cs` (`execute_UnityEvent`) |
| Game version / patch status | `Builds/Shared/Status.json` | `Builds/Shared/ModInfo.json` |

## Directory index

| Directory | Contents |
|---|---|
| `Unturned/Bundles` ★ | 236 files. Asset classes parsed from `.dat`: `*Asset.cs`, NPC conditions/rewards, asset loading (`Assets.cs`) |
| `Unturned/Level` | 106 files. Level data, spawnpoints, spawn tables, volumes, weather components |
| `Unturned/Command` ★ | 95 files. One class per chat/console command |
| `Unturned/UI` ★ | Screens: `Menu`, `Player` (HUD/dashboard), `Edit` (map editor) |
| `Unturned/Menu` | Main-menu logic: `MenuUI.cs` (menu UI root), characters, customization, menu settings |
| `Unturned/Sleek` | 62 files. Reusable game widgets built on Glazier (`SleekItem`, `SleekInventory`, ...) |
| `Unturned/Interactable` ★ | Components on placed objects/vehicles that the player can use |
| `Unturned/Managers` ★ | Static world-state managers (items, barricades, structures, vehicles, zombies, effects, chat, save) |
| `Unturned/ModHooks` ★ | MonoBehaviours mod makers add to prefabs (event hooks, spawners) |
| `Unturned/Player` ★ | `Player` + its components (life, inventory, equipment, movement, quests, ...) |
| `Unturned/Provider` ★ | Networking/session hub: `Provider.cs`, `Dedicator.cs`, `SteamPlayer`, admin/ban lists |
| `Unturned/Useable` ★ | Behaviour of the equipped item (`Useable*`) |
| `Unturned/Edit` | Legacy level editor |
| `Unturned/Tools` | Static helpers: `DamageTool`, `PlayerTool`, `ItemTool`, `NPCTool`, `VehicleTool` |
| `Unturned/Utils` | Misc utilities, logging (`UnturnedLog`), `CommandLine`, layers/masks |
| `Unturned/Files` | File IO, savedata, localization |
| `Unturned/Settings` | Client options + server `PlayConfigData` |
| `Unturned/Inventory` | `Item`, `ItemJar`, `Items` (page), blueprints |
| `Unturned/Zombies`, `Unturned/Animals` | AI entities |
| `Unturned/Game` | Enums for server/game modes |
| `Unturned/Loading` | Startup: `Setup.cs`, loading screen, custom player loop |
| `Unturned/Regions` | World grid helpers |
| `Unturned/Damage` | Damage parameter structs, multipliers |
| `Framework/Devkit` | Devkit editor systems: volumes, nodes, hierarchy, selection, undo transactions |
| `Framework/Landscapes`, `Framework/Foliage`, `Framework/Water` | Terrain, foliage, water volumes |
| `Framework/Modules` | Loading of `.module` plugin assemblies |
| `Framework/IO` | Serialization helpers, formatted files |
| `NetInvokable` ★ | RPC runtime |
| `NetGen` | Generated code — regenerate, never edit |
| `NetMessaging` | Connection-level messages, `ClientMessageHandler_*` / `ServerMessageHandler_*` |
| `Provider`, `SteamworksProvider` | Service abstraction over Steamworks (economy, workshop, cloud, achievements) |
| `Glazier`, `Glazier_IMGUI`, `Glazier_uGUI`, `Glazier_UIToolkit` | UI backend implementations; interfaces in `Assets/Runtime/SDG.Glazier` |
| `ItemStore` | In-game cosmetic store UI |

## Large files — read by line range, grep first

`Unturned/Provider/Provider.cs` (~7.2k lines), `Unturned/Useable/UseableGun.cs` (~6.6k),
`Unturned/Interactable/InteractableVehicle.cs` (~6.4k), `Unturned/Managers/VehicleManager.cs`,
`Unturned/Zombies/Zombie.cs`, `Unturned/Managers/BarricadeManager.cs`, `Unturned/Player/PlayerEquipment.cs`,
`Unturned/Settings/PlayConfigData.cs`, `Unturned/UI/Player/PlayerDashboardInventoryUI.cs`,
`Unturned/Bundles/Assets.cs`, `Unturned/Player/PlayerQuests.cs`, `Unturned/Level/LevelLighting.cs`,
`Unturned/Bundles/VehicleAsset.cs`, `Unturned/Player/PlayerLife.cs`, `Unturned/Player/PlayerUI.cs`,
`Unturned/Bundles/ItemAsset.cs`, `Unturned/Level/Level.cs` (all ~2.4k+ lines).

## Do not read unless the task is about them

- `NetGen/**` — generated serializers, ~19k lines of boilerplate.
- `Assets/com.rlabrecque.steamworks.net/**` — third-party Steamworks bindings.
- `Assets/Game/**`, `Assets/Resources/**` — Unity assets (textures, materials, prefabs), not code.
- `ProjectSettings/**`, `Packages/**` — Unity project config.
