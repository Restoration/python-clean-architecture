# Python Clean Architecture - 構成ガイド

Python + FastAPI によるクリーンアーキテクチャの構成規約をまとめたドキュメント。

---

## ディレクトリ構成

```
app/
├── main.py                              # FastAPI エントリポイント・ルーティング
├── factory/
│   └── user.py                          # 依存性注入ファクトリ（クラスベース）
├── domain/
│   └── user/
│       └── entity.py                    # ドメインエンティティ
├── presentation/
│   └── controller/
│       └── user.py                      # HTTPハンドラー実装
├── interface/
│   ├── controller/
│   │   └── user.py                      # ハンドラー抽象インターフェース
│   ├── usecase/
│   │   └── user.py                      # ユースケース抽象インターフェース
│   └── repository/
│       └── user.py                      # リポジトリ抽象インターフェース
├── application/
│   └── interactor/
│       └── user.py                      # ビジネスロジック実装
└── infrastructure/
    ├── dto/
    │   └── user.py                      # データ転送オブジェクト
    └── repository/
        └── user.py                      # データアクセス実装
```

---

## 層の責務

### domain（ドメイン層）
- ビジネスエンティティを定義する
- 他の層に依存しない。依存方向はすべてドメイン層に向かう
- `@dataclass` でエンティティを定義する

```python
# domain/user/entity.py
from dataclasses import dataclass

@dataclass
class User:
    message: str
```

### interface（インターフェース層）
- 各層の抽象契約を定義する
- `abc.ABC` + `@abstractmethod` を使用する
- `__init__` は `@abstractmethod` にしない
- ハンドラーインターフェースは `domain` や `infrastructure` に依存しない

```python
# interface/controller/user.py
from abc import ABC, abstractmethod
from typing import Dict

class IUserController(ABC):
    @abstractmethod
    def hello_world(self) -> Dict[str, str]:
        pass
```

```python
# interface/usecase/user.py
from abc import ABC, abstractmethod

class IUserInteractor(ABC):
    @abstractmethod
    def hello_world(self) -> str:
        pass
```

```python
# interface/repository/user.py
from abc import ABC, abstractmethod
from domain.user.entity import User

class IUserRepository(ABC):
    @abstractmethod
    def request(self) -> User:
        pass
```

### application（アプリケーション層）
- `interactor/` ディレクトリにユースケースを実装する
- 対応するインターフェースを必ず継承する
- ドメインエンティティを受け取り、ビジネスルールを実行する

```python
# application/interactor/user.py
from interface.usecase.user import IUserInteractor
from interface.repository.user import IUserRepository

class UserInteractor(IUserInteractor):
    def __init__(self, repo: IUserRepository) -> None:
        self.repo = repo

    def hello_world(self) -> str:
        user = self.repo.request()
        return user.message
```

### presentation（プレゼンテーション層）
- HTTPハンドラーを実装する
- 対応するインターフェースを必ず継承する
- ユースケースインターフェースを受け取り、レスポンスを返す

```python
# presentation/controller/user.py
from typing import Dict
from interface.controller.user import IUserController
from interface.usecase.user import IUserInteractor

class UserController(IUserController):
    def __init__(self, usecase: IUserInteractor) -> None:
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
# infrastructure/dto/user.py
from dataclasses import dataclass

@dataclass
class UserDto:
    message: str
```

```python
# infrastructure/repository/user.py
from domain.user.entity import User
from interface.repository.user import IUserRepository
from infrastructure.dto.user import UserDto

class UserRepository(IUserRepository):
    def request(self) -> User:
        dto = UserDto(message="hello world")
        return User(message=dto.message)
```

### factory（依存性注入）
- エンティティ単位でファクトリクラスを定義する
- `@staticmethod` で依存チェーンを組み立てる

```python
# factory/user.py
from presentation.controller.user import UserController
from application.interactor.user import UserInteractor
from infrastructure.repository.user import UserRepository


class UserFactory:
    @staticmethod
    def controller():
        return UserController(UserFactory.usecase())

    @staticmethod
    def usecase():
        return UserInteractor(UserFactory.repository())

    @staticmethod
    def repository():
        return UserRepository()
```

### main.py（エントリポイント）
- FastAPI のルーティングのみを記述する
- エンドポイント関数名は重複させない
- ファクトリクラスを呼び出す

```python
from fastapi import FastAPI
from factory.user import UserFactory

app = FastAPI()

@app.get("/healthcheck")
def healthcheck():
    return {}

@app.get("/user/hello_world")
def hello_world():
    return UserFactory.controller().hello_world()
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
UserController（presentation）
    ↓
UserInteractor（application/interactor）
    ↓
UserRepository（infrastructure/repository）
    ↓
UserDto（infrastructure/dto）  ← 外部データをDTOで受け取る
    ↓
User（domain/entity）          ← ドメインエンティティに変換
    ↑ 以降はドメインエンティティを上位層へ伝播
```

---

## 命名規則

| 種別 | 規則 | 例 |
|---|---|---|
| エンティティ | PascalCase | `User` |
| インターフェース | `I*` プレフィックス | `IUserController` |
| DTO | `*Dto` サフィックス | `UserDto` |
| ファクトリ | `*Factory` サフィックス + `@staticmethod` | `UserFactory.controller()` |
| インタラクター | ユースケース名をそのまま使用 | `UserInteractor` |

---

## 依存方向の原則

- 依存は常に内側（ドメイン層）へ向かう
- `infrastructure` → `domain` は許可
- `domain` → `infrastructure` は禁止
- インターフェースを介することで上位層が下位層の実装に依存しない
