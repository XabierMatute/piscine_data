# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    customers_table.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/04/17 12:14:14 by xmatute-          #+#    #+#              #
#    Updated: 2025/04/17 12:28:44 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

POSTGRES_CONTAINER_NAME="postgres_db"
POSTGRES_USER="xmatute-"
POSTGRES_DB="piscineds"
POSTGRES_PASSWORD="mysecretpassword"

import sys
import psycopg

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

def create_table(table_name, columns):
    sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"
    print(sql)
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql)
            print(f"Table {table_name} created successfully.")
            conn.commit()
    except psycopg.Error as e:
        print(f"Error creating table: {e}")
        conn.rollback()
        raise Exception(f"Error creating table: {e}")

def populate_customers_table():
    pass #TODO

def create_customers_table():
    create_table("customers", collumns)
    populate_customers_table()
    

def main():
    try:
        create_customers_table()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    
    
if __name__ == "__main__":
    main()