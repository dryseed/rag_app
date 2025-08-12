# 支払

概要

マーチャントシステムから受け取った支払リクエストをイシュアへ送信する。また、オーダIDや取引ステータス、取引時間等の情報を応答する。

使用シーン

- (1)ユーザがバーコード／QRコードを提示し、店員がそれをマーチャントシステムに読み込む。読み込んだ支払情報を本システムへ送信し、支払手続きを完成するのに使用する。

- (2)フロー

ONEPAYONEPAY

アクセスURL

/gateway/pay/{data}/{serviceMode}/{signType}/{isBackTran}/{token}

リクエストパラメータ（共通部）

| 番号 | 名称 | 英名 | データ型 | 必須 | 設定値 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | URL拡張データ | data | String<br>(32) | Y | version=1.0 | URLの拡張部<br>現時点、ｖersion=1.0のみ指定可能 |
| 2 | サービス接続モード | serviceMode | String<br>(3) | Y | B01 | B2Cモードの場合：C01<br>B2Bモードの場合：B01 |
| 3 | 署名方式 | signType | String<br>(1) | Y | 0 | 0:RSA(B2Bの場合、RSAのみサポート) |
| 4 | バックエンドフラグ | isBackTran | String<br>(1) | Y | 0 | バックエンドによるトランザクション<br>0：いいえ |
| 5 | トークン | token | String<br>(128) | Y | 100386873084281004qSB0sMj7FU0020180213170446674563 | B2Bモードの場合：<br>ﾏｰﾁｬﾝﾄID（12桁）+ｶｽﾀﾏｲｽﾞの店舗ｺｰﾄﾞ(最長32桁)＋ｶｽﾀﾏｲｽﾞの端末ｺｰﾄﾞ(最長32桁)+14桁ﾀｲﾑｽﾀﾝﾌﾟ+6桁ｼﾘｱﾙ<br><br>B2Cモードの場合：<br>14桁店舗コード+16桁端末コード+14桁タイムタンプ+6桁シリアル |

リクエストパラメータ

| 番号 | 名称 | 英名 | データ型 | 必須 | 設定値 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | ロケール | locale | String<br>(30) | N | JAPAN | 国際化コード（US：英語,CHINA：中国語, JAPAN：日本語） |
| 2 | タイムゾーン | timeZone | String<br>(4) | Y | p9 | タイムゾーン（日本はUTC+9） |
| 3 | 支払方法 | payType | String<br>(4) | Y | 01 | コード定義の支払方法をご参照ください |
| 4 | 店舗コード | branchCode | String<br>(32) | Y | B2B:<br>AShop001<br>B2C:<br>10036859104261 | B2Cモードの場合：<br>ONEPAYシステム内部の店舗コード<br>B2Bモードの場合：<br>加盟店内部のｶｽﾀﾏｲｽﾞ店舗コード |
| 5 | 端末コード | terminalCode | String<br>(32) | N | B2B:<br>BTer001<br>B2C:<br>10040bQQW23GEWEA | B2Cモードの場合(必須)：<br>ONEPAYシステム内部の端末コード<br>B2Bモードの場合：<br>加盟店内部のｶｽﾀﾏｲｽﾞ端末コード |
| 6 | 正札通貨 | currencyCode | String<br>(10) | Y | JPY | コード定義の通貨をご参照ください |
| 7 | 正札金額 | amount | BigDecimal(15,2) | Y | 3333 | 取引金額（日本円の場合、小数点以下は不要） |
| 8 | レシート番号 | receiptNo | String<br>(32) | N | 100022200001 | レシート番号 |
| 9 | 決済コード | userCode | String<br>(512) | Y | 2016092613361229 | ワンタイムバーコード値またはQRコード値 |
| 10 | バージョン | appVersion | String<br>(32) | Y | ios-CpayPro-1.0.0 | サービス接続元のバージョン情報です。<br>以下の情報を [-]で連結<br>(1)オペレータシステム名称(最長１０桁まで)<br>(2)APP名称(最長１０桁まで) <br>(3)APPバージョン(最長１０桁まで)<br>コード定義のオペレータシステムをご参照ください。 |
| 11 | 署名 | sign | String<br>(500) | Y |  |  |
| 12 | 備考 | remark | String<br>(128) | N |  |  |
| 13 | 拡張情報 | extendInfo | String<br>(128) | N |  | 未使用 |
| 14 | 支払種類 | valueType | String(2) | N |  | 未使用 |

