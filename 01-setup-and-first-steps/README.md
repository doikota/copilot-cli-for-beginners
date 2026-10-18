<!--
---
id: CopilotCLI-01
title: !translate 最初のステップ
description: !translate 実践的なデモで GitHub Copilot CLI を体験し、interactive、plan、programmatic の各モードの使いどころを学びます。
audience: 開発者 / 学生 / ターミナルを使う方
slug: first-steps
weight: 2
---
-->

![第 01 章: 最初のステップ](assets/chapter-header.png)

> **AI がすばやくバグを見つけ、わかりにくいコードを説明し、動作するスクリプトを生成する様子を見てみましょう。その後、GitHub Copilot CLI の 3 つの使い方を学びます。**

ここから、いよいよ本格的な学習が始まります！GitHub Copilot CLI が「いつでも相談できるシニアエンジニア」のようだと言われる理由を、実際に体験しましょう。AI が数秒でセキュリティ上のバグを見つけ、複雑なコードをわかりやすく説明し、動作するスクリプトをすぐに生成する様子を見ていきます。その後、3 つの対話モード（Interactive、Plan、Programmatic）を学び、タスクに応じて使い分けられるようになります。

> ⚠️ **受講前に必要なこと**: 先に **[第 00 章: クイックスタート](../00-quick-start/README.md)** を完了してください。以下のデモを実行するには、GitHub Copilot CLI のインストールと認証が必要です。

## 🎯 この章で学ぶこと

この章を終えると、次のことができるようになります。

- 実践的なデモを通して、GitHub Copilot CLI による生産性向上を体験する
- タスクに合ったモード（Interactive、Plan、Programmatic）を選ぶ
- slash command を使ってセッションを操作する

> ⏱️ **所要時間の目安**: 約 45 分（読む時間 15 分 + 実践 30 分）

---

# Copilot CLI を初めて使ってみる

<img src="assets/first-copilot-experience.png" alt="モニターにコードを表示した机に座る開発者と、AI の支援を表す光る粒子" width="800"/>

さっそく Copilot CLI を使って、何ができるか見てみましょう。

---

## まずは慣れてみる: 最初のプロンプト

本格的なデモに進む前に、すぐに試せる簡単なプロンプトから始めましょう。**コードリポジトリは必要ありません**。ターミナルを開いて Copilot CLI を起動します。

```bash
copilot
```

次のような初心者向けのプロンプトを試してみましょう。

```
> Python の dataclass とは何か、簡単に説明してください

> 辞書のリストを指定したキーでソートする関数を書いてください

> Python の list と tuple の違いは何ですか？

> 読みやすい Python コードを書くためのベストプラクティスを 5 つ教えてください
```

Python を使っていなくても大丈夫です。使いたいプログラミング言語について質問してみましょう。

同僚に聞くように自然な言葉で質問できることを体験してください。試し終えたら `/exit` と入力してセッションを終了します。

**ポイント**: GitHub Copilot CLI は会話形式で使えます。始めるときに特別な構文は必要ありません。普段使う言葉で質問するだけです。

## 実際に使ってみる

それでは、開発者が「いつでも相談できるシニアエンジニア」と表現する理由を見てみましょう。

> 📖 **例の読み方**: `>` で始まる行は、Copilot CLI の interactive セッション内で入力するプロンプトです。`>` が付いていない行は、ターミナルで実行する shell command です。

> 💡 **出力例について**: このコースの出力例は説明用です。Copilot CLI の応答は毎回異なるため、表示される文章、形式、詳細さは例と異なることがあります。文章そのものではなく、返される情報の*種類*に注目してください。

### デモ 1: 数秒でコードレビュー

このコースには、コード品質上の問題を意図的に含めたサンプルファイルがあります。ローカル環境で作業していて、まだリポジトリを clone していない場合は、以下の `git clone` コマンドを実行し、`copilot-cli-for-beginners` フォルダーに移動してから `copilot` コマンドを実行してください。

```bash
# ローカル環境で作業していて、まだの場合はコースのリポジトリを clone する
git clone https://github.com/github/copilot-cli-for-beginners
cd copilot-cli-for-beginners

# Copilot を起動する
copilot
```

Copilot CLI の interactive セッションが始まったら、次を実行します。

```
> @samples/book-app-project/book_app.py のコード品質上の問題をレビューし、改善案を提案してください
```

> 💡 **`@` 記号は何に使う？** `@` 記号を付けると、Copilot CLI にファイルを読み込ませることができます。詳しくは第 02 章で学びます。ここでは、表示どおりにコマンドをコピーしてください。

---

<details>
<summary>🎬 実際の動作を見る</summary>

![コードレビューのデモ](assets/code-review-demo.gif)

*デモの出力は環境によって異なります。使用する model、tools、応答はここに表示されているものと異なる場合があります。*

</details>

---

**ポイント**: 数秒で専門的なコードレビューができます。手作業でレビューする場合は……もちろん、もっと時間がかかります！

---

### デモ 2: わかりにくいコードを説明してもらう

