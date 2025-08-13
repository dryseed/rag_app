# 返金

## 概要

マーチャントシステムが支払済のオーダに対して全額または一部の返金を要求し、ONEPAYサービスシステム
はそれをイシュアへ送信する。

返金可能な実効期間はイシュアより設定され、手数料も含む返金か否かは支払方法との契約によるものとなる。

Alipay(01)、WechatPay(02) 、LINE Pay(04)、Alipay+(GN90) のみが一部返金を利用可能です。それ以外の支払方法は全額返金のみをサポートしています。

## 使用シーン

お客様から返送された商品を受領した後、それに応じる金額を払い戻すのに使用する。

## アクセスURL

/gateway/refund/{serviceMode}/{signType}/{isBackTran}/{token}

## リクエストパラメータ（共通部）

| 番号 | 名称 | 英名 | データ型 | 必須 | 設定例 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | サービス<br>接続モード | serviceMode | String<br>(3) | Y | B01 | B2Bモードの場合：B01<br>B2Cモードの場合：C01 |
| 2 | 署名<br>方式 | signType | String<br>(1) | Y | 0 | 0:RSA |
| 3 | バックエンドフラグ | isBackTran | String<br>(1) | Y | 0 | バックエンドによるトランザクション<br>0：いいえ |
| 4 | トークン | token | String<br>(128) | Y | 100386873084281004qSB0sMj7FU0020180213170446674563 | B2Bモードの場合：<br>マーチャントID（12桁）+ｶｽﾀﾏｲｽﾞの店舗ｺｰﾄﾞ(最長32桁)＋ｶｽﾀﾏｲｽﾞの端末ｺｰﾄﾞ(最長32桁)<br>+14桁ﾀｲﾑｽﾀﾝﾌﾟ+6桁ｼﾘｱﾙ<br>B2Cモードの場合：<br>14桁店舗コード+16桁端末コード+14桁タイムタンプ+6桁シリアル |

## リクエストパラメータ

| 番号 | 名称 | 英名 | データ型 | 必須 | 設定例 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | ロケール | locale | String<br>(30) | N | JAPAN | 国際化コード（US：英語,CHINA：中国語, JAPAN：日本語） |
| 2 | タイム<br>ゾーン | timeZone | String<br>(4) | Y | p9 | タイムゾーン（日本はUTC+9） |
| 3 | 店舗コード | branchCode | String<br>(32) | Y | B2B:<br>AShop001<br>B2C：<br>10036859104261 | B2Bモードの場合：<br>加盟店内部のｶｽﾀﾏｲｽﾞ店舗コード<br>B2Cモードの場合：<br>ONEPAYシステム内部の店舗コード |
| 4 | 端末コード | terminalCode | String<br>(32) | N | B2B:<br>BTer001<br>B2C：<br>10040bQQW23GEWEA | B2Bモードの場合：<br>加盟店内部のｶｽﾀﾏｲｽﾞ端末コード<br>B2Cモードの場合(必須)：<br>ONEPAYシステム内部の端末コード |
| 5 | 返金金額 | refundAmount | BigDecimal(15，2) | Y | 100 | 返金金額（小数点不要） |
| 6 | 元オーダID | orderId | String<br>(32) | N | OVD20161104181148726rpVQ | 元オーダID、元オーダ明細ID、トークン<br>いずれかは設定必須<br><br>※トークン：<br>タイムアウトなど、上記のオーダID, オーダ明細IDわからない場合、支払時のトークンを設定する |
| 7 | 元オーダ明細ID | orderDetailId | String<br>(32) | N | J1VP20161104181148726FFl | 元オーダID、元オーダ明細ID、トークン<br>いずれかは設定必須<br><br>※トークン：<br>タイムアウトなど、上記のオーダID, オーダ明細IDわからない場合、支払時のトークンを設定する |
| 8 | トークン | qryToken | String<br>(128) | N | 100386873084281004qSB0sMj7FU0020180213170446674563 | 元オーダID、元オーダ明細ID、トークン<br>いずれかは設定必須<br><br>※トークン：<br>タイムアウトなど、上記のオーダID, オーダ明細IDわからない場合、支払時のトークンを設定する |
| 9 | 通貨 | currencyCode | String<br>(10) | N | JPY | コード定義の通貨をご参照ください |
| 10 | 返金理由 | refundReason | String<br>(256) | N |  |  |
| 11 | 備考 | remark | String<br>(256) | N |  |  |
| 12 | バージョン | appVersion | String<br>(32) | Y | ios-CpayPro-1.0.0 | サービス接続元のバージョン情報。<br>以下の情報を [-]で連結<br>(1)オペレータシステム名称(最長１０桁まで)<br>(2)APP名称(最長１０桁まで) <br>(3)APPバージョン(最長１０桁まで)<br><br>コード定義のオペレータシステムをご参照ください。 |
| 13 | 署名 | sign | String<br>(500) | Y |  |  |

