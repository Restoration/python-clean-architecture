# docs

## SKILL_TEMPLATE.md

Python + FastAPI クリーンアーキテクチャの構成規約テンプレート。
新しいエンティティを追加する際のスキャフォールディングガイドとして使用する。

### 使い方

1. `SKILL_TEMPLATE.md` をコピーしてプロジェクトの `SKILL.md` として配置する
2. `{Entity}` を PascalCase のエンティティ名に一括置換する（例: `User`, `Order`）
3. `{entity}` を小文字のエンティティ名に一括置換する（例: `user`, `order`）
4. 各層のコード例を実際のビジネスロジックに合わせて修正する

```bash
# 例: Order エンティティ用の SKILL.md を生成
sed -e 's/{Entity}/Order/g' -e 's/{entity}/order/g' docs/SKILL_TEMPLATE.md > SKILL.md
```

### テンプレートの構成

| セクション | 内容 |
|---|---|
| ディレクトリ構成 | 各層のファイル配置 |
| 層の責務 | domain / interface / application / presentation / infrastructure / factory 各層の役割とコード例 |
| データフロー | HTTP リクエストからレスポンスまでの流れ |
| 命名規則 | エンティティ・インターフェース・DTO・ファクトリの命名パターン |
| 依存方向の原則 | クリーンアーキテクチャの依存ルール |

### Claude Code での活用

プロジェクトルートに `SKILL.md` として配置すると、Claude Code がこの規約に従ってコードを生成する。

```bash
# スラッシュコマンドとして登録する場合
cp docs/SKILL_TEMPLATE.md .claude/commands/python-clean-arch.md
```
