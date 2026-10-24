<!--
---
id: CopilotCLI-04
title: !translate 専門分野に特化したAIアシスタントを作成する
description: !translate 組み込みエージェントの利用、カスタムエージェントの作成、GitHub Copilot CLIを特定のタスクへ導くカスタム指示の作成方法を学びます。
audience: Developers / Students / Terminal users
slug: create-specialized-ai-assistants
weight: 5
---
-->

![第04章：エージェントとカスタム指示](assets/chapter-header.png)

> **Pythonコードレビュー担当、テストの専門家、セキュリティレビュー担当を、1つのツールで雇えたらどうでしょう？**

第03章では、コードレビュー、リファクタリング、デバッグ、テスト生成、Git連携という基本的なワークフローを習得しました。これらを活用すると、GitHub Copilot CLIでの作業が大幅に効率化します。ここからさらに一歩進みましょう。

これまではCopilot CLIを汎用アシスタントとして使ってきました。エージェントを使うと、型ヒントとPEP 8を徹底するコードレビュー担当や、pytestのテストケースを書くテスト支援担当のように、特定の役割と標準を持たせられます。目的に合わせた指示を持つエージェントに任せることで、同じプロンプトでも結果が大きく改善する様子を見ていきましょう。

## 🎯 学習目標

この章を終えると、次のことができるようになります。

- 組み込みエージェントのPlan（`/plan`）とCode-review（`/review`）を使い、自動で使われるエージェント（Explore、Task）を理解する
- エージェントファイル（`.agent.md`）を使って、専門エージェントを作成する
- 特定分野のタスクにエージェントを活用する
- `/agent` と `--agent` を使ってエージェントを切り替える
- プロジェクト固有の規約を定めるカスタム指示ファイルを書く

> ⏱️ **目安時間**：約55分（読解20分＋実習35分）

---

## 🧩 身近な例：専門家に依頼する

家のことで助けが必要なとき、「何でも屋さん」一人に頼むのではなく、専門家に依頼します。

| 問題 | 専門家 | 理由 |
|---------|------------|-----|
| 水漏れする配管 | 配管工 | 配管の基準に詳しく、専用工具を持っている |
| 電気配線のやり直し | 電気工事士 | 安全要件を理解し、基準に沿って作業する |
| 屋根の葺き替え | 屋根職人 | 建材や地域の気候を考慮できる |

エージェントも同じです。汎用AIの代わりに、特定のタスクに集中し、適切な手順を知っているエージェントを使います。指示を一度設定すれば、コードレビュー、テスト、セキュリティ、ドキュメント作成など、必要なときに繰り返し利用できます。

<img src="assets/hiring-specialists-analogy.png" alt="専門家に依頼する例：家の修理を専門職に頼むように、AIエージェントもコードレビュー、テスト、セキュリティ、ドキュメント作成などのタスクに特化しています" width="800" />

---

# エージェントを使う

組み込みエージェントとカスタムエージェントをすぐに使い始めましょう。

---

## *エージェントを初めて使う方へ*：ここから始めましょう
エージェントを使ったことも作ったこともない方は、このコースで使い始めるために必要なことを確認しましょう。

1. **組み込みエージェントを今すぐ試す：**
   ```bash
   copilot
   > /plan 書籍アプリの出版年に入力検証を追加する
   ```
   Planエージェントが呼び出され、実装手順を段階的にまとめた計画が作成されます。

2. **カスタムエージェントの例を見る：** エージェントの指示を定義するのは簡単です。パターンを確認するには、サンプルの[python-reviewer.agent.md](../.github/agents/python-reviewer.agent.md)を見てください。

3. **基本的な考え方を理解する：** エージェントを使うのは、何でもできる人ではなく専門家に相談するようなものです。「frontend agent」はアクセシビリティやコンポーネントのパターンに自動的に注目します。エージェントの指示にすでに書かれているため、毎回念押しする必要はありません。


## 組み込みエージェント

**第03章「開発ワークフロー」ですでに組み込みエージェントを使っています！**
<br>`/plan` と `/review` は、実は組み込みエージェントです。内部で何が起きているかが分かったところで、一覧を見てみましょう。

| エージェント | 呼び出し方 | 役割 |
|-------|---------------|--------------|
| **Plan** | `/plan` または `Shift+Tab`（モードを切り替え） | コーディング前に、実装計画を段階的に作成する |
| **Code-review** | `/review` | ステージ済み／未ステージの変更を確認し、要点を絞った実行可能なフィードバックを返す |
| **Init** | `/init` | プロジェクト設定ファイル（指示、エージェント）を生成する |
| **Explore** | *自動* | コードベースの調査や分析をCopilotに頼んだとき、内部で使われる |
| **Task** | *自動* | テスト、ビルド、Lint、依存関係のインストールなどのコマンドを実行する |

