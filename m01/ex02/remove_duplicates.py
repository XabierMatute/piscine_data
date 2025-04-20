# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    remove_duplicates.py                               :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/04/17 13:18:55 by xmatute-          #+#    #+#              #
#    Updated: 2025/04/20 18:15:06 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


POSTGRES_CONTAINER_NAME="postgres_db"
POSTGRES_USER="xmatute-"
POSTGRES_DB="piscineds"
POSTGRES_PASSWORD="mysecretpassword"

import sys
import psycopg

from datetime import timedelta

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

collumns = [
    "event_time TIMESTAMPTZ NOT NULL",
    "event_type event_type_enum NOT NULL",
    "product_id INTEGER NOT NULL",
    "price MONEY NOT NULL",
    "user_id NUMERIC(9, 0) NOT NULL",
    "user_session UUID"
]

def get_first_time():
    sql = "SELECT MIN(event_time) FROM customers;"
    with conn.cursor() as cur:
        try:
            cur.execute(sql)
            result = cur.fetchone()
            if result and result[0]:
                return result[0]
            else:
                print("No data found in the table.")
                return None
        except psycopg.Error as e:
            print(f"Error fetching first time: {e}")
            return None

def get_last_time():
    sql = "SELECT MAX(event_time) FROM customers;"
    with conn.cursor() as cur:
        try:
            cur.execute(sql)
            result = cur.fetchone()
            if result and result[0]:
                return result[0]
            else:
                print("No data found in the table.")
                return None
        except psycopg.Error as e:
            print(f"Error fetching last time: {e}")
            return None

def remove_duplicates():
    sql = """
        CREATE TABLE temp_customers AS
        SELECT DISTINCT ON (
            event_type, 
            product_id, 
            price, 
            user_id, 
            user_session,
            date_trunc('minute', event_time)
        ) *
        FROM customers
        ORDER BY 
            event_type, 
            product_id, 
            price, 
            user_id, 
            user_session,
            date_trunc('minute', event_time),
            event_time;
        ALTER TABLE customers RENAME TO customers_with_duplicates;
        ALTER TABLE temp_customers RENAME TO customers;
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
            raise Exception(f"Error removing duplicates: {e}")

def main():
    try:
        remove_duplicates()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    
    
if __name__ == "__main__":
    main()