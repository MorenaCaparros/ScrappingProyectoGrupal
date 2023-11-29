import streamlit as st
import pandas as pd
import os
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
st.write(""" ## Empezo el merge""")
df = orders[["order_id", "customer_id", "order_status"]].merge(
    order_items[["order_id","order_item_id","product_id","seller_id", "price","freight_value"]], 
    how="inner", on="order_id"
).merge(
    customers, how="left", on="customer_id"
).merge(
    order_reviews[["review_id","order_id","review_score","review_creation_date"]],
    how="left", on="order_id"
).merge(
    products[["product_id","product_category_name"]], 
    how="left", on="product_id"
).merge(
    sellers, how="left", on="seller_id"
)

st.write(""" ## Termino el merge""")

st.write("""  Traduccion de portugues a ingles""")


df["product_category_name"] = df["product_category_name"].map(
    product_category_name_translation.set_index("product_category_name")["product_category_name_english"])

#Replace null for 0 and for without_category
df['review_score'] = df['review_score'].fillna(0)
df['product_category_name'] = df['product_category_name'].fillna("without_category")


st.write("""  Eliminar comillas""")

# Elimina las comillas de los datos
df = df.replace("\"", "", regex=True)

st.write(""" Borrar una categoria porque ya la traduje antes""")
print(df.columns)


st.write(""" Creando csv""")
df_sin_duplicados = df.drop_duplicates()
df_sin_duplicados.to_csv("new_df.csv", index=False)
st.write(""" Terminando csv""")

#grouped_df = df.groupby(["customer_city", "customer_state", "geolocation_zip_code_prefix", "geolocation_city", "geolocation_state", "order_item_id", "product_id", "seller_id", "review_id", "review_score", "review_creation_date", "seller_zip_code_prefix", "seller_city", "seller_state", "product_category_name_english"])

# if os.path.exists("./new_df.csv"):
#     print("existe")
#     st.write(""" existe""")
#     df = pd.read_csv("new_df.csv")
#     print("aca")
#     df["product_category_name_english"] = df["product_category_name"].map(
#     product_category_name_translation.set_index("product_category_name")["product_category_name_english"])
#     print("translate")
    
#     df.to_csv("new_df.csv")

# else:
#     df.to_csv("new_df.csv")
#     print("no existe")
    


# Group the data by seller_id and calculate the number of orders
# st.write(""" groupby""")

# df_grouped = df.groupby("seller_id")["order_id"].count()

# # Sort the data by the number of orders
# df_grouped = df_grouped.sort_values(ascending=False)

# # Get the top 10 sellers
# st.write(""" obtener top 10""")

# top_10_sellers = df_grouped.head(10)

# # Print the top 10 sellers
# st.write(""" mostrarlos como tabla""")

# st.table(top_10_sellers, header=True, title="Los 10 mejores vendedores")
