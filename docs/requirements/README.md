# 需求文档分工说明

## 模块划分

本项目需求文档按功能模块划分为 **4 个独立章节**，分配给小组成员完成：

| 章节编号 | 章节名称 | 负责人 | 文件路径 |
|----------|----------|--------|----------|
| REQ-1 | 车票查询与展示 | 同学A | `1.车票查询与展示.yaml` |
| REQ-2 | 用户认证与个人中心 | 同学B | `2.用户认证与个人中心.yaml` |
| REQ-3 | 订单系统 | 同学C | `3.订单系统.yaml` |
| REQ-4 | 乘客管理 | 同学A/B/C（可选） | `4.乘客管理.yaml` |

## 目录结构

```
docs/requirements/
├── README.md                      # 本说明文档
├── assets/                        # 界面截图存放目录
│   ├── 1.车票查询与展示/
│   │   ├── 1.png
│   │   ├── 1.1.png
│   │   └── ...
│   ├── 2.用户认证与个人中心/
│   ├── 3.订单系统/
│   └── 4.乘客管理/
├── 1.车票查询与展示.yaml
├── 2.用户认证与个人中心.yaml
├── 3.订单系统.yaml
└── 4.乘客管理.yaml
```

## 填写规范

每个需求节点需包含以下字段：

```yaml
- id: REQ-X-X           # 需求编号，层级用 - 分隔
  name: 功能名称         # 简短名称
  functional_description: |  # 功能描述
    描述该功能做什么
  ui_description: |      # UI 描述
    参考图片路径: requirements/assets/X.xxx/X.X.png
    描述界面布局、组件样式等
  scenarios:             # 使用场景（可选）
    - name: 场景名称
      steps:
        - action: 用户操作
          expectation: 预期结果
  children:              # 子需求（可选）
    - id: REQ-X-X-X
      ...
```

## 关联代码路径参考

| 模块 | 前端代码路径 | 后端代码路径 |
|------|-------------|-------------|
| 车票查询 | `frontend/src/views/ticket/` | `backend/app/api/v1/endpoints/trains.py` |
| 用户认证 | `frontend/src/views/auth/` | `backend/app/api/v1/endpoints/auth.py` |
| 个人中心 | `frontend/src/views/user/` | `backend/app/api/v1/endpoints/users.py` |
| 订单系统 | `frontend/src/views/order/` | `backend/app/api/v1/endpoints/orders.py` |
| 乘客管理 | `frontend/src/views/user/PassengerPage.vue` | `backend/app/api/v1/endpoints/passengers.py` |