コードを見ても何をしているのかわからず、困ったことはありませんか？Copilot CLI のセッションで、次を試してください。

```
> @samples/book-app-project/books.py が何をするファイルなのか、簡単に説明してください
```

---

<details>
<summary>🎬 実際の動作を見る</summary>

![コード説明のデモ](assets/explain-code-demo.gif)

*デモの出力は環境によって異なります。使用する model、tools、応答はここに表示されているものと異なる場合があります。*

</details>

---

**何が起きるか**: （出力は異なる場合があります）Copilot CLI がファイルを読み込んでコードを理解し、わかりやすい言葉で説明します。

```
これは Python の dataclass を使った蔵書管理モジュールです。

デジタル本棚のようなものだと考えてください。
- Book は dataclass で、本の情報（タイトル、著者、出版年、読了状況）を簡単に保存するためのものです。
- BookCollection は蔵書全体を管理し、保存と読み込みを担当します。

主な構成要素:

1. @dataclass デコレーター（8 行目）
   - __init__、__repr__ などを自動的に作成します。
   - Python でデータ構造をすっきり定義できます。

2. BookCollection クラス（16 行目）
   - Book オブジェクトのリストを管理します。
   - JSON ファイルの入出力によってデータを保存します。
   - load_books() は data.json から読み込みます。
   - save_books() は asdict() を使って data.json に書き込みます。

3. Book の操作:
   - add_book() - 本を新規作成して保存します。
   - find_book_by_title() - 蔵書を検索します。
   - mark_as_read() - 読了状況を更新します。
   - find_by_author() - 著者名で絞り込みます。

よくある処理の流れ: JSON から読み込む → Python オブジェクトを操作する → JSON に書き戻す
```

**ポイント**: 複雑なコードを、根気強いメンターが教えてくれるように説明してもらえます。

---

### デモ 3: 動作するコードを生成する

検索に 15 分かけて調べるような関数が必要ですか？そのまま同じセッションで、次のように依頼してみましょう。

```
> 本のリストを受け取り、統計情報を返す Python 関数を書いてください。
  総数、読了した本の数、未読の本の数、最も古い本と最も新しい本を含めてください。
```

---

<details>
<summary>🎬 実際の動作を見る</summary>

![コード生成のデモ](assets/generate-code-demo.gif)

*デモの出力は環境によって異なります。使用する model、tools、応答はここに表示されているものと異なる場合があります。*

</details>

---

**何が起きるか**: コピーしてすぐ実行できる、完全な関数が数秒で生成されます。

試し終えたら、セッションを終了します。

```
> /exit
```

**ポイント**: セッションを切り替えることなく、すぐに結果を得られました。

---

# モードとコマンド

<img src="assets/modes-and-commands.png" alt="Copilot CLI のモードとコマンドを表す、画面やダイヤル、イコライザーが光る近未来的な操作パネル" width="800"/>

Copilot CLI でできることを体験しました。次は、これらの機能を*どのように*活用するかを学びましょう。ポイントは、状況に応じて 3 つの対話モードを使い分けることです。

> 💡 **注意**: Copilot CLI には、入力を待たずにタスクを進める **Autopilot** モードもあります。強力な機能ですが、すべての権限を許可する必要があり、premium request を自動的に使用します。このコースでは、以下の 3 つのモードを中心に学びます。基本操作に慣れたあとで Autopilot を紹介します。

---

## 🧩 身近な例え: 外食

GitHub Copilot CLI の使い方を、外食に例えてみましょう。店までの行き方を考えるときと注文するときでは、状況に応じて異なる方法を使います。

| モード | 外食での例え | 使う場面 |
|------|----------------|-------------|
| **Plan** | レストランまでの GPS ルート | 複雑なタスク: 経路を決め、途中の場所を確認し、計画に合意してから出発する |
| **Interactive** | ウェイターとの会話 | 試行錯誤しながら進める場合: 質問し、注文を調整し、リアルタイムで応答を得る |
| **Programmatic** | ドライブスルーでの注文 | すばやく結果が欲しい具体的なタスク: 今の環境のまま、すぐに結果を得る |

外食と同じように、それぞれの方法がどんな場面に合うのか、自然にわかるようになります。

<img src="assets/ordering-food-analogy.png" alt="GitHub Copilot CLI の 3 つの使い方 - Plan モード（レストランまでの GPS ルート）、Interactive モード（ウェイターとの会話）、Programmatic モード（ドライブスルー）" width="800"/>

*タスクに合わせてモードを選びましょう。最初に計画を立てるなら Plan、対話を重ねて進めるなら Interactive、すぐに一度で結果を得るなら Programmatic が適しています。*

### どのモードから始めればよいですか？

**まずは Interactive モードから始めましょう。**
- いろいろ試しながら、追加の質問ができます。
- 会話を重ねることで、自然にコンテキストが蓄積されます。
- `/clear` を使えば、簡単にやり直せます。

慣れてきたら、次のモードも試してみましょう。
- すぐに答えが欲しい単発の質問には **Programmatic モード**（`copilot -p "<プロンプト>"`）
- コーディングの前に詳しい計画を立てたいときは **Plan モード**（`/plan`）

