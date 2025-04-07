from flask import Blueprint, render_template, url_for
import json
from .postgres_connector import PostgresDB
from dotenv import dotenv_values


config = dotenv_values(".env")
views = Blueprint("views", __name__)


@views.route("/")
def dashboard_home():
    return render_template("dashboard.html")


@views.route("/metrics")
def get_metrics():
    try:
        db = PostgresDB(
            host=config["PG_HOST"],
            port=config["PG_PORT"],
            user=config["PG_USER"],
            pw=config["PG_PASS"],
            db=config["SALES_DB"],
        )
        total_sales = db.read_one("SELECT SUM(billed_amount) FROM fact_transaction")[0]
        total_orders = db.read_one("SELECT COUNT(DISTINCT transaction_id) FROM fact_transaction")[0]
        total_products_sold = db.read_one("SELECT SUM(quantity) FROM fact_transaction")[0]
        max_order_value = db.read_one(
            """SELECT MAX(order_value) FROM 
                                    (SELECT transaction_id, SUM(billed_amount) AS order_value 
                                    FROM fact_transaction GROUP BY transaction_id) 
                                    AS transaction_data;"""
        )[0]
        average_order_value = db.read_one(
            """SELECT AVG(order_value) FROM 
                                    (SELECT transaction_id, SUM(billed_amount) AS order_value 
                                    FROM fact_transaction GROUP BY transaction_id) 
                                    AS transaction_data;"""
        )[0]

        metrics = {
            "total_sales": total_sales if total_sales else 0,
            "total_orders": total_orders if total_orders else 0,
            "max_order_value": max_order_value if max_order_value else 0,
            "total_products_sold": total_products_sold if total_products_sold else 0,
            "average_order_value": (
                float(average_order_value) if average_order_value else 0
            ),
        }
    except Exception as e:
        print(f"An Unexpected error occured: {e}")
        metrics = {}

    return json.dumps(metrics)
