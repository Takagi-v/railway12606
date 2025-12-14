"""
Validators
通用验证器模块
"""
import re
from typing import Optional
from datetime import datetime, date
import logging
from app.core.exceptions import ValidationException
from app.core.config import settings

logger = logging.getLogger(__name__)


class UserValidator:
    """用户相关验证器"""
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """验证用户名格式"""
        if not username:
            raise ValidationException("用户名不能为空")
        
        if len(username) < 6 or len(username) > 30:
            raise ValidationException("用户名长度必须在6-30个字符之间")
        
        if not re.match(r'^[a-zA-Z0-9]+$', username):
            raise ValidationException("用户名只能包含字母和数字")
        
        return True
    
    @staticmethod
    def validate_password(password: str) -> bool:
        """验证密码强度"""
        if not password:
            raise ValidationException("密码不能为空")
        
        if len(password) < 6 or len(password) > 20:
            raise ValidationException("密码长度必须在6-20个字符之间")
        
        if not re.search(r'[a-zA-Z]', password):
            raise ValidationException("密码必须包含字母")
        
        if not re.search(r'\d', password):
            raise ValidationException("密码必须包含数字")
        
        return True
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """验证手机号格式"""
        if not phone:
            raise ValidationException("手机号不能为空")
        
        if not re.match(r'^1\d{10}$', phone):
            raise ValidationException("请输入有效的手机号")
        
        return True
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """验证邮箱格式"""
        if not email:
            raise ValidationException("邮箱不能为空")
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValidationException("请输入有效的邮箱地址")
        
        return True
    
    @staticmethod
    def validate_real_name(real_name: str) -> bool:
        """验证真实姓名"""
        if not real_name:
            raise ValidationException("真实姓名不能为空")
        
        if len(real_name) < 2 or len(real_name) > 50:
            raise ValidationException("姓名长度必须在2-50个字符之间")
        
        if not re.match(r'^[\u4e00-\u9fa5a-zA-Z\s]+$', real_name):
            raise ValidationException("姓名只能包含中文、英文字母和空格")
        
        return True
    
    @staticmethod
    def validate_id_number(id_number: str, id_type: str = "身份证") -> bool:
        """验证身份证号"""
        if not id_number:
            raise ValidationException("身份证号不能为空")
        
        # 去除首尾空格
        id_number = id_number.strip()
        
        if id_type in ("身份证", "居民身份证"):
            # 18位身份证号验证
            if not re.match(r'^\d{17}[\dXx]$', id_number):
                raise ValidationException("请输入有效的18位身份证号")
            
            # 简单的校验位验证
            weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
            check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
            
            sum_val = sum(int(id_number[i]) * weights[i] for i in range(17))
            check_code = check_codes[sum_val % 11]
            
            if id_number[17].upper() != check_code:
                if settings.DEBUG:
                    logger.warning(f"DEBUG模式: 身份证号 {id_number} 校验位错误，但在调试模式下忽略此错误。正确校验位应为: {check_code}")
                    return True
                raise ValidationException("身份证号校验位错误")
        
        return True


class TrainValidator:
    """列车相关验证器"""
    
    @staticmethod
    def validate_train_number(train_number: str) -> bool:
        """验证列车号格式"""
        if not train_number:
            raise ValidationException("列车号不能为空")
        
        # 列车号格式：字母+数字，如G123, D456, K789
        if not re.match(r'^[A-Z]\d{1,4}$', train_number):
            raise ValidationException("列车号格式不正确")
        
        return True
    
    @staticmethod
    def validate_seat_number(seat_number: str) -> bool:
        """验证座位号格式"""
        if not seat_number:
            raise ValidationException("座位号不能为空")
        
        # 座位号格式：数字+字母，如01A, 12F
        if not re.match(r'^\d{1,2}[A-F]$', seat_number):
            raise ValidationException("座位号格式不正确")
        
        return True


class OrderValidator:
    """订单相关验证器"""
    
    @staticmethod
    def validate_travel_date(travel_date: date) -> bool:
        """验证出行日期"""
        if not travel_date:
            raise ValidationException("出行日期不能为空")
        
        today = date.today()
        if travel_date < today:
            raise ValidationException("出行日期不能早于今天")
        
        # 限制最多提前60天购票
        max_advance_days = 60
        if (travel_date - today).days > max_advance_days:
            raise ValidationException(f"最多只能提前{max_advance_days}天购票")
        
        return True
    
    @staticmethod
    def validate_passenger_count(passenger_count: int) -> bool:
        """验证乘客数量"""
        if passenger_count <= 0:
            raise ValidationException("乘客数量必须大于0")
        
        if passenger_count > 5:
            raise ValidationException("单次最多只能购买5张票")
        
        return True


class CommonValidator:
    """通用验证器"""
    
    @staticmethod
    def validate_pagination(page: int, size: int) -> bool:
        """验证分页参数"""
        if page < 1:
            raise ValidationException("页码必须大于0")
        
        if size < 1 or size > 100:
            raise ValidationException("每页大小必须在1-100之间")
        
        return True
    
    @staticmethod
    def validate_not_empty(value: str, field_name: str) -> bool:
        """验证字段不为空"""
        if not value or not value.strip():
            raise ValidationException(f"{field_name}不能为空")
        
        return True
    
    @staticmethod
    def validate_length(value: str, min_length: int, max_length: int, field_name: str) -> bool:
        """验证字符串长度"""
        if len(value) < min_length or len(value) > max_length:
            raise ValidationException(f"{field_name}长度必须在{min_length}-{max_length}个字符之间")
        
        return True