## レスポンスパラメータ

| 番号 | 名称 | 英名 | データ型 | 必須 | 設定例 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 |  | meta | String | Y |  |  |
| 1-1 | ステータス | code | String<br>(2) | Y | 00 | 00|02|09<br>00：成功，02：通信異常，09：異常 |
| 1-2 | 詳細 | message | String<br>(16) | Y | SUCCESS | SUCCESS|FAILURE<br>SUCCESS:成功，FAILURE：失敗 |
| 2 |  | data | String | Y |  |  |
| 2-1 | エラー<br>コード | errorCode | String<br>(6) | N | E02001 | ステータスが00以外時設定 |
| 2-2 | エラー<br>メッセージ | errorInfo | String<br>(256) | N | エラーの詳細メッセージ | ステータスが00以外時設定 |
| 2-3 | サブエラーコード | subErrorCode | String<br>(128) | N | TRADE_NOT_EXIST | エラーコードがE09301の場合のみ設定する。※イシュアから返却されるエラーコード。 |
| 2-4 | 署名 | sign | String<br>(500) | N |  |  |
| 2-5 |  | result | String | N |  | ステータスが00時のみ返却 |
| 2-5-1 | 元オーダID | orderId | String<br>(32) | N | OVD20161104181148726rpVQ | 支払成功のONEPAYシステム内部採番したオーダID |
| 2-5-2 | オーダ明細ID | orderDetailId | String<br>(32) | N | J1VF20161104181148726FFl | ONEPAYシステム内部のオーダ明細ID |
| 2-5-3 | 取引<br>ステータス | transStatus | String<br>(2) | N | 06 | コード定義の取引ステータスをご参照ください |
| 2-5-4 | 通貨 | currencyCode | String<br>(10) | N | JPY | 通貨 |
| 2-5-5 | 返金金額 | refundAmount | BigDecimal(15,2) | N | 100 | 返金金額 |
| 2-5-6 | 取引日時 | transTime | String<br>(14) | N | 20160506102021 | YYYYMMDDHHMMSS |

## 使用凡例

### URL

https://gateway.onepay.finance/gateway/refund/B01/0/0/OB0244899999AShop001BTer00120190814162855548406

### リクエストパラメータ

{

"appVersion" : "ios-CpayPro-1.0.0",

"branchCode" : "AShop001",

"currencyCode" : "JPY",

"locale" : "JAPAN",

"orderDetailId" : "J1VP20161104181148726FFl ",

"orderId" : "OVD20161104181148726rpVQ ",

"qryToken" : "100386873084281004qSB0sMj7FU0020180213170446674563",

"refundAmount" : "1",

"sign" : "12454DC3EF93DA19AF23B5F496FF0014",

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

"sign" : "819408FBAE32EF674DC3F84ED0A293BB",

"result" :

{

"orderDetailId" : "J1VF20161103154306118i4Y",

"orderId" : "OVD20161104181148726rpVQ ",

"currencyCode" : "JPY",

"refundAmount" : 1,

"transStatus" : "06",

"transTime" : "20190814162857"

}

}

}