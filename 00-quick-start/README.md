<!--
---
id: CopilotCLI-00
title: !translate クイックスタート
description: !translate GitHub Copilot CLI をインストールし、GitHub アカウントでサインインして、動作を確認します。
audience: 開発者 / 学生 / ターミナルを使う方
slug: quick-start
weight: 1
---
-->

![第 00 章: クイックスタート](assets/chapter-header.png)

ようこそ！この章では、GitHub Copilot CLI（Command Line Interface）をインストールし、GitHub アカウントでサインインして、正しく動作することを確認します。まずは簡単なセットアップを行いましょう。準備ができたら、第 01 章から本格的なデモを始めます。

## 🎯 この章で学ぶこと

この章を終えると、次のことができるようになります。

- GitHub Copilot CLI をインストールする
- GitHub アカウントでサインインする
- 簡単なテストで動作を確認する

> ⏱️ **所要時間の目安**: 約 10 分（読む時間 5 分 + 実践 5 分）

---

## ✅ 受講前に必要なもの

- Copilot を利用できる **GitHub アカウント**。[プランの一覧](https://github.com/features/copilot/plans)をご覧ください。学生・教職員は [GitHub Education を通じて Copilot Pro を無料で利用](https://education.github.com/pack)できます。
- **ターミナルの基本操作**: `cd` や `ls` などのコマンドを使えること

### 「Copilot を利用できる」とは

GitHub Copilot CLI を使うには、有効な Copilot サブスクリプションが必要です。[github.com/settings/copilot](https://github.com/settings/copilot) で利用状況を確認できます。次のいずれかが表示されていることを確認してください。

- **Copilot Individual** - 個人向けサブスクリプション
- **Copilot Business** - 所属組織を通じた利用
- **Copilot Enterprise** - 所属企業を通じた利用
- **GitHub Education** - 認証済みの学生・教職員向けの無料利用

「You don't have access to GitHub Copilot」と表示された場合は、無料プランを利用するか、プランを契約するか、Copilot を利用できる組織に参加してください。

---

## インストール

> ⏱️ **所要時間の目安**: インストールに 2〜5 分、認証にさらに 1〜2 分かかります。

### GitHub Codespaces（セットアップ不要）

必要なツールを自分の環境にインストールしたくない場合は、GitHub Codespaces を利用できます。GitHub Copilot CLI は利用できる状態になっており（サインインは必要です）、Python と pytest もあらかじめインストールされています。

1. このリポジトリを [Fork](https://github.com/github/copilot-cli-for-beginners/fork) して、自分の GitHub アカウントにコピーします。
2. **Code** > **Codespaces** > **Create codespace on main** を選択します。
3. コンテナーの作成が完了するまで、数分待ちます。
4. 準備完了です。Codespace 環境でターミナルが自動的に開きます。

> 💡 **Codespace での動作確認**: `cd samples/book-app-project && python book_app.py help` を実行して、Python とサンプルアプリが動作することを確認します。

### ローカル環境へのインストール

自分のコンピューターでコースのサンプルと Copilot CLI を使う場合は、次の手順に従ってください。

1. リポジトリを clone して、コースのサンプルを自分の環境にコピーします。

    ```bash
    git clone https://github.com/github/copilot-cli-for-beginners
    cd copilot-cli-for-beginners
    ```

2. 次のいずれかの方法で Copilot CLI をインストールします。

    > 💡 **どの方法を選べばよいかわからない場合**: Node.js がインストールされていれば `npm` を使います。そうでない場合は、自分のシステムに合った方法を選んでください。

    ### すべてのプラットフォーム（npm）

    ```bash
    # Node.js がインストールされている場合は、この方法で CLI をすばやくインストールできます
    npm install -g @github/copilot
    ```

    ### macOS/Linux（Homebrew）

    ```bash
    brew install copilot-cli
    ```

    ### Windows（WinGet）

    ```bash
    winget install GitHub.Copilot
    ```

    ### macOS/Linux（インストールスクリプト）

    ```bash
    curl -fsSL https://gh.io/copilot-install | bash
    ```

<details>
<summary>任意: シェルの Tab 補完を有効にする</summary>

シェルの Tab 補完を有効にすると、**Tab** キーを押して `copilot` のサブコマンド、コマンドオプション、一部のオプション値を補完できます。設定は任意ですが、CLI の操作に慣れてきたら便利です。

現在、Copilot CLI は Bash、Zsh、Fish 用の補完スクリプトに対応しています。

```shell
# Bash, current session only
source <(copilot completion bash)

# Bash, persistent on Linux
copilot completion bash | sudo tee /etc/bash_completion.d/copilot

# Zsh
copilot completion zsh > "${fpath[1]}/_copilot"

# Fish
copilot completion fish > ~/.config/fish/completions/copilot.fish
```

永続的な補完を追加した場合は、シェルを再起動してください。Windows では PowerShell から Copilot CLI を実行できますが、`copilot completion` が現在対応しているのは Bash、Zsh、Fish のみです。

</details>

---

## 認証

`copilot-cli-for-beginners` リポジトリのルートでターミナルを開き、CLI を起動してフォルダーへのアクセスを許可します。

```bash
copilot
```

まだ信頼するフォルダーとして登録していない場合、リポジトリが入っているフォルダーを信頼するか確認されます。一度だけ信頼するか、今後のすべてのセッションで信頼するかを選べます。

<img src="assets/copilot-trust.png" alt="Copilot CLI でフォルダー内のファイルを信頼する" width="800"/>

フォルダーを信頼すると、GitHub アカウントでサインインできます。

```
> /login
```

**次の手順（ローカルターミナルの場合）:**

1. GitHub.com アカウントか、Enterprise アカウントでサインインするかを選びます。
2. `Sign in with your browser (recommended)` を選択します。
3. ブラウザーで GitHub の認証ページが自動的に開きます。まだ GitHub にサインインしていない場合は、ここでサインインします。
4. 「Authorize」を選択して、GitHub Copilot CLI にアクセスを許可します。
5. ターミナルに戻ると、サインインが完了しています。

> 💡 **リモート環境やブラウザーのないターミナルの場合**: リモートサーバーや SSH など、ブラウザーを使えないターミナルでは、代わりに **device code flow** が使われます。`ABCD-1234` のような一度限りのコードが表示されるので、別のコンピューターのブラウザーで [github.com/login/device](https://github.com/login/device) にアクセスし、コードを入力してサインインを完了します。特定の方法を指定するには、ブラウザーのポップアップを使う `copilot login --web-flow`、またはコードを使う `copilot login --device-code` を実行します。`/login` を使って対話的に選ぶこともできます。
> 
> <img src="assets/auth-device-flow.png" alt="Device Authorization Flow - ターミナルでのログインからサインイン完了までの 5 つの手順" width="800"/>
>
 
*ブラウザーを使う場合は、ブラウザーが自動的に開き、1 回の操作で認証できます。リモート環境やブラウザーのないターミナルでは、代わりに device code が表示されます。*

**ヒント**: サインイン状態はセッションをまたいで保持されます。token の有効期限が切れるか、明示的にサインアウトしない限り、サインインは一度だけで済みます。

---

## 動作確認

### ステップ 1: Copilot CLI を試す

サインインできたら、Copilot CLI が動作することを確認しましょう。まだ CLI を起動していない場合は、ターミナルで起動して次のように入力します。

```bash
> Say hello and tell me what you can help with
```

応答が表示されたら、次のコマンドで CLI を終了できます。

```bash
> /exit
```

---

<details>
<summary>🎬 実際の動作を見る</summary>

![Hello Demo](assets/hello-demo.gif)

*デモの出力は環境によって異なります。使用する model、tools、応答はここに表示されているものと異なる場合があります。*

</details>

---

**期待される出力**: Copilot CLI でできることを紹介する応答が表示されます。

### ステップ 2: サンプルの蔵書管理アプリを実行する

このコースでは、CLI を使って調べたり改善したりするためのサンプルアプリを用意しています（コードは `/samples/book-app-project` にあります）。学習を始める前に、*Python 製の蔵書管理ターミナルアプリ*が動作することを確認してください。環境に応じて `python` または `python3` を実行します。

> **注意:** コース全体を通して、主な例では Python（`samples/book-app-project`）を使います。ローカル環境を選んだ場合は、[Python 3.10 以降](https://www.python.org/downloads/)をインストールしてください（Codespace にはあらかじめインストールされています）。JavaScript（`samples/book-app-project-js`）版と C#（`samples/book-app-project-cs`）版もあります。各サンプルの README に、その言語でアプリを実行する手順が記載されています。

```bash
cd samples/book-app-project
python book_app.py list
```

**期待される出力**: "The Hobbit"、"1984"、"Dune" を含む 5 冊の本の一覧が表示されます。

### ステップ 3: 蔵書管理アプリについて Copilot CLI に聞く

ステップ 2 を実行した場合は、先にリポジトリのルートに戻ります。

```bash
cd ../..   # Back to the repository root if needed
copilot 
> What does @samples/book-app-project/book_app.py do?
```

**期待される出力**: 蔵書管理アプリの主な機能とコマンドの概要が表示されます。

エラーが表示された場合は、以下の[トラブルシューティング](#トラブルシューティング)を確認してください。

完了したら、次のコマンドで Copilot CLI を終了できます。

```bash
> /exit
```

---

## ✅ 準備完了！

インストールはこれで完了です。第 01 章から、次の内容に取り組みます。

- AI が蔵書管理アプリをレビューし、コード品質の問題を見つける様子を見る
- Copilot CLI の 3 つの使い方を学ぶ
- 普通の言葉で指示して、動作するコードを作成する

**[第 01 章「最初のステップ」へ進む →](../01-setup-and-first-steps/README.md)**

---

## トラブルシューティング

### 「copilot: command not found」と表示される

CLI がインストールされていません。別のインストール方法を試してください。

```bash
# If brew failed, try npm:
npm install -g @github/copilot

# Or the install script:
curl -fsSL https://gh.io/copilot-install | bash
```

### 「You don't have access to GitHub Copilot」と表示される

1. [github.com/settings/copilot](https://github.com/settings/copilot) で Copilot サブスクリプションがあることを確認します。
2. 仕事用アカウントを使用している場合は、所属組織が CLI の利用を許可していることを確認します。

### 「Authentication failed」と表示される

もう一度認証します。

```bash
copilot
> /login
```

### ブラウザーが自動的に開かない

リモート環境やブラウザーのないターミナルでは、代わりに device code flow が使われます。ターミナルに一度限りのコードが表示されるので、[github.com/login/device](https://github.com/login/device) にアクセスしてコードを入力し、アクセスを許可してください。

### token の有効期限が切れた

もう一度 `/login` を実行してください。

```bash
copilot
> /login
```

### まだ解決しない場合

- [GitHub Copilot CLI ドキュメント](https://docs.github.com/copilot/concepts/agents/about-copilot-cli)を確認してください。
- [GitHub Issues](https://github.com/github/copilot-cli/issues)を検索してください。

---

## 🔑 この章のまとめ

1. **GitHub Codespaces ならすぐに始められる** - Python、pytest、GitHub Copilot CLI があらかじめインストールされているため、すぐにデモを試せます。
2. **複数のインストール方法がある** - 自分のシステムに合った方法（Homebrew、WinGet、npm、インストールスクリプト）を選べます。
3. **認証は一度で済む** - token の有効期限が切れるまで、サインイン状態が保持されます。
4. **蔵書管理アプリが動作する** - コース全体を通して `samples/book-app-project` を使います。

> 📚 **公式ドキュメント**: インストール方法と要件については、[Copilot CLI のインストール](https://docs.github.com/copilot/how-tos/copilot-cli/cli-getting-started)をご覧ください。

> 📋 **クイックリファレンス**: コマンドとショートカットの一覧は、[GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)をご覧ください。

---

**[第 01 章「最初のステップ」へ進む →](../01-setup-and-first-steps/README.md)**
