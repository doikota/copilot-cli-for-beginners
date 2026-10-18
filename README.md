<!--
---
id: CopilotCLI-ROOT
title: !translate はじめての GitHub Copilot CLI
description: !translate ターミナルから AI の支援を受けて、開発ワークフローを効率化しましょう。
audience: 開発者 / 学生 / ターミナルを使う方
slug: copilot-cli-for-beginners
weight: 0
---
-->

![はじめての GitHub Copilot CLI](./assets/copilot-banner.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)&ensp;
[![Open project in GitHub Codespaces](https://img.shields.io/badge/Codespaces-Open-blue?style=flat-square&logo=github)](https://codespaces.new/github/copilot-cli-for-beginners?hide_repo_select=true&ref=main&quickstart=true)&ensp;
[![Official Copilot CLI documentation](https://img.shields.io/badge/GitHub-CLI_Documentation-00a3ee?style=flat-square&logo=github)](https://docs.github.com/en/copilot/how-tos/copilot-cli)&ensp;
[![Join AI Foundry Discord](https://img.shields.io/badge/Discord-AI_Community-blue?style=flat-square&logo=discord&color=5865f2&logoColor=fff)](https://aka.ms/foundry/discord)

🎯 [学べること](#-学べること) &ensp; ✅ [受講前に必要なもの](#-受講前に必要なもの) &ensp; 🤖 [GitHub Copilot の各種ツール](#-github-copilot-の各種ツール) &ensp; 📚 [コース構成](#-コース構成) &ensp; 📋 [コマンドリファレンス](#-github-copilot-cli-コマンドリファレンス)

# はじめての GitHub Copilot CLI

> **✨ AI によるコマンドライン支援を活用して、開発ワークフローを効率化しましょう。**

GitHub Copilot CLI は、AI の支援をターミナルで直接利用できるツールです。ブラウザーやコードエディターに切り替えなくても、質問をしたり、機能を備えたアプリケーションを作成したり、コードレビューやテストの作成、問題のデバッグを行ったりできます。

コードを読み、わかりにくい書き方を説明し、作業を効率化してくれる頼もしい同僚が、いつでもそばにいるようなものです。

> 📘 **Web で学習したいですか？** このコースは GitHub 上でそのまま進められます。また、一般的な Web サイトの形式で閲覧したい場合は、[Awesome Copilot](https://awesome-copilot.github.com/learning-hub/cli-for-beginners/) をご覧ください。

このコースは、次のような方を対象としています。

- コマンドラインから AI を活用したい **ソフトウェア開発者**
- IDE 連携よりもキーボード中心のワークフローを好む **ターミナルユーザー**
- AI を活用したコードレビューや開発方法を標準化したい **チーム**

## 🎯 学べること

この実践的なコースでは、GitHub Copilot CLI の基本から、実際の開発で活用する方法まで学べます。すべての章を通して、Python 製の蔵書管理アプリを題材にし、AI を活用したワークフローで段階的に改善していきます。コースを終えるころには、ターミナルから AI を使ってコードレビュー、テスト作成、デバッグ、ワークフローの自動化を自信を持って行えるようになります。

**AI の知識や経験は必要ありません。** ターミナルを使えれば学習を始められます。

**対象:** 開発者、学生、ソフトウェア開発の経験がある方

## ✅ 受講前に必要なもの

受講を始める前に、次のものをご用意ください。

- **GitHub アカウント**: [無料で作成](https://github.com/signup)<br>
- **GitHub Copilot を利用できる環境**: [無料プラン](https://github.com/features/copilot/plans)、[月額プラン](https://github.com/features/copilot/plans)、または[学生・教職員向けの無料プラン](https://education.github.com/pack)<br>
- **ターミナルの基本操作**: `cd` や `ls` を使ったり、コマンドを実行したりできること

## 🤖 GitHub Copilot の各種ツール

GitHub Copilot には、AI を活用したさまざまなツールがあります。それぞれの利用場所と役割を紹介します。

| 製品 | 利用場所 | 説明 |
|---------|---------------|----------|
| [**GitHub Copilot CLI**](https://docs.github.com/copilot/how-tos/copilot-cli/cli-getting-started)<br>（このコースで学習） | ターミナル | ターミナルで使える AI コーディングアシスタント |
| [**GitHub Copilot**](https://docs.github.com/copilot) | VS Code、Visual Studio、JetBrains など | Agent mode、チャット、インライン候補 |
| [**GitHub.com の Copilot**](https://github.com/copilot) | GitHub | リポジトリについてのチャット、エージェントの作成など |
| [**GitHub Copilot cloud agent**](https://docs.github.com/copilot/using-github-copilot/using-copilot-coding-agent-to-work-on-tasks) | GitHub | Issue をエージェントに割り当てて、PR を受け取る |

このコースでは、AI の支援をターミナルで直接利用できる **GitHub Copilot CLI** を学びます。

## 📚 コース構成

![GitHub Copilot CLI の学習ロードマップ](assets/learning-path.png)

| 章 | タイトル | 学ぶ内容 |
|:-------:|-------|-------------------|
| 00 | 🚀 [クイックスタート](./00-quick-start/README.md) | インストールと動作確認 |
| 01 | 👋 [最初のステップ](./01-setup-and-first-steps/README.md) | デモと 3 つの対話モード |
| 02 | 🔍 [コンテキストと会話](./02-context-conversations/README.md) | 複数ファイルにまたがるプロジェクトの分析 |
| 03 | ⚡ [開発ワークフロー](./03-development-workflows/README.md) | コードレビュー、デバッグ、テストの作成 |
| 04 | 🤖 [専門 AI アシスタントの作成](./04-agents-custom-instructions/README.md) | ワークフローに合わせたカスタムエージェント |
| 05 | 🛠️ [繰り返し作業の自動化](./05-skills/README.md) | 自動で読み込まれるスキル |
| 06 | 🔌 [GitHub、データベース、API との接続](./06-mcp-servers/README.md) | MCP サーバーとの連携 |
| 07 | 🎯 [学んだことを総合して実践](./07-putting-it-together/README.md) | 機能開発の一連のワークフロー |

## 📖 コースの進め方

各章は、次の流れで進みます。

1. **身近なものにたとえて理解**: よく知っているものとの比較を通じて、概念を理解します。
2. **基本概念**: 必要な知識を学びます。
3. **実践例**: 実際にコマンドを実行し、結果を確認します。
4. **課題**: 学んだことを練習します。
5. **次の章**: 次に学ぶ内容を紹介します。

**コード例は実行できます。** このコースにある `copilot` のコードブロックは、ターミナルにコピーして実行できます。

## 📋 GitHub Copilot CLI コマンドリファレンス

**[GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)** では、Copilot CLI を効果的に使うためのコマンドやキーボードショートカットを確認できます。

## 🙋 困ったときは

- 🐛 **バグを見つけましたか？** [Issue を作成](https://github.com/github/copilot-cli-for-beginners/issues)
- 📚 **公式ドキュメント:** [GitHub Copilot CLI ドキュメント](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)

## コントリビューション

> **注意:** コース内のコードは、レビュー、説明、デバッグの際に特定の出力が得られるように設計されています。そのため、既存コードを変更する PR は受け付けていません。

**コントリビューションの手順:**

1. このリポジトリを Fork し、手元の環境に clone します。
2. feature branch を作成します（`git checkout -b my-improvement`）。
3. 変更を加えます。
4. pull request を送信します。

## ライセンス

このプロジェクトは MIT オープンソースライセンスのもとで公開されています。詳細は [LICENSE](./LICENSE) ファイルをご確認ください。
