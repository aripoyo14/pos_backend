# from db_control.mymodels import Base
from db_control.mymodels_MySQL import Base
# from db_control.connect import engine
from db_control.connect_MySQL import engine
from sqlalchemy import inspect


def init_db():
    # インスペクターを作成
    inspector = inspect(engine)

    # 既存のテーブルを取得
    existing_tables = inspector.get_table_names()

    print("Checking tables...")

    # item_masterテーブルが存在しない場合は作成
    if 'item_master' not in existing_tables:
        print("Creating tables >>> ")
        try:
            Base.metadata.create_all(bind=engine)
            print("Tables created successfully!")
        except Exception as e:
            print(f"Error creating tables: {e}")
            raise
    else:
        print("Tables already exist.")

    # transactionテーブルが存在しない場合は作成
    if 'transaction' not in existing_tables:
        print("Creating tables >>> ")
        try:
            Base.metadata.create_all(bind=engine)
            print("Tables created successfully!")
        except Exception as e:
            print(f"Error creating tables: {e}")
            raise
    else:
        print("Tables already exist.")
        
    # transactionテーブルが存在しない場合は作成
    if 'transaction_details' not in existing_tables:
        print("Creating tables >>> ")
        try:
            Base.metadata.create_all(bind=engine)
            print("Tables created successfully!")
        except Exception as e:
            print(f"Error creating tables: {e}")
            raise
    else:
        print("Tables already exist.")

if __name__ == "__main__":
    init_db()

