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
│   └── user.py                          # ドメインエンティティ
├── presentation/
│   ├── controller/
│   │   └── user.py                      # コントローラ実装
│   └── dto/
│       └── user.py                      # リクエスト/レスポンスDTO（Pydantic）
├── interface/
│   ├── controller/
│   │   └── user.py                      # コントローラ抽象インターフェース
│   ├── usecase/
│   │   └── user.py                      # ユースケース抽象インターフェース
│   └── repository/
│       └── user.py                      # リポジトリ抽象インターフェース
├── application/
│   └── interactor/
│       └── user.py                      # ユースケース実装（ビジネスロジック）
└── infrastructure/
    ├── dao/
    │   └── user.py                      # データアクセスオブジェクト
    └── repository/
        └── user.py                      # データアクセス実装
tests/
└── unit/                                # ユニットテスト
```

---

## 層の責務

### domain（ドメイン層）
- ビジネスエンティティを定義する
- 他の層に依存しない。依存方向はすべてドメイン層に向かう
- `@dataclass` でエンティティを定義する。外部ライブラリに依存しない

```python
# domain/user.py
from dataclasses import dataclass


@dataclass
class UserEntity:
    name: str
    email: str
    age: int
```

### interface（インターフェース層）
- 各層の抽象契約を定義する
- `abc.ABC` + `@abstractmethod` を使用する
- `__init__` は `@abstractmethod` にしない
- ユースケース抽象は `I*Usecase`、実装は `*Interactor`（DECISIONS.md 参照）

```python
# interface/usecase/user.py
from abc import ABC, abstractmethod

from domain.user import UserEntity


class IUserUsecase(ABC):
    @abstractmethod
    def create_user(self, name: str, email: str, age: int) -> UserEntity:
        pass
```

```python
# interface/repository/user.py
from abc import ABC, abstractmethod
from domain.user import UserEntity


class IUserRepository(ABC):
    @abstractmethod
    def create_user(self, name: str, email: str, age: int) -> UserEntity:
        pass
```

```python
# interface/controller/user.py
from abc import ABC, abstractmethod

from presentation.dto.user import CreateUserRequest, CreateUserResponse


class IUserController(ABC):
    @abstractmethod
    def create_user(self, request: CreateUserRequest) -> CreateUserResponse:
        pass
```

### application（アプリケーション層）
- `interactor/` ディレクトリにユースケースを実装する
- ユースケース抽象（`IUserUsecase`）を必ず継承する
- リポジトリ抽象を注入され、ドメインエンティティでビジネスルールを実行する

```python
# application/interactor/user.py
from interface.usecase.user import IUserUsecase
from interface.repository.user import IUserRepository
from domain.user import UserEntity


class UserInteractor(IUserUsecase):
    def __init__(self, repo: IUserRepository) -> None:
        self.repo = repo

    def create_user(self, name: str, email: str, age: int) -> UserEntity:
        return self.repo.create_user(name, email, age)
```

### presentation（プレゼンテーション層）
- `dto/` にリクエスト/レスポンスDTOを Pydantic で定義する
- **Pydantic バリデーションはこの層に閉じる**。domain / application に持ち込まない
- `controller/` にコントローラを実装し、対応するインターフェースを必ず継承する
- コントローラはDTOとドメインエンティティの変換に徹する

```python
# presentation/dto/user.py
from pydantic import BaseModel, Field, field_validator


class CreateUserRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    age: int = Field(..., ge=0, le=150)

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if v.strip() == "":
            raise ValueError("name must not be blank")
        return v.strip()


class CreateUserResponse(BaseModel):
    name: str
    email: str
    age: int
```

```python
# presentation/controller/user.py
from interface.controller.user import IUserController
from interface.usecase.user import IUserUsecase
from presentation.dto.user import CreateUserRequest, CreateUserResponse


class UserController(IUserController):
    def __init__(self, usecase: IUserUsecase) -> None:
        self.uc = usecase

    def create_user(self, request: CreateUserRequest) -> CreateUserResponse:
        user = self.uc.create_user(
            name=request.name,
            email=request.email,
            age=request.age,
        )
        return CreateUserResponse(
            name=user.name,
            email=user.email,
            age=user.age,
        )
