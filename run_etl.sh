apt-get update
apt-get python3
apt-get python3-pip

bash pip install -r requirements.txt

python simulate_orders.py

python extract_data.py 

python load_data_to_bucket.py

python load_data_to_bigQuery.py 