<br>

**組み込みエージェントの実行例** - Plan、Code-review、Explore、Taskの呼び出し例

```bash
copilot

# Planエージェントを呼び出して実装計画を作成
> /plan 書籍アプリの出版年に入力検証を追加する

# Code-reviewエージェントで変更をレビュー
> /review

# ExploreとTaskのエージェントは、必要に応じて自動で呼び出されます。
> テストスイートを実行する        # Taskエージェントを使用

> 書籍データの読み込み方法を調べる    # Exploreエージェントを使用
```

Taskエージェントはどうでしょうか。裏側で処理の進行を管理・追跡し、結果を分かりやすく整理して報告します。

| 結果 | 表示される内容 |
|---------|--------------|
| ✅ **成功** | 簡潔な概要（例：「247件のテストがすべて成功」「ビルド成功」） |
| ❌ **失敗** | スタックトレース、コンパイラーエラー、詳細なログを含む出力全体 |

> 💡 **複数ターンに対応するサブエージェント**：サブエージェント（エージェントが起動するバックグラウンドタスク）には、追加のメッセージを送れます。エージェントがバックグラウンドで動作している間に`/tasks`を開き、状況を確認して追加の指示を送れます。完了を待たずに方向を調整できます。作業中のアシスタントに声をかけ、追加の指示を出せるイメージです。

### Planモードで使うモデルを選ぶ

既定では、`/plan`はセッションで選択したものと同じAIモデルを使います。Planモードだけで使う別のモデルを選ぶこともできます。計画には高速または低コストのモデルを使い、実装時にはより高性能なモデルに戻す、といった使い方ができます。

```bash
copilot

# Planモード専用のモデル選択画面を開く
> /model plan

# モデルIDを直接指定する（Planモードのモデルを解除するには'off'を使う）
> /model plan gpt-5.6-sol

# Planモードを終了すると、モデルは自動的にセッションのものに戻る
```

> 💡 **Planモード用のモデルを設定する理由**：最初に高性能モデルで質の高い計画を立てると、結果としてトークンと時間を節約できることがあります。範囲が明確で正確な計画があれば、実装中のやり取りや修正が減ります。