```

### infrastructure（インフラ層）
- `repository/` にデータアクセスを実装する
- `dao/` に外部データのアクセスオブジェクトを定義する
- DAOはインフラ層内部に留め、ドメインエンティティに変換してから返す

```python
# infrastructure/dao/user.py
from dataclasses import dataclass


@dataclass
class UserDao:
    message: str
```

```python
# infrastructure/repository/user.py
from domain.user import UserEntity
from interface.repository.user import IUserRepository


class UserRepository(IUserRepository):
    def create_user(self, name: str, email: str, age: int) -> UserEntity:
        # TODO: 実際のDB保存処理に置き換える
        return UserEntity(name=name, email=email, age=age)
```

### factory（依存性注入）
- エンティティ単位でファクトリクラスを定義する
- `@staticmethod` で依存チェーンを組み立てる
- 戻り値の型はインターフェース（抽象）で宣言する

```python
# factory/user.py
from interface.controller.user import IUserController
from interface.usecase.user import IUserUsecase
from interface.repository.user import IUserRepository
from presentation.controller.user import UserController
from application.interactor.user import UserInteractor
from infrastructure.repository.user import UserRepository


class UserFactory:
    @staticmethod
    def controller() -> IUserController:
        return UserController(UserFactory.usecase())

    @staticmethod
    def usecase() -> IUserUsecase:
        return UserInteractor(UserFactory.repository())

    @staticmethod
    def repository() -> IUserRepository:
        return UserRepository()
```

### main.py（エントリポイント）
- FastAPI のルーティングのみを記述する
- エンドポイント関数名は重複させない
- ファクトリクラスを呼び出す

```python
from fastapi import FastAPI
from factory.user import UserFactory
from presentation.dto.user import CreateUserRequest

app = FastAPI()

@app.get("/healthcheck")
def healthcheck():
    return {}

@app.post("/user")
def create_user(request: CreateUserRequest):
    return UserFactory.controller().create_user(request)
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
UserController（presentation/controller）  ← DTO ⇔ エンティティ変換
    ↓
UserInteractor（application/interactor）
    ↓
UserRepository（infrastructure/repository）
    ↓
UserDao（infrastructure/dao）  ← 外部データをDAOで受け取る
    ↓
UserEntity（domain/user.py）   ← ドメインエンティティに変換
    ↑ 以降はドメインエンティティを上位層へ伝播し、最後にDTOへ変換して返す
```

---

## テスト

- `tests/unit/` に層ごとにファイルを分ける
- 上位層のテストでは抽象を継承した Fake を注入する（モックライブラリは使わない）

| ファイル | 対象 |
|---|---|
| `test_create_user_validation.py` | DTO のバリデーション（正常系 + 境界値） |
| `test_user_controller.py` | コントローラ（`FakeUserUsecase` を注入） |
| `test_user_interactor.py` | インタラクター（`FakeUserRepository` を注入） |
| `test_user_repository.py` | リポジトリ実装 |

```bash
cd app && python -m pytest ../tests/ -v
```

---

## 命名規則

| 種別 | 規則 | 例 |
|---|---|---|
| エンティティ | PascalCase | `UserEntity` |
| インターフェース | `I*` プレフィックス | `IUserController` |
| ユースケース抽象 | `I*Usecase` | `IUserUsecase` |
| ユースケース実装 | `*Interactor` | `UserInteractor` |
| DAO | `*Dao` サフィックス | `UserDao` |
| DTO | `*Request` / `*Response` | `CreateUserRequest` |
| ファクトリ | `*Factory` サフィックス + `@staticmethod` | `UserFactory.controller()` |

---

## 依存方向の原則

- 依存は常に内側（ドメイン層）へ向かう
- `infrastructure` → `domain` は許可
- `domain` → `infrastructure` は禁止
- Pydantic への依存は `presentation/dto/` に閉じる
- インターフェースを介することで上位層が下位層の実装に依存しない
