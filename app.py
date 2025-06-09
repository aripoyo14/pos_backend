from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
from sqlalchemy.orm import sessionmaker
from db_control.connect_MySQL import engine
# from db_control import crud, mymodels
from db_control import crud, mymodels_MySQL
from schemas import Barcode, ItemInfo, Transaction,TransactionDetail, TransactionId ,PurchasePrice
import math

# MySQLのテーブル作成
from db_control.create_tables_MySQL import init_db

# # アプリケーション初期化時にテーブルを作成
init_db()

app = FastAPI()
SessionLocal = sessionmaker(bind=engine)

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return {"message": "AriPOS_Lv2!"}

@app.post("/api/barcode")
def getitem(barcode: Barcode):
    result = crud.selectitem(mymodels_MySQL.Item_master, barcode.code)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    result_obj = json.loads(result)
    return result_obj[0] if result_obj else None

@app.post("/api/transaction", response_model=PurchasePrice)
def purchase(purchase_item: Transaction):
    data = purchase_item.model_dump()
    #1) ヘッダー登録
    session = SessionLocal()
    try:
        trd_id = crud.register(mymodels_MySQL.Transaction, data, session)
        
        #2) 明細登録
        for i in data.get("ITEMS", []):
            detail_vals = {
                "TRD_ID": trd_id,
                "PRD_ID":i["PRD_ID"],
                "PRD_CODE":i["PRD_CODE"],
                "PRD_NAME":i["PRD_NAME"],
                "PRD_PRICE":i["PRD_PRICE"],
                "TAX_CD":i["TAX_CD"],
                "PRD_COUNT":i["PRD_COUNT"]
            }
            crud.register(mymodels_MySQL.Transaction_Details, detail_vals, session)
            
        #3) 合計金額計算
        # 各明細ごとにprice × countを足し合わせ
        total_price = math.floor(
            sum(
                (item.PRD_PRICE * item.PRD_COUNT) * ((100+int(item.TAX_CD))*0.01)
                for item in purchase_item.ITEMS
            )
        )
        
        #4) 税抜き金額計算
        # 各明細ごとに(price × count) ÷ ((100+TAX_CD)×0.01)を足し合わせ
        total_price_no_tax = sum(item.PRD_PRICE * item.PRD_COUNT for item in purchase_item.ITEMS)

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:    
        session.close()

    # Pydanticモデルをそのまま返す
    return PurchasePrice(totalPrice=total_price, totalPriceNoTax=total_price_no_tax)

# @app.post("/customers")
# def create_customer(customer: Customer):
#     values = customer.dict()
#     # tmp = crud.myinsert(mymodels.Customers, values)
#     tmp = crud.myinsert(mymodels_MySQL.Customers, values)
#     # result = crud.myselect(mymodels.Customers, values.get("customer_id"))
#     result = crud.myselect(mymodels_MySQL.Customers, values.get("customer_id"))

#     if result:
#         result_obj = json.loads(result)
#         return result_obj if result_obj else None
#     return None


# @app.get("/customers")
# def read_one_customer(customer_id: str = Query(...)):
#     # result = crud.myselect(mymodels.Customers, customer_id)
#     result = crud.myselect(mymodels_MySQL.Customers, customer_id)
#     if not result:
#         raise HTTPException(status_code=404, detail="Customer not found")
#     result_obj = json.loads(result)
#     return result_obj[0] if result_obj else None


# @app.get("/allcustomers")
# def read_all_customer():
#     # result = crud.myselectAll(mymodels.Customers)
#     result = crud.myselectAll(mymodels_MySQL.Customers)    
#     # 結果がNoneの場合は空配列を返す
#     if not result:
#         return []
#     # JSON文字列をPythonオブジェクトに変換
#     return json.loads(result)


# @app.put("/customers")
# def update_customer(customer: Customer):
#     values = customer.dict()
#     values_original = values.copy()
#     # tmp = crud.myupdate(mymodels.Customers, values)
#     tmp = crud.myupdate(mymodels_MySQL.Customers, values)
#     # result = crud.myselect(mymodels.Customers, values_original.get("customer_id"))
#     result = crud.myselect(mymodels_MySQL.Customers, values_original.get("customer_id"))
#     if not result:
#         raise HTTPException(status_code=404, detail="Customer not found")
#     result_obj = json.loads(result)
#     return result_obj[0] if result_obj else None


# @app.delete("/customers")
# def delete_customer(customer_id: str = Query(...)):
#     # result = crud.mydelete(mymodels.Customers, customer_id)
#     result = crud.mydelete(mymodels_MySQL.Customers, customer_id)
#     if not result:
#         raise HTTPException(status_code=404, detail="Customer not found")
#     return {"customer_id": customer_id, "status": "deleted"}


@app.get("/fetchtest")
def fetchtest():
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    return response.json()
