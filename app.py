from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Text
from datetime import datetime
from uuid import uuid4 as uuid
import uvicorn

app = FastAPI()

products = []

# Products Model
class Product(BaseModel):
    id: Optional[str]
    name: str
    prize: float
    stock: int

@app.get("/")
def read_root():
    return {"welcome": "Welcome to my API"}

@app.get("/products")
def get_products():
    return products

@app.post("/products")
def save_product(product: Product):
    product.id = str(uuid())
    products.append(product.dict())
    return products[-1]

@app.get("/products/{product_id}")
def get_product(product_id: str):
    for product in products:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.put("/products/{product_id}")
def update_product(product_id: str, update_product: Product):
    for index, product in enumerate(products):
        if product["id"] == product_id:
            products[index]["name"] = update_product.dict()["name"]
            products[index]["prize"] = update_product.dict()["prize"]
            products[index]["stock"] = update_product.dict()["stock"]
            return {"message": "Product has been updated successfully"}
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}")
def delete_product(product_id: str):
    for index, product in enumerate(products):
        if product["id"] == product_id:
            products.pop(index)
            return {"message": "Product has been deleted successfully"}
    raise HTTPException(status_code=404, detail="Product not found")