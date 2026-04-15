# 意思決定ログ

アーキテクチャ・命名規則に関する意思決定の記録。

---

## [2026-04-15] Presentation層の抽象名称に `Controller` を採用

### 決定

Presentation層のインターフェース・実装クラスの名称に `Controller` を採用する。

```
interface/controller/user.py   → IUserController
presentation/controller/user.py → UserController
```

### 検討した選択肢

| 候補 | 文脈 | 不採用の理由 |
|---|---|---|
| **Handler** | Go・FastAPI などのフレームワーク慣習 | フレームワーク寄りの用語であり、Clean Architecture の原著に登場しない。HTTPハンドラーとしての意味合いが強く、層の役割を正確に表現しない |
| **Port** | Hexagonal Architecture（Ports & Adapters） | 本リポジトリは Clean Architecture ベースであり、Hexagonal Architecture の用語を混在させると設計思想が曖昧になる |
| **Controller** | Clean Architecture 原著 | Robert C. Martin の原著で明示的に登場する用語。Presenter・View とともに Presentation層の構成要素として定義されており、設計思想と一致する |

### 理由

本リポジトリは Clean Architecture の原著に忠実な構成を目指しているため、原著の用語である `Controller` を採用する。

---

## [2026-04-15] 依存性注入にクラスベースの `Factory` を採用

### 決定

依存性注入の組み立てにクラスベースの `Factory` パターンを採用する。

```
factory/user.py → UserFactory（@staticmethod でチェーンを組み立て）
```

### 検討した選択肢

| 候補 | 概要 | 不採用の理由 |
|---|---|---|
| **`build_*` 関数（snake_case）** | `build_user_handler()` のようなトップレベル関数 | エンティティが増えると関数が散在し、どの関数がどのエンティティに属するか一目で把握しにくい |
| **`new_*` 関数** | Go のコンストラクタ慣習に近いスタイル | 同上。関数ベースのため、エンティティ単位のまとまりが生まれない |
| **`provide_*` 関数** | DI フレームワーク（Injector 等）寄りのスタイル | フレームワーク導入を前提とした命名であり、現構成では過剰 |
| **クラスベース `*Factory`** | エンティティ単位でクラスにまとめ `@staticmethod` で定義 | **採用**。エンティティ追加時に `UserFactory` `OrderFactory` と整理でき、スケール時の見通しが良い |

### 理由

エンティティが増えた際に依存チェーンをエンティティ単位で管理できるよう、クラスベースの `Factory` を採用する。`@staticmethod` により状態を持たないシンプルな構成を維持しつつ、呼び出し側も `UserFactory.controller()` と明示的に記述できる。

---

## [2026-04-15] Application層の実装名称に `Interactor` を採用

### 決定

Application層の実装クラス名に `Interactor` を採用し、抽象（`IUserUsecase`）と明確に区別する。

```
interface/usecase/user.py          → IUserUsecase（抽象）
application/interactor/user.py     → UserInteractor（実装）
```

### 理由

Clean Architecture の原著では「Use Case」はインターフェース（抽象）として、「Interactor」はその実装として区別されている。実装クラスに `Usecase` を使うと抽象と混同しやすいため、原著の用語に従い `Interactor` を採用する。
