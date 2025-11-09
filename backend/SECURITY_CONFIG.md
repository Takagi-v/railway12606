# 🔒 Railway 12306 安全配置文档

## 📋 概述

本文档详细介绍了Railway 12306系统的安全配置和实现，包括认证、授权、中间件和安全最佳实践。

## 🛡️ 安全架构

### 1. 认证系统 (Authentication)

#### JWT令牌认证
- **算法**: HS256
- **过期时间**: 7天 (10080分钟)
- **令牌格式**: Bearer Token
- **存储位置**: HTTP Authorization Header

#### 密码安全
- **加密算法**: bcrypt
- **盐值**: 自动生成随机盐值
- **密码策略**: 6-20位，包含字母和数字

### 2. 授权系统 (Authorization)

#### 用户角色
- **普通用户**: 基本购票功能
- **管理员**: 系统管理功能
- **扩展性**: 支持角色扩展

#### 权限控制
- **接口级权限**: 基于装饰器的权限验证
- **资源级权限**: 用户只能访问自己的资源
- **管理员权限**: 特殊权限验证

## 🔧 核心组件

### 1. 安全工具 (`app/core/security.py`)

```python
# 主要功能
- verify_password()      # 密码验证
- get_password_hash()    # 密码加密
- create_access_token()  # JWT令牌生成
- decode_token()         # JWT令牌解码
- get_current_user()     # 获取当前用户
```

**特性**:
- ✅ bcrypt密码加密
- ✅ JWT令牌管理
- ✅ 用户认证依赖
- ✅ 错误处理机制

### 2. 认证依赖 (`app/api/deps.py`)

```python
# 依赖函数
- get_current_user()          # 获取当前认证用户
- get_current_active_user()   # 获取当前活跃用户
- get_optional_current_user() # 可选用户认证
- require_admin()             # 管理员权限验证
- require_permissions()       # 权限验证
```

**特性**:
- ✅ 灵活的认证依赖
- ✅ 权限级别控制
- ✅ 可选认证支持
- ✅ 详细错误信息

### 3. 认证API (`app/api/v1/endpoints/auth.py`)

```python
# API端点
POST /api/auth/register    # 用户注册
POST /api/auth/login       # 用户登录
POST /api/auth/logout      # 用户登出
GET  /api/auth/test-token  # 令牌验证
POST /api/auth/refresh     # 令牌刷新
```

**特性**:
- ✅ 完整的认证流程
- ✅ 数据验证
- ✅ 错误处理
- ✅ 令牌管理

## 🛡️ 安全中间件

### 1. 安全中间件 (`SecurityMiddleware`)

**功能**:
- 添加安全HTTP头部
- 请求日志记录
- 响应时间统计
- 错误处理

**安全头部**:
```http
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

### 2. 速率限制中间件 (`RateLimitMiddleware`)

**配置**:
- 最大请求数: 100次/分钟
- 时间窗口: 60秒
- 存储方式: 内存存储 (生产环境建议使用Redis)

### 3. 请求验证中间件 (`RequestValidationMiddleware`)

**验证项目**:
- 请求体大小限制: 10MB
- Content-Type验证
- 恶意请求检测

## 🔐 CORS配置

### 配置项
```python
CORS_ORIGINS = [
    "http://localhost:5173",  # Vite开发服务器
    "http://localhost:3000"   # React开发服务器
]
```

### 安全设置
- ✅ 限制允许的源域
- ✅ 支持认证凭据
- ✅ 允许所有HTTP方法
- ✅ 允许自定义头部

## 📊 安全测试

### 1. 权限控制测试
- ✅ 无认证访问测试
- ✅ 无效令牌测试
- ✅ 过期令牌测试
- ✅ 权限验证测试

### 2. 令牌管理测试
- ✅ 令牌生成测试
- ✅ 令牌验证测试
- ✅ 令牌刷新测试
- ✅ 令牌过期测试

### 3. CORS功能测试
- ✅ 预检请求测试
- ✅ 跨域请求测试
- ✅ 安全头部测试
- ✅ 源域验证测试

### 4. 中间件测试
- ✅ 安全头部测试
- ✅ 速率限制测试
- ✅ 请求验证测试
- ✅ 错误处理测试

## ⚙️ 环境配置

### 必需环境变量
```env
# JWT配置
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# CORS配置
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]

# 数据库配置
DATABASE_URL=sqlite:///./test_railway.db
```

### 安全建议
- 🔑 SECRET_KEY必须使用强密码（至少32位）
- 🔄 定期轮换SECRET_KEY
- 🌐 生产环境限制CORS_ORIGINS
- 📝 启用详细的安全日志
- 🔒 使用HTTPS协议

## 🚀 部署安全

### 生产环境配置
1. **SECRET_KEY**: 使用强随机密钥
2. **DEBUG**: 设置为False
3. **CORS_ORIGINS**: 限制为实际前端域名
4. **HTTPS**: 强制使用HTTPS
5. **数据库**: 使用生产级数据库

### 监控和日志
- 📊 请求日志记录
- ⚠️ 安全事件告警
- 📈 性能监控
- 🔍 异常追踪

## 🔍 安全检查清单

### 认证安全
- [x] JWT令牌正确实现
- [x] 密码安全加密
- [x] 令牌过期处理
- [x] 认证错误处理

### 授权安全
- [x] 权限验证实现
- [x] 资源访问控制
- [x] 管理员权限分离
- [x] 权限错误处理

### 网络安全
- [x] CORS正确配置
- [x] 安全头部设置
- [x] 请求验证
- [x] 速率限制

### 数据安全
- [x] 密码加密存储
- [x] 敏感信息保护
- [x] 输入验证
- [x] SQL注入防护

## 📞 安全联系

如发现安全问题，请联系：
- 邮箱: security@railway12306.com
- 问题追踪: GitHub Issues
- 紧急联系: 安全团队

---

**最后更新**: 2024年10月29日  
**版本**: v1.0.0  
**状态**: ✅ 已验证通过