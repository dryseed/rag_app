インターフェース概要
通信プロトコルと伝送方式
ONEPAYシステムへ接続する上で必要となる通信プロトコルと伝送方式等について下記のように定める。
パラメータ規定
サービス接続モード
OnePayへの接続には「B2Cモード」と「B2Bモード」がある。それにより、いくつかのインターフェース項目
の設定値が異なる場合がある。「B2Cモード」と「B2Bモード」の説明は以下に示す。
（1）B2Cモード　：クライアント－サーバー間通信。iOS/androidアプリ等の端末から、直接OnePayへ接続する方式である。
（2）B2Bモード　：サーバー間通信。ゲートウェイなどのサーバーから、OnePayへ接続する方式である。
デジタル署名
通信データの正確性、完全性を確保するため、送信時はデジタル署名を作成し、受信時はデジタル署名を検証する。
(1)リクエストパラメータのsign以外の項目を、アルファベット順でソートする。（大文字、小文字を区別しない）
(2)項目（Key）と値（Value）の間は「＝」で連結し、項目と項目の間は「&」で連結する。
※Keyが存在し、かつValueが空白フィールドの場合でも、デジタル署名を行う必要がある。尚、空白フィールドとは、スペース （0x20）、タブ(0x09)、エンター(0x0d)、改行(0x0a)、空文字の５つを意味する。nullの場合は、署名対象とならない。
(3)連結した内容を{}括弧で括る。
例 ）項目と値の内容が下記①の場合、連結したデータは下記③のようになる。
① service=create_order, partner_id=1001201111111212, trans_type=
② partner_id=1001201111111212&service=create_order&trans_type=
③ {partner_id=1001201111111212&service=create_order&trans_type=}
(4)SHA-256によって(3)のデータをハッシュ化する。(16進文字列、且つ大文字である)
(5)デジタル証明書（秘密キー2048）によって署名する。署名のアルゴリズムは、SHA1WithRSAとなる。
(6)BASE64にて２回エンコードし、signフィールドに設定する。
※：デジタル署名検証の流れが同様です。署名検証の際には、サーバー側から応答するsignをBase６４で2回デコードする
インターフェース詳細
支払
概要
マーチャントシステムから受け取った支払リクエストをイシュアへ送信する。また、オーダIDや取引ステータス、取引時間等の情報を応答する。
使用シーン
(1)ユーザがバーコード／QRコードを提示し、店員がそれをマーチャントシステムに読み込む。読み込んだ支払情報を本システムへ送信し、支払手続きを完成するのに使用する。
(2)フロー
アクセスURL
/gateway/pay/{data}/{serviceMode}/{signType}/{isBackTran}/{token}
リクエストパラメータ（共通部）
リクエストパラメータ
レスポンスパラメータ
	使用凡例
	(1)URL
https://gateway.onepay.finance/gateway/pay/version=1.0/B01/0/0/OB0244899999AShop001BTer00120190813183047778295
	(2)リクエストパラメータ
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
(3)レスポンスパラメータ
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

返金
概要
マーチャントシステムが支払済のオーダに対して全額または一部の返金を要求し、ONEPAYサービスシステム
はそれをイシュアへ送信する。
※ 返金可能な実効期間はイシュアより設定され、手数料も含む返金か否かは支払方法との契約に
よるものとなる。
※　Alipay(01)、WechatPay(02) 、LINE Pay(04)、Alipay+(GN90) のみが一部返金を利用可能です。
それ以外の支払方法は全額返金のみをサポートしています。
使用シーン
お客様から返送された商品を受領した後、それに応じる金額を払い戻すのに使用する。
フロー
アクセスURL
 /gateway/refund/{serviceMode}/{signType}/{isBackTran}/{token}
リクエストパラメータ（共通部）
リクエストパラメータ
レスポンスパラメータ
使用凡例
URL
https://gateway.onepay.finance/gateway/refund/B01/0/0/OB0244899999AShop001BTer00120190814162855548406
リクエストパラメータ
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
レスポンスパラメータ
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

