# 仕様書

## 問題

### トップダウン的に分解してみる

自動販売機を実装する。
- 10円玉、50円玉、100円玉、500円玉、1000円札を１つずつ投入できる。
    - お金を受け取る機能を持つ
    - お金を一単位ずつ投入できる
    - お金のクラスは10円玉、50円玉、100円玉、500円玉、1000円札とする
- 投入は複数回できる。
    - 投入された金額の状態を保持する イメージ財布, 配列
- 投入金額の総計を取得できる。
    - 投入金額の総計をカウントする機能を持つ
    - さらに出力もできる
- 払い戻し操作を行うと、投入金額の総計を釣り銭として出力する。
    - 払い戻し機能を持つ
    - 釣り銭はお金クラスの配列

### 抽象度や重要度順に並び替える

- 自動販売機は複数の機能を持つ
    - [x] お金を一単位受け取る機能を持つ
        - [x] Moneyクラスを受け取る機能を持つ
    - [x] 投入された金額の状態を保持する機能を持つ
    - [x] 投入金額の総計をカウントする機能を持つ
        - [x] さらに出力もできる (出力の仕様が変わったら考える)
    - [x] 払い戻し機能を持つ
        - [x] お釣りの金額を計算する機能を持つ
        - [x] お釣りを実際の硬貨・紙幣に変換する機能を持つ
        - (Step ex) 偽造硬貨対策

- Moneyクラスは複数のサブクラスを持つ
    - [x] お金のクラスは10円玉、50円玉、100円玉、500円玉、1000円札とする
        - [x] step0 のスコープ外だけど step1 以降は必要な気がするのでMoneyクラスを実装する


    
## リファクタリング

- test_money.py
    - [x] Money.members()を実装したので、test_money.pyのテストをまとめる
    - [x] test_cannot_create_2_yen()もMoney.members()を使う
- vending_machine.py
    - [x] return_refund()がスメルコードっぽい
- test_vending_machine.py
    - [x] VendingMachine()の呼び出しをfixtureでまとめたい