> 📚 **公式ドキュメント**：[GitHub Copilot CLIのエージェント](https://docs.github.com/copilot/how-tos/copilot-cli/use-copilot-cli/invoke-custom-agents)

---

# Copilot CLIにエージェントを追加する

自分のワークフローに合わせてエージェントを定義できます。一度定義すれば、あとは呼び出すだけです。

<img src="assets/using-agents.png" alt="それぞれ異なる道具を持つ、専門エージェントの能力を表した4体のカラフルなAIロボット" width="800"/>

<a id="add-your-agents"></a>
## 🗂️ エージェントを追加する

エージェントファイルは、拡張子が`.agent.md`のMarkdownファイルです。YAMLフロントマター（メタデータ）とMarkdown形式の指示の2つの部分で構成されます。

> 💡 **YAMLフロントマターを初めて使う方へ**：ファイル先頭の`---`で囲まれた設定ブロックです。YAMLは`キー: 値`の組み合わせで記述します。それ以外の部分は通常のMarkdownです。

最小構成のエージェントは次のとおりです。

```markdown
---
name: my-reviewer
description: バグとセキュリティ問題に注目するコードレビュー担当
---

# コードレビュー担当

あなたはバグやセキュリティ問題の発見に注力するコードレビュー担当です。

コードをレビューするときは、必ず次の点を確認してください。
- SQLインジェクションの脆弱性
- エラーハンドリングの不足
- ハードコードされたシークレット
```

> 💡 **必須項目と任意項目**：`description`フィールドは必須です。`name`、`tools`、`model`などのフィールドは任意です。

<a id="where-to-put-agent-files"></a>
## エージェントファイルの配置場所

| 場所 | 適用範囲 | 主な用途 |
|----------|-------|----------|
| `.github/agents/` | プロジェクト固有 | プロジェクトの規約に合わせ、チームで共有するエージェント |
| `~/.copilot/agents/` | グローバル（すべてのプロジェクト） | どこでも使う個人用エージェント |

**このプロジェクトには、[.github/agents/](../.github/agents/)フォルダーにエージェントのサンプルがあります**。自分で作成することも、既存のサンプルをカスタマイズすることもできます。

<details>
<summary>📂 このコースのエージェントサンプルを見る</summary>

| ファイル | 説明 |
|------|-------------|
| `hello-world.agent.md` | 最小限の例 - ここから始める |
| `python-reviewer.agent.md` | Pythonコード品質レビュー担当 |
| `pytest-helper.agent.md` | pytestテストの専門家 |

```bash
# または個人用エージェントフォルダーにコピーする（すべてのプロジェクトで利用可能）
cp .github/agents/python-reviewer.agent.md ~/.copilot/agents/
```

コミュニティのエージェントについては、[github/awesome-copilot](https://github.com/github/awesome-copilot)を参照してください。

</details>


## 🚀 カスタムエージェントを使う2つの方法

### 対話モード
対話モードでは、`/agent`を使ってエージェントの一覧を表示し、使いたいエージェントを選びます。
エージェントを選択すると、そのエージェントとの会話を続けられます。

```bash
copilot
> /agent
```

別のエージェントに切り替える場合や既定のモードに戻る場合は、もう一度`/agent`を使います。

### コマンドモード

エージェントを指定して新しいセッションを直接開始します。

```bash
copilot --agent=python-reviewer
> @samples/book-app-project/books.py をレビューする
```

> 💡 **エージェントの切り替え**：`/agent`または`--agent`をもう一度使えば、いつでも別のエージェントに切り替えられます。通常のCopilot CLIに戻るには、`/agent`を使って**エージェントなし**を選びます。

> 💡 **エージェントの設定はセッション単位**：選択したエージェントは現在のセッションだけに適用されます。`/new`や`/clear`で新しいセッションを始めるか、新しいターミナルを開くと、Copilotは既定のモードに戻ります。選択したエージェントは自動では引き継がれません。毎回まっさらな状態から始まるので、作業に集中しやすくなります。

---

# エージェントをさらに活用する

<img src="assets/creating-custom-agents.png" alt="カスタムエージェントの作成を表す、部品や工具に囲まれた作業台で組み立てられるロボット" width="800"/>

> 💡 **このセクションは任意です。** 組み込みエージェント（`/plan`、`/review`）は、ほとんどのワークフローで十分に強力です。作業全体で一貫して専門知識を適用したい場合に、カスタムエージェントを作成しましょう。

以下の各トピックは、それぞれ独立しています。**興味のあるものを選んでください。一度にすべて読む必要はありません。**

| やりたいこと | 移動先 |
|---|---|
| エージェントが汎用プロンプトより優れている理由を見る | [専門エージェントと汎用プロンプトの違い](#specialist-vs-generic-see-the-difference) |
| 機能開発で複数のエージェントを組み合わせる | [複数のエージェントを使う](#working-with-multiple-agents) |
| エージェントを整理し、命名して共有する | [エージェントの整理と共有](#organizing--sharing-agents) |
| 常に有効なプロジェクトコンテキストを設定する | [Copilot向けにプロジェクトを設定する](#configuring-your-project-for-copilot) |
| YAMLのプロパティやツールを調べる | [エージェントファイルのリファレンス](#agent-file-reference) |

以下のシナリオを選択すると、詳細が表示されます。

---

<a id="specialist-vs-generic-see-the-difference"></a>
<details>
<summary><strong>専門エージェントと汎用プロンプトの違い</strong> - エージェントがより良い結果を生む理由</summary>

## 専門エージェントと汎用プロンプトの違い

ここでエージェントの効果を確認しましょう。違いを見てください。

### エージェントを使わない場合（汎用Copilot）

```bash
copilot

> 書籍アプリに、出版年の範囲で本を検索する関数を追加する
```

**汎用Copilotの出力**：
```python
def search_by_year_range(books, start_year, end_year):
    results = []
    for book in books:
        if book['year'] >= start_year and book['year'] <= end_year:
            results.append(book)
    return results
```

基本的な機能は動きますが、多くの点が不足しています。

---

### Python Reviewerエージェントを使う場合

```bash
copilot

> /agent
# 「python-reviewer」を選択

> 書籍アプリに、出版年の範囲で本を検索する関数を追加する
```

**専門エージェントの出力**：
```python
from typing import List, Dict, Any

def search_by_year_range(
    books: List[Dict[str, Any]],
    start_year: int,
    end_year: int
) -> List[Dict[str, Any]]:
    """
    指定した出版年の範囲に含まれる本を検索します。

    Args:
        books: 書籍の辞書のリスト
        start_year: 開始年（含む）
        end_year: 終了年（含む）

    Returns:
        指定した出版年の範囲に含まれる本のリスト

    Raises:
        ValueError: start_yearがend_yearより大きい場合
        TypeError: 年の値が整数でない場合
    """
    if not isinstance(start_year, int) or not isinstance(end_year, int):
        raise TypeError("年の値は整数である必要があります")

    if start_year > end_year:
        raise ValueError(f"開始年（{start_year}）は終了年（{end_year}）より大きくできません")

    return [
        book for book in books
        if isinstance(book.get('year'), int)
        and start_year <= book['year'] <= end_year
    ]
```

**python-reviewerエージェントが自動的に含める内容**：
- ✅ すべての引数と戻り値の型ヒント
- ✅ Args／Returns／Raisesを含む詳しいdocstring
- ✅ 適切なエラーハンドリングを伴う入力検証
- ✅ パフォーマンス向上につながるリスト内包表記
- ✅ 欠落・不正な年の値などのエッジケースへの対応
- ✅ PEP 8に準拠したフォーマット
- ✅ 防御的プログラミングの実践

**この違いに注目してください**：同じプロンプトでも、出力の質が大きく向上しています。エージェントは、依頼するのを忘れがちな専門知識も補ってくれます。

</details>

---

<a id="working-with-multiple-agents"></a>
<details>
<summary><strong>複数のエージェントを使う</strong> - 専門家を組み合わせ、セッション中に切り替え、エージェントをツールとして使う</summary>

## 複数のエージェントを使う

専門家が機能開発に一緒に取り組むと、エージェントの力をさらに発揮できます。

### 例：簡単な機能を作る

```bash
copilot

> 書籍アプリに「出版年の範囲で検索」する機能を追加したい

# 設計にはpython-reviewerを使う
> /agent
# 「python-reviewer」を選択

> @samples/book-app-project/books.py find_by_year_rangeメソッドを設計してください。どのような方法が最適ですか？

# テストの設計にはpytest-helperに切り替える
> /agent
# 「pytest-helper」を選択

> @samples/book-app-project/tests/test_books.py find_by_year_rangeメソッドのテストケースを設計してください。
> どのようなエッジケースを確認すべきですか？

# 2つの設計案をまとめる
> メソッドの実装と包括的なテストを含む実装計画を作成してください。
```

**大切なポイント**：あなたは専門家を指揮する設計者です。細部はエージェントに任せ、全体の方向性はあなたが決めます。

<details>
<summary>🎬 実際の動きを見る</summary>

![Python Reviewerのデモ](assets/python-reviewer-demo.gif)

*デモの出力は異なる場合があります。使用するモデルやツール、応答によって、ここに示す内容と異なることがあります。*

</details>

### ツールとしてのエージェント

エージェントを設定すると、複雑なタスクの途中でCopilotがそれらをツールとして呼び出すこともできます。フルスタック機能を依頼した場合、Copilotが作業の一部を適切な専門エージェントに自動で委任することがあります。

</details>

---

<a id="organizing--sharing-agents"></a>
<details>
<summary><strong>エージェントの整理と共有</strong> - 命名、ファイルの配置、指示ファイル、チームでの共有</summary>

## エージェントの整理と共有

### エージェントに名前を付ける

エージェントファイルを作るときは、名前が重要です。`/agent`や`--agent`の後に入力する名前であり、チームのメンバーがエージェント一覧で見る名前でもあります。

| ✅ 良い名前 | ❌ 避ける名前 |
|--------------|----------|
| `frontend` | `my-agent` |
| `backend-api` | `agent1` |
| `security-reviewer` | `helper` |
| `react-specialist` | `code` |
| `python-backend` | `assistant` |

**命名規則：**
- 小文字とハイフンを使う：`my-agent-name.agent.md`
- 分野を名前に含める：`frontend`、`backend`、`devops`、`security`
- 必要に応じて具体的にする：単に`frontend`とせず、`react-typescript`のようにする

---

### チームで共有する

エージェントファイルを`.github/agents/`に置くと、バージョン管理の対象になります。リポジトリにプッシュすれば、チームの全員が自動的に利用できます。ただし、エージェントはCopilotがプロジェクトから読み込むファイルの一種にすぎません。`/agent`を実行しなくても、すべてのセッションに自動で適用される**指示ファイル**もサポートされています。

たとえるなら、エージェントは必要なときに呼ぶ専門家、指示ファイルは常に有効なチームのルールです。

### ファイルの配置場所

主な配置場所はすでに確認しました（上の[エージェントファイルの配置場所](#where-to-put-agent-files)を参照）。どちらにするか、次の判断フローで選びましょう。

<img src="assets/agent-file-placement-decision-tree.png" alt="エージェントファイルの配置場所を選ぶ判断フロー：試す場合は現在のフォルダー、チームで使う場合は.github/agents/、すべてのプロジェクトで使う場合は~/.copilot/agents/" width="800"/>

**まずはシンプルに始めましょう：** プロジェクトフォルダーに`*.agent.md`ファイルを1つ作成します。内容に満足したら、正式な配置場所に移しましょう。

エージェントファイルに加えて、Copilotは**プロジェクトレベルの指示ファイル**も自動で読み込みます。`/agent`は必要ありません。`AGENTS.md`、`.instructions.md`、`/init`については、後述の[Copilot向けにプロジェクトを設定する](#configuring-your-project-for-copilot)を参照してください。

</details>

---

<a id="configuring-your-project-for-copilot"></a>
<details>
<summary><strong>Copilot向けにプロジェクトを設定する</strong> - AGENTS.md、指示ファイル、/initによる設定</summary>

## Copilot向けにプロジェクトを設定する

エージェントは必要なときに呼び出す専門家です。これとは異なり、**プロジェクト設定ファイル**はCopilotが毎回のセッションで自動的に読み込み、プロジェクトの規約、技術スタック、ルールを理解するために使います。誰かが`/agent`を実行する必要はなく、リポジトリで作業する全員に常にコンテキストが適用されます。

### /initで簡単に設定する

最も手早く始めるには、Copilotに設定ファイルを生成してもらいましょう。

```bash
copilot
> /init
```

Copilotがプロジェクトを調べて、それに合わせた指示ファイルを作成します。あとから編集できます。

### 指示ファイルの形式

| ファイル | 適用範囲 | 備考 |
|------|-------|-------|
| `AGENTS.md` | プロジェクトのルートまたはその下の階層 | **クロスプラットフォーム標準** - Copilotや他のAIアシスタントで利用可能 |
| `.github/copilot-instructions.md` | プロジェクト | GitHub Copilot専用 |
| `.github/instructions/*.instructions.md` | プロジェクト | 細分化された、トピック別の指示 |
| `~/.copilot/instructions/**/*.instructions.md` | ユーザー（すべてのプロジェクト） | すべてのリポジトリに適用される個人用指示 |
| `CLAUDE.md`、`GEMINI.md` | プロジェクトのルート | 互換性のためにサポート |

> 🎯 **まず始めるなら**：プロジェクトの指示には`AGENTS.md`を使いましょう。他の形式は、必要に応じてあとで確認できます。

### AGENTS.md

`AGENTS.md`は推奨される形式です。Copilotや他のAIコーディングツールで使える[オープン標準](https://agents.md/)です。リポジトリのルートに置くと、Copilotが自動で読み込みます。このプロジェクトの[AGENTS.md](../AGENTS.md)は実際に使える例です。

一般的な`AGENTS.md`には、プロジェクトのコンテキスト、コードスタイル、セキュリティ要件、テスト規約などを記述します。サンプルファイルのパターンを参考に、自分のファイルを書いてみましょう。

### カスタム指示ファイル（.instructions.md）

より細かく管理したいチームでは、指示をトピック別のファイルに分割できます。各ファイルは1つの項目を扱い、自動的に適用されます。

```
.github/
└── instructions/
    ├── python-standards.instructions.md
    ├── security-checklist.instructions.md
    └── api-design.instructions.md
```

> 💡 **注**：指示ファイルはどの言語にも使えます。この例ではコースのプロジェクトに合わせてPythonを使っていますが、チームで使うTypeScript、Go、Rustなどの技術向けにも同様のファイルを作成できます。

#### `applyTo`で指示の適用範囲を指定する

既定では、指示ファイルはすべての会話に適用されます。特定のファイル形式に限定するには、ファイル先頭のYAMLフロントマター（`---`で囲まれたブロック）に`applyTo`フィールドを追加します。

```markdown
---
applyTo: "**/*.py"
---
# Pythonの規約
常にPEP 8のスタイル規約に従ってください。
すべての関数シグネチャに型ヒントを使ってください。
```

`applyTo: "**/*.py"`を設定すると、Pythonファイルを扱うときだけCopilotがその指示ファイルを読み込みます。Pythonのスタイルに関する指示が、DockerfileやSQLクエリについての会話に混ざることはありません。

よく使われるパターンをいくつか紹介します。

| `applyTo`の値 | 適用される対象 |
|---|---|
| `"**/*.py"` | すべてのPythonファイル |
| `"**/*.{ts,tsx}"` | TypeScriptとTSXのファイル |
| `"tests/**"` | `tests/`フォルダー内のすべてのファイル |
| （フロントマターなし） | 既定の設定。すべての会話に適用 |

> 💡 **ヒント**：すべてのOSやシェルで正しく解釈されるように、globパターンは引用符で囲みましょう（例：`"**/*.py"`）。

#### `@`で他のファイルを読み込む

`@filepath`構文を使うと、`AGENTS.md`や任意の指示ファイルから別のファイルを参照できます。Copilotが参照先を展開し、その内容を自動的に取り込むため、詳細を別の場所に保存してメインのファイルを短く保てます。

```markdown
<!-- AGENTS.md -->
# プロジェクトの指示

@.github/instructions/python-standards.instructions.md
@.github/instructions/test-standards.instructions.md
```

指示が長くなったときに便利です。内容ごとにファイルを分け、1つの`AGENTS.md`から`@`で読み込みましょう。同じ構文は`.github/copilot-instructions.md`や他の指示ファイル内でも使えます。

> 💡 **ヒント**：`@`による読み込みを使うと、共通の基本ファイルを複数の指示ファイルで共有できます。たとえば、他のすべての指示ファイルから読み込む`@.github/instructions/shared-rules.md`を用意できます。

**コミュニティの指示ファイルを探す**：[github/awesome-copilot](https://github.com/github/awesome-copilot)には、.NET、Angular、Azure、Python、Dockerなど、さまざまな技術向けの指示ファイルがあります。

### カスタム指示を無効にする

プロジェクト固有の設定をすべて無視してCopilotを動かしたい場合（デバッグや動作の比較に便利です）は、次のコマンドを使います。

```bash
copilot --no-custom-instructions
```

</details>

---

<a id="agent-file-reference"></a>
<details>
<summary><strong>エージェントファイルのリファレンス</strong> - YAMLプロパティ、ツールの別名、完全な例</summary>

## エージェントファイルのリファレンス

### より詳細な例

上の[エージェントの最小構成](#add-your-agents)を確認しました。ここでは`tools`プロパティを使った、より詳しいエージェントを紹介します。`~/.copilot/agents/python-reviewer.agent.md`を作成します。

```markdown
---
name: python-reviewer
description: Pythonプロジェクトをレビューするコード品質の専門家
tools: ["read", "edit", "search", "execute"]
---

# Pythonコードレビュー担当

あなたはコード品質とベストプラクティスに注力するPythonの専門家です。

**重点分野：**
- コード品質（PEP 8、型ヒント、docstring）
- パフォーマンスの最適化（リスト内包表記、ジェネレーター）
- エラーハンドリング（適切な例外処理）
- 保守性（DRY原則、分かりやすい命名）

**コードスタイルの要件：**
- Python 3.10以降の機能（dataclass、型ヒント、パターンマッチング）を使う
- PEP 8の命名規則に従う
- ファイル入出力にはコンテキストマネージャーを使う
- すべての関数に型ヒントとdocstringを付ける

**コードレビューでは、必ず次の点を確認してください。**
- 関数シグネチャの型ヒント不足
- ミュータブルなデフォルト引数
- 適切なエラーハンドリング（裸のexceptを使わない）
- 入力検証の網羅性
```

### YAMLプロパティ

| プロパティ | 必須 | 説明 |
|----------|----------|-------------|
| `name` | いいえ | 表示名（既定値はファイル名） |
| `description` | **はい** | エージェントの役割。Copilotが提案するタイミングを判断するために使う |
| `tools` | いいえ | 使用を許可するツールの一覧（省略するとすべてのツールが利用可能）。下記のツール別名を参照 |
| `target` | いいえ | `vscode`または`github-copilot`のみに限定する |

### ツールの別名

`tools`リストでは、次の名前を使います。
- `read` - ファイルの内容を読み取る
- `edit` - ファイルを編集する
- `search` - ファイルを検索する（grep／glob）
- `execute` - シェルコマンドを実行する（別名：`shell`、`Bash`）
- `agent` - 他のカスタムエージェントを呼び出す

> 📖 **公式ドキュメント**：[カスタムエージェントの設定](https://docs.github.com/copilot/reference/custom-agents-configuration)
>
> ⚠️ **VS Codeのみ**：AIモデルを選択する`model`プロパティはVS Codeでは使えますが、GitHub Copilot CLIではサポートされていません。複数のプラットフォームで使うエージェントファイルに含めても問題ありません。GitHub Copilot CLIでは無視されます。

### エージェントのテンプレート

> 💡 **初心者向けの注**：以下の例はテンプレートです。**具体的な技術名は、プロジェクトで使っているものに置き換えてください。** 大切なのはエージェントの*構成*であり、例に記載されている技術そのものではありません。

このプロジェクトの[.github/agents/](../.github/agents/)フォルダーには、実際に使える例があります。
- [hello-world.agent.md](../.github/agents/hello-world.agent.md) - 最小限の例。ここから始めましょう
- [python-reviewer.agent.md](../.github/agents/python-reviewer.agent.md) - Pythonコード品質レビュー担当
- [pytest-helper.agent.md](../.github/agents/pytest-helper.agent.md) - pytestテストの専門家

コミュニティのエージェントについては、[github/awesome-copilot](https://github.com/github/awesome-copilot)を参照してください。

</details>

---

# 実践

<img src="../assets/practice.png" alt="コードを表示するモニター、ランプ、コーヒーカップ、ヘッドホンを備えた、実習にぴったりの温かみのあるデスク" width="800"/>

自分のエージェントを作成し、実際に使ってみましょう。

---

## ▶️ 試してみましょう

```bash

# エージェント用のディレクトリを作成する（まだない場合）
mkdir -p .github/agents

# コードレビューエージェントを作成する
cat > .github/agents/reviewer.agent.md << 'EOF'
---
name: reviewer
description: セキュリティとベストプラクティスに注力するシニアコードレビュー担当
---

# コードレビューエージェント

あなたはコード品質に注力するシニアコードレビュー担当です。

**レビューの優先事項：**
1. セキュリティ上の脆弱性
2. パフォーマンスの問題
3. 保守性に関する懸念
4. ベストプラクティスへの違反

**出力形式：**
問題を深刻度タグ付きの番号付きリストで示してください。
[CRITICAL], [HIGH], [MEDIUM], [LOW]
EOF

# ドキュメント作成エージェントを作成する
cat > .github/agents/documentor.agent.md << 'EOF'
---
name: documentor
description: 明確で完全なドキュメントを作成するテクニカルライター
---

# ドキュメント作成エージェント

あなたは分かりやすいドキュメントを作成するテクニカルライターです。

**ドキュメントの規約：**
- 1文の要約から始める
- 使用例を含める
- パラメーターと戻り値を説明する
- 注意点や制限事項を記載する
EOF

# 作成したエージェントを使う
copilot --agent=reviewer
> @samples/book-app-project/books.py をレビューする

# またはエージェントを切り替える
copilot
> /agent
# 「documentor」を選択
> @samples/book-app-project/books.py のドキュメントを作成する
```

---

## 📝 課題

### メイン課題：専門エージェントチームを作る

実習では`reviewer`と`documentor`エージェントを作成しました。次は別のタスク、つまり書籍アプリのデータ検証を改善するためのエージェントを作成して使ってみましょう。

1. 書籍アプリに合わせたエージェントファイル（`.agent.md`）を3つ作成し、`.github/agents/`に配置します（エージェントごとに1ファイル）。
2. 次のエージェントを作成します。
   - **data-validator**：`data.json`に欠落または不正なデータ（空の著者名、year=0、フィールド不足）がないか確認する
   - **error-handler**：Pythonコードのエラーハンドリングに一貫性があるか確認し、統一した方法を提案する
   - **doc-writer**：docstringやREADMEの内容を生成または更新する
3. 書籍アプリで各エージェントを使います。
   - `data-validator` → `@samples/book-app-project/data.json`を監査する
   - `error-handler` → `@samples/book-app-project/books.py`と`@samples/book-app-project/utils.py`をレビューする
   - `doc-writer` → `@samples/book-app-project/books.py`にdocstringを追加する
4. 連携させます：`error-handler`でエラーハンドリングの不足を見つけてから、`doc-writer`で改善後の方法を文書化します。

**達成基準**：一貫性のある質の高い結果を出すエージェントを3つ作成し、`/agent`で切り替えられること。

<details>
<summary>💡 ヒント（クリックして展開）</summary>

**スターターテンプレート**：`.github/agents/`にエージェントごとのファイルを作成します。

`data-validator.agent.md`:
```markdown
---
description: JSONデータファイルに欠落または不正な項目がないか分析する
---

あなたはJSONデータファイルに欠落または不正な項目がないか分析します。

**重点項目：**
- 空または欠落しているauthorフィールド
- 不正な年（year=0、未来の年、負の年）
- 必須フィールド（title、author、year、read）の不足
- 重複した項目
```

`error-handler.agent.md`:
```markdown
---
description: Pythonコードのエラーハンドリングに一貫性があるかレビューする
---

あなたはPythonコードのエラーハンドリングに一貫性があるかレビューします。

**規約：**
- 裸のexcept節を使わない
- 適切な場合はカスタム例外を使う
- すべてのファイル操作でコンテキストマネージャーを使う
- 成功時と失敗時の戻り値の型を統一する
```

`doc-writer.agent.md`:
```markdown
---
description: 分かりやすいPythonドキュメントを作成するテクニカルライター
---

あなたは分かりやすいPythonドキュメントを作成するテクニカルライターです。

**規約：**
- Google形式のdocstringを使う
- パラメーターの型と戻り値を記載する
- 公開メソッドには使用例を追加する
- 発生する例外を記載する
```

**エージェントをテストする：**

> 💡 **注**：このリポジトリのローカルコピーには、`samples/book-app-project/data.json`がすでに含まれているはずです。見つからない場合は、ソースリポジトリから元のファイルをダウンロードしてください。
> [data.json](https://github.com/github/copilot-cli-for-beginners/blob/main/samples/book-app-project/data.json)

```bash
copilot
> /agent
# 一覧から「data-validator」を選択
> @samples/book-app-project/data.json 著者名が空の本や、不正な出版年が設定された本がないか確認してください
```

**ヒント**：エージェントを動作させるには、YAMLフロントマターの`description`フィールドが必要です。

</details>

### ボーナス課題：指示ライブラリ

必要なときに呼び出すエージェントを作成しました。次はもう一方、`/agent`を使わずにCopilotが毎回のセッションで自動的に読み込む**指示ファイル**に挑戦しましょう。

`.github/instructions/`フォルダーを作成し、次のような指示ファイルを3つ以上用意します。
- `python-style.instructions.md`：PEP 8と型ヒントの規約を徹底する
- `test-standards.instructions.md`：テストファイルでpytestの規約を徹底する
- `data-quality.instructions.md`：JSONデータの項目を検証する

書籍アプリのコードで各指示ファイルを試しましょう。

---

<details>
<summary>🔧 <strong>よくある間違いとトラブルシューティング</strong>（クリックして展開）</summary>

### よくある間違い

| 間違い | 起きること | 対処方法 |
|---------|--------------|-----|
| エージェントのフロントマターに`description`がない | エージェントが読み込まれない、または一覧に表示されない | YAMLフロントマターに必ず`description:`を含める |
| エージェントファイルの配置場所が違う | エージェントを使おうとしても見つからない | 個人用は`~/.copilot/agents/`、プロジェクト用は`.github/agents/`に配置する |
| `.agent.md`ではなく`.md`を使っている | エージェントファイルとして認識されない場合がある | `python-reviewer.agent.md`のような名前にする |
| エージェントのプロンプトが長すぎる | 30,000文字の上限に達する場合がある | エージェントの定義を簡潔に保ち、詳細な指示にはスキルを使う |

### トラブルシューティング

**エージェントが見つからない** - エージェントファイルが次のいずれかの場所にあるか確認してください。
- `~/.copilot/agents/`
- `.github/agents/`

利用可能なエージェントを一覧表示します。

```bash
copilot
> /agent
# 利用可能なエージェントをすべて表示する
```

**エージェントが指示に従わない** - プロンプトを具体的にし、エージェントの定義に次の詳細を追加してください。
- バージョンを含む具体的なフレームワークやライブラリ
- チームの規約
- コードパターンの例

**カスタム指示が読み込まれない** - プロジェクトで`/init`を実行し、プロジェクト固有の指示を設定してください。

```bash
copilot
> /init
```

または、カスタム指示が無効になっていないか確認してください。
```bash
# 指示を読み込む場合は、--no-custom-instructionsを使わない
copilot  # カスタム指示は既定で読み込まれる
```

</details>

---

# まとめ

## 🔑 要点

1. **組み込みエージェント**：`/plan`と`/review`は直接呼び出し、ExploreとTaskは自動で動作する
2. **カスタムエージェント**は`.agent.md`ファイルで定義する専門家
3. **優れたエージェント**には、明確な専門分野、規約、出力形式がある
4. **複数エージェントの連携**では、専門知識を組み合わせて複雑な問題を解決する
5. **指示ファイル**（`.instructions.md`）には、チームの規約を記述して自動的に適用する
6. **一貫した出力**は、明確に定義されたエージェントの指示から生まれる

> 📋 **クイックリファレンス**：[GitHub Copilot CLIコマンドリファレンス](https://docs.github.com/en/copilot/reference/cli-command-reference)で、コマンドとショートカットの一覧を確認できます。

---

## ➡️ 次の章

エージェントは、Copilotがコードに*どのように取り組み、狙いを定めて行動するか*を変えます。次は、Copilotが*どの手順に従うか*を変える**スキル**について学びます。エージェントとスキルの違いが気になりますか？第05章で詳しく説明します。

**[第05章：スキルシステム](../05-skills/README.md)**では、次の内容を学びます。

- プロンプトからスキルを自動的に起動する方法（スラッシュコマンドは不要）
- コミュニティのスキルをインストールする方法
- SKILL.mdファイルを使ってカスタムスキルを作る方法
- エージェント、スキル、MCPの違い
- それぞれを使い分ける場面

---

**[← 第03章に戻る](../03-development-workflows/README.md)** | **[第05章に進む →](../05-skills/README.md)**
