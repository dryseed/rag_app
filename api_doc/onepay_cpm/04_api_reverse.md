# 取消

## 概要

マーチャントシステムがステース不明のトランザクションに対して取消を要求し、ONEPAYサービスシステムはそれをイシュアへ送信する。また、オーダID、取引ステータス、取引時間等の情報を応答する。取引ステータスが不明の場合、確認APIにて確認リクエストを送信し、レスポンスの取引ステータスが「取消成功」であることを確認する必要がある。

## 使用シーン

取引ステータス不明の際に取引をキャンセルするのに使用する。


## アクセスURL

/gateway/reverse/{serviceMode}/{signType}/{isBackTran}/{token}

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
| 5 | オーダID | orderId | String<br>(32) | N | OVD20161104181148726rpVQ | オーダID、トークンいずれか必須入力<br><br>※トークン：<br>タイムアウトなど、上記のオーダID,トランザクションシリアル番号わからない場合、支払時のトークンを設定する |
| 6 | トークン | qryToken | String<br>(128) | N | 1234567890123456789012345678901220160923093712000001 | オーダID、トークンいずれか必須入力<br><br>※トークン：<br>タイムアウトなど、上記のオーダID,トランザクションシリアル番号わからない場合、支払時のトークンを設定する |
| 7 | 署名 | sign | String<br>(500) | Y |  |  |
| 8 | バージョン | appVersion | String<br>(32) | Y | ios-CpayPro-1.0.0 | サービス接続元のバージョン情報。<br>以下の情報を [-]で連結<br>(1)オペレータシステム名称(最長１０桁まで)<br>(2)APP名称(最長１０桁まで) <br>(3)APPバージョン(最長１０桁まで)<br><br>コード定義のオペレータシステムをご参照ください。 |

## レスポンスパラメータ

| 番号 | 名称 | 英名 | データ型 | 必須 | 設定例 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 |  | meta | String | Y |  |  |
| 1-1 | ステータス | code | String<br>(2) | Y | 00 | 00|02|09<br>00：成功，02：通信異常，09：異常 |
| 1-2 | 詳細 | message | String<br>(16) | Y | SUCCESS | SUCCESS|FAILURE<br>SUCCESS:成功，FAILURE：失敗 |
| 2 |  | data | String | Y |  |  |
| 2-1 | エラー<br>コード | errorCode | String<br>(6) | N | E02001 | ステータスが00以外時設定 |
| 2-2 | エラー<br>メッセージ | errorInfo | String<br>(256) | N | エラーの詳細メッセージ | ステータスが00以外時設定 |
| 2-3 | サブエラー<br>コード | subErrorCode | String<br>(128) | N | TRADE_NOT_EXIST | エラーコードがE09301の場合のみ設定する。※イシュアから返却されるエラーコード。 |
| 2-4 | 署名 | sign | String<br>(500) | N |  |  |
| 2-5 |  | result | String | N |  | ステータスが00時のみ返却 |
| 2-5-1 | オーダID | orderId | String<br>(32) | N | OVD20161104181148726rpVQ | 支払成功のONEPAYシステム内部採番したオーダID |
| 2-5-2 | オーダ明細ID | orderDetailId | String<br>(32) | N | J1VV20161104181148726FFl | ONEPAYシステム内部採番したオーダ明細ID |
| 2-5-3 | 取引<br>ステータス | transStatus | String<br>(2) | N | 10 |  |
| 2-5-4 | 取消金額 | amount | BigDecimal(15,2) | N | 100 | 取消金額 |
| 2-5-5 | 通貨 | currencyCode | String<br>(10) | N | JPY | コード定義の通貨をご参照ください |
| 2-5-6 | 取引日時 | transTime | String<br>(14) | N | 20160506102021 | YYYYMMDDHHMMSS |

## 使用凡例

### URL

https://gateway.onepay.finance/gateway/reverse/B01/0/0/OB0244899999AShop001BTer00120190814183307737756

### リクエストパラメータ

{

"appVersion" : "ios-CpayPro-1.0.0",

"branchCode" : "AShop001",

"locale" : "JAPAN",

"orderId" : "OVD20161103154408723BehP",

"sign" : "23C5ED7A5ED04C9398B1CADA59693F12",

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

"sign" : "6F42C5BE9309D0A9C15DB57AB284EE14",

"result" :

{

"orderDetailId" : "J1VV20161103154545125rfZ",

"orderId" : "OVD20161103154408723BehP",

"currencyCode" : "JPY",

"amount" : 1,

"transStatus" : "10",

"transTime" : "20190814183309"

}

}

}