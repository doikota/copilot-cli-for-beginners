# AGENTS.md

GitHub Copilot CLIを学ぶ、初心者向けのコースです。ソフトウェアではなく、学習用コンテンツです。

## Structure

| パス | 内容 |
|------|---------|
| `00-07/` | 各章：たとえ話 → 概念 → 実践 → 課題 → 次のステップ |
| `samples/book-app-project/` | **メインのサンプル**：全章で使用する、Python製のCLI書籍コレクションアプリ |
| `samples/book-app-project-cs/` | 書籍コレクションアプリのC#版 |
| `samples/book-app-project-js/` | 書籍コレクションアプリのJavaScript版 |
| `samples/book-app-buggy/` | デバッグ演習用の**意図的なバグ**（第03章） |
| `samples/agents/` | Agentテンプレートの例（python-reviewer、pytest-helper、hello-world） |
| `samples/skills/` | Skillテンプレートの例（code-checklist、pytest-gen、commit-message、hello-world） |
| `samples/mcp-configs/` | MCPサーバー設定の例 |
| `samples/buggy-code/` | **追加の任意コンテンツ**：セキュリティに関するバグを含むコード（JavaScriptとPython） |
| `samples/src/` | **追加の任意コンテンツ**：以前のコースで使用していた旧版のJS/Reactサンプル |
| `appendices/` | 補足資料 |

## 守ること

- 初心者にもわかりやすい説明にし、AI/MLの専門用語を使う場合は説明を加える
- bashの例はコピー＆ペーストですぐに実行できるようにする
- 親しみやすく、前向きで、実践的な語り口にする
- 主要な例ではすべて `samples/book-app-project/` のパスを使う
- コード例ではPython/pytestを使う
- コマンドを実行する際は、その直前に必ずコマンドの内容を解説する

## してはいけないこと

- `samples/book-app-buggy/` や `samples/buggy-code/` のバグを修正しない（演習用に意図的に含まれています）
- README.mdのコース一覧を更新せずに章を追加しない
- 読者がAI/MLの専門用語を知っている前提で書かない

## ビルド

```bash
npm install && npm run release
```
