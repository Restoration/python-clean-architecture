---
name: add-entity
description: このリポジトリ（Python + FastAPI クリーンアーキテクチャ）に新しいエンティティ／APIリソースを追加するときに使う。全層（domain / interface / application / infrastructure / presentation / factory / main.py / tests）のスキャフォールディング手順と規約を定義する。「エンティティを追加」「〜のAPIを作って」「Order を追加して」などの依頼で必ず読むこと。
---

# エンティティ追加スキル

新しいエンティティ（例: `Order`, `Product`）を追加する際は、以下の順序で **8ファイル + テスト** を作成する。
`{Entity}` = PascalCase（`Order`）、`{entity}` = 小文字（`order`）に読み替える。

## 作成ファイル一覧（作成順）

| # | ファイル | 内容 |
|---|---|---|
| 1 | `app/domain/{entity}.py` | ドメインエンティティ（`@dataclass`） |
| 2 | `app/interface/repository/{entity}.py` | リポジトリ抽象 `I{Entity}Repository` |
| 3 | `app/interface/usecase/{entity}.py` | ユースケース抽象 `I{Entity}Usecase` |
| 4 | `app/interface/controller/{entity}.py` | コントローラ抽象 `I{Entity}Controller` |
| 5 | `app/infrastructure/dao/{entity}.py` | DAO `{Entity}Dao` |
| 6 | `app/infrastructure/repository/{entity}.py` | リポジトリ実装 `{Entity}Repository` |
| 7 | `app/presentation/dto/{entity}.py` | Pydantic DTO（リクエスト/レスポンス） |
| 8 | `app/presentation/controller/{entity}.py` | コントローラ実装 `{Entity}Controller` |
| 9 | `app/application/interactor/{entity}.py` | ユースケース実装 `{Entity}Interactor` |
| 10 | `app/factory/{entity}.py` | DIファクトリ `{Entity}Factory` |
| 11 | `app/main.py` に追記 | ルーティング追加 |
| 12 | `tests/unit/test_{entity}_*.py` | 単体テスト |

## 絶対規約（違反禁止）

- 依存は常に内側（domain）へ向かう。`domain → infrastructure` は禁止
- domain 層は `@dataclass` のみ。Pydantic 等の外部ライブラリを import しない
- Pydantic バリデーションは `presentation/dto/` に閉じる。domain/application に持ち込まない
- DAO は infrastructure 層内部に留め、リポジトリがドメインエンティティに変換してから返す
- 抽象は `abc.ABC` + `@abstractmethod`。`__init__` は `@abstractmethod` にしない
- 命名: 抽象は `I` プレフィックス、ユースケース抽象は `I{Entity}Usecase`、実装は `{Entity}Interactor`（DECISIONS.md 参照）
- main.py のエンドポイント関数名は重複させない

## 各層のテンプレート（現行コード準拠）

### 1. domain

```python
# app/domain/{entity}.py
from dataclasses import dataclass


@dataclass
class {Entity}Entity:
    name: str
```

### 2-4. interface（抽象）

```python
# app/interface/repository/{entity}.py
from abc import ABC, abstractmethod
from domain.{entity} import {Entity}Entity


class I{Entity}Repository(ABC):
    @abstractmethod
    def create_{entity}(self, name: str) -> {Entity}Entity:
        pass
```

```python
# app/interface/usecase/{entity}.py
from abc import ABC, abstractmethod
from domain.{entity} import {Entity}Entity


class I{Entity}Usecase(ABC):
    @abstractmethod
    def create_{entity}(self, name: str) -> {Entity}Entity:
        pass
```

```python
# app/interface/controller/{entity}.py
from abc import ABC, abstractmethod
from presentation.dto.{entity} import Create{Entity}Request, Create{Entity}Response


class I{Entity}Controller(ABC):
    @abstractmethod
    def create_{entity}(self, request: Create{Entity}Request) -> Create{Entity}Response:
        pass
```

### 5-6. infrastructure

