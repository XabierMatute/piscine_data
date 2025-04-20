CSV_PATH=~/sgoinfre/data/pdc00
python3 old_scripts/automatic_table.py ${CSV_PATH}/customer/
python3 old_scripts/items_table.py ${CSV_PATH}/item/item.csv
python3 old_scripts/customer_table.py
python3 old_scripts/remove_duplicates.py
python3 old_scripts/fusion.py