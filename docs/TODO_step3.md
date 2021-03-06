# 仕様書

## 問題

> 投入金額、在庫の点で、コーラが購入できるかどうかを取得できる。
> ジュース値段以上の投入金額が投入されている条件下で購入操作を行うと、ジュースの在庫を減らし、売り上げ金額を増やす。
> 投入金額が足りない場合もしくは在庫がない場合、購入操作を行っても何もしない。
> 現在の売上金額を取得できる。
> 払い戻し操作では現在の投入金額からジュース購入金額を引いた釣り銭を出力する。

> 注意：責務が集中していませんか？責務が多すぎると思ったら分けてみましょう

### トップダウン的に分解してみる

- 購入する、ジュースを買うという機能がいる
  - 購入リクエストを送る
  - 状態をチェックする
  - レスポンスを返す
- 売り上げ金額属性を追加する
- 払い戻し
  - 状態チェック後、ジュースの最低金額より投入金額が低い時におつりをジュースと一緒に返す
  - 払い戻しリクエストがあったときに投入金額全額を返す

### 抽象度や重要度順に並び替える

- [x] 状態(在庫、投入金額)をチェックする
- [x] 状態を更新する + JuiceSupplier を VendingMachine からアクセスできるようにする
- [ ] 購入リクエストを送る
- [ ] レスポンスを返す

- [ ] 状態チェック後、ジュースの最低金額より投入金額が低い時におつりをジュースと一緒に返す
- [ ] 払い戻しリクエストがあったときに投入金額全額を返す

- [ ] 売り上げ金額属性を追加する