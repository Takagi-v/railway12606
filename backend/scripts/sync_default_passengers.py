"""
为所有现有用户同步默认乘车人
Sync default passengers for all existing users
"""
import sys
from pathlib import Path

# Add parent directory to path to import app modules
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.db.session import SessionLocal
from app.models.enums import PassengerType
from app.models.passenger import Passenger
from app.models.user import User
from sqlalchemy.orm import Session


def sync_default_passengers():
    """为所有用户创建或更新默认乘车人"""
    db: Session = SessionLocal()
    
    try:
        # 获取所有用户
        users = db.query(User).all()
        
        created_count = 0
        updated_count = 0
        skipped_count = 0
        
        for user in users:
            print(f"处理用户: {user.username} (ID: {user.id})")
            
            # 检查是否已有默认乘客
            default_passenger = db.query(Passenger).filter(
                Passenger.user_id == user.id,
                Passenger.is_default == True
            ).first()
            
            # Map user_type to passenger_type
            passenger_type_map = {
                "成人": PassengerType.ADULT,
                "学生": PassengerType.STUDENT
            }
            passenger_type = passenger_type_map.get(user.user_type.value, PassengerType.ADULT)
            
            if default_passenger:
                # 更新现有默认乘客
                default_passenger.name = user.real_name
                default_passenger.id_type = user.id_type
                default_passenger.id_number = user.id_number
                default_passenger.phone = user.phone
                default_passenger.passenger_type = passenger_type
                default_passenger.verified = True
                updated_count += 1
                print(f"  ✓ 更新默认乘客")
            else:
                # 检查是否存在与用户证件号相同的乘客
                existing_passenger = db.query(Passenger).filter(
                    Passenger.user_id == user.id,
                    Passenger.id_type == user.id_type,
                    Passenger.id_number == user.id_number
                ).first()
                
                if existing_passenger:
                    # 如果已存在相同证件的乘客，将其设为默认
                    existing_passenger.is_default = True
                    existing_passenger.name = user.real_name
                    existing_passenger.phone = user.phone
                    existing_passenger.passenger_type = passenger_type
                    existing_passenger.verified = True
                    updated_count += 1
                    print(f"  ✓ 将现有乘客设为默认")
                else:
                    # 创建新的默认乘客
                    new_default_passenger = Passenger(
                        user_id=user.id,
                        name=user.real_name,
                        id_type=user.id_type,
                        id_number=user.id_number,
                        phone=user.phone,
                        passenger_type=passenger_type,
                        verified=True,
                        is_default=True
                    )
                    db.add(new_default_passenger)
                    created_count += 1
                    print(f"  ✓ 创建默认乘客")
        
        # 提交所有更改
        db.commit()
        
        print("\n" + "="*50)
        print(f"同步完成！")
        print(f"总用户数: {len(users)}")
        print(f"创建: {created_count}")
        print(f"更新: {updated_count}")
        print(f"跳过: {skipped_count}")
        print("="*50)
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ 错误: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("开始为所有用户同步默认乘车人...")
    print("="*50)
    sync_default_passengers()
    print("\n✅ 脚本执行完成！")
