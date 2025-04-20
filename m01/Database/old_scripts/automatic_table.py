# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    automatic_table.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/04/17 11:05:42 by xmatute-          #+#    #+#              #
#    Updated: 2025/04/20 21:17:08 by xmatute-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

POSTGRES_CONTAINER_NAME="postgres_db"
POSTGRES_USER="xmatute-"
POSTGRES_DB="piscineds"
POSTGRES_PASSWORD="mysecretpassword"

import sys
import psycopg
import os

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

enum_sql = "CREATE TYPE event_type_enum AS ENUM ('view', 'cart', 'remove_from_cart', 'purchase');"
print(enum_sql)
try:
    with conn.cursor() as cur:
        cur.execute(enum_sql)
        print("Enum type created successfully.")
        conn.commit()  # Commit the changes to the database
except psycopg.Error as e:
    conn.rollback()  # Rollback the transaction in case of error
    if "already exists" in str(e):
        print("Enum type already exists.")
    else:
        print(f"Error creating enum type: {e}")
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
        

def table_already_populated(table_name):
    with conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) > 0 FROM {table_name};")
        return cur.fetchone()[0]

def populate_table(table_name, csv):
    if table_already_populated(table_name):
        print(f"Table {table_name} already populated.")
        return
    print(f"Populating table {table_name}...")
    try:
        with conn.cursor() as cur:
            with cur.copy(f"COPY {table_name} FROM STDIN WITH CSV HEADER") as copy:
                copy.write(csv.read())
            print(f"Table {table_name} populated successfully.")
            conn.commit()
    except psycopg.Error as e:
        print(f"Error populating table: {e}")
        raise Exception(f"Error populating table: {e}")

def create_customer_table(csv_path):
    if not csv_path.endswith('.csv'):
        print("Please provide a valid CSV file.")
        raise ValueError("Invalid file format. Expected .csv")

    try:
        with open(csv_path, 'r') as csv_file:
            header = csv_file.readline().strip().split(',')
            if len(header) != len(collumns):
                print(len(header), len(collumns))
                print(collumns)
                raise ValueError("CSV header does not match expected columns.")
        table_name = csv_path.split('/')[-1][:-4]
        create_table(table_name, collumns)
        with open(csv_path, 'r') as csv_file:
            populate_table(table_name, csv_file)
    except FileNotFoundError:
        print(f"File {csv_path} not found.")
        raise FileNotFoundError(f"File {csv_path} not found.")
    except ValueError as e:
        print(e)
        raise ValueError(f"Error in CSV file: {e}")

def create_all_customer_tables(customer_dir):
    if not os.path.isdir(customer_dir):
        print(f"Directory {customer_dir} does not exist.")
        raise ValueError(f"Directory {customer_dir} does not exist.")

    for filename in os.listdir(customer_dir):
        if filename.endswith('.csv'):
            csv_path = os.path.join(customer_dir, filename)
            try:
                create_customer_table(csv_path)
            except ValueError as e:
                print(f"Skipping {filename}: {e}")
        else:
            print(f"Skipping non-CSV file: {filename}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python automatic_table.py <customer_dir/>")
        sys.exit(1)
    try:
        create_all_customer_tables(sys.argv[1])
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()