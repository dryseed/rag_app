# 確認

## 概要

マーチャントシステムがステータス不明のトランザクションに対して確認を要求し、最新のステータスを取得する。重複して呼び出すことも可能だが、成功したトランザクションには確認要求を送信しないことを推奨する。

## 使用シーン

取引ステータス不明の際にイシュアに問い合わせるのに使用する。


## アクセスURL

/gateway/confirm/{data}/{serviceMode}/{signType}/{isBackTran}/{token}

## リクエストパラメータ（共通部）

| 番号 | 名称 | 英名 | データ型 | 必須 | 設定値 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | URL拡張データ | data | String<br>(32) | Y | version=1.0 | URLの拡張部<br>現時点、ｖersion=1.0のみ指定可能 |
| 2 | サービス接続モード | serviceMode | String<br>(3) | Y | B01 | B2Cモードの場合：C01<br>B2Bモードの場合：B01 |
| 3 | 署名<br>方式 | signType | String<br>(1) | Y | 0 | 0:RSA(B2Bの場合、RSAのみサポート) |
| 4 | バックエンドフラグ | isBackTran | String | Y | 0 | バックエンドによるトランザクション<br>0：いいえ |
| 5 | トークン | token | String<br>(128) | Y | 100386873084281004qSB0sMj7FU0020180213170446674563 | B2Bモードの場合：<br>ﾏｰﾁｬﾝﾄID（12桁）+ｶｽﾀﾏｲｽﾞの店舗ｺｰﾄﾞ(最長32桁)＋ｶｽﾀﾏｲｽﾞの端末ｺｰﾄﾞ(最長32桁※)+14桁ﾀｲﾑｽﾀﾝﾌﾟ+6桁ｼﾘｱﾙ<br>B2Cモードの場合：<br>14桁店舗コード+16桁端末コード+14桁タイムタンプ+6桁シリアル |

## リクエストパラメータ

| 番号 | 名称 | 英名 | データ型 | 必須 | 設定値 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | ロケール | locale | String<br>(32) | N | JAPAN | 国際化コード（US：英語,CHINA：中国語, JAPAN：日本語） |
| 2 | タイム<br>ゾーン | timeZone | String<br>(4) | Y | P9 | タイムゾーン（日本はUTC+9） |
| 3 | 店舗コード | branchCode | String<br>(32) | Y | B2C:<br>10036859104261<br>B2B:<br>AShop001 | B2Cモードの場合：<br>ONEPAYシステム内部の店舗コード<br>B2Bモードの場合：<br>加盟店内部のｶｽﾀﾏｲｽﾞ店舗コード |
| 4 | 端末コード | terminalCode | String<br>(32) | N | B2C:<br>10040bQQW23GEWEA B2B:<br>BTer001 | B2Cモードの場合(必須)：<br>ONEPAYシステム内部の端末コード<br>B2Bモードの場合：<br>加盟店内部のｶｽﾀﾏｲｽﾞ端末コード |
| 5 | オーダID | orderId | String<br>(32) | N | OWC20161104181148726rpVQ |  |
| 6 | オーダ<br>明細ID | orderDetailId | String<br>(32) | N | J1WP20161104181148726FFl | ONEPAYシステム内部のオーダ明細ID |
| 7 | 署名 | sign | String<br>(500) | Y | 1234567890123456789012345678901 |  |
| 8 | トークン | qryToken | String<br>(128) | N | 1234567890123456789012345678901 | オーダ明細ID，トークンいずれか必須入力 |
| 9 | 照会フラグ | queryFlg | String<br>(2) | N | 1　固定 | 1：OnePayシステムの最新状態を照会&更新 |

## レスポンスパラメータ

| 番号 | 名称 | 英名 | データ型 | 必須 | 設定値 | 説明 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 |  | meta | String | Y |  |  |
| 1-1 | ステータス | code | String<br>(2) | Y | 00 | 00|02|09<br>00:成功，02：通信異常，09：異常 |
| 1-2 | 詳細 | message | String<br>(16) | Y | SUCCESS | SUCCESS|FAILURE<br>SUCCESS:成功，FAILURE：失敗 |
| 2 |  | data | String | Y |  |  |
| 2-1 | エラーコード | errorCode | String<br>(6) | N | E02001 | ステータスが00以外時必須 |
| 2-2 | エラー<br>メッセージ | errorInfo | String<br>(256) | N | エラーの詳細メッセージ | ステータスが00以外時必須 |
| 2-3 | サブエラーコード | subErrorCode | String<br>(128) | N | APPID_NOT_EXIST | エラーコードがE09301の場合のみ設定する。※イシュアから返却されるエラーコード。 |
| 2-4 | 署名 | sign | String<br>(500) | N |  |  |
| 2-5 |  | result | String | N |  | ステータスが00時のみ返却 |
| 2-5-1 | 取引ステータス | transStatus | String<br>(2) | N | 01 | オーダ明細IDに付随するステータス<br>コード定義の取引ステータスをご参照ください |
| 2-5-2 | 確認<br>日付 | payCheckDate | String<br>(8) | N | 20160502 | yyyyMMdd |
| 2-5-3 | 取引<br>日時 | transTime | String<br>(14) | N | 20160926154010 | YYYYMMDDHHMMSS |
| 2-5-4 | オーダID | orderId | String<br>(32) | N | OWC201611031003138263FF6 | ONEPAYシステム内部のオーダID |
| 2-5-5 | オーダ明細ID | orderDetailId | String<br>(32) | N | J1WF20161103100437632gCM | ONEPAYシステム内部のオーダ明細ID |
| 2-5-6 | 支払方法 | payType | String<br>(4) | N | 01 | コード定義の支払方法をご参照ください |

## 使用凡例

### URL

https://gateway.onepay.finance/gateway/confirm/version=1.0/B01/0/0/OB0244899999AShop001BTer00120190814164943745172

### リクエストパラメータ

{

"branchCode" : "AShop001",

"locale" : "JAPAN",

"orderDetailId" : "J1WP201611031544087236Kw",

"orderId" : "OWC20161103154408723BehP",

"sign" : "804C46C0A71DA29CE2D0E77A007A7627",

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

"sign" : "8E0BFEB360F6FD97F5EA4EEDBA25ABC0",

"result" :

{

"transStatus" : "06",

"payCheckDate" : "20190814",

"transTime" : "20190814162857",

"orderId" : "OWC20161103154408723BehP",

"orderDetailId" : "J1WP201611031544087236Kw",

"payType" : "01"

}

}

}