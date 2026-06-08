---
outline: deep
---

# 👋 I'm NovaBot

## 简介

NovaBot 是一个开源的一站式 Agentic 个人和群聊助手，可在 QQ、Telegram、企业微信、飞书、钉钉、Slack 等数十款主流即时通讯软件上部署，此外还内置类似 OpenWebUI 的轻量化 ChatUI，为个人、开发者和团队打造可靠、可扩展的对话式智能基础设施。无论是个人 AI 伙伴、智能客服、自动化助手，还是企业知识库，NovaBot 都能在你的即时通讯软件平台的工作流中快速构建 AI 应用。

## 文档概览

本文档分为以下几个部分：

- **部署**。我们提供多种方式帮助您把 NovaBot 快速部署到云服务器或本地机器上。
- **消息平台接入**。我们提供 18+ 主流即时通讯软件的接入指南，帮助您把 NovaBot 连接到您喜欢的 IM 平台。
- **AI 模型提供商接入**。我们支持各种 AI 模型提供商的接入，您可以选择使用 NovaBot 内置的 Agent 执行器，也可以接入第三方的 Agent 执行器服务，例如 Dify、Coze、阿里云百炼应用、DeerFlow 等，或者自己开发 Agent 执行器。
- **使用指南**。我们提供了丰富的使用指南，帮助您充分利用 NovaBot 的各种功能，例如插件、工具调用、知识库、MCP、Skills、Agent 沙箱环境等。

## 快速开始

> 您也可以使用 [☁️ 雨云部署](/deploy/nova-bot/rainyun) 来一键部署 NovaBot，无需自行配置。

- 部署 NovaBot：阅读部署指南，快速在本地机器或云服务器上部署 NovaBot。
- 连接 IM 平台：按照说明将 NovaBot 连接到您喜欢的 IM 平台，如 Discord、Telegram、Slack 等。
- 配置 AI 模型：NovaBot 支持各种 AI 模型。请参阅 [连接模型服务](/providers/start)

## 它是如何实现的？

下面的拓扑图基本简述了 NovaBot 的架构。

![Architecture](https://files.bulinbot.app/docs/source/images/what-is-nova-bot/image.png)

## 说明

- NovaBot 是一个非盈利项目，由全世界热心开源贡献者维护，并受 [AGPL-v3](https://www.chinasona.org/gnu/agpl-3.0-cn.html) 开源许可证保护。如果您对 NovaBot 进行了修改并将其用于提供具有商业盈利性质的网络服务，您必须开源所做的修改。详细联系 [community@nova-bot.app](mailto:community@nova-bot.app)。
- 使用此项目前，请务必阅读本项目的最终用户许可协议（EULA）：[最终用户许可协议](https://github.com/NovaBotDevs/NovaBot/blob/master/EULA.md)。如果您不同意该协议的任何条款，请勿使用本项目。
