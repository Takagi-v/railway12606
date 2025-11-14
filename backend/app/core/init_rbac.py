"""
RBAC System Initialization Script
RBAC系统初始化脚本
"""
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.role import Role, Permission
from app.models.user import User
from app.core.permissions import Permissions, Roles


def init_permissions(db: Session) -> Dict[str, Permission]:
    """
    初始化系统权限
    
    Args:
        db: 数据库会话
        
    Returns:
        Dict[str, Permission]: 权限代码到权限对象的映射
    """
    permissions_data = [
        # 用户管理权限
        {
            "name": "用户查看",
            "code": Permissions.USER_READ,
            "description": "查看用户信息",
            "resource": "user",
            "action": "read"
        },
        {
            "name": "用户创建",
            "code": Permissions.USER_CREATE,
            "description": "创建新用户",
            "resource": "user",
            "action": "create"
        },
        {
            "name": "用户更新",
            "code": Permissions.USER_UPDATE,
            "description": "更新用户信息",
            "resource": "user",
            "action": "update"
        },
        {
            "name": "用户删除",
            "code": Permissions.USER_DELETE,
            "description": "删除用户",
            "resource": "user",
            "action": "delete"
        },
        {
            "name": "用户管理",
            "code": Permissions.USER_MANAGE,
            "description": "完整的用户管理权限",
            "resource": "user",
            "action": "manage"
        },
        
        # 角色管理权限
        {
            "name": "角色查看",
            "code": Permissions.ROLE_READ,
            "description": "查看角色信息",
            "resource": "role",
            "action": "read"
        },
        {
            "name": "角色创建",
            "code": Permissions.ROLE_CREATE,
            "description": "创建新角色",
            "resource": "role",
            "action": "create"
        },
        {
            "name": "角色更新",
            "code": Permissions.ROLE_UPDATE,
            "description": "更新角色信息",
            "resource": "role",
            "action": "update"
        },
        {
            "name": "角色删除",
            "code": Permissions.ROLE_DELETE,
            "description": "删除角色",
            "resource": "role",
            "action": "delete"
        },
        {
            "name": "角色管理",
            "code": Permissions.ROLE_MANAGE,
            "description": "完整的角色管理权限",
            "resource": "role",
            "action": "manage"
        },
        
        # 权限管理权限
        {
            "name": "权限查看",
            "code": Permissions.PERMISSION_READ,
            "description": "查看权限信息",
            "resource": "permission",
            "action": "read"
        },
        {
            "name": "权限创建",
            "code": Permissions.PERMISSION_CREATE,
            "description": "创建新权限",
            "resource": "permission",
            "action": "create"
        },
        {
            "name": "权限更新",
            "code": Permissions.PERMISSION_UPDATE,
            "description": "更新权限信息",
            "resource": "permission",
            "action": "update"
        },
        {
            "name": "权限删除",
            "code": Permissions.PERMISSION_DELETE,
            "description": "删除权限",
            "resource": "permission",
            "action": "delete"
        },
        {
            "name": "权限管理",
            "code": Permissions.PERMISSION_MANAGE,
            "description": "完整的权限管理权限",
            "resource": "permission",
            "action": "manage"
        },
        
        # 订单管理权限
        {
            "name": "订单查看",
            "code": Permissions.ORDER_READ,
            "description": "查看订单信息",
            "resource": "order",
            "action": "read"
        },
        {
            "name": "订单创建",
            "code": Permissions.ORDER_CREATE,
            "description": "创建新订单",
            "resource": "order",
            "action": "create"
        },
        {
            "name": "订单更新",
            "code": Permissions.ORDER_UPDATE,
            "description": "更新订单信息",
            "resource": "order",
            "action": "update"
        },
        {
            "name": "订单删除",
            "code": Permissions.ORDER_DELETE,
            "description": "删除订单",
            "resource": "order",
            "action": "delete"
        },
        {
            "name": "订单管理",
            "code": Permissions.ORDER_MANAGE,
            "description": "完整的订单管理权限",
            "resource": "order",
            "action": "manage"
        },
        
        # 车次管理权限
        {
            "name": "车次查看",
            "code": Permissions.TRAIN_READ,
            "description": "查看车次信息",
            "resource": "train",
            "action": "read"
        },
        {
            "name": "车次创建",
            "code": Permissions.TRAIN_CREATE,
            "description": "创建新车次",
            "resource": "train",
            "action": "create"
        },
        {
            "name": "车次更新",
            "code": Permissions.TRAIN_UPDATE,
            "description": "更新车次信息",
            "resource": "train",
            "action": "update"
        },
        {
            "name": "车次删除",
            "code": Permissions.TRAIN_DELETE,
            "description": "删除车次",
            "resource": "train",
            "action": "delete"
        },
        {
            "name": "车次管理",
            "code": Permissions.TRAIN_MANAGE,
            "description": "完整的车次管理权限",
            "resource": "train",
            "action": "manage"
        },
        
        # 系统管理权限
        {
            "name": "系统管理",
            "code": Permissions.SYSTEM_ADMIN,
            "description": "系统管理员权限",
            "resource": "system",
            "action": "admin"
        }
    ]
    
    permission_map = {}
    
    for perm_data in permissions_data:
        # 检查权限是否已存在
        existing_permission = db.query(Permission).filter(
            Permission.code == perm_data["code"]
        ).first()
        
        if not existing_permission:
            permission = Permission(
                name=perm_data["name"],
                code=perm_data["code"],
                description=perm_data["description"],
                resource=perm_data["resource"],
                action=perm_data["action"],
                is_active=1
            )
            db.add(permission)
            db.flush()  # 获取ID
            permission_map[perm_data["code"]] = permission
        else:
            permission_map[perm_data["code"]] = existing_permission
    
    db.commit()
    return permission_map


