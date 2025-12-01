"""
Shared Enums for database models
"""
from enum import Enum


class IdType(Enum):
    ID_CARD = "身份证"
    RESIDENT_ID_CARD = "居民身份证"
    PASSPORT = "护照"
    CN_PASSPORT = "中国护照"
    FOREIGN_PASSPORT = "外国护照"
    HK_MO = "港澳通行证"
    HKMO_TRAVEL_PERMIT = "港澳居民来往内地通行证"
    TAIWAN = "台胞证"
    TAIWAN_TRAVEL_PERMIT = "台湾居民来往大陆通行证"
    HKMO_RESIDENT_PERMIT = "港澳居民居住证"
    TAIWAN_RESIDENT_PERMIT = "台湾居民居住证"
    FOREVER_RESIDENT_ID = "外国人永久居留身份证"


class UserType(Enum):
    ADULT = "成人"
    STUDENT = "学生"


class PassengerType(Enum):
    ADULT = "成人"
    STUDENT = "学生"
    CHILD = "儿童"


class TrainType(Enum):
    HIGH_SPEED = "高铁"
    BULLET = "动车"
    DIRECT = "直达"


class SeatType(Enum):
    FIRST_CLASS = "一等座"
    SECOND_CLASS = "二等座"
    SOFT_SLEEPER = "软卧"
    HARD_SLEEPER = "硬卧"


class SeatStatus(Enum):
    AVAILABLE = "可售"
    LOCKED = "已锁定"
    SOLD = "已售"


class OrderStatus(Enum):
    PENDING = "待支付"
    PAID = "已支付"
    PARTIALLY_REFUNDED = "部分退票"
    CANCELED = "已取消"
    REFUNDED = "已退票"


class RefundStatus(Enum):
    NOT_REFUNDED = "未退票"
    REFUNDED = "已退票"