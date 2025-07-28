💸 返金 API 知识块（Markdown）
🧾 接口概要
- 名称：返金（Refund）
- 功能描述：マーチャントシステムが支払済のオーダに対して全額または一部の返金を要求し、ONEPAYサービスシステムはそれをイシュアへ送信する。
- 使用场景：
- 顧客退货后需返金
- 超额支付或误操作需部分退款
📌 限制条件
- 退款时间限制：由 Issuer 设置有效期
- 是否支持部分退款：仅限以下支付方式：
- Alipay(01)、WechatPay(02)、LINE Pay(04)、Alipay+(GN90)
- 其他支付方式仅支持全额退款
- 是否含手续费，取决于与支付方式的签约协议

🔗 接口信息
| 字段 | 值 | 
| URL | /gateway/refund/{serviceMode}/{signType}/{isBackTran}/{token} | 
| 请求方式 | POST | 
| 数据格式 | JSON | 
| 字符编码 | UTF-8 | 



📥 请求参数说明（共通部）
| 名称 | 类型 | 是否必填 | 说明 | 
| serviceMode | String(3) | ✅ | 服务模式（B2B → B01，B2C → C01） | 
| signType | String(1) | ✅ | 签名类型，固定为 0 表示 RSA | 
| isBackTran | String(1) | ✅ | 后台交易标识，固定为 0 | 
| token | String(128) | ✅ | 接入令牌，包含商户/门店/终端编号与时间戳序列信息 | 



📥 请求参数说明（Body 部分）
| 名称 | 类型 | 必填 | 说明 | 
| locale | String(30) | ❌ | 语言标识，例：JAPAN | 
| timeZone | String(4) | ✅ | 时区，例：p9 表示 UTC+9 | 
| branchCode | String(32) | ✅ | 店铺编号（系统生成或定制） | 
| terminalCode | String(32) | ❌ | 终端编号（部分场景必填） | 
| refundAmount | BigDecimal(15,2) | ✅ | 退款金额，整数日元为主 | 
| orderId | String(32) | ❌ | 原订单编号（与其它识别字段三选一） | 
| orderDetailId | String(32) | ❌ | 原明细编号 | 
| qryToken | String(128) | ❌ | 支付时生成的 token，用于 fallback | 
| currencyCode | String(10) | ❌ | 币种（目前为 JPY） | 
| refundReason | String(256) | ❌ | 退款原因 | 
| remark | String(256) | ❌ | 备注 | 
| appVersion | String(32) | ✅ | APP版本字符串，如 ios-CpayPro-1.0.0 | 
| sign | String(500) | ✅ | 数字签名（见“签名规则”章节） | 



📤 响应参数结构
✅ meta 字段（状态）
| 名称 | 类型 | 示例 | 说明 | 
| code | String(2) | 00 | 状态码：00成功，02通信异常，09业务异常 | 
| message | String(16) | SUCCESS | 状态描述 | 


✅ data 字段（业务数据）
| 名称 | 类型 | 是否出现 | 说明 | 
| errorCode | String(6) | 异常时 | 错误编码，如 E09128 | 
| errorInfo | String(256) | 异常时 | 错误信息 | 
| subErrorCode | String(128) | 条件时 | Issuer 子错误码 | 
| sign | String(500) | 可选 | 返回签名 | 
| result | Object | 成功时有 | 返金结果对象 | 


🔹 result 子字段说明
| 名称 | 类型 | 示例 | 说明 | 
| orderDetailId | String(32) | J1VF2016... | 明细ID | 
| orderId | String(32) | OVD2016... | 订单编号 | 
| transStatus | String(2) | 06 | 状态码：06表示“返金済” | 
| currencyCode | String(10) | JPY | 币种 | 
| refundAmount | BigDecimal | 100 | 退款金额 | 
| transTime | String(14) | YYYYMMDDHHMMSS | 交易时间戳 | 



❗ 常见错误码示例（部分）
| 错误码 | 含义 | 
| E09117 | 支払が未成功のため、当該オーダは返金できません | 
| E09123 | 返金可能な額を超過しました | 
| E09128 | 返金金額が不正です | 



🧪 示例
🔹 请求示例
{
  "appVersion": "ios-CpayPro-1.0.0",
  "branchCode": "AShop001",
  "currencyCode": "JPY",
  "locale": "JAPAN",
  "orderDetailId": "J1VP20161104181148726FFl",
  "orderId": "OVD20161104181148726rpVQ",
  "qryToken": "100386873084281004qSB0sMj7FU0020180213170446674563",
  "refundAmount": "1",
  "sign": "12454DC3EF93DA19AF23B5F496FF0014",
  "terminalCode": "BTer001",
  "timeZone": "p9"
}


🔹 响应示例
{
  "meta": { "code": "00", "message": "SUCCESS" },
  "data": {
    "errorCode": "",
    "errorInfo": "",
    "sign": "819408FBAE32EF674DC3F84ED0A293BB",
    "result": {
      "orderDetailId": "J1VF20161103154306118i4Y",
      "orderId": "OVD20161104181148726rpVQ",
      "currencyCode": "JPY",
      "refundAmount": 1,
      "transStatus": "06",
      "transTime": "20190814162857"
    }
  }
}