def init_roles(db: Session, permission_map: Dict[str, Permission]) -> Dict[str, Role]:
    """
    初始化系统角色
    
    Args:
        db: 数据库会话
        permission_map: 权限映射
        
    Returns:
        Dict[str, Role]: 角色名称到角色对象的映射
    """
    roles_data = [
        {
            "name": Roles.SUPER_ADMIN,
            "description": "超级管理员，拥有所有权限",
            "permissions": list(permission_map.keys())  # 所有权限
        },
        {
            "name": Roles.ADMIN,
            "description": "系统管理员，拥有大部分管理权限",
            "permissions": [
                Permissions.USER_READ,
                Permissions.USER_CREATE,
                Permissions.USER_UPDATE,
                Permissions.USER_MANAGE,
                Permissions.ROLE_READ,
                Permissions.ORDER_READ,
                Permissions.ORDER_CREATE,
                Permissions.ORDER_UPDATE,
                Permissions.ORDER_MANAGE,
                Permissions.TRAIN_READ,
                Permissions.TRAIN_CREATE,
                Permissions.TRAIN_UPDATE,
                Permissions.TRAIN_MANAGE
            ]
        },
        {
            "name": Roles.MANAGER,
            "description": "业务管理员，拥有业务相关权限",
            "permissions": [
                Permissions.USER_READ,
                Permissions.ORDER_READ,
                Permissions.ORDER_CREATE,
                Permissions.ORDER_UPDATE,
                Permissions.TRAIN_READ,
                Permissions.TRAIN_UPDATE
            ]
        },
        {
            "name": Roles.USER,
            "description": "普通用户，拥有基本权限",
            "permissions": [
                Permissions.ORDER_READ,
                Permissions.ORDER_CREATE,
                Permissions.TRAIN_READ
            ]
        },
        {
            "name": Roles.GUEST,
            "description": "访客用户，只有查看权限",
            "permissions": [
                Permissions.TRAIN_READ
            ]
        }
    ]
    
    role_map = {}
    
    for role_data in roles_data:
        # 检查角色是否已存在
        existing_role = db.query(Role).filter(
            Role.name == role_data["name"]
        ).first()
        
        if not existing_role:
            role = Role(
                name=role_data["name"],
                description=role_data["description"],
                is_active=1
            )
            db.add(role)
            db.flush()  # 获取ID
            
            # 分配权限
            role_permissions = [
                permission_map[perm_code] 
                for perm_code in role_data["permissions"]
                if perm_code in permission_map
            ]
            role.permissions = role_permissions
            
            role_map[role_data["name"]] = role
        else:
            role_map[role_data["name"]] = existing_role
    
    db.commit()
    return role_map


def create_default_admin_user(db: Session, role_map: Dict[str, Role]) -> User:
    """
    创建默认管理员用户
    
    Args:
        db: 数据库会话
        role_map: 角色映射
        
    Returns:
        User: 创建的管理员用户
    """
    from app.core.security import get_password_hash
    
    # 检查是否已存在管理员用户
    existing_admin = db.query(User).filter(
        User.username == "admin"
    ).first()
    
    if existing_admin:
        return existing_admin
    
    # 创建管理员用户
    admin_user = User(
        username="admin",
        password=get_password_hash("admin123"),
        real_name="系统管理员",
        id_type="身份证",
        id_number="000000000000000000",
        phone="13800000001",
        email="admin@railway.com",
        user_type="成人",
        is_active=1
    )
    
    # 分配超级管理员角色
    if Roles.SUPER_ADMIN in role_map:
        admin_user.roles = [role_map[Roles.SUPER_ADMIN]]
    
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    print("✓ 管理员用户创建成功")
    
    return admin_user


def init_rbac_system():
    """
    初始化RBAC系统
    
    创建默认的权限、角色和管理员用户
    """
    db = SessionLocal()
    
    try:
        print("开始初始化RBAC系统...")
        
        # 1. 初始化权限
        print("正在初始化权限...")
        permission_map = init_permissions(db)
        print(f"已初始化 {len(permission_map)} 个权限")
        
        # 2. 初始化角色
        print("正在初始化角色...")
        role_map = init_roles(db, permission_map)
        print(f"已初始化 {len(role_map)} 个角色")
        
        # 3. 创建默认管理员用户
        print("正在创建默认管理员用户...")
        admin_user = create_default_admin_user(db, role_map)
        print(f"已创建管理员用户: {admin_user.username}")
        
        print("RBAC系统初始化完成！")
        print("\n默认管理员账户信息:")
        print("用户名: admin")
        print("密码: admin123")
        print("请在生产环境中及时修改默认密码！")
        
    except Exception as e:
        print(f"RBAC系统初始化失败: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_rbac_system()