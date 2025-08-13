# オーダ照会

## 概要

オーダ情報について最新のステータスを照会する。

リクエストパラメ―タの設定により、単一または複数のオーダを照会することが可能。

## 使用シーン

取引ステータス不明の際にONEPAYに問い合わせるのに使用する。

## アクセスURL

/gateway/orderQuery/{data}/{serviceMode}/{signType}/{isBackTran}/{token}

## リクエストパラメータ（共通部）

| 番号 | 名称 | 英名 | データ型 | 必須 | 設定値 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | URL拡張データ | data | String<br>(32) | Y | version=1.0 | URLの拡張部<br>現時点、ｖersion=1.0のみ指定可能 |
| 2 | サービス接続モード | serviceMode | String<br>(3) | Y | B01 | B2Cモードの場合：C01<br>B2Bモードの場合：B01 |
| 3 | 署名方式 | signType | String<br>(1) | Y | 0 | 0:RSA |
| 4 | バックエンドフラグ | isBackTran | String | Y | 0 | バックエンドによるトランザクション<br>0：いいえ |
| 5 | トークン | token | String<br>(128) | Y | 100386873084281004qSB0sMj7FU0020180213170446674563 | B2Bモードの場合：<br>ﾏｰﾁｬﾝﾄID（12桁）+ｶｽﾀﾏｲｽﾞの店舗ｺｰﾄﾞ(最長32桁)＋ｶｽﾀﾏｲｽﾞの端末ｺｰﾄﾞ(最長32桁)+14桁ﾀｲﾑｽﾀﾝﾌﾟ+6桁ｼﾘｱﾙ<br>B2Cモードの場合：<br>14桁店舗コード+16桁端末コード+14桁タイムタンプ+6桁シリアル |

## リクエストパラメータ

| 番号 | 名称 | 英名 | データ型 | 必須 | 設定値 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | ロケール | locale | String<br>(30) | N | JAPAN | 国際化コード（US：英語,CHINA：中国語, JAPAN：日本語） |
| 2 | タイム<br>ゾーン | timeZone | String<br>(4) | Y | p9 | タイムゾーン（日本はUTC+9） |
| 3 | 店舗コード | branchCode | String<br>(32) | Y | B2C:<br>10036859104261<br>B2B:<br>AShop001 | B2Cモードの場合：<br>ONEPAYシステム内部の店舗コード<br>B2Bモードの場合：<br>加盟店内部のｶｽﾀﾏｲｽﾞ店舗コード |
| 4 | 端末コード | terminalCode | String<br>(32) | N | B2C:<br>10040bQQW23GEWEA B2B:<br>BTer001 | B2Cモードの場合：<br>ONEPAYシステム内部の端末コード<br>B2Bモードの場合：<br>加盟店内部のｶｽﾀﾏｲｽﾞ端末コード |
| 5 | オーダID | orderId | String<br>(32) | N | J1VF20161104181148726FFl | ONEPAYシステム内部のオーダID |
| 6 | オーダ明細ID | orderDetailId | String<br>(32) | N | J1WP20161104181148726FFl | ONEPAYシステム内部のオーダ明細ID |
| 6 | 支払方法 | payType | String<br>(4) | N | 01 | コード定義の支払方法をご参照ください |
| 7 | レシート<br>番号 | receiptNo | String<br>(32) | N | 100022200001 |  |
| 8 | 決済コード | userCode | String<br>(512) | N | 2015040302011229 | ワンタイムバーコード値またはQRコード値 |
| 9 | 開始<br>レコード数 | start | String<br>(10) | Y | 1 | デフォルト値：1 |
| 10 | 件数 | limit | String<br>(10) | Y | 10 | 1ページあたりの件数<br>DEFAULTは10件<br>※最大1000件が照会可能 |
| 11 | 開始日付 | startDate | String<br>(8) | N | 20160502 | 照会開始日時<br>※開始日付を過去90日以内に設定してください。 |
| 12 | 終了日付 | endDate | String<br>(8) | N | 20160503 | 照会終了日時<br>※終了日付を開始日付から7日以内に設定してください |
| 13 | 署名 | sign | String<br>(500) | Y | 1234567890123456789012345678901 |  |
| 14 | ｶｽﾀﾏｲｽﾞ<br>端末番号 | terminalSelfCode | String<br>(32) | N | ASHOP01 | B2Bモードの場合、空白 |

注：オーダID、オーダ明細ID、レシート番号、端末番号、バーコード、日付すべてが未入力の場合、エラーとする

