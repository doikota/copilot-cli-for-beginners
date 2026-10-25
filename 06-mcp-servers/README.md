<!--
---
id: CopilotCLI-06
title: !translate GitHub、データベース、APIに接続する
description: !translate MCPサーバーを設定して、GitHub Copilot CLIがGitHub、ローカルファイル、ドキュメント、データベース、その他のライブデータソースに接続できるようにします。
audience: 開発者 / 学生 / ターミナル利用者
slug: connect-to-github-databases-and-apis
weight: 7
---
-->

![第6章: MCP サーバー](assets/chapter-header.png)

> **もしCopilotがGitHubの課題を読み取り、データベースを確認し、PRを作成できたら？**

これまでは、Copilotはあなたが直接渡したものだけを扱えます: `@` で参照したファイル、会話履歴、そしてそのモデルの学習済みデータです。では、GitHub リポジトリを確認したり、プロジェクトファイルを参照したり、ライブラリの最新ドキュメントを調べたりするために、自分から外部へアクセスできたらどうでしょうか。

それがMCP（Model Context Protocol）です。Copilotを外部サービスに接続し、最新の実データにアクセスできるようにする仕組みです。Copilotが接続する各サービスを「MCPサーバー」と呼びます。この章では、いくつかの接続を設定し、Copilotがどれほど便利になるかを体験します。

