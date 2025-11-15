# 铁路畅行会员服务接口文档

文档版本：v1.0  
更新日期：2025-11-14

## 概述
本接口文档用于设计与实现中国铁路12306“铁路畅行”会员服务相关API，包括会员管理、积分账户、积分补登、积分兑换、受让人管理、会员专享与站点会员服务信息查询。接口遵循统一约定，便于后续TDD与实现。

参考来源（页面证据）：
- https://cx.12306.cn/tlcx/index.html — 会员中心导航包含会员管理、积分账户、积分兑换、会员专享、帮助中心
- https://cx.12306.cn/tlcx/becomeMember.html — 成为会员需年满12周岁并完成身份认证
- https://cx.12306.cn/tlcx/certificates.html — 可用证件类型列举
- https://cx.12306.cn/tlcx/memberApp.html — 网站/APP提交→站机或窗口完成认证
- https://cx.12306.cn/tlcx/enjoyService.html — 积分获取与兑换范围说明
- https://cx.12306.cn/tlcx/jfNoCc.html — 会员服务渠道（网站/APP/车站窗口）
- https://cx.12306.cn/tlcx/jfNoCp.html — 不参与积分累积的车票类型
- https://cx.12306.cn/tlcx/howBoard.html — 漏登积分90日内可申请补登
- https://cx.12306.cn/tlcx/stations.html — 开通会员服务的车站检索

## 统一约定
- 基础路径：`/api/v1`
- 鉴权：`Authorization: Bearer <token>`（除公开接口）
- 请求头：`Content-Type: application/json`（POST/PATCH等）
- 响应包装：`{ code:number, message:string, data:any }`
- 幂等键：对需保证幂等的写操作使用`Idempotency-Key: <string>`
- 时间格式：`ISO8601`（例：`2025-11-14T09:30:00Z`）
- ID类型与枚举（依据页面与手册，部分待澄清）：
  - `idType`枚举：`居民身份证`、`港澳居民来往内地通行证`、`台湾居民来往大陆通行证`、`外国人永久居留身份证`、`港澳台居民居住证`、`护照`（当前后端枚举支持子集，需扩展，待澄清具体映射）
- 错误码与HTTP状态码：统一覆盖`400/401/403/404/409/422/429/500`

## 错误码规范
- `UNAUTHORIZED`（401）：未提供或无效的鉴权
- `FORBIDDEN_NOT_MEMBER`（403）：非会员或未认证用户尝试会员操作
- `INVALID_INPUT`（400）：参数校验失败
- `INVALID_AGE`（422）：未满12周岁不可申请会员
- `MEMBER_ALREADY_EXISTS`（409）：重复申请会员
- `NOT_MEMBER`（404）：未找到会员信息
- `BENEFICIARY_EXISTS`（409）：受让人已存在
- `BENEFICIARY_LIMIT_EXCEEDED`（422）：受让人数量达到上限（待澄清）
- `BENEFICIARY_NOT_ALLOWED`（403）：受让人未设置或不符合资格
- `INVALID_TICKET`（400）：补登票据或格式不合法
- `SUPPLEMENT_WINDOW_EXPIRED`（422）：超过90日补登窗口
- `NO_OPTIONS`（404）：无可兑换选项
- `POINTS_INSUFFICIENT`（409）：积分余额不足
- `SEAT_NOT_AVAILABLE`（422）：兑换座席不可用
- `TOO_MANY_REQUESTS`（429）：触发速率限制
- `INTERNAL_ERROR`（500）：服务器错误

## 模块与端点

### 1. 会员管理

#### 1.1 申请成为会员
- method: `POST`
- path: `/api/v1/members`
- auth: `Authorization: Bearer <token>`
- headers: `Content-Type: application/json`
- request body:
```json
{
  "name": "张三",
  "idType": "居民身份证",
  "idNumber": "123456789012345678",
  "birthDate": "2010-05-01",
  "phone": "13800138000",
  "email": "user@example.com"
}
```
- 校验规则：
  - `name:string(minLength=2)`
  - `idType:enum(见统一约定)`
  - `idNumber:string(non-empty)`
  - `birthDate:ISO8601`，需年满12周岁
  - `phone:string(pattern=^1[3-9]\d{9}$)`
  - `email:string(format=email, optional)`
