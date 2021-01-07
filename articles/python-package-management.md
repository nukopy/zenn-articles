---
title: "Python のパッケージの仕組みを理解する"
emoji: "✒️"
type: "tech"
topics: ["python", "pip", "package", "poetry"]
published: false
---

この記事を読めば，Python のパッケージ管理を根本から理解できる．

## この記事で扱うこと，扱わないもの

### 扱うこと

- 現状変化のしにくい pip の仕組みが分かり，新しく出てくるパッケージ管理ツール pipenv，poetry，pyflow などで何をしようとしているかが理解できるようになる．

### 扱わないもの

- C 拡張を書いてそれをパッケージに導入する方法
  - 本記事の応用である．本記事の内容を学べばこれを行う際の基本的な知識を得ることができる．

## 記事を読む前に理解度チェック

- Python で書いたソースコードを配布するときの形式は？
  - ソースコード配布物
  - バイナリ配布物
- `setup.py` って何か知ってる
- setuptools って何？
- `pip install -e .` が何をするか分かる？
- egg，wheel って何？
- パッケージを公開する方法
  - pip
  - poetry

## エコシステムとは？

〜〜〜を「エコシステム」と言ったりします．

## パッケージの配布に関するリンク

- [公式 doc：Python モジュールの配布](https://docs.python.org/ja/3/distributing/index.html)
- [Python Packaging User Guide](https://packaging.python.org/)
- [Python Packaging User Guide: Guides - Packaging and distributing projects](https://packaging.python.org/guides/distributing-packages-using-setuptools/)
- [Python Packaging User Guide: Glossary](https://packaging.python.org/glossary/#term-Distribution-Package)
  - Python のパッケージングに関する公式用語集

## Python で書かれたソフトウェアの配布

Python で書かれたソフトウェアの配布フォーマットは大きく 2 種類．

- Python モジュール
- source distribution package，ソースコード配布物
- binary distribution package，バイナリ配布物

**これを読んで Python のパッケージング，sdist，wheel，setup.py の仕組みを理解する**
**[Python Packaging User Guide: Glossary](https://packaging.python.org/glossary/#term-Distribution-Package)**
**-----------------------------------------------------**

## 用語

### パッケージ管理モジュール

現在は setuptools 一強．現在主要でないものは括弧をつける．

- （distutils）
  - [公式 doc：distutils について](https://docs.python.org/ja/3/distutils/index.html)
  - Python 標準のパッケージ管理の基本的な機能（ビルド & 配布）を提供するモジュール (import distutils)。
  - Python 標準ライブラリに 1998 年に最初に追加されました。 distutils の直接的な利用は段階的に取り払われていきますが、それは今でも現時点でのパッケージングと配布のインフラストラクチャの基礎として鎮座していて、標準ライブラリの一部として残っているだけでなく、その名前はほかの文脈でも生き続けています(Python のパッケージング標準の開発をまとめるのに使われているメーリングリストの名前のように)。
  - setuptools が distutils の高機能版で広く使われているので setuptools を使うのが一般的。
- **setuptools**
  - distutils を強化したパッケージ管理用（ビルド & 配布）の setuptools というモジュールと、easy_install というコマンドラインツールのセット。
  - distutils (の大部分)をまるごと置き換える後継プロジェクトで、2004 年に最初に公開されました。未修正の distutils ツールに比べて、他のパッケージへの依存関係を宣言できる機能が追加されたことが最も注目に値します。今では distutils よりも定期的に更新される代替品として推奨されていて、広範囲の Python バージョンに渡るより新しいパッケージングの標準を一貫してサポートしています。
  - 構成要素
    - （easy_install）
      - setuptools に付属しているコマンドラインツール。easy_install を使うと簡単なコマンドで web 上 (e.g. PyPI) から パッケージをダウンロードしてインストールすることができる。
    - **pip**
      - easy_install の強化版ツール
    - **setup.py**（**重要**）
      - setuptools，distutils でパッケージの定義を記述するスクリプトに使われるファイル名。 作成されたパッケージをインストールする際にも利用される。
  - インストール
    - ez_setup.py
      - setuptools をインストールする際に利用されるスクリプトの名前。
- （distribute）
  - setuptools の更新が停滞していた時に発生した setuptools のクローン。 2013 年に setuptools とマージされたので、distribute のことは気にする必要はないはず。

### パッケージ配布形式

- Python Eggs
  - setuptools で定義された Python パッケージの配布形式。Python のコードやメタ情報その他を所定のフォーマットに従って zip で固めたもの (distutils の生成する zip/tar の拡張版)。setuptools を使って (つまり setuptools を使って setup.py を定義していれば) 作成することができる。
- Python Wheels
  - Python Eggs の後継の Python パッケージの配布形式。**wheels，wheel files** と呼ばれる．
  - 実態は zip 形式のアーカイブであり、PEP427 で定義された。pip でパッケージをインストールする時は、wheel 形式のファイルをダウンロードするところから始まる。逆に、Python のパッケージを作って配布したい場合は、wheel 形式のファイルを作成する必要がある。
  - wheel は (このドキュメントの文脈では) distutils/setuptools に bdist_wheel コマンドを追加するプロジェクトです。これは、それがバイナリの拡張を含んでいようと、Python ライブラリをローカルでビルドする必要性なしでシステムにインストール出来るようにする、クロスプラットフォームのバイナリのパッケージング形式("wheels" または "wheel files" と呼ばれ、 PEP 427 で定義されています)を生成します。

### 重要用語

- Python Packaging Index，PyPI
  - Python Package Index。Python パッケージのパブリック・リポジトリです。このリポジトリのパッケージは、他の Python ユーザが利用できるように、オープンソースでライセンスされています。
  - だれでも Python のパッケージが登録できる python.org のサイト。 easy_install とか pip は基本的にここからパッケージを探してきてインストールしてくれる。
- Python Packaging Authority，PyPA
  - 標準のパッケージングツール、関連するメタデータとファイルフォーマット標準の保守と発展を担っている、開発者・ドキュメントの著者のグループです。彼らは様々なツールやドキュメント、issue tracker を GitHub と Bitbucket の両方で管理しています。

## 参考

- [【Python】pip と wheel](https://qiita.com/kenta1984/items/16a14f3bfaf1f257c585)
- [Python パッケージ管理技術まとめ (pip, setuptools, easy_install, etc)](https://www.yunabe.jp/docs/python_package_management.html)
