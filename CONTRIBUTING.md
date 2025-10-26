# 贡献指南

感谢您对本项目的关注！这份文档将指导您如何参与项目开发。

## 开始之前

1. 阅读 [README.md](./README.md) 了解项目概况
2. 阅读 [requirement.md](./requirement.md) 了解详细需求
3. 确保本地环境配置完成

## 开发流程

### 1. 选择 Issue

在 GitHub Issues 中选择一个您想要实现的功能或修复的问题：

- 标记为 `good first issue` 的适合新手
- 标记为 `help wanted` 的需要支持
- 查看 Issue 描述了解具体需求

### 2. 创建分支

```bash
# 更新主分支
git checkout main
git pull origin main

# 创建功能分支
git checkout -b feature/issue-name

# 或创建修复分支
git checkout -b fix/issue-name
```

### 3. 开发

#### 前端开发

```bash
cd frontend
npm run dev
```

开发时注意：
- 组件应该可复用
- 使用 TypeScript 类型提示（如果适用）
- 遵循 Vue 3 Composition API 最佳实践
- 使用 Ant Design Vue 组件

#### 后端开发

```bash
cd backend
uvicorn app.main:app --reload
```

开发时注意：
- 使用类型提示
- 编写清晰的文档字符串
- 遵循 RESTful API 设计原则
- 添加适当的错误处理

### 4. 测试

#### 前端测试
- 在浏览器中测试功能
- 检查控制台是否有错误
- 测试不同的用户场景

#### 后端测试
- 访问 http://localhost:8000/api/docs 测试API
- 使用 Postman 测试复杂场景
- 检查数据库数据是否正确

### 5. 提交代码

```bash
# 添加修改的文件
git add .

# 提交（使用规范的提交信息）
git commit -m "feat: 添加车次查询功能"

# 推送到远程分支
git push origin feature/issue-name
```

### 6. 创建 Pull Request

1. 在 GitHub 上创建 Pull Request
2. 填写 PR 描述，说明：
   - 实现了什么功能
   - 解决了哪个 Issue
   - 如何测试
3. 等待代码审查
4. 根据反馈修改代码

## 代码规范

### 提交信息规范

使用约定式提交格式：

```
<类型>(<范围>): <描述>

[可选的正文]

[可选的脚注]
```

类型：
- `feat`: 新功能
- `fix`: 修复问题
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 代码重构
- `test`: 添加测试
- `chore`: 构建过程或辅助工具的变动

示例：
```
feat(train): 实现车次查询功能

- 添加车次查询API
- 实现余票计算逻辑
- 添加筛选功能

Closes #12
```

### 前端代码规范

#### 组件命名
```vue
<!-- 使用 PascalCase -->
<script setup>
// UserProfile.vue
</script>
```

#### 代码风格
```javascript
// 使用 const/let，不使用 var
const userName = 'John'

// 使用箭头函数
const handleClick = () => {
  console.log('clicked')
}

// 使用解构
const { name, age } = user
```

#### Vue 组件结构
```vue
<template>
  <!-- 模板 -->
</template>

<script setup>
// 导入
import { ref, computed } from 'vue'

// 组件逻辑
const count = ref(0)
const doubleCount = computed(() => count.value * 2)

// 方法
const increment = () => {
  count.value++
}
</script>

<style scoped>
/* 样式 */
</style>
```

### 后端代码规范

#### 函数定义
```python
def get_user_by_id(user_id: int, db: Session) -> User:
    """
    根据ID获取用户
    
    Args:
        user_id: 用户ID
        db: 数据库会话
        
    Returns:
        User: 用户对象
        
    Raises:
        HTTPException: 用户不存在时
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user
```

#### API 端点
```python
@router.get("/users/{user_id}", response_model=Response[UserResponse])
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户信息"""
    user = get_user_by_id(user_id, db)
    return Response(
        code=200,
        message="查询成功",
        data=UserResponse.model_validate(user)
    )
```

## Issue 创建指南

### 功能请求

```markdown
### 功能描述
简要描述需要实现的功能

### 详细说明
详细描述功能的实现细节和业务逻辑

### 验收标准
- [ ] 标准1
- [ ] 标准2

### 相关文档
链接到相关的需求文档或设计文档

### 技术建议
可选：给出技术实现建议
```

### Bug 报告

```markdown
### Bug 描述
简要描述问题

### 复现步骤
1. 步骤1
2. 步骤2
3. 看到错误

### 期望行为
描述期望的正确行为

### 实际行为
描述实际发生的行为

### 环境信息
- 浏览器/Python版本：
- 操作系统：
- 其他相关信息：

### 截图
如果适用，添加截图

### 可能的解决方案
可选：如果您有解决思路，请分享
```

## Pull Request 指南

### PR 标题

使用清晰的标题描述变更：

- ✅ `feat: 实现车次查询功能`
- ✅ `fix: 修复订单支付失败的问题`
- ❌ `更新代码`
- ❌ `修复bug`

### PR 描述

```markdown
## 变更说明
简要说明本次PR的目的和内容

## 关联 Issue
Closes #12

## 变更类型
- [ ] Bug 修复
- [x] 新功能
- [ ] 重构
- [ ] 文档更新

## 测试说明
如何测试这些变更：
1. 启动后端服务
2. 访问车次查询页面
3. 输入北京到上海
4. 验证结果正确显示

## 截图
如果有UI变更，请添加截图

## 检查清单
- [x] 代码遵循项目规范
- [x] 已在本地测试
- [x] 更新了相关文档
- [ ] 添加了测试用例（如果适用）
```

## 代码审查

### 审查者职责

1. 检查代码质量
2. 验证功能是否符合需求
3. 提出改进建议
4. 确保代码规范

### 提供反馈

- 友好和建设性
- 具体说明问题
- 提供改进建议
- 认可好的做法

示例：
```
✅ 建议将这个函数拆分为更小的函数，提高可读性

❌ 这段代码写得不好
```

## 开发技巧

### 前端开发

1. **使用 Vue DevTools** 调试组件状态
2. **使用 Vite 的 HMR** 快速预览更改
3. **使用 Ant Design Vue 的示例** 快速实现UI
4. **检查浏览器控制台** 查看错误和警告

### 后端开发

1. **使用 FastAPI 自动文档** (/api/docs) 测试接口
2. **使用 Postman** 保存和组织测试用例
3. **使用 Python 调试器** 定位问题
4. **查看日志** 了解程序运行状态

### 数据库

1. **使用数据库客户端** (Navicat/DBeaver) 查看数据
2. **使用 Alembic** 管理数据库迁移
3. **定期备份** 开发数据库
4. **使用事务** 确保数据一致性

## 获取帮助

如果遇到问题：

1. 查看项目文档
2. 搜索现有的 Issues
3. 查看相关技术的官方文档
4. 在 Issue 中提问
5. 联系项目维护者

## 行为准则

- 尊重他人
- 接受建设性批评
- 关注对项目最有利的事情
- 展现同理心

感谢您的贡献！🎉