- response:
```json
{ "code": 201, "message": "Created", "data": { "memberId": "m_123", "status": "pending", "submittedAt": "2025-11-14T09:30:00Z" } }
```
- status codes：`400 INVALID_INPUT`，`401 UNAUTHORIZED`，`409 MEMBER_ALREADY_EXISTS`，`422 INVALID_AGE`，`500 INTERNAL_ERROR`
- 幂等：否
- 速率限制：建议`10/min/账户`（待澄清）
- 审计：记录证件散列与时间戳

#### 1.2 查询本人会员信息
- method: `GET`
- path: `/api/v1/members/me`
- auth: `Authorization: Bearer <token>`
- response:
```json
{ "code": 200, "message": "OK", "data": { "memberId": "m_123", "status": "verified", "level": "银卡", "name": "张三", "idType": "居民身份证", "maskedIdNumber": "1234**********5678", "birthDate": "2010-05-01", "phone": "13800138000", "email": "user@example.com", "verifiedAt": "2025-11-15T10:00:00Z" } }
```
- status codes：`401 UNAUTHORIZED`，`403 FORBIDDEN_NOT_MEMBER`，`404 NOT_MEMBER`，`500 INTERNAL_ERROR`
- 幂等：是

#### 1.3 更新联系信息
- method: `PATCH`
- path: `/api/v1/members/me`
- auth: `Authorization: Bearer <token>`
- headers: `Content-Type: application/json`
- request body:
```json
{ "phone": "13800138001", "email": "new@example.com" }
```
- 校验：`phone`与`email`格式
- response：`200 Updated`
- status codes：`400 INVALID_INPUT`，`401 UNAUTHORIZED`，`409 CONFLICT_CONTACT_IN_USE`，`500 INTERNAL_ERROR`
- 幂等：是

#### 1.4 会员等级列表
- method: `GET`
- path: `/api/v1/members/levels`
- auth: `Authorization: Bearer <token>`
- response:
```json
{ "code": 200, "message": "OK", "data": [{ "code": "Silver", "name": "银卡", "threshold": 10000, "benefits": ["专享兑换" ] }] }
```
- 说明：等级阈值与权益以《会员手册》为准（待澄清）
- status codes：`401`，`500`

### 2. 积分账户

#### 2.1 查询积分余额
- method: `GET`
- path: `/api/v1/points`
- auth: `Authorization: Bearer <token>`
- response:
```json
{ "code": 200, "message": "OK", "data": { "balance": 12500, "currency": "points", "updatedAt": "2025-11-14T09:30:00Z" } }
```
- status codes：`401`，`500`

#### 2.2 查询积分流水
- method: `GET`
- path: `/api/v1/points/transactions`
- auth: `Authorization: Bearer <token>`
- query：`page:int>=1`，`size:int<=100`，`dateFrom:ISO8601`，`dateTo:ISO8601`，`type:enum[earn,redeem,supplement,expire,adjust]`，`sort:enum[time_desc,time_asc]`
- response：分页列表
```json
{ "code": 200, "message": "OK", "data": { "items": [ { "id": "pt_001", "type": "earn", "amount": 300, "occurredAt": "2025-11-10T08:00:00Z", "ref": "order_123" } ], "page": 1, "size": 20, "total": 1 } }
```
- status codes：`401`，`404`，`500`

#### 2.3 不参与积分累积的车票类型
- method: `GET`
- path: `/api/v1/points/exclusions`
- auth: `Authorization: Bearer <token>`
- response：
```json
{ "code": 200, "message": "OK", "data": { "items": [ { "type": "redeemed_ticket", "description": "积分兑换车票不参与累积" }, { "type": "substitute_ticket", "description": "代用票不参与累积" }, { "type": "onboard_supplement", "description": "列车补票不参与累积" }, { "type": "arrival_supplement", "description": "到站补票不参与累积" }, { "type": "non_realname", "description": "非实名制车票不参与累积" } ] } }
```
- 证据：`jfNoCp.html`
- status codes：`401`，`500`

