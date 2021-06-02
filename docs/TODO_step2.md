# 仕様書

## 問題

> 値段と名前の属性からなるジュースを１種類格納できる。初期状態で、コーラ（値段:120円、名前”コーラ”）を5本格納している。
> 格納されているジュースの情報（値段と名前と在庫）を取得できる。

### トップダウン的に分解してみる

- Juice クラスを定義する
- VendingMachine クラスは Juice の情報を取得できる

### 抽象度や重要度順に並び替える

- [ ] Juice クラスを定義する
- [ ] Juice クラスは値段と名前の状態を持つ
- [ ] VendingMachine クラスは在庫照会メソッドを持つ