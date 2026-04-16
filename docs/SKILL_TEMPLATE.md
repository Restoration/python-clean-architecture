# {Language} Clean Architecture - 構成ガイド

{Language} + {Framework} によるクリーンアーキテクチャの構成規約をまとめたドキュメント。

---

## ディレクトリ構成

```
{root}/
├── main.{ext}                              # エントリポイント・ルーティング
├── factory/
│   └── {entity}.{ext}                      # 依存性注入ファクトリ
├── domain/
│   └── {entity}.{ext}                      # ドメインエンティティ
├── presentation/
│   └── controller/
│       └── {entity}.{ext}                  # HTTPハンドラー実装
├── interface/
│   ├── controller/
│   │   └── {entity}.{ext}                  # ハンドラー抽象インターフェース
│   ├── usecase/
│   │   └── {entity}.{ext}                  # ユースケース抽象インターフェース
│   └── repository/
│       └── {entity}.{ext}                  # リポジトリ抽象インターフェース
├── application/
│   └── interactor/
│       └── {entity}.{ext}                  # ビジネスロジック実装
└── infrastructure/
    ├── dto/
    │   └── {entity}.{ext}                  # データ転送オブジェクト
    └── repository/
        └── {entity}.{ext}                  # データアクセス実装
```

---

## 層の責務

### domain（ドメイン層）
- ビジネスエンティティを定義する
- 他の層に依存しない。依存方向はすべてドメイン層に向かう

### interface（インターフェース層）
- 各層の抽象契約を定義する
- 抽象クラス/インターフェースを使用する
- ハンドラーインターフェースは `domain` や `infrastructure` に依存しない

### application（アプリケーション層）
- `interactor/` ディレクトリにユースケースを実装する
- 対応するインターフェースを必ず継承する
- ドメインエンティティを受け取り、ビジネスルールを実行する

### presentation（プレゼンテーション層）
- HTTPハンドラーを実装する
- 対応するインターフェースを必ず継承する
- ユースケースインターフェースを受け取り、レスポンスを返す

### infrastructure（インフラ層）
- `repository/` にデータアクセスを実装する
- `dto/` に外部データの転送オブジェクトを定義する
- DTOはインフラ層内部に留め、ドメインエンティティに変換してから返す

### factory（依存性注入）
- エンティティ単位でファクトリクラス/関数を定義する
- 依存チェーンを組み立てる

### エントリポイント
- ルーティングのみを記述する
- エンドポイント関数名は重複させない
- ファクトリを呼び出す

---

## データフロー

```
HTTP Request
    ↓
エントリポイント（ルーティング）
    ↓
factory（依存性の組み立て）
    ↓
Controller（presentation）
    ↓
Interactor（application/interactor）
    ↓
Repository（infrastructure/repository）
    ↓
DTO（infrastructure/dto）  ← 外部データをDTOで受け取る
    ↓
Entity（domain）            ← ドメインエンティティに変換
    ↑ 以降はドメインエンティティを上位層へ伝播
```

---

## 命名規則

| 種別 | 規則 | 例 |
|---|---|---|
| エンティティ | PascalCase | `{Entity}` |
| インターフェース | `I*` プレフィックス | `I{Entity}Controller` |
| DTO | `*Dto` サフィックス | `{Entity}Dto` |
| ファクトリ | `*Factory` サフィックス | `{Entity}Factory` |
| インタラクター | ユースケース名をそのまま使用 | `{Entity}Interactor` |

---

## 依存方向の原則

- 依存は常に内側（ドメイン層）へ向かう
- `infrastructure` → `domain` は許可
- `domain` → `infrastructure` は禁止
- インターフェースを介することで上位層が下位層の実装に依存しない

---

## カスタマイズガイド

このテンプレートを使用する際、以下のプレースホルダーを置き換えてください：

| プレースホルダー | 説明 | 例 |
|---|---|---|
| `{Language}` | プログラミング言語 | Python, Go, TypeScript |
| `{Framework}` | Webフレームワーク | FastAPI, Gin, Express |
| `{root}` | ソースルートディレクトリ | `app/`, `src/`, `internal/` |
| `{ext}` | ファイル拡張子 | `.py`, `.go`, `.ts` |
| `{entity}` | エンティティ名（小文字） | `user`, `order`, `product` |
| `{Entity}` | エンティティ名（PascalCase） | `User`, `Order`, `Product` |

### 言語別の補足

各言語に応じて以下を追記してください：

- **抽象化の方法**: Python は `abc.ABC`、Go は `interface`、TypeScript は `interface`/`abstract class`
- **DI の方法**: コンストラクタインジェクション、フレームワーク固有のDIコンテナなど
- **エンティティ定義**: `@dataclass`、`struct`、`class` など
- **具体的なコード例**: 各層のサンプルコードを言語に合わせて追加