#### 2.4 积分补登
- method: `POST`
- path: `/api/v1/points/supplements`
- auth: `Authorization: Bearer <token>`
- headers: `Content-Type: application/json`, `Idempotency-Key: <string>`
- request body：
```json
{ "ticketNo": "E1234567890", "trainNo": "G1234", "departDate": "2025-10-01", "passengerIdType": "居民身份证", "passengerIdNumber": "123456789012345678" }
```
- 校验：开车日期后90日内；证件与票据匹配
- response：`202 Accepted`，状态`pending`
```json
{ "code": 202, "message": "Accepted", "data": { "supplementId": "sp_001", "status": "pending" } }
```
- status codes：`400 INVALID_TICKET`，`401 UNAUTHORIZED`，`403 FORBIDDEN_NOT_MEMBER`，`409 DUPLICATE_SUPPLEMENT`，`422 SUPPLEMENT_WINDOW_EXPIRED`，`429 TOO_MANY_REQUESTS`，`500 INTERNAL_ERROR`
- 幂等：是（`Idempotency-Key`）
- 速率限制：建议`5/min/账户`（待澄清）
- 审计：票号、证件散列、时间戳

### 3. 受让人管理

#### 3.1 受让人列表
- method: `GET`
- path: `/api/v1/beneficiaries`
- auth: `Authorization: Bearer <token>`
- response：
```json
{ "code": 200, "message": "OK", "data": [ { "id": "b_001", "name": "李四", "idType": "居民身份证", "maskedIdNumber": "1234**********5678", "verified": true, "createdAt": "2025-10-02T10:00:00Z" } ] }
```
- status codes：`401`，`500`

#### 3.2 添加受让人
- method: `POST`
- path: `/api/v1/beneficiaries`
- auth: `Authorization: Bearer <token>`
- headers: `Content-Type: application/json`
- request body：
```json
{ "name": "王五", "idType": "居民身份证", "idNumber": "987654321098765432" }
```
- response：`201 Created`
```json
{ "code": 201, "message": "Created", "data": { "id": "b_002", "verified": false } }
```
- status codes：`400 INVALID_INPUT`，`401 UNAUTHORIZED`，`409 BENEFICIARY_EXISTS`，`422 BENEFICIARY_LIMIT_EXCEEDED`，`500 INTERNAL_ERROR`
- 幂等：按`memberId+idType+idNumber`去重
- 速率限制：建议`10/day`（待澄清）
- 审计：实名信息散列

#### 3.3 删除受让人
- method: `DELETE`
- path: `/api/v1/beneficiaries/{id}`
- auth: `Authorization: Bearer <token>`
- response：`200 Deleted`
- status codes：`401`，`403`，`404`，`500`
- 幂等：是

### 4. 积分兑换

#### 4.1 兑换可选项查询
- method: `GET`
- path: `/api/v1/redemptions/options`
- auth: `Authorization: Bearer <token>`
- query：`from:string(stationCode)`，`to:string(stationCode)`，`date:ISO8601`，`trainNo?:string`，`class?:enum[second,first,business]`
- response：
```json
{ "code": 200, "message": "OK", "data": { "options": [ { "product": "ticket", "trainNo": "G1234", "class": "second", "pointsCost": 8000, "seatsAvailable": 20 } ] } }
```
- status codes：`400 INVALID_QUERY`，`401 UNAUTHORIZED`，`404 NO_OPTIONS`，`500 INTERNAL_ERROR`
- 说明：可兑换范围以官方公告为准（待澄清）

#### 4.2 积分兑换车票
- method: `POST`
- path: `/api/v1/redemptions/tickets`
- auth: `Authorization: Bearer <token>`
- headers: `Content-Type: application/json`, `Idempotency-Key: <string>`
- request body：
```json
{ "passengerUse": "self", "from": "SHH", "to": "BJP", "date": "2025-11-20", "trainNo": "G1234", "class": "second", "seats": 1 }
```
- 对他人：`passengerUse:"beneficiary"`并提供`beneficiaryId`
- 校验：积分余额足够；乘车人资格；车次在指定范围；席别余座
- response：`201 Created`
```json
{ "code": 201, "message": "Created", "data": { "redemptionId": "r_001", "status": "created", "pointsCost": 8000 } }
```
- status codes：`400 INVALID_INPUT`，`401 UNAUTHORIZED`，`403 BENEFICIARY_NOT_ALLOWED`，`404 TRAIN_NOT_REDEEMABLE`，`409 POINTS_INSUFFICIENT`，`422 SEAT_NOT_AVAILABLE`，`429 TOO_MANY_REQUESTS`，`500 INTERNAL_ERROR`
- 幂等：是（`Idempotency-Key`）
- 审计：兑换明细记录

#### 4.3 查询兑换订单
- method: `GET`
- path: `/api/v1/redemptions/{id}`
- auth: `Authorization: Bearer <token>`
- response：
```json
{ "code": 200, "message": "OK", "data": { "status": "confirmed", "ticket": { "pnr": "PNR123456", "seat": "二等座 05车12A" } } }
```
- status codes：`401`，`404`，`500`