## レスポンスパラメータ

| 番号 | 名称 | 英名 | データ型 | 必須 | 設定値 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 |  | meta | String | Y |  |  |
| 1-1 | ステータス | code | String<br>(2) | Y | 00 | 00|02|09<br>00:成功，02：通信異常，09：異常 |
| 1-2 | 詳細 | message | String<br>(16) | Y | SUCCESS | SUCCESS|FAILURE<br>SUCCESS:成功，FAILURE：失敗 |
| 2 |  | data | String | Y |  |  |
| 2-1 | エラーコード | errorCode | String<br>(256) | N | E02001 | ステータスが00以外時必須 |
| 2-2 | エラー<br>メッセージ | errorInfo | String<br>(128) | N | エラーの詳細メッセージ | ステータスが00以外時必須 |
| 2-3 | 署名 | sign | String<br>(500) | N |  |  |
| 2-4 |  | result | String | N |  | ステータスが00時のみ返却 |
| 2-4-1 | 現ページ | currentPage | String<br>(10) | N | 1 |  |
| 2-4-2 | 表示<br>件数 | limit | String<br>(10) | N | 10 |  |
| 2-4-3 | 開始<br>レコード数 | start | String<br>(10) | N | 10 |  |
| 2-4-4 | 総件数 | totalCount | String<br>(10) | N | 10 |  |
| 2-4-5 | 総ページ数 | totalPages | String<br>(10) | N | 1 |  |
| 2-4-6 |  | orderBeans |  |  |  | ソート順：オーダ更新日付の降順 |
| 2-4-6-1 | 取引日時 | transTime | String（14） | N | 20116050211091500 | YYYYMMDDHHMMSS |
| 2-4-6-2 | 店舗コード | branchCode | String<br>(32) | N | 10036859104261 |  |
| 2-4-6-3 | 端末コード | terminalCode | String<br>(32) | N | 10040BQQW23GEWEA |  |
| 2-4-6-4 | ｶｽﾀﾏｲｽﾞ端末番号 | terminalSelfCode | String<br>(32) | N | Ashop001 | B2Bモードの場合、空白 |
| 2-4-6-5 | レシート番号 | receiptNo | String<br>(10) | N | 100022200001 |  |
| 2-4-6-6 | 正札通貨 | currencyCode | String<br>(10) | N | JPY |  |
| 2-4-6-7 | 取引金額 | amount | BigDecimal(15,2) | N | 100 |  |
| 2-4-6-8 | 返金済<br>金額 | refundAmount | BigDecimal(15,2) | N | 20 |  |
| 2-4-6-9 | 返金中<br>金額 | refundingAmount | BigDecimal(15,2) | N | 80 |  |
| 2-4-6-10 | 元オーダID | orderId | String<br>(32) | N |  |  |
| 2-4-6-11 | 取引ステータス | orderStatus | String<br>(2) | N |  | コード定義の取引ステータスをご参照ください |
| 2-4-6-12 | 支払方法 | payType | String<br>(4) | N | 01 | コード定義の支払方法をご参照ください |

## 使用凡例

### URL

https://gateway.onepay.finance/gateway/orderQuery/version=1.0/B01/0/0/OB0244899999AShop001BTer00120190814183307730477

### リクエストパラメータ（個別部）

{

"branchCode" : "AShop001",

"endDate" : "20190819",

"limit" : "10",

"locale" : "JAPAN",

"sign" : "A6A5B20D0009ACDB115D012D884C8899",

"start" : "1",

"startDate" : "20190819",

"terminalCode" : "BTer001",

"timeZone" : "p9"

}

### レスポンスパラメータ

{

"meta" :

{

"code" : "00",

"message" : "SUCCESS"

},

"data" :

{

"errorCode" : "",

"errorInfo" : "",

"sign" : "3817462B550A339ABDB7B741F203C422",

"result" :

{

"currentPage" : "1",

"limit" : "10",

"start" : "1",

"totalCount" : "1",

"totalPages" : "1",

"orderBeans" : [

{

"transTime" : "20190819161814",

"branchCode" : "AShop001",

"terminalCode" : "BTer001",

"receiptNo" : "esdfghjklzxcvbnmqwertyuioplkjhgf",

"currencyCode" : "JPY",

"amount" : 1,

"refundAmount" : 0,

"refundingAmount" : 0,

"orderId" : "OWC20161104181148726rpVQ",

"orderStatus" : "03",

"payType" : "01"

}

]

}

}

}