取消
概要
マーチャントシステムがステース不明のトランザクションに対して取消を要求し、ONEPAYサービスシステムはそれをイシュアへ送信する。また、オーダID、取引ステータス、取引時間等の情報を応答する。取引ステータスが不明の場合、確認APIにて確認リクエストを送信し、レスポンスの取引ステータスが「取消成功」であることを確認する必要がある。
使用シーン
取引ステータス不明の際に取引をキャンセルするのに使用する。
フロー
アクセスURL
/gateway/reverse/{serviceMode}/{signType}/{isBackTran}/{token}
リクエストパラメータ（共通部）
リクエストパラメータ
レスポンスパラメータ
使用凡例
URL
	https://gateway.onepay.finance/gateway/reverse/B01/0/0/OB0244899999AShop001BTer00120190814183307737756
リクエストパラメータ
	{
		"appVersion" : "ios-CpayPro-1.0.0",
		"branchCode" : "AShop001",
		"locale" : "JAPAN",
		"orderId" : "OVD20161103154408723BehP",
		"sign" : "23C5ED7A5ED04C9398B1CADA59693F12",
		"terminalCode" : "BTer001",
		"timeZone" : "p9"
	} 
レスポンスパラメータ
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

オーダ照会
概要
オーダ情報について最新のステータスを照会する。
リクエストパラメ―タの設定により、単一または複数のオーダを照会することが可能。
使用シーン
(1)取引ステータス不明の際にONEPAYに問い合わせるのに使用する。
(2)フロー
アクセスURL
 /gateway/orderQuery/{data}/{serviceMode}/{signType}/{isBackTran}/{token}
リクエストパラメータ（共通部）
リクエストパラメータ
	注：オーダID、オーダ明細ID、レシート番号、端末番号、バーコード、日付すべてが未入力の場合、エラーとする
レスポンスパラメータ
使用凡例
(1)URL
	https://gateway.onepay.finance/gateway/orderQuery/version=1.0/B01/0/0/OB0244899999AShop001BTer00120190814183307730477
(2)リクエストパラメータ（個別部）
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
(3)レスポンスパラメータ
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
確認
概要
マーチャントシステムがステータス不明のトランザクションに対して確認を要求し、最新のステータスを取得する。重複して呼び出すことも可能だが、成功したトランザクションには確認要求を送信しないことを推奨する。
使用シーン
(1)取引ステータス不明の際にイシュアに問い合わせるのに使用する。
(2)フロー
アクセスURL
/gateway/confirm/{data}/{serviceMode}/{signType}/{isBackTran}/{token}
リクエストパラメータ（共通部）
リクエストパラメータ
レスポンスパラメータ
使用凡例
(1)URL
	https://gateway.onepay.finance/gateway/confirm/version=1.0/B01/0/0/OB0244899999AShop001BTer00120190814164943745172
(2)リクエストパラメータ
{
	"branchCode" : "AShop001",
	"locale" : "JAPAN",
	"orderDetailId" : "J1WP201611031544087236Kw",
	"orderId" : "OWC20161103154408723BehP",
	"sign" : "804C46C0A71DA29CE2D0E77A007A7627",
	"terminalCode" : "BTer001",
	"timeZone" : "p9"
}
(3)レスポンスパラメータ
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
コード定義
通貨
現時点、JPY以外の通貨はサポートしない。
注：返金と支払の通貨単位は同じでなければならない。
取引ステータス
支払方法
支払方式とも呼ばれている。
オペレータシステム
エラーコード
APIステータス：00|02|09
00: 成功
02: ネット通信異常
09: 異常
1：パラメータチェック異常
2：データベース関連異常および予期せぬシステム異常
3：イシュアから戻って来る異常
9：セキュリティ、権限など異常
##凡例：E           09           1           01
##凡例：固定    異常タイプ     サブタイプ    エラーコード
※サブエラーコード（ONEPAY集約したサブエラーコードを以下に示す。）
-- END--