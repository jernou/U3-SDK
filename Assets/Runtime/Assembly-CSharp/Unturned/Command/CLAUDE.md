# Command — chat / console commands

One class per command (`CommandKill.cs`, `CommandBan.cs`, ...), all deriving from `Command.cs`.

## How it works

- Registration: `Commander.cs` (`Commander.register(new CommandFoo(Localization.read("/Server/ServerCommandFoo.dat")))`).
- Dispatch: `Commander.execute(executorID, "name args")` → each command's `check()` compares the name and
  calls `execute(executorID, parameter)`. Sources: server console (`CommandWindow.cs`, executor = `CSteamID.Nil`),
  chat starting with `/` (`Unturned/Managers/ChatManager.cs`, admin/permission check happens there), startup
  commands (`Provider.cs`), UnityEvents (`execute_UnityEvent`, restricted by config).
- Texts (command name, info, help, error messages) come from localization `.dat` files in the game install.

## Adding a command (copy `CommandKill.cs`)

1. `CommandFoo : Command`, constructor takes `Local`, sets `_command`, `_info`, `_help` from localization.
2. Override `execute`; first check `Provider.isServer`; parse `parameter` (use `Parser`/`PlayerTool.tryGetSteamPlayer`);
   report via `CommandWindow.Log` / `CommandWindow.LogError`.
3. Register in `Commander.cs`. 4. Localization keys must exist in `/Server/ServerCommandFoo.dat`
   (not in this repo — note it in the report). 5. `.meta`.

## Rules

- `executorID == CSteamID.Nil` means server console — handle it (no player to reply to).
- Command names are user-facing API (server configs, plugins). Don't rename.
