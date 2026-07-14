# Python Clean Architecture - 構成ガイド（テンプレート）

Python + FastAPI によるクリーンアーキテクチャの構成規約テンプレート。
`{Entity}` / `{entity}` を実際のエンティティ名に置き換えて使用する。

---

## ディレクトリ構成

```
app/
├── main.py                              # FastAPI エントリポイント・ルーティング
├── factory/
│   └── {entity}.py                      # 依存性注入ファクトリ（クラスベース）
├── domain/
│   └── {entity}.py                      # ドメインエンティティ
├── presentation/
│   ├── controller/
│   │   └── {entity}.py                  # コントローラ実装
│   └── dto/
│       └── {entity}.py                  # リクエスト/レスポンスDTO（Pydantic）
├── interface/
│   ├── controller/
│   │   └── {entity}.py                  # コントローラ抽象インターフェース
│   ├── usecase/
│   │   └── {entity}.py                  # ユースケース抽象インターフェース
│   └── repository/
│       └── {entity}.py                  # リポジトリ抽象インターフェース
├── application/
│   └── interactor/
│       └── {entity}.py                  # ユースケース実装（ビジネスロジック）
└── infrastructure/
    ├── dao/
    │   └── {entity}.py                  # データアクセスオブジェクト
    └── repository/
        └── {entity}.py                  # データアクセス実装
tests/
└── unit/
    ├── test_create_{entity}_validation.py
    ├── test_{entity}_controller.py
    ├── test_{entity}_interactor.py
    └── test_{entity}_repository.py
```

---

## 層の責務

### domain（ドメイン層）
- ビジネスエンティティを定義する
- 他の層に依存しない。依存方向はすべてドメイン層に向かう
- `@dataclass` でエンティティを定義する。外部ライブラリに依存しない

```python
# domain/{entity}.py
from dataclasses import dataclass


@dataclass
class {Entity}Entity:
    name: str
```

### interface（インターフェース層）
- 各層の抽象契約を定義する
- `abc.ABC` + `@abstractmethod` を使用する
- `__init__` は `@abstractmethod` にしない
- ユースケース抽象は `I{Entity}Usecase`、実装は `{Entity}Interactor`（DECISIONS.md 参照）

```python
# interface/usecase/{entity}.py
from abc import ABC, abstractmethod

from domain.{entity} import {Entity}Entity


class I{Entity}Usecase(ABC):
    @abstractmethod
    def create_{entity}(self, name: str) -> {Entity}Entity:
        pass
```

```python
# interface/repository/{entity}.py
from abc import ABC, abstractmethod
from domain.{entity} import {Entity}Entity


class I{Entity}Repository(ABC):
    @abstractmethod
    def create_{entity}(self, name: str) -> {Entity}Entity:
        pass
```

```python
# interface/controller/{entity}.py
from abc import ABC, abstractmethod

from presentation.dto.{entity} import Create{Entity}Request, Create{Entity}Response


class I{Entity}Controller(ABC):
    @abstractmethod
    def create_{entity}(self, request: Create{Entity}Request) -> Create{Entity}Response:
        pass
```

### application（アプリケーション層）
- `interactor/` ディレクトリにユースケースを実装する
- ユースケース抽象（`I{Entity}Usecase`）を必ず継承する
- リポジトリ抽象を注入され、ドメインエンティティでビジネスルールを実行する

```python
# application/interactor/{entity}.py
from interface.usecase.{entity} import I{Entity}Usecase
from interface.repository.{entity} import I{Entity}Repository
from domain.{entity} import {Entity}Entity


class {Entity}Interactor(I{Entity}Usecase):
    def __init__(self, repo: I{Entity}Repository) -> None:
        self.repo = repo

    def create_{entity}(self, name: str) -> {Entity}Entity:
        return self.repo.create_{entity}(name)
```

### presentation（プレゼンテーション層）
- `dto/` にリクエスト/レスポンスDTOを Pydantic で定義する
- **Pydantic バリデーションはこの層に閉じる**。domain / application に持ち込まない
- `controller/` にコントローラを実装し、対応するインターフェースを必ず継承する
- コントローラはDTOとドメインエンティティの変換に徹する

