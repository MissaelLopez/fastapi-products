from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Text
from datetime import datetime
from uuid import uuid4 as uuid
from starlette.requests import Request
from starlette.responses import Response
import uvicorn
from fastapi.templating import Jinja2Templates

app = FastAPI()

products = []

templates = Jinja2Templates(directory="templates")

# Products Model


class Product(BaseModel):
    id: Optional[str]
    name: str
    price: float
    stock: int


@app.get("/api")
def api_root():
    return {"welcome": "Welcome to my FastAPI"}

@app.get("/api/products")
def get_products():
    return products


@app.post("/api/products")
def save_product(product: Product):
    product.id = str(uuid())
    products.append(product.dict())
    return products[-1]


@app.get("/api/products/{product_id}")
def get_product(product_id: str):
    for product in products:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")


@app.put("/api/products/{product_id}")
def update_product(product_id: str, update_product: Product):
    for index, product in enumerate(products):
        if product["id"] == product_id:
            products[index]["name"] = update_product.dict()["name"]
            products[index]["prize"] = update_product.dict()["prize"]
            products[index]["stock"] = update_product.dict()["stock"]
            return {"message": "Product has been updated successfully"}
    raise HTTPException(status_code=404, detail="Product not found")


@app.delete("/api/products/{product_id}")
def delete_product(product_id: str):
    for index, product in enumerate(products):
        if product["id"] == product_id:
            products.pop(index)
            return {"message": "Product has been deleted successfully"}
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/")
def index(req: Request):
    return templates.TemplateResponse("index.html", {"request": req})

@app.get("/products")
def list_products(req: Request):
    return templates.TemplateResponse("products-list.html", {"request": req, "products": products})