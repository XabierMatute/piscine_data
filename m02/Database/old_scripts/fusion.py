# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    fusion.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/04/20 18:00:46 by xmatute-          #+#    #+#              #
#    Updated: 2025/04/20 19:35:37 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

POSTGRES_CONTAINER_NAME="postgres_db"
POSTGRES_USER="xmatute-"
POSTGRES_DB="piscineds"
POSTGRES_PASSWORD="mysecretpassword"

import sys
import psycopg

print(psycopg.__version__)

try:
    conn = psycopg.connect(
        host="localhost",
        port=5432,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DB
    )
    print(f"Connected to database {POSTGRES_DB} as user {POSTGRES_USER}")
except psycopg.Error as e:
    print(f"Error connecting to database: {e}")
    sys.exit(1)

customers_collumns = [
    "event_time TIMESTAMPTZ NOT NULL",
    "event_type event_type_enum NOT NULL",
    "product_id INTEGER NOT NULL",
    "price MONEY NOT NULL",
    "user_id NUMERIC(9, 0) NOT NULL",
    "user_session UUID"
]

items_collumns = [
    "product_id INTEGER NOT NULL",
    "category_id NUMERIC(19, 0)",
    "category_code text",
    "brand VARCHAR(127)",
]

def remove_item_duplicates():
    sql = """
        CREATE TABLE temp_items AS
        SELECT DISTINCT ON (
            product_id
        ) *
        FROM items
        ORDER BY 
            product_id,
            category_id,
            category_code,
            brand
        ;
        ALTER TABLE items RENAME TO items_with_duplicates;
        ALTER TABLE temp_items RENAME TO items;
    """
    print(sql)
    with conn.cursor() as cur:
        try:
            print("Removing duplicates...")
            cur.execute(sql)
            print("Duplicates removed successfully.")
            conn.commit()
        except psycopg.Error as e:
            conn.rollback()
            # raise Exception(f"Error removing duplicates: {e}")
            print(f"Error removing duplicates: {e}")

def add_item_columns_to_customers():
    sql = """   
        ALTER TABLE customers
        ADD COLUMN category_id NUMERIC(19, 0),
        ADD COLUMN category_code text,
        ADD COLUMN brand VARCHAR(127)
    """
    print(sql)
    with conn.cursor() as cur:
        try:
            print("Adding columns to customers...")
            cur.execute(sql)
            print("Columns added successfully.")
            conn.commit()
        except psycopg.Error as e:
            conn.rollback()
            # raise Exception(f"Error adding columns: {e}")
            print(f"Error adding columns: {e}")

def fusion():
    sql = """
        UPDATE customers
        SET
            category_id = items.category_id,
            category_code = items.category_code,
            brand = items.brand
        FROM items
        WHERE customers.product_id = items.product_id;  
"""
    print(sql)
    with conn.cursor() as cur:
        try:
            print("Fusing data...")
            cur.execute(sql)
            print("Fusion completed successfully.")
            conn.commit()
        except psycopg.Error as e:
            conn.rollback()
            raise Exception(f"Error removing duplicates: {e}")

def main():
    try:
        remove_item_duplicates()
        add_item_columns_to_customers()
        fusion()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    
    
if __name__ == "__main__":
    main()