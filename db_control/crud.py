# uname() error回避
import platform
print("platform", platform.uname())


from sqlalchemy import create_engine, insert, delete, update, select
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json
import pandas as pd

# from db_control.connect import engine
from db_control.connect_MySQL import engine
# from db_control.mymodels import Customers
from db_control.mymodels_MySQL import Item_master, Transaction, Transaction_Details

def selectitem(mymodel, code):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(mymodel).filter(mymodel.CODE == code)
    try:
        # トランザクションを開始
        with session.begin():
            result = query.all()
        # 結果をオブジェクトから辞書に変換し、リストに追加
        result_dict_list = []
        for item_info in result:
            result_dict_list.append({
                "prd_id": item_info.PRD_ID,
                "code": item_info.CODE,
                "name": item_info.NAME,
                "price": item_info.PRICE
            })
        # リストをJSONに変換
        result_json = json.dumps(result_dict_list, ensure_ascii=False)
    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")

    # セッションを閉じる
    session.close()
    return result_json

def register(mymodel, values):
    # session構築
    Session = sessionmaker(bind=engine)
    session = Session()

    query = insert(mymodel).values(values)
    try:
        # トランザクションを開始
        with session.begin():
            # データの挿入
            result = session.execute(query)
            # 挿入されたデータのIDを取得
            inserted_id = result.inserted_primary_key[0]
            # 挿入されたデータを取得
            inserted_data = session.query(mymodel).filter(mymodel.TRD_ID == inserted_id).first()
            result_json = json.dumps({
                "trd_id": inserted_data.TRD_ID
            }, ensure_ascii=False)

    except sqlalchemy.exc.IntegrityError:
        print("一意制約違反により、挿入に失敗しました")
        session.rollback()

    # セッションを閉じる
    session.close()
    return result_json

# def myselectAll(mymodel):
#     # session構築
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     query = select(mymodel)
#     try:
#         # トランザクションを開始
#         with session.begin():
#             df = pd.read_sql_query(query, con=engine)
#             result_json = df.to_json(orient='records', force_ascii=False)

#     except sqlalchemy.exc.IntegrityError:
#         print("一意制約違反により、挿入に失敗しました")
#         result_json = None

#     # セッションを閉じる
#     session.close()
#     return result_json


# def myupdate(mymodel, values):
#     # session構築
#     Session = sessionmaker(bind=engine)
#     session = Session()

#     customer_id = values.pop("customer_id")

#     query = update(mymodel).where(mymodel.customer_id == customer_id).values(values)
#     try:
#         # トランザクションを開始
#         with session.begin():
#             result = session.execute(query)
#     except sqlalchemy.exc.IntegrityError:
#         print("一意制約違反により、挿入に失敗しました")
#         session.rollback()
#     # セッションを閉じる
#     session.close()
#     return "put"


# def mydelete(mymodel, customer_id):
#     # session構築
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     query = delete(mymodel).where(mymodel.customer_id == customer_id)
#     try:
#         # トランザクションを開始
#         with session.begin():
#             result = session.execute(query)
#     except sqlalchemy.exc.IntegrityError:
#         print("一意制約違反により、挿入に失敗しました")
#         session.rollback()

#     # セッションを閉じる
#     session.close()
#     return customer_id + " is deleted"