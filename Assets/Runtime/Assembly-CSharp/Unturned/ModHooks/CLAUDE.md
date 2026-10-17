# ModHooks — components for mod/map makers

`MonoBehaviour`s that modders attach to prefabs in their own asset bundles (`[AddComponentMenu("Unturned/...")]`):
event hooks (`*EventHook`), spawners (`ItemSpawner`, `EffectSpawner`, ...), messengers that run commands/chat.

## Rules (these are a binary contract with published mods)

- **Never rename/move the class or change its `.meta` GUID** — bundles reference the script by GUID+class.
- **Never rename or retype serialized fields** (public fields / `[SerializeField]`); use
  `[UnityEngine.Serialization.FormerlySerializedAs("old")]` when a rename is unavoidable.
- `UnityEvent` fields are a security surface: events calling static methods are blocked by
  `Unturned/Bundles/StaticUnityEventPrevention.cs`; server command execution is gated by
  `Provider.configData.UnityEvents` (see `Commander.execute_UnityEvent`).
- Server/client: many hooks only fire on one side — document which in an XML `<summary>` like neighbours do.
