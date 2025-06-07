# uname() error回避
import platform
print("platform", platform.uname())


from sqlalchemy import create_engine, insert, delete, update, select
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
import json
import pandas as pd

# from db_control.connect import engine
from db_control.connect_MySQL import engine
# from db_control.mymodels import Customers
from db_control.mymodels_MySQL import Item_master, Transaction, Transaction_Details

SessionLocal = sessionmaker(bind=engine)

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

def register(mymodel, values:dict, session:Session=None):
    """
    mymodel: SQLAlchemyモデルクラス
    values: モデルのカラムにマッピング可能なキーだけを含むdict
    session: 既存セッションを渡すとそれを使い回します
    戻り値: 挿入したレコードの主キー値（例: trd_id）
    """
    own_session = False
    if session is None:
        session = SessionLocal()
        own_session = True
        
    # モデル定義から許可カラムを抽出
    allowed_cols = {c.name for c in mymodel.__table__.columns}
    filterd = {k: v for k, v in values.items() if k in allowed_cols}
    
    stmt = insert(mymodel).values(**filterd)
 
    try:
        # トランザクションを開始
        with session.begin():
            # データの挿入
            result = session.execute(stmt)
            # 挿入されたデータのIDを取得
            inserted_id = result.inserted_primary_key[0]
    except sqlalchemy.exc.IntegrityError:
        session.rollback()
        raise
    finally:
        # 外部からセッションを受け取った場合はcloseしない
        if own_session:
            session.close()
            
    return inserted_id

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