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
│   └── controller/
│       └── {entity}.py                  # HTTPハンドラー実装
├── interface/
│   ├── controller/
│   │   └── {entity}.py                  # ハンドラー抽象インターフェース
│   ├── usecase/
│   │   └── {entity}.py                  # ユースケース抽象インターフェース
│   └── repository/
│       └── {entity}.py                  # リポジトリ抽象インターフェース
├── application/
│   └── interactor/
│       └── {entity}.py                  # ビジネスロジック実装
└── infrastructure/
    ├── dto/
    │   └── {entity}.py                  # データ転送オブジェクト
    └── repository/
        └── {entity}.py                  # データアクセス実装
```

---

## 層の責務

### domain（ドメイン層）
- ビジネスエンティティを定義する
- 他の層に依存しない。依存方向はすべてドメイン層に向かう
- `@dataclass` でエンティティを定義する

```python
# domain/{entity}.py
from dataclasses import dataclass

@dataclass
class {Entity}:
    message: str
```

### interface（インターフェース層）
- 各層の抽象契約を定義する
- `abc.ABC` + `@abstractmethod` を使用する
- `__init__` は `@abstractmethod` にしない
- ハンドラーインターフェースは `domain` や `infrastructure` に依存しない

```python
# interface/controller/{entity}.py
from abc import ABC, abstractmethod
from typing import Dict

class I{Entity}Controller(ABC):
    @abstractmethod
    def hello_world(self) -> Dict[str, str]:
        pass
```

```python
# interface/usecase/{entity}.py
from abc import ABC, abstractmethod

class I{Entity}Interactor(ABC):
    @abstractmethod
    def hello_world(self) -> str:
        pass
```

```python
# interface/repository/{entity}.py
from abc import ABC, abstractmethod
from domain.{entity} import {Entity}

class I{Entity}Repository(ABC):
    @abstractmethod
    def request(self) -> {Entity}:
        pass
```

### application（アプリケーション層）
- `interactor/` ディレクトリにユースケースを実装する
- 対応するインターフェースを必ず継承する
- ドメインエンティティを受け取り、ビジネスルールを実行する

```python
# application/interactor/{entity}.py
from interface.usecase.{entity} import I{Entity}Interactor
from interface.repository.{entity} import I{Entity}Repository

class {Entity}Interactor(I{Entity}Interactor):
    def __init__(self, repo: I{Entity}Repository) -> None:
        self.repo = repo

    def hello_world(self) -> str:
        entity = self.repo.request()
        return entity.message
```

### presentation（プレゼンテーション層）
- HTTPハンドラーを実装する
- 対応するインターフェースを必ず継承する
- ユースケースインターフェースを受け取り、レスポンスを返す

```python
# presentation/controller/{entity}.py
from typing import Dict
from interface.controller.{entity} import I{Entity}Controller
from interface.usecase.{entity} import I{Entity}Interactor

class {Entity}Controller(I{Entity}Controller):
    def __init__(self, usecase: I{Entity}Interactor) -> None:
        self.uc = usecase

    def hello_world(self) -> Dict[str, str]:
        return {
            "say": self.uc.hello_world()
        }
```

### infrastructure（インフラ層）
- `repository/` にデータアクセスを実装する
- `dto/` に外部データの転送オブジェクトを定義する
- DTOはインフラ層内部に留め、ドメインエンティティに変換してから返す

```python
# infrastructure/dto/{entity}.py
from dataclasses import dataclass

@dataclass
class {Entity}Dto:
    message: str
```

```python
# infrastructure/repository/{entity}.py
from domain.{entity} import {Entity}
from interface.repository.{entity} import I{Entity}Repository
from infrastructure.dto.{entity} import {Entity}Dto

class {Entity}Repository(I{Entity}Repository):
    def request(self) -> {Entity}:
        dto = {Entity}Dto(message="hello world")
        return {Entity}(message=dto.message)
```

### factory（依存性注入）
- エンティティ単位でファクトリクラスを定義する
- `@staticmethod` で依存チェーンを組み立てる

```python
# factory/{entity}.py
from presentation.controller.{entity} import {Entity}Controller
from application.interactor.{entity} import {Entity}Interactor
from infrastructure.repository.{entity} import {Entity}Repository


class {Entity}Factory:
    @staticmethod
    def controller():
        return {Entity}Controller({Entity}Factory.usecase())

    @staticmethod
    def usecase():
        return {Entity}Interactor({Entity}Factory.repository())

    @staticmethod
    def repository():
        return {Entity}Repository()
```

### main.py（エントリポイント）
- FastAPI のルーティングのみを記述する
- エンドポイント関数名は重複させない
- ファクトリクラスを呼び出す

```python
from fastapi import FastAPI
from factory.{entity} import {Entity}Factory

app = FastAPI()

@app.get("/healthcheck")
def healthcheck():
    return {}

@app.get("/{entity}/hello_world")
def hello_world():
    return {Entity}Factory.controller().hello_world()
```

---

## データフロー

```
HTTP Request
    ↓
main.py（ルーティング）
    ↓
factory（依存性の組み立て）
    ↓
{Entity}Controller（presentation）
    ↓
{Entity}Interactor（application/interactor）
    ↓
{Entity}Repository（infrastructure/repository）
    ↓
{Entity}Dto（infrastructure/dto）  ← 外部データをDTOで受け取る
    ↓
{Entity}（domain/{entity}.py）      ← ドメインエンティティに変換
    ↑ 以降はドメインエンティティを上位層へ伝播
```

---

## 命名規則

| 種別 | 規則 | 例 |
|---|---|---|
| エンティティ | PascalCase | `{Entity}` |
| インターフェース | `I*` プレフィックス | `I{Entity}Controller` |
| DTO | `*Dto` サフィックス | `{Entity}Dto` |
| ファクトリ | `*Factory` サフィックス + `@staticmethod` | `{Entity}Factory.controller()` |
| インタラクター | ユースケース名をそのまま使用 | `{Entity}Interactor` |

---

## 依存方向の原則

- 依存は常に内側（ドメイン層）へ向かう
- `infrastructure` → `domain` は許可
- `domain` → `infrastructure` は禁止
- インターフェースを介することで上位層が下位層の実装に依存しない

---

## 使い方

`{Entity}` と `{entity}` を実際のエンティティ名に一括置換してください。

| プレースホルダー | 説明 | 例 |
|---|---|---|
| `{entity}` | エンティティ名（小文字） | `user`, `order`, `product` |
| `{Entity}` | エンティティ名（PascalCase） | `User`, `Order`, `Product` |
