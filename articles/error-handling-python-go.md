---
title: "Go と Python のエラーハンドリングの違いとその考察" # 記事のタイトル
emoji: "✏️" # アイキャッチとして使われる絵文字（1文字だけ）
type: "tech"
topics: ["go", "golang", "python", "error handling"]
published: false # 公開設定（falseにすると下書き）
---

## きっかけ

Python でのエラーハンドリングのベストプラクティスが良く分からなかった．

## 考えたこと

Go の多値返却でのエラーハンドリング見ると Python のエラーハンドリングが非自明に思える．
関数実行したときに Go だと

## Go でのエラーハンドリング

Go でエラーハンドリングする場合，以下 2 通りの書き方がある．

- 多値返却
- defer/panic/recover

上記の書き方を見たあと Go におけるエラーハンドリングのベストプラクティスを見る

### 多値返却

```go

```

### Go でのエラーハンドリングのベストプラクティス：error vs panic/recover

- [Golang の defer 文と panic/recover 機構について](https://blog.amedama.jp/entry/2015/10/11/123535)
- [PanicAndRecover · golang/go Wiki · GitHub](https://github.com/golang/go/wiki/PanicAndRecover#usage-in-a-package)
- [Defer, Panic, and Recover - The Go Blog](http://blog.golang.org/defer-panic-and-recover)
- [Frequently Asked Questions (FAQ) - The Go Programming Language](https://golang.org/doc/faq#exceptions)

## Python でのエラーハンドリング

```python
def divide(a: float, b: float) -> float:
    try:

    except ZeroDivisionError:
        raise

```

## なぜ違うのか