---

## 3 つのモード

### モード 1: Interactive モード（まずはこちらから）

<img src="assets/interactive-mode.png" alt="Interactive モード - 質問に答え、注文を調整してくれるウェイターとの会話のようなモード" width="250"/>

**適した場面**: 試行錯誤、反復的な作業、複数回のやりとり。質問に答え、要望を聞き、その場で注文を調整するウェイターとの会話に似ています。

interactive セッションを開始します。

```bash
copilot
```

これまでに見たように、自然な言葉で入力できるプロンプトが表示されます。使用できるコマンドを確認するには、次のように入力します。

```
> /help
```

**ポイント**: Interactive モードではコンテキストが維持されます。実際の会話と同じように、メッセージを送るたびに前のやりとりを踏まえて進みます。

#### Interactive モードの例

```bash
copilot

> @samples/book-app-project/utils.py をレビューして、改善案を提案してください

> すべての関数に型ヒントを追加してください

> エラー処理をより堅牢にしてください

> /exit
```

各プロンプトが前の回答を踏まえていることに注目してください。毎回最初からやり直すのではなく、会話を続けています。

---

### モード 2: Plan モード

<img src="assets/plan-mode.png" alt="Plan モード - GPS を使って旅行前にルートを計画するようなモード" width="250"/>

**適した場面**: 実行前に進め方を確認したい複雑なタスク。GPS を使って旅行前にルートを計画するのに似ています。

Plan モードでは、コードを書く前に段階的な計画を作成できます。`/plan` コマンドを使うか、**Shift+Tab** を押して Plan モードに切り替えます。

```bash
copilot

> /plan 蔵書管理アプリに「読了にする」コマンドを追加してください
```

> 💡 **ヒント**: **Shift+Tab** を押すと、Interactive → Plan → Autopilot の順にモードが切り替わります。interactive セッション中なら、コマンドを入力せずにいつでもモードを切り替えられます。

`--plan` flag を使って、Copilot CLI を最初から Plan モードで起動することもできます。

```bash
copilot --plan
```

**Plan モードの出力例:**（実際の出力は異なる場合があります）

```
📋 実装計画

ステップ 1: book_app.py のコマンドハンドラーを更新する
  - "mark" コマンド用の elif 分岐を追加する
  - handle_mark_as_read() 関数を作成する

ステップ 2: ハンドラー関数を実装する
  - ユーザーに本のタイトルを入力してもらう
  - collection.mark_as_read(title) を呼び出す
  - 成功または失敗のメッセージを表示する

ステップ 3: ヘルプの説明を更新する
  - 使用可能なコマンド一覧に "mark" を追加する
  - コマンドの使い方を記載する

ステップ 4: 一連の動作をテストする
  - 本を追加する
  - 読了にする
  - 一覧の出力で状態が変わったことを確認する

実装に進みますか？[Y/n]
```

**ポイント**: Plan モードでは、コードを書く前に進め方を確認し、変更できます。Plan モード中の Copilot CLI は**読み取り専用**で、計画を承認して実装に進むまでは、ファイルを編集したり、作業環境を変更するコマンドを実行したりしません。準備ができるまで、安全に検討を続けられます。完成した計画を後で参照できるよう、ファイルに保存するよう指示することもできます。たとえば、「この計画を `mark_as_read_plan.md` に保存してください」と伝えると、計画の詳細を記載した Markdown ファイルが作成されます。

> 💡 **もっと複雑なタスクを試したいですか？** `/plan 蔵書管理アプリに検索と絞り込み機能を追加してください` を試しましょう。Plan モードは簡単な機能からアプリケーション全体まで対応できます。

