# zenn-contents

Repository for Zenn contents

- [Zenn](https://zenn.dev/)
- [nukopy](https://zenn.dev/pyteyon)

## Setup

### Install Zenn CLI

```sh
npm install -g zenn-cli
```

### Zenn コンテンツのためのプロジェクトの初期化

ref: [Zenn 公式：Zenn CLI をインストールする](https://zenn.dev/zenn/articles/install-zenn-cli)

```sh
mkdir zenn-contents
cd zenn-contents
zenn init
```

## Zenn CLI で記事・本を執筆する

ref: [Zenn CLI で記事・本を管理する方法](https://zenn.dev/zenn/articles/zenn-cli-guide)

### 記事の作成

```sh
zenn new:article
```

### 記事をローカルでプレビューする

Zenn CLI のプレビューモードでは、ブラウザで実際の記事の表示と同じ内容を表示しながら好きなエディタで記事の編集ができる。また、Zenn CLI の使用方法や、Zenn のマークダウン記法も確認できる。

```sh
zenn preview
# 👀 Preview on http://localhost:8000
```

ポートの指定も可能。

```sh
zenn preview --port 3333
# 👀 Preview on http://localhost:3333
```

### 日時を指定して記事を公開する

Front Matter の `published` を `true` にした上で、`published_at` を指定する。`published_at` のフォーマットは、`YYYY-MM-DD` または `YYYY-MM-DD HH:MM` である必要がある。

```yml
published: true # 公開設定（false にすると下書き）
published_at: "1970-01-01 00:00" # 公開日
```

> **Warning**
>
> 公開日時の指定は一度しかできず、既に設定された値を変更することはできない。

### 公開した記事を更新する

Markdown ファイルを編集して、GitHub リポジトリに push すると、自動的に記事が更新される。

### 公開した記事を削除する

ダッシュボードから手動で行う。安全のため、GitHub の `articles` ディレクトリから Markdown ファイルを削除しても、zenn.dev 上では削除されない。

- [Zenn: Dashboard](https://zenn.dev/dashboard)

## その他

### Markdown のリンター

Markdown のリンターとして、VSCode 拡張の [markdownlint](https://marketplace.visualstudio.com/items?itemName=DavidAnson.vscode-markdownlint) を使用している。リポジトリルートに置いてある `.markdownlint.yml` を編集することで適用するルールを設定できる。
