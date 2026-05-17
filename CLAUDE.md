# CLAUDE.md

## プロジェクト概要

Python + FastAPI によるクリーンアーキテクチャの検証リポジトリ。

## 技術スタック

- Python 3.9+ / FastAPI / Pydantic / uvicorn
- テスト: pytest
- コンテナ: Docker + docker-compose

## ディレクトリ構成

```
app/
├── domain/              # エンティティ（dataclass、外部依存なし）
├── application/
│   └── interactor/      # ユースケース実装（Interactor）
├── interface/
│   ├── usecase/         # ユースケース抽象（IUserUsecase）
│   ├── repository/      # リポジトリ抽象（IUserRepository）
│   └── controller/      # コントローラ抽象（IUserController）
├── infrastructure/
│   ├── repository/      # リポジトリ実装
│   └── dao/             # データアクセスオブジェクト
├── presentation/
│   ├── controller/      # コントローラ実装
│   └── dto/             # リクエスト/レスポンスDTO（Pydantic）
├── factory/             # DI組み立て（クラスベース + @staticmethod）
└── main.py              # FastAPIエントリポイント・ルーティング
tests/
└── unit/                # ユニットテスト
```

## よく使うコマンド

```bash
# テスト実行
cd app && python -m pytest ../tests/ -v

# 起動（Docker）
docker-compose up

# 起動（直接）
cd app && uvicorn main:app --reload
```

## アーキテクチャ規約

- **依存方向**: 常に内側（Domain層）へ向かう。`domain → infrastructure` は禁止
- **Domain層**: `@dataclass` のみ、外部ライブラリ依存なし
- **Interface層**: `abc.ABC` + `@abstractmethod`。`__init__` は `@abstractmethod` にしない
- **Pydantic バリデーション**: Presentation層（DTO）に閉じる
- **DAO**: Infrastructure層内部に留め、ドメインエンティティに変換してから返す
- **Factory**: エンティティ単位でクラスを定義し `@staticmethod` で依存チェーンを組み立てる

## 命名規則

| 種別 | 規則 | 例 |
|---|---|---|
| エンティティ | PascalCase | `User` |
| インターフェース | `I*` プレフィックス | `IUserController` |
| DAO | `*Dao` サフィックス | `UserDao` |
| ファクトリ | `*Factory` + `@staticmethod` | `UserFactory.controller()` |
| ユースケース実装 | `*Interactor` | `UserInteractor` |

## pytest 設定

- `pythonpath = app`（app/ がインポートルート）
- `testpaths = tests`