> 📚 **Autopilot モード**: Shift+Tab で切り替えられる 3 つ目のモード、**Autopilot** に気づいたかもしれません。Autopilot モードでは、各ステップで入力を待つことなく、計画全体に沿って Copilot が作業を進めます。「終わったら知らせて」と同僚に仕事を任せるようなものです。一般的な流れは「計画 → 承認 → Autopilot」です。そのため、まず計画をうまく書けるようになる必要があります。`copilot --autopilot` で直接起動するか、`/autopilot <objective>`（例: `/autopilot 蔵書管理アプリに検索コマンドを追加してください`）で目標を指定することもできます。`copilot --plan --mode autopilot` を実行して、計画と Autopilot を組み合わせることもできます。Copilot が最初に計画を作成し、その後、承認を待たずに自動で実装します。まずは Interactive モードと Plan モードに慣れてから、準備ができたら[公式ドキュメント](https://docs.github.com/copilot/concepts/agents/copilot-cli/autopilot)をご覧ください。

---

### モード 3: Programmatic モード

<img src="assets/programmatic-mode.png" alt="Programmatic モード - すばやく注文できるドライブスルーのようなモード" width="250"/>

**適した場面**: 自動化、スクリプト、CI/CD、1 回で完結するコマンド。ウェイターと会話せず、ドライブスルーですばやく注文するようなものです。

対話を必要としない単発のコマンドには、`-p` flag を使います。

```bash
# コードを生成する
copilot -p "数値が偶数か奇数かを判定する関数を書いてください"

# すぐに質問する
copilot -p "Python で JSON ファイルを読み込むにはどうすればよいですか？"
```

**ポイント**: Programmatic モードでは、すばやく回答を得て終了します。会話のやりとりはなく、入力 → 出力だけです。

<details>
<summary>📚 <strong>さらに学ぶ: スクリプトで Programmatic モードを使う</strong>（クリックして展開）</summary>

慣れてきたら、shell script の中で `-p` を使うこともできます。

```bash
#!/bin/bash

# commit message を自動生成する
COMMIT_MSG=$(copilot -p "次の変更に対する commit message を作成してください: $(git diff --staged)")
git commit -m "$COMMIT_MSG"

# ファイルをレビューする
copilot --allow-all -p "@myfile.py の問題点をレビューしてください"
```
> ⚠️ **`--allow-all` について**: この flag を使うと、Copilot CLI が許可を求めずにファイルの読み取り、コマンドの実行、URL へのアクセスを行えるようになり、すべての許可確認が省略されます。Programmatic モード（`-p`）では、操作を承認する interactive セッションがないため、この設定が必要です。自分で作成したプロンプトを使い、信頼できるディレクトリ内でのみ `--allow-all` を使用してください。信頼できない入力や機密情報を扱うディレクトリでは、絶対に使用しないでください。

</details>

---

## 基本的な slash command

Copilot CLI を使い始めるときに、まず覚えておくと便利なコマンドです。

| コマンド | 機能 | 使う場面 |
|---------|--------------|-------------|
| `/ask` | 会話履歴に影響を与えずに質問する | 今のタスクを中断せず、すぐに答えを知りたいとき |
| `/clear` | 会話をクリアして新しく始める | 話題を切り替えるとき |
| `/config` | 既定値（例: default model）を表示または設定する | 以降のすべてのセッションに設定を適用したいとき |
| `/help` | 使用可能なコマンドをすべて表示する | コマンドを忘れたとき |
| `/model` | 現在のセッションで使う AI model を表示または切り替える | AI model を変更したいとき |
| `/plan` | コーディング前に作業の計画を立てる | 複雑な機能に取り組むとき |
| `/refine` | まとまりのないプロンプトを、明確で要点を絞った文章に書き直す | プロンプトを整理して、よりよい結果を得たいとき |
| `/research` | GitHub と Web の情報を使って詳しく調査する | コーディング前にトピックを調べたいとき |
| `/exit` | セッションを終了する | 作業が終わったとき |

> 💡 **`/ask` と通常のチャットの違い**: 通常は、送信したメッセージが会話に追加され、以降の応答に影響します。`/ask` は会話履歴に残さずに質問できるショートカットです。たとえば `/ask YAML とは何ですか？` のように、セッションのコンテキストに影響させず単発の質問をしたいときに便利です。

> 💡 **よりよいプロンプトを書くための `/refine`**: プロンプトが明確かどうかわからない場合は、まず思いつくままに入力し、送信する前に `/refine` を実行して Copilot に正確で構成の整ったプロンプトに書き直してもらいましょう。AI ツールを使い始めたばかりで、効果的なプロンプトの書き方を学んでいる方に特に便利です。

> 💡 **Tab 補完**: slash command の入力中に **Tab** を押すと、コマンド名が自動補完されるか、使用可能なサブコマンドや引数を順番に選べます。コマンドの正確な名前を思い出せないときに便利です。

> 💡 **Copilot の作業中にプロンプトをキューに入れる**: Copilot がタスクを処理している間に次の依頼を思いついたら、入力して **Enter** を押してください。現在のタスクが終わると自動的に実行されるため、待つ必要はありません。

まずはこれだけ覚えれば十分です。慣れてきたら、ほかのコマンドも試してみましょう。

> 📚 **公式ドキュメント**: コマンドと flag の全一覧は、[CLI コマンドリファレンス](https://docs.github.com/copilot/reference/cli-command-reference)をご覧ください。

<details>
<summary>📚 <strong>その他のコマンド</strong>（クリックして展開）</summary>

> 💡 上記の基本コマンドで、日常的な作業の多くをカバーできます。この一覧は、さらに詳しく知りたくなったときにご覧ください。

### Agent 環境

| コマンド | 機能 |
|---------|--------------|
| `/agent` | 使用可能な agent を確認して選択する |
| `/env` | 読み込まれている環境の詳細（有効な instructions、MCP server、skill、agent、plugin）を表示する |
| `/init` | リポジトリ用の Copilot instructions を初期化する |
| `/instructions` | 現在のセッションで読み込まれている instruction file を表示・管理する |
| `/mcp` | plugin ダッシュボード（MCP server 関連）を開く。専用の MCP 設定ウィザードを使うには `/mcp config` を実行する |
| `/plugin` | plugin を確認、インストール、有効化、更新するためのダッシュボードを開く |
| `/settings` | すべてのユーザー設定をまとめて確認・編集する対話型ダイアログを開く |
| `/skills` | skill を確認・管理するためのダッシュボードを開く |
| `/subagents` | 現在のセッションで実行中の subagent を表示・管理する |

> 💡 agent については[第 04 章](../04-agents-custom-instructions/README.md)、skill については[第 05 章](../05-skills/README.md)、MCP server については[第 06 章](../06-mcp-servers/README.md)で説明します。

### Model と subagent

| コマンド | 機能 |
|---------|--------------|
| `/config` | 永続的な既定値を表示・設定する（例: `/config model` で今後のすべてのセッションの default model を設定） |
| `/delegate` | タスクを GitHub Copilot cloud agent に引き継ぐ |
| `/fleet` | 複雑なタスクを並列のサブタスクに分け、より速く完了させる |
| `/model` | 現在のセッションで使う AI model の表示・切り替えを行う |
| `/tasks` | バックグラウンドの subagent と detached shell session を表示する |

### コード

| コマンド | 機能 |
|---------|--------------|
| `/diff` | 現在のディレクトリで行った変更をレビューする |
| `/pr` | 現在の branch の pull request を操作する |
| `/research` | GitHub と Web の情報を使って詳しく調査する |
| `/review` | code-review agent を実行して変更を分析する |
| `/terminal-setup` | 複数行入力（shift+enter と ctrl+enter）を有効にする |

### 権限

| コマンド | 機能 |
|---------|--------------|
| `/add-dir <directory>` | 許可リストにディレクトリを追加する |
| `/allow-all [on\|off\|show]` | すべての権限確認を自動承認する。`on` で有効化、`off` で無効化、`show` で現在の状態を確認する |
| `/permissions` | Copilot が確認なしで実行できる範囲を制御する承認モード（interactive、plan、autopilot）を切り替える |
| `/yolo` | `/allow-all on` の短縮形。すべての権限確認を自動承認します。 |
| `/cwd`、`/cd [directory]` | 作業ディレクトリを表示または変更する |
| `/list-dirs` | 許可されているディレクトリをすべて表示する |

> ⚠️ **注意して使用してください**: `/allow-all` と `/yolo` は確認を省略します。信頼できるプロジェクトでは便利ですが、信頼できないコードを扱う場合は注意してください。

### セッション

| コマンド | 機能 |
|---------|--------------|
| `/clear` | 現在のセッションを破棄し（履歴は保存されません）、新しい会話を始める |
| `/compact` | 会話を要約してコンテキストの使用量を減らす（必要に応じて `/compact バグ一覧に注目` のように指示を追加） |
| `/context` | context window の token 使用量を視覚的に表示する |
| `/keep-alive` | Copilot CLI の実行中にシステムがスリープするのを防ぐ。ノート PC で時間のかかるタスクを実行するときに便利 |
| `/memory [on\|off\|show]` | セッションをまたいで記憶する事実や設定の有効化、無効化、表示を行う |
| `/new` | 現在のセッションを終了し（検索・再開できるよう履歴に保存）、新しい会話を始める |
| `/resume` | 別のセッションに切り替える（session ID または名前を指定可能） |
| `/rename` | 現在のセッションの名前を変更する（名前を省略すると自動生成） |
| `/rewind` | タイムラインから会話の過去の時点に戻る。Copilot が変更したファイルも復元可能（git 不要） |
| `/usage` | quota の進捗バーを含む、セッションの使用量や統計情報を表示する |
| `/session` | セッション情報と workspace の概要を表示する。`/session delete`、`/session delete <id>`、`/session delete-all` でセッションを削除する |
| `/share` | セッションを Markdown ファイル、GitHub gist、または単独で表示できる HTML ファイルにエクスポートする |
| `/every <interval> <prompt>` | 繰り返し実行するプロンプトをスケジュールする（例: `/every 1h 新しい commit を要約`）。間隔は自然な言葉で指定します。`/loop` は `/every` の別名です。 |
| `/after <time> <prompt>` | 指定した時間の後に一度だけ実行するプロンプトをスケジュールする（例: `/after 30m テストを実行`）。時間は自然な言葉で指定します。 |

> 💡 **Sessions tab**: interactive な Copilot CLI の UI では、ウィンドウ上部に **Sessions tab** があります。複数のセッションを同時に実行して表示・切り替えできます。Sessions tab で `n` を押すと、現在のセッションを閉じずに新しいセッションを開始できます。

### 表示

| コマンド | 機能 |
|---------|--------------|
| `/statusline`（または `/footer`） | セッション下部の status bar に表示する項目（ディレクトリ、branch、effort、context window、quota）をカスタマイズする |
| `/theme` | ターミナルの theme を表示・設定する |
| `/vim` | 入力欄で Vim mode を有効・無効にする。`hjkl` で移動し、`i`、`a`、`o` で挿入モードにするなど、Vim の keybinding で入力できます |
| `/voice` | 音声認識でプロンプトを入力する。タイピングせず、自然に話して入力できます |

### ヘルプとフィードバック

| コマンド | 機能 |
|---------|--------------|
| `/app` | CLI から GitHub app（利用できない場合はブラウザー）を開く |
| `/changelog` | CLI の各バージョンの changelog を表示する |
| `/feedback` | GitHub にフィードバックを送信する |
| `/help` | 使用可能なコマンドをすべて表示する |

### shell command をすばやく実行する

`!` を先頭に付けると、AI を介さずに shell command を直接実行できます。

```bash
copilot

> !git status
# AI を介さずに git status を直接実行する

> !python -m pytest tests/
# pytest を直接実行する
```

### model を切り替える

Copilot CLI は OpenAI、Anthropic、Google などの複数の AI model に対応しています。利用できる model は、サブスクリプションの種類や地域によって異なります。`/model` で選択肢を確認し、model を切り替えられます。

```bash
copilot
> /model

# 利用可能な model を表示して選択します。例: GPT-6 Sol、GPT-6 Luna、Claude Sonnet 5.5、Claude Opus 5.5。
```

> 💡 **セッション限定の model と永続的な model**: `/model` コマンドで変更されるのは、**現在のセッションで使う model のみ**です。新しいセッションを開始すると、再び default model が使われます。今後のすべてのセッションで使う default model を設定するには、セッション内で `/config model` を使うか、通常の shell から `copilot config` コマンドを実行します（セッションは不要です）。

```bash
# Copilot セッションの外から、ターミナルで default model を設定する
copilot config set model claude-sonnet-5.5

# 保存済みの設定をすべて表示する
copilot config list

# 設定を削除して default に戻す
copilot config remove model
```

> 💡 **ヒント**: Copilot CLI の利用量は **GitHub AI Credits** で測定されます。消費する credit 数は、選択した model とタスクで使う token 数によって異なります。高性能な model はより多くの credit を消費する場合があります。日常的なタスクには軽量な model を使い、複雑な作業には推論能力の高い model を使うとよいでしょう。`/usage` を実行すると、現在のセッションで消費した AI credit 数を確認できます。

> 💡 **どの model を選べばよいかわからない場合**: model picker で **`Auto`** を選ぶと、セッションごとに利用可能な model の中から Copilot が自動で選択します。使い始めたばかりで model 選びに迷う場合におすすめです。

> 💡 **model family のショートカット**: `/model` picker で一覧をスクロールする代わりに、`opus`、`sonnet`、`haiku`、`gpt`、`gemini` などの family alias を入力することもできます。その family で利用可能な最適な model が選ばれます。

> 💡 **model picker の操作**: model picker では、model が **Recent**、**Recommended**、**New** のセクションに分類されます。前回使った model をすぐに見つけたり、新しく利用可能になった model を試したりできます。picker 内で **Shift+Tab** を押すと、表示するグループを切り替えられます。

### Auto routing tier

Copilot CLI には、タスクごとに最適な model を自動で選択する **Auto** routing tier があります。

```bash
copilot

> /model
# 「Auto」を選択すると、速度とコストを考慮して Copilot が最適な model を選びます
```

Auto routing はタスクの複雑さを考慮し、速度と性能のバランスを取るために、高速な軽量 model と高性能な推論対応 model のどちらかを選びます。組織で管理対象の Auto policy が設定されている場合は、**Strict** mode や、ユーザーが上書きできる routing 設定などの追加オプションが表示されることがあります。

> 💡 **新しい model**: Copilot CLI は既存の model に加えて、**GPT-6 Astra**、**GPT-6.1 Sol**、**GPT-6 Luna**、**Claude Opus 5.5** に対応しています。`/model` picker で試してみてください。

### `copilot config` で設定を管理する

interactive な `/config` slash command のほかに、ターミナルから `copilot config` コマンドを使って Copilot CLI の設定を管理できます。

```bash
# 現在の設定をすべて表示する
copilot config list

# 指定した設定を確認する
copilot config read model
copilot config read editorMode

# default 値を設定する
copilot config set model opus        # default model を Claude Opus に設定する
copilot config set editorMode vim    # Vim mode を default で有効にする

# 独自の設定を削除して default に戻す
copilot config remove model
```

この方法は、スクリプトでの利用、新しいマシンのセットアップ、interactive セッション外での設定管理に便利です。`copilot config` で管理する設定は `~/.copilot/config.json` に保存され、今後のすべてのセッションに適用されます。

### transcript view をカスタマイズする

transcript view mode を設定すると、Copilot が tool の実行状況や推論をどのように表示するかを変更できます。

```bash
copilot

> /settings
# 「Transcript view」オプションを探し、「concise」に設定する

# または ~/.copilot/config.json で直接設定する:
# "transcriptView": "concise"
```

**表示オプション:**
- **Default**: すべての tool call と推論の手順を展開して表示します。
- **Concise**: 関連する tool の操作を折りたたみ可能な作業の要約にまとめます。詳細を確認できる状態を保ちながら、画面をすっきりさせます。

途中の手順が多くて見づらくなるのを避け、全体の進捗に集中したい場合は concise view が便利です。

### セッション開始前に実行環境を選ぶ

Copilot CLI の起動後、最初のプロンプトを入力する前に、**local** と **cloud** の実行モードを切り替えられます。

```bash
copilot
# Copilot の起動後、Ctrl+E を押して environment picker を開く
# Local（自分のマシンで実行）または Cloud（リモートで実行）を選ぶ
```

自分のマシン上での対話的な作業と、cloud 上で実行するバックグラウンドタスクなど、作業方法を切り替えるときに便利です。選択内容はそのセッションに適用され、再度切り替えるまで保持されます。

</details>

---

# 実践

<img src="../assets/practice.png" alt="コードを表示したモニター、ランプ、コーヒーカップ、ヘッドホンが置かれた、実践学習のための落ち着いた机" width="800"/>

学んだことを実際に試してみましょう。

---

## ▶️ 自分で試してみる

### Interactive モードで試す

Copilot を起動し、追加のプロンプトを使って蔵書管理アプリを段階的に改善してみましょう。

```bash
copilot

> @samples/book-app-project/book_app.py をレビューしてください。どのように改善できますか？

> if/elif の連鎖を、より保守しやすい構造にリファクタリングしてください

> すべての handler 関数に型ヒントを追加してください

> /exit
```

### 機能を計画する

`/plan` を使って、コードを書く前に Copilot CLI に実装計画を作ってもらいます。

```bash
copilot

> /plan 蔵書管理アプリに、タイトルまたは著者で本を検索する機能を追加してください

# 計画を確認する
# 承認するか、変更を加える
# 段階的に実装される様子を見る
```

### Programmatic モードで自動化する

`-p` flag を使うと、interactive モードに入らず、ターミナルから Copilot CLI を直接実行できます。リポジトリのルートで、次のスクリプトを Copilot の中ではなくターミナルにコピーして実行すると、蔵書管理アプリ内のすべての Python ファイルをレビューできます。

```bash
# 蔵書管理アプリ内のすべての Python ファイルをレビューする
for file in samples/book-app-project/*.py; do
  echo "$file をレビュー中..."
  copilot --allow-all -p "@$file のコード品質を簡潔にレビューしてください。重大な問題のみ指摘してください"
done
```

**PowerShell（Windows）:**

```powershell
# 蔵書管理アプリ内のすべての Python ファイルをレビューする
Get-ChildItem samples/book-app-project/*.py | ForEach-Object {
  $relativePath = "samples/book-app-project/$($_.Name)";
  Write-Host "$relativePath をレビュー中...";
  copilot --allow-all -p "@$relativePath のコード品質を簡潔にレビューしてください。重大な問題のみ指摘してください"
}
```

---

デモを終えたら、次のバリエーションも試してみましょう。

1. **Interactive モードのチャレンジ**: `copilot` を起動して蔵書管理アプリを調べましょう。`@samples/book-app-project/books.py` について質問し、続けて 3 回改善を依頼してください。

2. **Plan モードのチャレンジ**: `/plan 蔵書管理アプリに評価とレビューの機能を追加してください` を実行します。計画をよく読み、妥当な内容か考えてみましょう。

3. **Programmatic モードのチャレンジ**: `copilot --allow-all -p "@samples/book-app-project/book_app.py にあるすべての関数を一覧にして、それぞれの役割を説明してください"` を実行します。最初からうまくいきましたか？

---

## 💡 ヒント: Web やモバイルから CLI セッションを操作する

GitHub Copilot CLI は **remote session** に対応しています。ターミナルの前にいなくても、デスクトップやモバイルの Web ブラウザー、または GitHub Mobile app から、実行中の CLI セッションを確認して操作できます。

`--remote` flag を使って remote session を開始します。

```bash
copilot --remote
```

Copilot CLI にリンクと QR code が表示されます。スマートフォンまたはデスクトップのブラウザーでリンクを開くと、セッションをリアルタイムで確認したり、追加のプロンプトを送信したり、計画をレビューしたり、agent に指示を出したりできます。セッションはユーザーごとに管理されるため、自分の Copilot CLI セッションのみアクセスできます。

実行中のセッション内で、いつでも remote access を有効にすることもできます。

```
> /remote
```

remote session の詳細は、[Copilot CLI ドキュメント](https://docs.github.com/copilot/how-tos/copilot-cli/steer-remotely)をご覧ください。

---

## 📝 課題

### メインチャレンジ: 蔵書管理アプリのユーティリティを改善する

実践例では `book_app.py` のレビューとリファクタリングを行いました。今度は同じスキルを別のファイル `utils.py` で試してみましょう。

1. interactive セッションを開始します: `copilot`
2. Copilot CLI にファイルの要約を依頼します: 「@samples/book-app-project/utils.py を要約し、このファイル内の各関数が何をするか説明してください」
3. input validation の追加を依頼します: 「`get_user_choice()` に検証を追加して、空の入力や数値以外の入力を処理できるようにしてください」
4. error handling の改善を依頼します: 「`get_book_details()` にタイトルとして空文字列を渡すとどうなりますか？それを防ぐチェックを追加してください」
5. docstring の追加を依頼します: 「`get_book_details()` に、引数の説明と戻り値を含む詳しい docstring を追加してください」
6. プロンプト間でコンテキストが引き継がれる様子を確認しましょう。各改善は前の作業を踏まえて進みます。
7. `/exit` で終了します。

**達成基準**: 複数回のやりとりを通じて改善し、input validation、error handling、docstring を備えた `utils.py` を作成できていること。

<details>
<summary>💡 ヒント（クリックして展開）</summary>

**試してみるプロンプトの例:**
```bash
> @samples/book-app-project/utils.py このファイル内の各関数は何をしますか？
> get_user_choice() に検証を追加して、空の入力や数値以外の入力を処理できるようにしてください
> get_book_details() にタイトルとして空文字列を渡すとどうなりますか？それを防ぐチェックを追加してください
> get_book_details() に、引数の説明と戻り値を含む詳しい docstring を追加してください
```

**よくあるケース:**
- Copilot CLI から確認の質問があったら、自然な言葉で答えてください。
- コンテキストは引き継がれるため、各プロンプトは前のやりとりを踏まえて進みます。
- 最初からやり直したい場合は `/clear` を使います。

</details>

### ボーナスチャレンジ: モードを比較する

例では、検索機能の追加に `/plan` を、まとめてレビューする作業に `-p` を使いました。今度は新しいタスクとして、`BookCollection` クラスに `list_by_year()` メソッドを追加する作業を 3 つのモードすべてで試してみましょう。

1. **Interactive**: `copilot` → メソッドの設計から実装まで、段階的に進めるよう依頼します。
2. **Plan**: `/plan BookCollection に、出版年の範囲で本を絞り込む list_by_year(start, end) メソッドを追加してください`
3. **Programmatic**: `copilot --allow-all -p "@samples/book-app-project/books.py list_by_year(start, end) メソッドを追加してください。start 年から end 年まで（両端を含む）に出版された本を返すようにしてください"`

**振り返り**: どのモードが最も使いやすく感じましたか？それぞれ、どんな場面で使いますか？

---

<details>
<summary>🔧 <strong>よくある間違いとトラブルシューティング</strong>（クリックして展開）</summary>

### よくある間違い

| 間違い | 起きること | 対処方法 |
|---------|--------------|-----|
| `/exit` ではなく `exit` と入力する | Copilot CLI は "exit" をコマンドではなくプロンプトとして扱う | slash command は必ず `/` から始めます |
| 複数回のやりとりに `-p` を使う | `-p` の呼び出しはそれぞれ独立しており、前の呼び出しを記憶しない | コンテキストを引き継ぐ会話には interactive モード（`copilot`）を使います |
| `$` や `!` を含むプロンプトを引用符で囲まない | Copilot CLI が受け取る前に、shell が特殊文字を解釈する | プロンプトをシングルクォートで囲みます: `copilot -p '環境変数 $HOME は何を表しますか？'` |
| 実行中のタスクを止めるために Esc を 1 回だけ押す | 誤操作を防ぐため、Esc 1 回では処理中の作業をキャンセルできません | Copilot CLI の処理中に **Esc を 2 回**押します |

### トラブルシューティング

**"Model not available"** - サブスクリプションによっては、すべての model を利用できない場合があります。`/model` で利用可能な model を確認してください。

**"Context too long"** - 会話で context window を使い切りました。`/new` を実行して新しいセッションを開始してください。

**"Rate limit exceeded"** - 数分待ってから、もう一度試してください。まとめて処理する場合は、間隔を空けながら Programmatic モードを使うことも検討してください。

</details>

---

# まとめ

## 🔑 この章のポイント

1. **Interactive モード**は探索や試行錯誤に適しています。コンテキストが引き継がれるため、それまでの会話を覚えている相手と話すように作業できます。
2. **Plan モード**は通常、より複雑なタスクに使います。実装前に計画を確認できます。
3. **Programmatic モード**は自動化に適しています。対話は必要ありません。
4. **基本コマンド**（`/ask`、`/help`、`/clear`、`/new`、`/plan`、`/research`、`/model`、`/exit`）で、日常的な作業の多くに対応できます。

> 📋 **クイックリファレンス**: コマンドとショートカットの全一覧は、[GitHub Copilot CLI コマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)をご覧ください。

---

## ➡️ 次の章

3 つのモードを理解したところで、次は Copilot CLI にコードのコンテキストを伝える方法を学びましょう。

**[第 02 章: コンテキストと会話](../02-context-conversations/README.md)** では、次の内容を学びます。

- ファイルやディレクトリを参照する `@` 構文
- `--resume` と `--continue` を使ったセッション管理
- コンテキスト管理によって Copilot CLI の能力を活用する方法

---

**[← コーストップに戻る](../README.md)** | **[第 02 章へ進む →](../02-context-conversations/README.md)**
