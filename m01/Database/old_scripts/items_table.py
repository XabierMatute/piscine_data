# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    items_table.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: xmatute- <xmatute-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/04/17 11:15:23 by xmatute-          #+#    #+#              #
#    Updated: 2025/04/17 11:46:48 by xmatute-         ###   ########.fr        #
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
    "product_id INTEGER NOT NULL",
    "category_id NUMERIC(19, 0)",
    "category_code text",
    "brand VARCHAR(127)",
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

def create_items_table(csv_path):
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
            table_name = "items"
            create_table(table_name, collumns)
            populate_table(table_name, csv_file)
    except FileNotFoundError:
        print(f"File {csv_path} not found.")
        raise FileNotFoundError(f"File {csv_path} not found.")
    except ValueError as e:
        print(e)
        raise ValueError(f"Error in CSV file: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python items_table.py <item.csv>")
        sys.exit(1)
    try:
        create_items_table(sys.argv[1])
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
