# UI — screens (menu, in-game HUD, editor)

| Folder | Screens |
|---|---|
| `Menu` | Main menu: `MenuDashboardUI`, `Play` (server list, singleplayer), `Survivors` (character), `Workshop`, `Configuration` (options) |
| `Player` | In-game: `PlayerDashboard*UI` (inventory, crafting, skills, info), `PlayerLifeUI` (HUD), `PlayerDeathUI`, NPC dialogue/quest/vendor, barricade UIs (sign, stereo, mannequin) |
| `Edit` | Legacy level-editor panels |

Root of the in-game UI: `Unturned/Player/PlayerUI.cs`. Root of the menu: `Unturned/Menu/MenuUI.cs`
(menu-side logic like characters/customization also lives in `Unturned/Menu`).

## Building blocks

- Widgets are created through the Glazier abstraction: `Glazier.Get().CreateButton()`, `CreateLabel()`,
  `CreateBox()`, `CreateToggle()`, ... returning `ISleekElement` types (interfaces in `Assets/Runtime/SDG.Glazier`).
  Backends: `Glazier_IMGUI`, `Glazier_uGUI`, `Glazier_UIToolkit` — feature code must not depend on a backend.
- Game-specific composite widgets: `Unturned/Sleek` (`SleekItem`, `SleekInventory`, `SleekButtonIcon`, ...).
- Screen convention: static class with `static SleekFullscreenBox container`, `static bool active`,
  `open()` / `close()` (animated via `AnimateIntoView` / `AnimateOutOfView`). Copy `Unturned/UI/Menu/MenuPauseUI.cs`.
- Texts come from `Local localization` (`.dat` in the game install), icons from `IconsBundle`.

## Rules

- UI is client-only: guard with `#if !DEDICATED_SERVER` like the surrounding file.
- UI never mutates game state directly — it calls a component method that sends a server RPC.
- Large files (`PlayerDashboardInventoryUI.cs`, `PlayerLifeUI.cs`, `MenuPlayServersUI.cs`): grep first.
