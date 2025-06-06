from pydantic import BaseModel

## バーコードスキャン
# 読み取ったバーコードの情報を受け取るためのスキーマ
class Barcode(BaseModel):
    code: str

# 商品情報を返すためのスキーマ    
class ItemInfo(BaseModel):
    code: str
    name: str
    price: int
    
## 購入
# 商品情報を受け取るためのスキーマ
class PurchaseItem(BaseModel):
    EMP_CD: str
    STORE_CD: str
    POS_NO: str
    TOTAL_AMT: int
    TTL_AMT_EX_TAX: int

# 取引一意キーを受け取るスキーマ
class TransactionId(BaseModel):
    trd_id: int

# 購入金額を返すためのスキーマ
class PurchasePrice(BaseModel):
    totalPrice: int
    totalPriceNoTax: int
