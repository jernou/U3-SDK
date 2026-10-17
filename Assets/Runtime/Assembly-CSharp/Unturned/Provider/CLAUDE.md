# Provider — session, connections, server lifecycle

`Provider.cs` (~7.2k lines) is the hub: hosting/connecting, accept/reject/kick/ban, client list,
server config, shutdown, network update loop. **Never read it whole** — grep for the method.

## Where things are

| Need | Look for |
|---|---|
| Am I server / client / connected? | `Provider.isServer`, `Provider.isClient`, `Provider.isConnected` |
| Dedicated server? | `Dedicator.IsDedicatedServer` (`Dedicator.cs`, also the server console window) |
| All connected players | `Provider.clients` (`List<SteamPlayer>`) |
| Pending (not yet accepted) players | `Provider.pending` (`SteamPending.cs`) |
| Client connects | `Provider.connect(...)`; host: `Provider.host()` |
| Accept / reject / kick / ban | `accept`, `reject`, `kick`, `onBanPlayerRequested*`, `onCheckBanStatus*` |
| Plugin hooks | public static delegates/events: `onServerConnected`, `onServerDisconnected`, `onCheckValid*`, ... |
| Server config (`Config.json`) | `Provider.configData`, per-mode values `Provider.modeConfigData` (`Unturned/Settings/PlayConfigData.cs`) |
| Admins / bans / whitelist | `SteamAdminlist.cs`, `SteamBlacklist.cs`, `SteamWhitelist.cs` |
| Choosing transport | `NetTransportFactory.cs` |
| Lobbies, server advertisement | `Lobbies.cs`, `SteamServerAdvertisement.cs` |
| Recipient lists for RPCs | `Provider.GatherRemoteClientConnections*`, `GatherClientConnectionsWithinSphere` |

Connection-level messages (authenticate, verify, ping, kicked, banned) are handled in `NetMessaging`
(`ServerMessageHandler_*`, `ClientMessageHandler_*`).

## Rules

- Security-sensitive: anything read from a client (auth payload, lobby IDs, workshop lists) is untrusted.
  Recent fixes in history are of this kind (e.g. ignoring a non-lobby lobby ID) — follow that style.
- Client-only parts are inside `#if !DEDICATED_SERVER`.
- Public static delegates here are the main plugin API — never change their signatures.