> 💡 **すでにMCPに慣れている方**: [クイックスタート](#-use-the-built-in-github-mcp) にジャンプして動作確認をし、サーバーの設定を始めましょう。

## 🎯 学習目標

この章の終わりまでに、次のことができるようになります:

- MCPとは何か、なぜ重要なのかを理解する
- `/mcp` コマンドでMCPサーバーを管理する
- GitHub、ファイルシステム、ドキュメント用のMCPサーバーを設定する
- 書籍アプリのプロジェクトでMCPを活用したワークフローを使う
- 必要に応じて、独自のMCPサーバーを構築する方法を知る

> ⏱️ **目安時間**: 約50分（15分読書 + 35分ハンズオン）

---

## 🧩 実世界のたとえ: ブラウザ拡張機能

<img src="assets/browser-extensions-analogy.png" alt="MCP サーバーはブラウザ拡張機能のようなもの" width="800"/>

MCPサーバーはブラウザ拡張機能のようなものだと考えてください。ブラウザ単体でもWebページを表示できますが、拡張機能によって余分なサービスに接続できます:

| ブラウザ拡張機能 | 何と接続するか | MCP相当のもの |
|-------------------|---------------------|----------------|
| パスワードマネージャー | パスワード保管庫 | **GitHub MCP** → リポジトリ、Issue、PR |
| Grammarly | 文章校正サービス | **Context7 MCP** → ライブラリのドキュメント |
| ファイルマネージャー | クラウドストレージ | **Filesystem MCP** → ローカルのプロジェクトファイル |

拡張機能がなくてもブラウザーは役に立ちますが、拡張機能を追加すると、さらに多くのことができます。MCPサーバーもCopilotに対して同じ役割を果たします。GitHubのIssueを読んだり、ファイルシステムを調べたり、最新のドキュメントを取得したりできるよう、Copilotを実際のデータソースに接続します。

***MCPサーバーはCopilotをGitHub、リポジトリ、ドキュメントなどの外部サービスにつなぎます。***

> 💡 **ポイント**: MCPがない場合、Copilotが参照できるのは`@`で明示的に共有したファイルだけです。MCPを使うと、プロジェクトの調査、GitHubリポジトリの確認、ドキュメントの検索を自動で行えるようになります。

---

<img src="assets/quick-start-mcp.png" alt="明るい電気の火花と浮かぶ技術アイコンに囲まれた電源ケーブル。MCP サーバー接続を表している" width="800"/>

# クイックスタート: 30秒でMCP

## 組み込みのGitHub MCPサーバーを使ってすぐ試す
MCPを動かすところを、設定前にすぐに体験してみましょう。
GitHub MCP サーバーはデフォルトで含まれています。次を試してください:

```bash
copilot
> このリポジトリの最近のコミットを一覧表示してください
```

Copilot が実際のコミットデータを返してきたら、もうMCPを体験したことになります。GitHub MCP サーバーがあなたに代わって GitHub にアクセスしているのです。ただし GitHub は *1つ* のサーバーにすぎません。この章では、さらに多くのサーバー（ファイルシステムアクセス、最新ドキュメント、その他）を追加して、Copilot をさらに強力にできるようにします。

---

## `/mcp show` コマンド

`/mcp show` を使うと、どの MCP サーバーが設定され、有効化されているかを確認できます:

```bash
copilot

> /mcp show

MCP サーバー:
✓ github (有効) - GitHub 統合
✓ filesystem (有効) - ファイルシステムアクセス
```

> 💡 **GitHub サーバーしか見えない？** それは通常どおりです！ 追加の MCP サーバーをまだ設定していない場合、GitHub だけが一覧に表示されます。次のセクションでさらに追加します。

> 📚 **MCP管理コマンドをすべて確認したい場合**: チャット内の`/mcp`スラッシュコマンド、またはターミナルから直接実行する`copilot mcp`でサーバーを管理できます。章末の[コマンドリファレンス](#-additional-mcp-commands)を参照してください。

<details>
<summary>🎬 実演を見る！</summary>

![MCPの状態表示デモ](assets/mcp-status-demo.gif)

*デモの出力は変わります。使用しているモデル、ツール、応答はここに示したものと異なる場合があります。*

</details>

---

## MCPで何が変わるのか？

MCP が実際にどのような違いを生むのか、例を見てみましょう:

**MCPなし:**
```bash
> GitHub issue #42 の内容を教えて

"GitHub へのアクセスがありません。課題の内容をコピー&ペーストしていただく必要があります。"
```

**MCPあり:**
```bash
> このリポジトリの GitHub issue #42 を教えて

Issue #42: 特殊文字を含むパスワードでログインできない
状態: オープン
ラベル: bug, priority-high
説明: 特殊文字を含むパスワードについて、ユーザーから...
```

MCP によって、Copilot は実際の開発環境を知ることができます。

> 📚 **公式ドキュメント**: [MCPについて](https://docs.github.com/copilot/concepts/context/mcp)で、GitHub Copilotと連携するMCPの仕組みを詳しく確認できます。

---

# MCP サーバーの設定

<img src="assets/configuring-mcp-servers.png" alt="MCP サーバーの設定を表す、ノブやスライダーを調整する手のイラスト" width="800"/>

MCP を動かしたので、次は追加のサーバーを設定していきましょう。サーバーは **組み込みレジストリから追加する方法**（最も簡単 — CLI のガイド付きセットアップ）または **設定ファイルを手動で編集する方法**（より柔軟）で追加できます。どちらを選ぶべきか迷ったら、まずはレジストリの方法から始めてください。

---

## レジストリからMCPサーバーをインストールする

CLI には組み込みの MCP サーバーレジストリがあり、人気のサーバーを発見してインストールできます。ガイド付きでセットアップできるので、JSON の編集は不要です。

```bash
copilot

> /mcp search
```

Copilot は利用可能なサーバーを表示する対話型ピッカーを開きます。1つ選ぶと、CLI が必要な設定（API キー、パスなど）を順に案内し、自動的に設定に追加します。

> 💡 **なぜレジストリを使うのか？** これは最も簡単な開始方法です。npm パッケージ名、コマンド引数、JSON の構造を知らなくても大丈夫です。CLI がすべて処理してくれます。

---

## MCP 設定ファイル

MCP サーバーは、プロジェクト横断に適用されるユーザーレベルの `~/.copilot/mcp-config.json`、またはプロジェクトレベルの `.mcp.json`、ワークスペース設定ファイル `.github/mcp.json` で設定できます。`.github/mcp.json` は `.mcp.json` と同様に自動的に読み込まれます。`/mcp search` を使った場合、CLI はユーザーレベルの `~/.copilot/mcp-config.json` を作成または更新しますが、JSON の形式を理解しておくと、プロジェクト単位の MCP 設定をカスタマイズしたり共有したりするときに役立ちます。

> ⚠️ **注意**: `.vscode/mcp.json` は MCP の設定ソースとしてはサポートされなくなりました。既存の `.vscode/mcp.json` がある場合は、プロジェクトルートにある `.mcp.json` に移行してください。古い設定ファイルを検出すると、CLI が移行のヒントを表示します。

```json
{
  "mcpServers": {
    "server-name": {
      "type": "local",
      "command": "npx",
      "args": ["@package/server-name"],
      "tools": ["*"]
    }
  }
}
```

*多くの MCP サーバーは npm パッケージとして配布され、`npx` コマンドで起動します。*

<details>
<summary>💡 <strong>JSON が初めてですか？</strong> ここをクリックして各フィールドの意味を学びましょう</summary>

| フィールド | 意味 |
|-----------|------|
| `"mcpServers"` | すべての MCP サーバー設定をまとめるコンテナ |
| `"server-name"` | 自分で決める名前（例: "github", "filesystem"） |
| `"type": "local"` | サーバーがローカルマシンで動作する |
| `"command": "npx"` | 実行するプログラム（npx は npm パッケージを実行します） |
| `"args": [...]` | コマンドに渡す引数 |
| `"tools": ["*"]` | このサーバーのすべてのツールを許可する |

**JSON の重要ルール:**
- 文字列には二重引用符 `"` を使う（シングルクォートは使わない）
- 最後の項目の後にはカンマを付けない
- ファイルは有効な JSON である必要がある（不明な場合は [JSON バリデータ](https://jsonlint.com/) を使う）

</details>

---

## MCP サーバーを追加する

GitHub MCP サーバーは組み込みであり、セットアップは不要です。以下は追加できるサーバーです。**興味のあるものを選ぶか、順番に試していってください。**

| 何をしたいですか | どこへ進むか |
|---|---|
| Copilotにプロジェクトファイルを調べてもらう | [Filesystemサーバー](#filesystem-server) |
| 最新のライブラリドキュメントを取得する | [Context7サーバー](#context7-server-documentation) |
| カスタムサーバーやweb_fetchなどの応用機能を試す | [基本を超えて](#beyond-the-basics) |

<details>
<summary><strong>Filesystemサーバー</strong> - Copilotにプロジェクトファイルを調べてもらう</summary>
<a id="filesystem-server"></a>

### Filesystemサーバー

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "tools": ["*"]
    }
  }
}
```

> 💡 **`.` パス**: `.` は「現在のディレクトリ」を意味します。Copilot は起動した場所を基準にファイルにアクセスできます。Codespace ではワークスペースのルートになります。必要なら `/workspaces/copilot-cli-for-beginners` のような絶対パスも使えます。

これを `~/.copilot/mcp-config.json` に追加してください。MCP の設定変更は次のターンから反映されます。

</details>

<details>
<summary><strong>Context7サーバー</strong> - 最新のライブラリドキュメントを取得する</summary>
<a id="context7-server-documentation"></a>

### Context7サーバー（ドキュメント）

Context7 は、人気のフレームワークやライブラリに関する最新ドキュメントに Copilot がアクセスできるようにします。学習データが古くなっていても、Copilot は現在の実際のドキュメントを取得します。

```json
{
  "mcpServers": {
    "context7": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "tools": ["*"]
    }
  }
}
```

- ✅ **APIキー不要**
- ✅ **アカウント不要**
- ✅ **コードはローカルに残る**

これを `~/.copilot/mcp-config.json` に追加してください。MCP の設定変更は次のターンから反映されます。

</details>

<details>
<summary><strong>基本を超えて</strong> - カスタムサーバーとWebアクセス（任意）</summary>
<a id="beyond-the-basics"></a>

これらは、上の基本サーバーに慣れたときに使うオプションの拡張機能です。

### Microsoft Learn MCPサーバー

ここまでに見てきた MCP サーバー（filesystem、Context7）はすべて、ローカルマシンで動作します。ただし MCP サーバーはリモートで動作することもあり、その場合は Copilot CLI に URL を伝えるだけで済みます。`npx` や `python` が不要で、ローカルプロセスや依存関係のインストールも不要です。

[Microsoft Learn MCP Server](https://github.com/microsoftdocs/mcp) はその良い例です。Copilot CLI に Microsoft の公式ドキュメント（Azure、Microsoft Foundry などの AI トピック、.NET、Microsoft 365、その他多数）への直接アクセスを与え、ドキュメントの検索、ページの取得、公式コードサンプルの参照をできるようにします。モデルの学習データに頼る必要がありません。

- ✅ **APIキー不要**
- ✅ **アカウント不要**
- ✅ **ローカルインストール不要**

**`/plugin install` を使ったクイックインストール:**

JSON 設定ファイルを手動で編集する代わりに、1つのコマンドでインストールできます:

```bash
copilot

> /plugin install microsoftdocs/mcp
```

このコマンドはサーバーと関連するエージェントスキルを自動的に追加します。インストールされるスキルには次のものがあります:

- **microsoft-docs**: 概念、チュートリアル、事実確認の参照
- **microsoft-code-reference**: API 参照、コードサンプル、トラブルシューティング
- **microsoft-skill-creator**: Microsoft 技術に関するカスタムスキルを生成するメタスキル

**使い方:**
```bash
copilot

> Azure App Service に Python アプリをデプロイする推奨方法は何ですか？ Microsoft Learn を検索してください。
```

📚 詳細: [Microsoft Learn MCPサーバーの概要](https://learn.microsoft.com/training/support/mcp-get-started)

### `web_fetch`によるWebアクセス

Copilot CLI には、任意の URL からコンテンツを取得できる組み込み `web_fetch` ツールがあります。ターミナルから離れずに README、API ドキュメント、リリースノートを取り込めます。MCP サーバーは不要です。

`~/.copilot/settings.json`（一般的な Copilot 設定）でアクセス可能な URL を制御できます。これは `~/.copilot/mcp-config.json`（MCP サーバー定義）とは別です。

> ⚠️ **設定ファイルの場所**: Copilot CLI はユーザー設定を `~/.copilot/settings.json` から読み込みます。古い `~/.copilot/config.json` はユーザー設定には使われません。そこに置いたキーは黙って無視されます。

```json
{
  "permissions": {
    "allowedUrls": [
      "https://api.github.com/**",
      "https://docs.github.com/**",
      "https://*.npmjs.org/**"
    ],
    "blockedUrls": [
      "http://**"
    ]
  }
}
```

**使い方:**
```bash
copilot

> https://github.com/facebook/react から README を取得して要約してください
```

### カスタムMCPサーバーを作る

自分の API、データベース、社内ツールに Copilot を接続したい場合は、Python でカスタム MCP サーバーを構築できます。これは任意であり、事前に用意されているサーバー（GitHub、filesystem、Context7）でほとんどの用途を満たせます。

📖 書籍アプリを例にした詳しい手順は、[カスタムMCPサーバーガイド](mcp-custom-server.md)を参照してください。

📚 背景知識については、[MCP for Beginnersコース](https://github.com/microsoft/mcp-for-beginners)も参照してください。

</details>

<a id="complete-configuration-file"></a>

### 完全な設定ファイル

ここでは、filesystem と Context7 サーバーを含む完全な `mcp-config.json` を示します:

> 💡 **メモ:** GitHub MCP は組み込みです。設定ファイルに追加する必要はありません。

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "tools": ["*"]
    },
    "context7": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "tools": ["*"]
    }
  }
}
```

これはグローバルアクセス用に `~/.copilot/mcp-config.json` として保存するか、プロジェクト固有の設定としてプロジェクトルートの `.mcp.json` として保存します。

---

# MCP サーバーの使用

MCP サーバーを設定したので、どう使えるのかを見ていきましょう。

<img src="assets/using-mcp-servers.png" alt="MCP サーバーの利用 - GitHub、Filesystem、Context7、Custom/Web Fetch サーバーに接続された開発者 CLI を表すハブアンドスポーク図" width="800" />

---

## サーバー使用例

**サーバーを選んで試すか、順番に読んでください。**

| 試したい内容 | どこへ進むか |
|---|---|
| GitHubのリポジトリ、Issue、PR | [GitHubサーバー](#github-server-built-in) |
| プロジェクトファイルを調べる | [Filesystemサーバーの使い方](#filesystem-server-usage) |
| ライブラリのドキュメントを調べる | [Context7サーバーの使い方](#context7-server-usage) |
| カスタムサーバー、Microsoft Learn MCP、web_fetchを使う | [応用機能の使い方](#beyond-the-basics-usage) |

<details>
<summary><strong>GitHubサーバー（組み込み）</strong> - リポジトリ、Issue、PRなどにアクセスする</summary>
<a id="github-server-built-in"></a>

### GitHubサーバー（組み込み）

GitHub MCP サーバーは **組み込み** です。Copilot にログインしていれば（初期セットアップ時にログイン済みです）、すでに動作しています。設定は不要です！

> 💡 **動作しない？** `/login` を実行して GitHub に再認証してください。

<details>
<summary><strong>Dev Containerでの認証</strong></summary>

- **GitHub Codespaces**（推奨）: 認証は自動的に行われます。`gh` CLI が Codespace のトークンを継承します。何もする必要はありません。
- **ローカルの dev container (Docker)**: コンテナ起動後に `gh auth login` を実行し、その後 Copilot を再起動してください。

**認証のトラブルシューティング:**
```bash
# 認証済みか確認する
gh auth status

# 認証されていない場合はログインする
gh auth login

# GitHub MCP が接続されているか確認する
copilot
> /mcp show
```

</details>

**主な機能:**

| 機能 | 例 |
|------|------|
| **リポジトリ情報** | コミット、ブランチ、貢献者の表示 |
| **Issue** | Issueの一覧表示、作成、検索、コメント |
| **プルリクエスト** | PRの表示、差分確認、作成、状態確認 |
| **コード検索** | リポジトリ全体のコード検索 |
| **Actions** | ワークフロー実行と状態の確認 |

```bash
copilot

# このリポジトリの最近のアクティビティを見る
> このリポジトリの直近5件のコミットを表示してください

最近のコミット:
1. abc1234 - 第05章のSkill例を更新（2日前）
2. def5678 - 書籍アプリのテストfixtureを追加（3日前）
3. ghi9012 - 第03章READMEの誤字を修正（4日前）
...

# リポジトリ構造を確認する
> このリポジトリに存在するブランチは何ですか？

ブランチ:
- main (デフォルト)
- chapter6 (現在)

# リポジトリ全体でコードパターンを検索する
> pytest をインポートしているファイルをこのリポジトリで検索してください

1件見つかりました:
- samples/book-app-project/tests/test_books.py
```

> 💡 **自分のフォークで作業している場合**: このコースのリポジトリをフォークしたなら、課題や PR の作成のような書き込み操作も試せます。以下の演習で実践します。

> ⚠️ **結果が見えない場合**: GitHub MCP はローカルファイルだけではなく、GitHub.com 上のリモートリポジトリを対象にします。リポジトリにリモートがあるか確認してください: `git remote -v` を実行します。

</details>

<details>
<summary><strong>Filesystemサーバー</strong> - プロジェクトファイルを調べて分析する</summary>
<a id="filesystem-server-usage"></a>

### Filesystemサーバー

設定が完了すると、filesystem MCP は Copilot が自動的に使えるツールを提供します:

```bash
copilot

> book-app-project ディレクトリにある Python ファイルは何個ですか？

samples/book-app-project/ に Python ファイルが 3 件見つかりました:
- book_app.py
- books.py
- utils.py

> data.json ファイルの合計サイズはどれくらいですか？

samples/book-app-project/data.json: 2.4 KB

> 書籍アプリで型ヒントが付いていない関数をすべて探してください

型注釈のない関数が 2 件見つかりました:
- samples/book-app-project/utils.py:10 - get_user_choice()
- samples/book-app-project/utils.py:14 - get_book_details()
```

</details>

<details>
<summary><strong>Context7サーバー</strong> - ライブラリのドキュメントを調べる</summary>
<a id="context7-server-usage"></a>

### Context7サーバー

```bash
copilot

> pytest fixture のベストプラクティスを教えてください

pytestのドキュメントより:

Fixtureはテストに一定の初期状態を用意するために使います。

    import pytest

    @pytest.fixture
    def sample_books():
        return [
            {"title": "1984", "author": "George Orwell", "year": 1949},
            {"title": "Dune", "author": "Frank Herbert", "year": 1965},
        ]

    def test_find_by_author(sample_books):
        # fixtureは引数として自動的に渡される
        results = [b for b in sample_books if "Orwell" in b["author"]]
        assert len(results) == 1

ベストプラクティス:
- setup/teardownメソッドの代わりにfixtureを使う
- 一時ファイルには`tmp_path` fixtureを使う
- 環境の変更には`monkeypatch`を使う
- 適切なfixtureのスコープ（function、class、module、session）を選ぶ

> これを書籍アプリのテストファイルにどう適用できますか？

# Copilot は公式の pytest パターンを知っており
# samples/book-app-project/tests/test_books.py に適用できます
```

</details>

<details>
<summary><strong>基本を超えて</strong> - カスタムサーバーとweb_fetchの使い方</summary>
<a id="beyond-the-basics-usage"></a>

### もっと上を目指す

**カスタムMCPサーバー**: [カスタムMCPサーバーガイド](mcp-custom-server.md)を参考に書籍検索サーバーを作成した場合、書籍コレクションを直接検索できます。

```bash
copilot

> 書籍検索サーバーを使って「1984」の情報を調べてください。George Orwellの本も検索してください。
```

**Microsoft Learn MCP**: [Microsoft Learn MCPサーバー](#microsoft-learn-mcp-server)をインストールした場合、Microsoftの公式ドキュメントを直接参照できます。

```bash
copilot

> Azure FunctionでマネージドIDを設定する方法を教えてください。Microsoft Learnを検索してください。
```

**Web Fetch**: 組み込みの`web_fetch`ツールを使って、任意のURLからコンテンツを取得できます。

```bash
copilot

> https://github.com/facebook/react から README を取得して要約してください
```

</details>

---

## マルチサーバーワークフロー

これらのワークフローを見ると、「もうこれなしでは仕事できない」と感じるでしょう。各例では、1つのセッションで複数の MCP サーバーを組み合わせています。

<img src="assets/issue-to-pr-workflow.png" alt="MCP を使った Issue から PR へのワークフロー - GitHub の課題取得からプルリクエスト作成までの完全な流れを示す" width="800"/>

*完全な MCP ワークフロー: GitHub MCP がリポジトリデータを取得し、Filesystem MCP がコードを探し、Context7 MCP がベストプラクティスを提供し、Copilot が分析を担当する*

以下の各例は独立しています。**興味のあるものを選ぶか、全部読んでください。**

| 見たい内容 | どこへ進むか |
|---|---|
| 複数のサーバーを組み合わせる | [複数サーバーでの調査](#multi-server-exploration) |
| IssueからPRまで1つのセッションで進める | [IssueからPRへのワークフロー](#issue-to-pr-workflow) |
| プロジェクトの健全性を手早く確認する | [ヘルスダッシュボード](#health-dashboard) |

<details>
<summary><strong>複数サーバーでの調査</strong> - 1つのセッションでFilesystem、GitHub、Context7を組み合わせる</summary>
<a id="multi-server-exploration"></a>

#### 複数のMCPサーバーで書籍アプリを調査する

```bash
copilot

# 手順1: Filesystem MCPを使って書籍アプリを調べる
> samples/book-app-project/ の Python ファイルをすべて列挙し、
> 各ファイルが何をするか要約してください

3つの Python ファイルが見つかりました:
- book_app.py: コマンドルーティングを持つ CLI エントリポイント（list, add, remove, find）
- books.py: JSON を使ったデータ永続化を行う BookCollection クラス
- utils.py: ユーザー入力と表示のためのヘルパー関数

# 手順2: GitHub MCPを使って最近の変更を確認する
> samples/book-app-project/ に関連する直近3件のコミットを教えてください

書籍アプリに関する最近のコミット:
1. abc1234 - BookCollection のテストフィクスチャを追加 (2日前)
2. def5678 - find_by_author メソッドを追加 (5日前)
3. ghi9012 - 書籍アプリの初期セットアップ（1週間前）

# 手順3: Context7 MCPでベストプラクティスを確認する
> JSON データ永続化に関する Python のベストプラクティスを教えてください

Pythonのドキュメントより:
- ファイル I/O には context manager（with 文）を使う
- 破損したファイルには JSONDecodeError を処理する
- 構造化データには dataclass を使う
- データ破損を防ぐために原子的書き込みを検討する

# 手順4: 改善案をまとめる
> 書籍アプリのコードとこれらのベストプラクティスに基づいて、
> どの改善を提案しますか？

提案:
1. add_book() に空文字や不正な年の入力バリデーションを追加する
2. save_books() でデータ破損を防ぐために原子的書き込みを検討する
3. utils.py の関数 (get_user_choice, get_book_details) に型注釈を追加する
```

<details>
<summary>🎬 MCP ワークフローを実演で見る</summary>

![MCPワークフローのデモ](assets/mcp-workflow-demo.gif)

*デモの出力は変わります。使用しているモデル、ツール、応答はここに示したものと異なる場合があります。*

</details>

**結果**: コード探索 → 履歴確認 → ベストプラクティスの調査 → 改善計画。**1つのターミナルセッションで、3つのMCPサーバーを同時に使っています。**

</details>

<details>
<summary><strong>IssueからPRへのワークフロー</strong> - ターミナルを離れずにGitHub Issueからプルリクエストまで進める</summary>
<a id="issue-to-pr-workflow"></a>

#### Issue-to-PR ワークフロー（自分のリポジトリで）

自分のフォークや書き込み権限のあるリポジトリで行うと最適です:

> 💡 **今すぐ試せなくても心配しないでください。** 読み取り専用のクローンにいる場合は、演習で実践します。まずは流れを理解するために読んでください。

```bash
copilot

> GitHub issue #1 の詳細を取得してください

Issue #1: 書籍の出版年に入力検証を追加する
状態: オープン
説明: add_book関数が任意の出版年を受け付けてしまう...

> @samples/book-app-project/books.py Issue #1に記載された問題を修正してください

[Copilotがadd_book()に出版年の検証を実装]

> 修正が正しく動くかテストを実行してください

すべての 8 テストが通過しました ✓

> 「書籍アプリに出版年の検証を追加」というタイトルでプルリクエストを作成してください

✓ PR #2を作成しました: 書籍アプリに出版年の検証を追加
```

**コピー&ペースト不要。コンテキスト切り替え不要。1つのターミナルセッションで完結。**

</details>

<details>
<summary><strong>ヘルスダッシュボード</strong> - 複数サーバーを使ってプロジェクトの状態をすばやく確認する</summary>
<a id="health-dashboard"></a>

#### 書籍アプリの健全性ダッシュボード

```bash
copilot

> 書籍アプリプロジェクトの健全性レポートを作成してください。
> 1. samples/book-app-project/ 内の Python ファイルからすべての関数を列挙してください
> 2. 型注釈がある関数とない関数を確認してください
> 3. samples/book-app-project/tests/ にどんなテストがあるか表示してください
> 4. このディレクトリの最近のコミット履歴を確認してください

書籍アプリの健全性レポート
======================

📊 関数の発見結果:
- books.py: BookCollection の 8 メソッド（すべて型注釈あり ✓）
- book_app.py: 6 関数（4 件に型注釈あり、2 件なし）
- utils.py: 3 関数（1 件に型注釈あり、2 件なし）

🧪 テストカバレッジ:
- test_books.py: BookCollection を対象にした 8 個のテスト関数
- 不足: book_app.py CLI 関数のテストなし
- 不足: utils.py ヘルパー関数のテストなし

📝 最近の活動:
- 過去1週間で 3 件のコミット
- 最新: テストfixtureを追加

推奨事項:
- utils.py の関数に型注釈を追加する
- book_app.py CLI ハンドラーのテストを追加する
- すべてのファイルが小さく保たれている（<100行）- 構造は良好
```

**結果**: 複数のデータソースを数秒で集約できます。手作業だと、grep の実行、行数の数え上げ、git log の確認、テストファイルの参照を手動で行う必要があり、15分以上かかります。

</details>

---

# 練習

<img src="../assets/practice.png" alt="コードが表示されたモニター、ランプ、コーヒーカップ、ヘッドフォンが並ぶ、実習用の暖かいデスク環境" width="800"/>

**🎉 ここまでで基礎は理解できました！** MCP の仕組みを理解し、サーバーの設定方法を学び、実際のワークフローも見てきました。次は自分で試してみましょう。

---

## ▶️ ぜひ自分で試してください

ここからはあなたの番です。以下の演習を完了して、書籍アプリのプロジェクトでMCPサーバーを使ってみましょう。

### 演習 1: MCP ステータスを確認する

まず、どの MCP サーバーが使えるかを確認します:

```bash
copilot

> /mcp show
```

GitHub サーバーが有効になっているはずです。もし表示されない場合は `/login` を実行して認証してください。

---

### 演習2: Filesystem MCPで書籍アプリを調べる

Filesystemサーバーを設定済みなら、それを使って書籍アプリを調べてみましょう。

```bash
copilot

> samples/book-app-project/ 内に何個の Python ファイルがありますか？
> 各ファイルで定義されている関数は何ですか？
```

**期待する結果**: Copilot が `book_app.py`、`books.py`、`utils.py` と、それぞれの関数を一覧表示します。

> 💡 **filesystem MCP をまだ設定していない場合**: 上の [完全な設定](#complete-configuration-file) セクションから設定ファイルを作成してください。MCP の設定変更は次のターンから反映されます。

---

### 演習 3: GitHub MCP でリポジトリ履歴を問い合わせる

組み込みの GitHub MCP を使って、このコースのリポジトリを調べてください:

```bash
copilot

> このリポジトリの直近5件のコミットを一覧表示してください

> このリポジトリに存在するブランチは何ですか？
```

**期待する結果**: Copilot が GitHub リモートから最近のコミットメッセージとブランチ名を表示します。

> ⚠️ **Codespace の場合**: これが自動的に動きます。認証は継承されます。ローカルクローンの場合は、`gh auth status` でログイン済みであることを確認してください。

---

### 演習 4: 複数の MCP サーバーを組み合わせる

今度は、filesystem と GitHub MCP を 1 つのセッションで組み合わせます:

```bash
copilot

> samples/book-app-project/data.json を読み込み、コレクションにどんな本があるか教えてください。次に、
> このファイルが最後に更新されたときの最近のコミットを確認してください。
```

**期待する結果**: Copilot が JSON ファイルを読み込み（filesystem MCP）、"The Hobbit"、"1984"、"Dune"、"To Kill a Mockingbird"、"Mysterious Book" を含む 5 冊をリストし、その後 GitHub にコミット履歴を問い合わせます。

**セルフチェック**: "GitHub のコミット履歴を確認して" と言うことが、`git log` を手動で実行して出力をプロンプトに貼り付けるよりも優れている理由を説明できれば、MCP を理解しています。

---

## 📝 課題

### メイン課題: MCPで書籍アプリを調べる

書籍アプリのプロジェクトで複数のMCPサーバーを組み合わせてみましょう。1つのCopilotセッションで次の手順を行います。

1. **MCP が動作していることを確認する**: `/mcp show` を実行し、少なくとも GitHub サーバーが有効になっていることを確認する
2. **filesystem MCP をセットアップする**（まだ行っていない場合）: filesystem サーバーの設定を使って `~/.copilot/mcp-config.json` を作成する
3. **コードを調べる**: Copilot に filesystem サーバーを使わせて次を確認する:
   - `samples/book-app-project/books.py` のすべての関数を一覧表示する
   - `samples/book-app-project/utils.py` のどの関数に型注釈がないかを確認する
   - `samples/book-app-project/data.json` を読み込み、データ品質の問題がないか確認する（ヒント: 最後のエントリを見てください）
4. **リポジトリのアクティビティを確認する**: Copilot に GitHub MCP を使わせて次を確認する:
   - `samples/book-app-project/` に関連する最近のコミットを一覧表示する
   - 未解決の課題や PR があるか確認する
5. **サーバーを組み合わせる**: 1つのプロンプトで Copilot に次を依頼する:
   - `samples/book-app-project/tests/test_books.py` を読み込む
   - テストされている関数と `books.py` 内のすべての関数を比較する
   - テストカバレッジの不足分を要約する

**達成基準**: filesystem と GitHub MCP のデータを 1 つの Copilot セッションでシームレスに組み合わせられ、各 MCP サーバーが応答にどのように貢献したかを説明できること。

<details>
<summary>💡 ヒント（クリックして展開）</summary>

**手順1: MCPの動作を確認する**
```bash
copilot
> /mcp show
# "github" が有効で表示されるはず
# 表示されない場合は: /login
```

**手順2: 設定ファイルを作成する**

[完全な設定](#complete-configuration-file) の JSON を使って、`~/.copilot/mcp-config.json` に保存します。

**手順3: データ品質の問題を探す**

`data.json` の最後の本は次のようになっています:
```json
{
  "title": "Mysterious Book",
  "author": "",
  "year": 0,
  "read": false
}
```

著者が空で、年が 0 になっているのがデータ品質の問題です。

**手順5: テストカバレッジを比較する**

`test_books.py` のテストは `add_book`、`mark_as_read`、`remove_book`、`get_unread_books`、`find_book_by_title` を対象にしています。`load_books`、`save_books`、`list_books` のような関数には直接のテストがありません。`book_app.py` の CLI 関数や `utils.py` のヘルパー関数にもテストがありません。

**MCP が動作しない場合**: MCP の設定変更は次のターンから自動的に反映されます。新しいサーバーを追加した直後に Copilot が見つけられない場合は、次のメッセージを入力するとサーバーが利用可能になります。

</details>

### 追加課題: カスタムMCPサーバーを作る

さらに学びたい場合は、[カスタムMCPサーバーガイド](mcp-custom-server.md)に沿って、任意のAPIに接続するPython製のMCPサーバーを作ってみましょう。

---

<details>
<summary>🔧 <strong>よくある間違いとトラブルシューティング</strong>（クリックして展開）</summary>

### よくある間違い

| 間違い | 何が起きるか | 修正方法 |
|--------|--------------|---------|
| GitHub MCPが組み込みだと知らない | 手動でインストール・設定しようとする | GitHub MCPは初めから利用できます。「このリポジトリの最近のコミットを教えて」と試してください |
| 設定ファイルの場所が違う | MCP の設定が見つからない/編集できない | ユーザーレベルの設定は `~/.copilot/mcp-config.json` です。プロジェクトレベルはプロジェクトルートの `.mcp.json` です |
| 設定ファイルの JSON が不正 | MCP サーバーが読み込まれない | `/mcp show` で設定を確認し、JSON 構文を検証してください |
| MCPサーバーの認証を忘れる | 「認証に失敗しました」というエラーが出る | サーバーによっては個別の認証が必要です。それぞれの要件を確認してください |

### トラブルシューティング

**「MCPサーバーが見つからない」** - 次の点を確認してください。
1. npm パッケージが存在する: `npm view @modelcontextprotocol/server-github`
2. 設定が有効な JSON になっている
3. サーバー名が設定と一致している

`/mcp show` で現在の設定を確認できます。

**「GitHubの認証に失敗した」** - 組み込みのGitHub MCPは`/login`の認証情報を使います。次を試してください。

```bash
copilot
> /login
```

GitHub に再認証します。問題が続く場合は、対象のリポジトリに必要な権限が GitHub アカウントにあるか確認してください。

**「MCPサーバーの起動に失敗した」** - サーバーのログを確認してください。
```bash
# サーバーコマンドを手動で実行してエラーを確認する
npx -y @modelcontextprotocol/server-github
```

**MCP ツールが使えない** - サーバーが有効になっているか確認してください:
```bash
copilot

> /mcp show
# サーバーが一覧にあり、有効かどうか確認する
```

サーバーが無効になっている場合は、以下の [追加の `/mcp` コマンド](#-additional-mcp-commands) を参照して再有効化してください。

</details>

---

<details>
<summary>📚 <strong>その他のMCPコマンド</strong>（クリックして展開）</summary>
<a id="-additional-mcp-commands"></a>

MCP サーバーは **チャットセッション内のスラッシュコマンド** または **ターミナルから `copilot mcp` コマンド** のどちらでも管理できます。

### 方法1: スラッシュコマンド（チャットセッション内）

これらは `copilot` の中にいるときに使えます:

| コマンド | 何をするか |
|---------|------------|
| `/mcp show` | すべての設定済みMCPサーバーとその状態を表示 |
| `/mcp list` | 現在接続中のMCPサーバーと状態を表示する。Copilotの作業中にも実行できる |
| `/mcp add` | 新しいサーバーを追加する対話型セットアップ |
| `/mcp edit <server-name>` | 既存のサーバー設定を編集 |
| `/mcp enable <server-name>` | 無効化されたサーバーを有効化（セッションをまたいで保持） |
| `/mcp disable <server-name>` | サーバーを無効化（セッションをまたいで保持） |
| `/mcp delete <server-name>` | サーバーを完全に削除 |
| `/mcp auth <server-name>` | OAuth を使う MCP サーバーに再認証（例: アカウントを切り替えた後） |

### 方法2: `copilot mcp`コマンド（ターミナルから）

チャットセッションを開始せずに、ターミナルから直接 MCP サーバーを管理できます:

```bash
# 設定済みの MCP サーバーを一覧表示
copilot mcp list

# サーバーを有効化
copilot mcp enable filesystem

# サーバーを無効化
copilot mcp disable context7
```

> 💡 **どちらを使うべきか？** すでにチャットセッションの途中なら `/mcp` スラッシュコマンドを使います。セッションを開始する前にサーバー設定をすばやく確認・変更したい場合は、ターミナルから `copilot mcp` を使います。

このコースでは、ほとんどの場合 `/mcp show` だけで十分です。他のコマンドは、サーバーを増やして管理するようになってから役立ちます。

</details>

---

# まとめ

## 🔑 重要なポイント

1. **MCP** は Copilot を外部サービス（GitHub、filesystem、ドキュメント）に接続します
2. **GitHub MCPは組み込み**です。設定は不要で、`/login`するだけで使えます
3. **FilesystemとContext7**は`~/.copilot/mcp-config.json`で設定します
4. **マルチサーバーのワークフロー** は 1 セッション内で複数のデータソースを組み合わせます
5. **サーバー管理は2通り**: チャット内では `/mcp` スラッシュコマンド、ターミナルでは `copilot mcp`
6. **カスタムサーバー**を使うと任意のAPIに接続できます（任意。付録のガイドで説明します）

> 📋 **クイックリファレンス**: [GitHub Copilot CLIコマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)で、コマンドとショートカットの一覧を確認できます。

---

## ➡️ 次のステップ

モード、コンテキスト、ワークフロー、Agent、Skill、MCPという基本要素を学びました。これらを組み合わせてみましょう。

**[第07章: すべてを組み合わせる](../07-putting-it-together/README.md)**では、次のことを学びます。

- Agent、Skill、MCPを組み合わせたワークフロー
- アイデアからマージ済みPRまでの機能開発
- Hookを使った自動化
- チームで使うためのベストプラクティス

---

**[← 第05章に戻る](../05-skills/README.md)** | **[第07章に進む →](../07-putting-it-together/README.md)**