```python
# presentation/dto/{entity}.py
from pydantic import BaseModel, Field


class Create{Entity}Request(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)


class Create{Entity}Response(BaseModel):
    name: str
```

```python
# presentation/controller/{entity}.py
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

### infrastructure（インフラ層）
- `repository/` にデータアクセスを実装する
- `dao/` に外部データのアクセスオブジェクトを定義する
- DAOはインフラ層内部に留め、ドメインエンティティに変換してから返す

```python
# infrastructure/dao/{entity}.py
from dataclasses import dataclass


@dataclass
class {Entity}Dao:
    name: str
```

```python
# infrastructure/repository/{entity}.py
from domain.{entity} import {Entity}Entity
from interface.repository.{entity} import I{Entity}Repository
from infrastructure.dao.{entity} import {Entity}Dao


class {Entity}Repository(I{Entity}Repository):
    def create_{entity}(self, name: str) -> {Entity}Entity:
        # TODO: 実際のDB保存処理に置き換える
        dao = {Entity}Dao(name=name)
        return {Entity}Entity(name=dao.name)
```

### factory（依存性注入）
- エンティティ単位でファクトリクラスを定義する
- `@staticmethod` で依存チェーンを組み立てる
- 戻り値の型はインターフェース（抽象）で宣言する

```python
# factory/{entity}.py
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

### main.py（エントリポイント）
- FastAPI のルーティングのみを記述する
- エンドポイント関数名は重複させない
- ファクトリクラスを呼び出す

```python
from fastapi import FastAPI
from factory.{entity} import {Entity}Factory
from presentation.dto.{entity} import Create{Entity}Request

app = FastAPI()

@app.post("/{entity}")
def create_{entity}(request: Create{Entity}Request):
    return {Entity}Factory.controller().create_{entity}(request)
```

---

## データフロー

```
HTTP Request
    ↓
main.py（ルーティング・DTOで受け取る）
    ↓
factory（依存性の組み立て）
    ↓
{Entity}Controller（presentation/controller）  ← DTO ⇔ エンティティ変換
    ↓
{Entity}Interactor（application/interactor）
    ↓
{Entity}Repository（infrastructure/repository）
    ↓
{Entity}Dao（infrastructure/dao）  ← 外部データをDAOで受け取る
    ↓
{Entity}Entity（domain/{entity}.py） ← ドメインエンティティに変換
    ↑ 以降はドメインエンティティを上位層へ伝播し、最後にDTOへ変換して返す
```

---

## テスト

- `tests/unit/` に層ごとにファイルを分ける
- 上位層のテストでは抽象を継承した Fake を注入する（モックライブラリは使わない）

```python
class Fake{Entity}Repository(I{Entity}Repository):
    def create_{entity}(self, name: str) -> {Entity}Entity:
        return {Entity}Entity(name=name)
```

```bash
cd app && python -m pytest ../tests/ -v
```

---

## 命名規則

| 種別 | 規則 | 例 |
|---|---|---|
| エンティティ | PascalCase | `{Entity}Entity` |
| インターフェース | `I*` プレフィックス | `I{Entity}Controller` |
| ユースケース抽象 | `I*Usecase` | `I{Entity}Usecase` |
| ユースケース実装 | `*Interactor` | `{Entity}Interactor` |
| DAO | `*Dao` サフィックス | `{Entity}Dao` |
| DTO | `*Request` / `*Response` | `Create{Entity}Request` |
| ファクトリ | `*Factory` サフィックス + `@staticmethod` | `{Entity}Factory.controller()` |

---

## 依存方向の原則

- 依存は常に内側（ドメイン層）へ向かう
- `infrastructure` → `domain` は許可
- `domain` → `infrastructure` は禁止
- Pydantic への依存は `presentation/dto/` に閉じる
- インターフェースを介することで上位層が下位層の実装に依存しない

---

## 使い方

`{Entity}` と `{entity}` を実際のエンティティ名に一括置換してください。

| プレースホルダー | 説明 | 例 |
|---|---|---|
| `{entity}` | エンティティ名（小文字） | `user`, `order`, `product` |
| `{Entity}` | エンティティ名（PascalCase） | `User`, `Order`, `Product` |