### 5. 会员专享

#### 5.1 专享权益列表
- method: `GET`
- path: `/api/v1/privileges`
- auth: `Authorization: Bearer <token>`
- response：
```json
{ "code": 200, "message": "OK", "data": [ { "code": "priority_service", "name": "优先服务", "levelRequired": "金卡", "description": "会员专享服务说明", "available": true } ] }
```
- status codes：`401`，`500`
- 说明：权益项目与条件以官方公告/会员手册为准（待澄清）

### 6. 站点会员服务查询

#### 6.1 查询开通会员服务的车站
- method: `GET`
- path: `/api/v1/stations/member-service`
- auth: `none`
- query：`q?:string(stationName)`，`page?:integer`，`size?:integer`
- response：
```json
{ "code": 200, "message": "OK", "data": { "items": [ { "stationCode": "SHH", "stationName": "上海", "hasServiceWindow": true } ], "page": 1, "size": 10, "total": 1 } }
```
- status codes：`400 INVALID_QUERY`，`404 NOT_FOUND`，`500 INTERNAL_ERROR`
- 证据：`stations.html`

## 数据模型

### Member
- 字段：`id:string(uuid)`，`userId:string`，`status:enum[pending,verified,disabled]`，`name:string`，`idType:enum(见统一约定)`，`idNumber:string`，`birthDate:ISO8601`，`phone:string`，`email?:string`，`level:string`，`createdAt:ISO8601`，`verifiedAt?:ISO8601`
- 约束：`userId`唯一；`idType+idNumber`唯一；年龄≥12周岁

### PointsAccount
- 字段：`memberId:string`，`balance:integer>=0`，`updatedAt:ISO8601`
- 约束：`memberId`唯一外键

### PointsTransaction
- 字段：`id:string`，`memberId:string`，`type:enum[earn,redeem,supplement,expire,adjust]`，`amount:integer`，`occurredAt:ISO8601`，`ref?:string`，`status:enum[posted,pending,rejected]`

### Beneficiary
- 字段：`id:string`，`memberId:string`，`name:string`，`idType:enum`，`idNumber:string`，`verified:boolean`，`createdAt:ISO8601`
- 约束：`memberId+idType+idNumber`唯一；数量上限（待澄清）

### RedemptionOrder
- 字段：`id:string`，`memberId:string`，`beneficiaryId?:string`，`productType:enum[ticket,service]`，`from:string`，`to:string`，`date:ISO8601`，`trainNo:string`，`class:enum[second,first,business]`，`seats:integer>=1`，`pointsCost:integer`，`status:enum[created,confirmed,failed,canceled]`，`createdAt:ISO8601`，`failureReason?:string`
- 幂等键：`memberId+productType+journey(from/to/date/trainNo/class)+beneficiaryId`

### StationServiceWindow
- 字段：`stationCode:string`，`stationName:string`，`hasServiceWindow:boolean`，`updatedAt:ISO8601`

### MembershipLevel
- 字段：`code:string`，`name:string`，`threshold:integer`，`benefits:string[]`
- 说明：以会员手册为准（待澄清）

## 幂等性与速率限制
- 幂等：对`POST /points/supplements`与`POST /redemptions/tickets`要求客户端提供`Idempotency-Key`，服务端在指定窗口内去重处理，返回同一资源。
- 重试策略：网络/5xx错误可重试，需复用同一`Idempotency-Key`；`4xx`错误不重试。
- 速率限制（建议值，待澄清）：
  - 申请会员：`10/min/账户`
  - 积分补登：`5/min/账户`
  - 添加受让人：`10/day/账户`
  - 兑换查询：`60/min/账户`
  - 兑换下单：`10/min/账户`

## 示例错误响应
```json
{ "code": 422, "message": "SUPPLEMENT_WINDOW_EXPIRED", "data": null }
```

## 备注与待澄清
- 会员等级与兑换规则细则以《会员手册》为准，需后续补全枚举与阈值。
- 受让人数量上限、资格条件、认证流程的具体要求需结合官方手册/公告明确。
- 积分有效期与过期策略未在页面直接给出，需运营规则补充。
- 可兑换列车/席别范围与黑白名单由官方发布控制，接口侧需支持规则查询或校验服务。