import streamlit as st
import pandas as pd
import pyxlsb
from pyxlsb import open_workbook
import pip

try:
    import xlwings
except ImportError:
    pip.install('xlwings')

import xlwings as xw

print(xw.__version__)

# PARA CORRER LA APP EN STREAMLIT --> 
# st run c:/Users/moren/OneDrive/Documents/scrapProyectogrupal/main.py

st.write("""
# My first app
Hello *world!*
""")

geolocation = pd.read_csv("e-comerce_Olist_dataset/olist_geolocation_dataset.csv")
orders = pd.read_csv("e-comerce_Olist_dataset/olist_orders_dataset.csv")
order_items = pd.read_csv("e-comerce_Olist_dataset/olist_order_items_dataset.csv")
customers = pd.read_csv("e-comerce_Olist_dataset/olist_customers_dataset.csv")
order_payments = pd.read_csv("e-comerce_Olist_dataset/olist_order_payments_dataset.csv")
order_reviews = pd.read_csv("e-comerce_Olist_dataset/olist_order_reviews_dataset.csv")
products = pd.read_csv("e-comerce_Olist_dataset/olist_products_dataset.csv")
sellers = pd.read_csv("e-comerce_Olist_dataset/olist_sellers_dataset.csv")
product_category_name_translation = pd.read_csv("e-comerce_Olist_dataset/product_category_name_translation.csv")
closed_deals = pd.read_csv("olist_Funnel_marketing/olist_closed_deals_dataset.csv")
marketing_leads = pd.read_csv("olist_Funnel_marketing/olist_marketing_qualified_leads_dataset.csv")



# Merge the datasets

df = orders[["order_id", "customer_id"]].merge(
    customers, how="left", on="customer_id"
).merge(
    geolocation[[
        "geolocation_zip_code_prefix",
        "geolocation_city",
        "geolocation_state"
    ]], how="left", left_on="customer_zip_code_prefix", right_on="geolocation_zip_code_prefix"
).merge(
    order_items[["order_id","order_item_id","product_id","seller_id"]], 
    how="left", on="order_id"
).merge(
    order_reviews[["review_id","order_id","review_score","review_creation_date"]],
    how="left", on="order_id"
).merge(
    products[["product_id","product_category_name"]], 
    how="left", on="product_id"
).merge(
    sellers, how="left", on="seller_id"
).merge(
    closed_deals[["mql_id","seller_id", "business_segment", "declared_product_catalog_size"]], how="left", on="seller_id" 
)

# Translate the product category names
df["product_category_name_english"] = df["product_category_name"].map(
    product_category_name_translation.set_index("product_category_name")["product_category_name_english"]
)

# Group the data by seller_id and calculate the number of orders
df_grouped = df.groupby("seller_id")["order_id"].count()

# Sort the data by the number of orders
df_grouped = df_grouped.sort_values(ascending=False)

# Get the top 10 sellers
top_10_sellers = df_grouped.head(10)

# Print the top 10 sellers
print(top_10_sellers)