```python
# app/infrastructure/dao/{entity}.py
from dataclasses import dataclass


@dataclass
class {Entity}Dao:
    name: str
```

```python
# app/infrastructure/repository/{entity}.py
from domain.{entity} import {Entity}Entity
from interface.repository.{entity} import I{Entity}Repository
from infrastructure.dao.{entity} import {Entity}Dao


class {Entity}Repository(I{Entity}Repository):
    def create_{entity}(self, name: str) -> {Entity}Entity:
        # TODO: 実際のDB保存処理に置き換える
        dao = {Entity}Dao(name=name)
        return {Entity}Entity(name=dao.name)
```

### 7-8. presentation

```python
# app/presentation/dto/{entity}.py
from pydantic import BaseModel, Field


class Create{Entity}Request(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class Create{Entity}Response(BaseModel):
    name: str
```

バリデーション（`Field` 制約、`@field_validator`）はここに集約する。

```python
# app/presentation/controller/{entity}.py
from interface.controller.{entity} import I{Entity}Controller
from interface.usecase.{entity} import I{Entity}Usecase
from presentation.dto.{entity} import Create{Entity}Request, Create{Entity}Response


class {Entity}Controller(I{Entity}Controller):
    def __init__(self, usecase: I{Entity}Usecase) -> None:
        self.uc = usecase

    def create_{entity}(self, request: Create{Entity}Request) -> Create{Entity}Response:
        entity = self.uc.create_{entity}(name=request.name)
        return Create{Entity}Response(name=entity.name)
```

### 9. application

```python
# app/application/interactor/{entity}.py
from interface.usecase.{entity} import I{Entity}Usecase
from interface.repository.{entity} import I{Entity}Repository
from domain.{entity} import {Entity}Entity


class {Entity}Interactor(I{Entity}Usecase):
    def __init__(self, repo: I{Entity}Repository) -> None:
        self.repo = repo

    def create_{entity}(self, name: str) -> {Entity}Entity:
        return self.repo.create_{entity}(name)
```

### 10. factory

```python
# app/factory/{entity}.py
from interface.controller.{entity} import I{Entity}Controller
from interface.usecase.{entity} import I{Entity}Usecase
from interface.repository.{entity} import I{Entity}Repository
from presentation.controller.{entity} import {Entity}Controller
from application.interactor.{entity} import {Entity}Interactor
from infrastructure.repository.{entity} import {Entity}Repository


class {Entity}Factory:
    @staticmethod
    def controller() -> I{Entity}Controller:
        return {Entity}Controller({Entity}Factory.usecase())

    @staticmethod
    def usecase() -> I{Entity}Usecase:
        return {Entity}Interactor({Entity}Factory.repository())

    @staticmethod
    def repository() -> I{Entity}Repository:
        return {Entity}Repository()
```

### 11. main.py（追記）

```python
from factory.{entity} import {Entity}Factory
from presentation.dto.{entity} import Create{Entity}Request

@app.post("/{entity}")
def create_{entity}(request: Create{Entity}Request):
    return {Entity}Factory.controller().create_{entity}(request)
```

## テスト規約

`tests/unit/` に層ごとにファイルを分ける。上位層のテストでは抽象を継承した Fake を注入する（モックライブラリは使わない）。

- `test_create_{entity}_validation.py` — DTO のバリデーション（正常系 + 各制約の境界値）
- `test_{entity}_controller.py` — `Fake{Entity}Usecase` を注入し DTO 変換を検証
- `test_{entity}_interactor.py` — `Fake{Entity}Repository` を注入しロジックを検証
- `test_{entity}_repository.py` — リポジトリ実装がドメインエンティティを返すことを検証

Fake の例:

```python
class Fake{Entity}Repository(I{Entity}Repository):
    def create_{entity}(self, name: str) -> {Entity}Entity:
        return {Entity}Entity(name=name)
```

## 完了時の検証

```bash
cd app && python -m pytest ../tests/ -v
```

全テストが通ることを確認してから完了とする。
