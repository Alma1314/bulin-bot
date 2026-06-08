# Connect to VoceChat

> [!TIP]
> NovaBot does not include this adapter by default. Install [nova-bot_plugin_vocechat](https://github.com/HikariFroya/nova-bot_plugin_vocechat), developed by [HikariFroya](https://github.com/HikariFroya).

> [!WARNING]
> This adapter is community-maintained and not officially maintained by NovaBot.

## Deploy VoceChat

VoceChat is an open-source instant messaging platform with simple multi-platform deployment.

See deployment methods on the [VoceChat official website](https://voce.chat/en-US).

## Install `nova-bot_plugin_vocechat`

In NovaBot Dashboard Plugin Market, search for `nova-bot_plugin_vocechat` and install it.

![image](https://files.bulinbot.app/docs/source/images/vocechat/image.png)

After installation, go to `Bots` -> `+ Create Bot` -> `VoceChat`.
If VoceChat is missing, restart NovaBot or verify plugin installation.

Enable the adapter in the configuration dialog.

## Configuration

- `vocechat_server_url` (required): full VoceChat server URL, e.g. `http://localhost:3009` or `https://your.vocechat.domain` (no trailing `/`).
- `api_key` (required): API key generated for the bot account in VoceChat.
- `webhook_path` (recommended default/custom): webhook path used by NovaBot to receive VoceChat messages, e.g. `/vocechat_webhook`.
- `webhook_listen_host` (usually `0.0.0.0`): listen host for NovaBot webhook server.
- `webhook_port` (required): listen port for NovaBot webhook server, e.g. `8080`.
- `get_user_nickname_from_api` (boolean, default `true`): fetch nickname via VoceChat API.
- `send_plain_as_markdown` (boolean, default `false`): send plain text in markdown format.
- `default_bot_self_uid` (required): UID of your VoceChat bot account.

After configuration, click Save and test in VoceChat.

## Issue Reporting

If needed, report issues to:

- Plugin repo: <https://github.com/HikariFroya/nova-bot_plugin_vocechat/issues>
- NovaBot repo: <https://github.com/NovaBotDevs/NovaBot/issues/new?template=bug-report.yml>
