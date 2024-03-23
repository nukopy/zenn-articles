---
title: "TouchDesigner のエラーメッセージをコピペできない問題を解決する" # 記事のタイトル
emoji: "🚨" # アイキャッチとして使われる絵文字（1 文字だけ）
type: "tech" # tech: 技術記事 / idea: アイデア
topics: ["touchdesigner"]
published: false # 公開設定（false にすると下書き）
# published_at: "1970-01-01 00:00" # 公開日
---

Zenn の練習に記事を書いてみた。

## 問題

TouchDesigner のプロジェクトにて、特定のノードでエラーが起きているとき、以下のようなポップアップを表示することでエラーメッセージを見ることができる。

![](https://storage.googleapis.com/zenn-user-upload/312bd033a34c-20240324.png)

しかし、このポップアップのテキストはコピペできない。テキストも選択できないし、クリックしてもポップアップがすぐ閉じられてしまう。エラーメッセージをコピペできないのは検索や ChatGPT に投げるときに致命的なので、これを解決する方法を調査してみた。

## 開発環境

- OS: macOS Sonoma 14.1
- TouchDesigner: 2022.33910 (NON-COMMERCIAL)

## 解決策の概要

解決策は以下の 2 つ：

1. Textport（TouchDesigner 内の Python 対話環境）を使用してコピペ可能なエラーメッセージを取得する
2. Error DAT、Textport を使用してコピペ可能なエラーメッセージを取得する

方法 2 でこの記事を書き始め、その途中でより簡単な方法 1 を見つけた。問題の解決策としては方法 1 で十分だが、せっかく方法 2 で Error DAT の使い方を調査したので覚書として残しておく。

## 解決策 1: Textport を使用してコピペ可能なエラーメッセージを取得する

手順は以下の通り。めっちゃ簡単。

1. メニューバー > Dialogs > Textport and DATs から Textport を開く
2. Textport でエラーが出ているノードの参照を取得し、エラーメッセージを出力する

### 1. メニューバー > Dialogs > Textport and DATs から Textport を開く

Textport は、メニューバー > Dialogs > Textport and DATs から開くことができる。Textport を開くと、Python の対話環境が起動される。

![](https://storage.googleapis.com/zenn-user-upload/e4808b3bba12-20240324.png)
*メニューから Textport and DATs を開く*

![](https://storage.googleapis.com/zenn-user-upload/56014f7189f8-20240324.png)
*Textport を開いたときのノードエディタの様子*

### 2. Textport でエラーが出ているノードの参照を取得し、エラーメッセージを出力する

エラーの内容は以下の通り。これはコピペできないエラー情報のポップアップ。`null1` というノードでエラーが発生している。

![](https://storage.googleapis.com/zenn-user-upload/312a4690716e-20240324.png)
*`null1` ノードで発生しているエラー情報のポップアップ*

`null1` ノードで発生しているエラーメッセージをコピペ可能な状態で取得するには、Textport で TouchDesigner の Python の組み込み関数である `op` 関数を使用してノードの参照を取得し、`<node ref>.errors()` メソッドを実行すればよい。

- コマンド（ちょっと変わった対話環境なのでプロンプトも書いてる）

```python
python >>> null1 = op("/project1/null1")
python >>> null1.errors()
# "  Error: TypeError: float() argument must be a string or a number, not 'td.nullCHOP'\nContext:(Parameter: Translate) (/project1/null1)"
```

![](https://storage.googleapis.com/zenn-user-upload/12c4f5817548-20240324.png)
*Textport でコピペ可能なエラーメッセージを出力した様子（マウス操作で選択できてる！）*

コピーできたエラーメッセージは以下の通り。ちゃんと**コピペ可能なエラーメッセージを出力することができた**。

```txt
TypeError: float() argument must be a string or a number, not 'td.nullCHOP'
```

:::message
Textport の環境では、ノードのフルパスを指定しないと `op` 関数でプロジェクト内のノードにアクセスできなかった。上記の例では、`op("null1")` ではなく、`op("/project1/null1")` としないとノードの参照が取得できない。

ノードのフルパスを確認するには、ノードのパラメータウィンドウの `i` ボタンを押し、ノード情報のポップアップの一番上の `Name` の値を見れば良い。

![](https://storage.googleapis.com/zenn-user-upload/c00b51bfdfa9-20240324.png)
:::


## 解決策 2: Error DAT と Textport を使用してコピペ可能なエラーメッセージを取得する

:::message
解決策 1 の方が簡単。

時間があって Error DAT に興味がある方は以下をどうぞ。
:::

Error DAT と Textport を使用することでコピペ可能なエラーメッセージを出力することができる。Textport を使用するのは解決策 1 と同様。解決策 2 の手順は以下の通り。

1. Error DAT を作る
2. プロジェクト（`.toe` ファイル）内のエラーが Error DAT のテーブルに自動で追加される
3. メニューバー > Dialogs > Textport and DATs から Textport を開く
4. Error DAT のテーブルからコピーしたいエラーメッセージを見つけ、Textport でその内容を出力する

### 1. Error DAT を作る

OP Create Dialog から Error DAT を作る。

![](https://storage.googleapis.com/zenn-user-upload/cd07ed3a98f6-20240324.png)

### 2. プロジェクト内のエラーが Error DAT のテーブルに自動で追加される

Error DAT は、プロジェクト内の各ノードで起きたエラーを拾い、自動でテーブル形式のデータとしてプログラムから扱えるようにしてくれるノードである。

ちなみに、Error DAT を作ると同時に、エラーが起きたときのコールバックを定義するための Text DAT（TouchDesigner 内で Python スクリプトを実行できるノード）が生成され、作成した Error DAT に自動で紐づけられる（下記画像内の `error1_callbacks` という Text DAT）。

![](https://storage.googleapis.com/zenn-user-upload/c8f62d0f1504-20240324.png)
*Error DAT を追加したときのノードエディタの様子*

![](https://storage.googleapis.com/zenn-user-upload/6b35faac5d72-20240324.png)
*Error DAT のテーブルにプロジェクト内のエラーが自動で追加されている*

### 3. メニューバー > Dialogs > Textport and DATs から Textport を開く

Textport で Error DAT のノードの参照を取得し、そのテーブルの中のエラーメッセージを出力したい[^1]。そのためにまずは Textport を開く。

Textport の開き方は[解決策 1 で先述した通り](#1.-メニューバー->-dialogs->-textport-and-dats-から-textport-を開く)。

[^1]: Error DAT のコールバック定義用の Text DAT を使用してエラーメッセージをログとして吐き出すのも良いが、Textport で直接エラーメッセージを取得する方法の方が楽。

### 4. Error DAT のテーブルからコピーしたいエラーメッセージを見つけ、Textport でその内容を出力する

Textport を開いたら、`op` 関数を使用して Error DAT の参照を取得し、その参照を使用して Error DAT のテーブルから目的のエラーメッセージを出力する。

例えば、以下の Error DAT のテーブルから 3 行目、1 列（`message` の列）の `TypeError...` というエラーメッセージを取得したい場合、以下のようにコードを実行するとよい。

![](https://storage.googleapis.com/zenn-user-upload/7b3639d288ca-20240324.png)
*Error DAT のテーブルデータ*

- 目的のエラーメッセージ（テーブル 3 行目、1 列）のエラーメッセージを取得するコマンド

```python
python >>> error1 = op("/project1/error1")
python >>> error1[3, 1]
# type:Cell cell:(3, 1) owner:/project1/error1 value:TypeError: float() argument must be a string or a number, not 'td.nullCHOP'
# Context:(Parameter: Translate)
```

![](https://storage.googleapis.com/zenn-user-upload/0e322909c8dc-20240324.png)
*エラーを出力した Textport の様子（マウス操作で選択できてる！）*

これで**コピペ可能なエラーメッセージが出力できるようになった**。

Error DAT のテーブル操作は、Error DAT クラスの公式ドキュメントの [ACCESSING TABLE CONTENT](https://derivative.ca/UserGuide/ErrorDAT_Class#:~:text=ACCESSING%20TABLE%20CONTENT) を参照するとよい。

## おまけ：Error DAT

Error DAT クラスのドキュメント

https://derivative.ca/UserGuide/ErrorDAT_Class

Error DAT で使えるメソッドリスト

```python
python >>> error1.__dir__()
['__init__', '__new__', '__doc__', 'type', 'label', 'icon', 'family', 'OPType', 'opType', 'isFilter', 'isCustom', 'subType', 'minInputs', 'maxInputs', 'isMultiInputs', 'visibleLevel', 'supported', 'licenseType', '__getitem__', '__setitem__', '__delitem__', 'run', 'write', 'flush', 'isatty', 'setSize', 'clear', 'copy', 'row', 'col', 'rows', 'cols', 'appendRow', 'appendRows', 'appendCol', 'appendCols', 'insertRow', 'insertCol', 'replaceRow', 'replaceCol', 'deleteRow', 'deleteRows', 'deleteCol', 'deleteCols', 'cell', 'cells', 'save', 'findCell', 'findCells', 'scroll', 'detectLanguage', 'export', 'text', 'jsonObject', 'module', 'numRows', 'numCols', 'locals', 'isTable', 'isText', 'isEditable', 'editingFile', '__repr__', '__hash__', '__str__', '__getattribute__', '__setattr__', '__delattr__', '__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__', '__add__', '__radd__', '__mul__', '__rmul__', '__bool__', 'copyParameters', 'ops', 'setInputs', 'pars', 'evalExpression', 'fetch', 'fetchOwner', 'store', 'unstore', 'storeStartupValue', 'unstoreStartupValue', 'cook', 'changeType', 'destroy', 'relativePath', 'shortcutPath', 'resetNodeSize', 'openViewer', 'closeViewer', 'resetViewer', 'openParameters', 'openMenu', 'var', 'warnings', 'errors', 'scriptErrors', 'addScriptError', 'addError', 'addWarning', 'clearScriptErrors', 'dependenciesTo', 'childrenCPUMemory', 'childrenGPUMemory', '__getstate__', '__setstate__', 'id', 'passive', 'op', 'parent', 'iop', 'ipar', 'valid', 'curPar', 'currentPage', 'name', 'path', 'digits', 'base', 'children', 'numChildren', 'recursiveChildren', 'numChildrenRecursive', 'time', 'color', 'storage', 'par', 'parGroup', 'pages', 'builtinPars', 'customPars', 'customPages', 'customTuplets', 'customParGroups', 'comment', 'tags', 'mod', 'warning', 'error', 'inputs', 'outputs', 'inputConnectors', 'outputConnectors', 'ext', 'replicator', 'nodeX', 'nodeY', 'nodeWidth', 'nodeHeight', 'nodeCenterX', 'nodeCenterY', 'dock', 'docked', 'display', 'render', 'viewer', 'activeViewer', 'lock', 'selected', 'python', 'current', 'bypass', 'expose', 'cloneImmune', 'showDocked', 'showCustomOnly', 'allowCooking', 'isCOMP', 'isBase', 'isObject', 'isPanel', 'isTOP', 'isCHOP', 'isSOP', 'isMAT', 'isDAT', 'totalCooks', 'cookFrame', 'cpuCookTime', 'gpuCookTime', 'cookAbsFrame', 'cookStartTime', 'cookEndTime', 'cookedThisFrame', 'cookedPreviousFrame', 'cpuMemory', 'gpuMemory', 'childrenCPUCookTime', 'childrenCPUCookAbsFrame', 'childrenGPUCookTime', 'childrenGPUCookAbsFrame', 'childrenCookTime', 'childrenCookAbsFrame', 'cookTime', '__reduce_ex__', '__reduce__', '__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__']
```

## 終わりに

エラーメッセージがコピペできないのはプログラミングをする上で致命的だったので、慣れない TouchDesigner と戦いながら調査してまとめてみた。まだまだ探り探りだけど、少しずつ慣れていければと思う。

解決策 2 を一通りまとめたあとに、`error1.__dir__()` を試しに実行してみたら `errors` というメソッドが見つかり、より簡単な解決策 1 が見つかったのは嬉しいような悲しいような。どこかで Error DAT を使いこなす必要が来れば、自分でこの記事に戻ってきて今回の調査が報われることでしょう。

もっと楽な方法あるよとかあれば教えてくださると嬉しいです。最後まで読んでくださりありがとうございました。

## 参考

- (2018) [satoruhiga.com/TDWS2018/day14/](http://satoruhiga.com/TDWS2018/day14/)
- [(2020/04, Qiita)TouchDesigner でデバッグするときに役立つこと](https://qiita.com/joe0hara/items/50228c39667dfac94f9e)
- [(2020/03, note) TouchDesigner の基本操作 / GUI の基本操作について](https://note.com/toyoshimorioka/n/ne2d37107b41c)
