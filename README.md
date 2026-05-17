# Python Clean Architecture

Python, FastAPI構成によるクリーンアーキテクチャの検証リポジトリ。

## ディレクトリ構成

```
app/
├── domain/                  # エンティティ（外部依存なし）
├── application/
│   └── interactor/          # ユースケース実装
├── interface/
│   ├── usecase/             # ユースケースインターフェース
│   ├── repository/          # リポジトリインターフェース
│   └── controller/          # コントローラインターフェース
├── infrastructure/
│   ├── repository/          # リポジトリ実装
│   └── dao/                 # データアクセスオブジェクト
├── presentation/
│   ├── controller/          # コントローラ実装
│   └── dto/                 # リクエスト/レスポンスDTO（Pydantic）
├── factory/                 # DI組み立て
└── main.py                  # FastAPIエントリポイント
tests/
└── unit/                    # ユニットテスト
```

## 依存関係の方向

```
Presentation → Interface ← Application
                  ↑
Infrastructure → Domain
```

- Domain層は外部ライブラリに依存しない（dataclass のみ）
- Pydantic によるバリデーションは Presentation層（DTO）に閉じる

## セットアップ

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 起動

```bash
docker-compose up
```

または直接実行:

```bash
cd app
uvicorn main:app --reload
```

## API エンドポイント

| メソッド | パス | 説明 |
|---|---|---|
| GET | `/healthcheck` | ヘルスチェック |
| GET | `/user/hello_world` | Hello World メッセージ取得 |
| POST | `/user` | ユーザー作成（バリデーション付き） |

### POST /user リクエスト例

```json
{
  "name": "Taro",
  "email": "taro@example.com",
  "age": 25
}
```

バリデーションルール:
- `name`: 1〜100文字、空白のみ不可
- `email`: メールアドレス形式
- `age`: 0〜150 の整数

バリデーションエラー時は 422 レスポンスが返ります。

## テスト

```bash
cd app
python -m pytest ../tests/ -v
```