レスポンスパラメータ

| 番号 | 名称 | 英名 | データ型 | 必須 | 設定値 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 |  | meta | String | Y |  |  |
| 1-1 | ステータス | code | String<br>(2) | Y | 00 | 00|02|09<br>00:成功，02：通信異常，09：異常 |
| 1-2 | 詳細 | message | String<br>(16) | Y | SUCCESS | SUCCESS|FAILURE<br>SUCCESS:成功，FAILURE：失敗 |
| 2 |  | data | String | Y |  |  |
| 2-1 | エラーコード | errorCode | String<br>(6) | N | E02001 | ステータスが00以外時必須 |
| 2-2 | エラーメッセージ | errorInfo | String<br>(256) | N | エラーの詳細メッセージ | ステータスが00以外時必須 |
| 2-3 | サブエラーコード | subErrorCode | String<br>(128) | N | APPID_NOT_EXIST | エラーコードがE09301の場合のみ設定する。※イシュアから返却されるエラーコード。 |
| 2-4 | 署名 | sign | String<br>(500) | N |  |  |
| 2-5 |  | result | String | N |  | ステータスが00時のみ返却 |
| 2-5-1 | オーダ明細ID | orderDetailId | String<br>(32) | N | J1WP20161103154004945P2J | ONEPAYシステム内部のオーダ明細ID |
| 2-5-2 | オーダID | orderId | String<br>(32) | N | OWC20161104181148726rpVQ | トランザクション番号 |
| 2-5-3 | 取引<br>日時 | transTime | String<br>(14) | N | 20160926154010 | YYYYMMDDHHMMSS |
| 2-5-4 | 正札通貨 | currencyCode | String<br>(10) | N | JPY | CNY|JPY |
| 2-5-5 | 支払<br>金額 | amount | BigDecimal(15,2) | N | 3333 | 取引金額（日本円の場合、小数点以下は不要） |
| 2-5-6 | 支払金額 | amountRmb | BigDecimal(15,2) | N | 160.23 | 取引金額（人民元）<br><br>※　amountRmbの小数点以下の2桁がすべて0になることがあります（例: 1.00）。 |
| 2-5-7 | 取引ステータス | transStatus | String<br>(2) | N | 09 | オーダ明細IDに付随するステータス<br>コード定義の取引ステータスをご参照ください |
| 2-5-8 | 支払方法 | payType | String<br>(4) | N | 01 | コード定義の支払方法をご参照ください |

使用凡例

- (1)URL

https://gateway.onepay.finance/gateway/pay/version=1.0/B01/0/0/OB0244899999AShop001BTer00120190813183047778295

- (2)リクエストパラメータ

{

"amount" : "1",

"appVersion" : "ios-CpayPro-1.0.0",

"branchCode" : "AShop001",

"currencyCode" : "JPY",

"locale" : "JAPAN",

"payType" : "99",

"receiptNo" : "esdfghjklzxcvbnmqwertyuioplkjhgf",

"remark" : "test",

"sign" : "59DB82ACCEEF2A095E79D1C5E98AD605",

"terminalCode" : "BTer001",

"timeZone" : "p9",

"userCode" : "130390312172859395"

}

- (3)レスポンスパラメータ

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

"sign" : "A0B41DD563BE51B2D40DE80F28EA143C",

"result" :

{

"orderDetailId" : "J1WP20161103154004945P2J",

"orderId" : "OWC201611031540049459Ty6",

"transTime" : "20190813183048",

"currencyCode" : "JPY",

"amount" : 1,

"amountRmb" : 0.07,

"transStatus" : "00",

"payType" : "01"

}

}

}
