from pymysqlreplication import BinLogStreamReader
from pymysqlreplication import row_event
import configparser
import csv
import datetime

'''
Grab Configuration Values
'''

# Creating a parser object and reading from the config file
parser = configparser.ConfigParser()
parser.read("pipeline.conf")

# Grabing the values from the config file
hostname = parser.get("mysql_config", "hostname")
port = parser.get("mysql_config", "port")
username = parser.get("mysql_config", "username")
dbname = parser.get("mysql_config", "database")
password = parser.get("mysql_config", "password")

# Creating a dictionary with MySQL settings
mysql_settings = {
    'host':hostname,
    'port': int(port),
    'user':username,
    'passwd':password,
    'database':dbname
}


# Grabbing today's date
today = datetime.datetime.today()
start_date = today - datetime.timedelta(days= 1 )
timestamp = start_date.timestamp()



# Connect to MySQL Binlog
print('Extracting Data...')
b_stream = BinLogStreamReader(
    connection_settings=mysql_settings,
    server_id=100,
    only_events=[row_event.WriteRowsEvent, row_event.UpdateRowsEvent, row_event.DeleteRowsEvent],
    skip_to_timestamp=timestamp,
)

order_events = []

for event in b_stream:
    for row in event.rows:

        # Collect events from the orders table
        if event.table =='orders':
            event_dict = {}
            if isinstance(event, row_event.DeleteRowsEvent):
                event_dict['action'] = 'delete'
                event_dict.update(row['values'].items())
            elif isinstance(event, row_event.UpdateRowsEvent):
                event_dict['action'] = 'update'
                event_dict.update(row['after_values'].items())
            elif isinstance(event, row_event.WriteRowsEvent):
                event_dict['action'] = 'insert'
                event_dict.update(row['values'].items())

        # Collect events from the orderdetails table
        if event.table =='ordersdetails':
            event_dict = {}
            if isinstance(event, row_event.DeleteRowsEvent):
                event_dict['action'] = 'delete'
                event_dict.update(row['values'].items())
            elif isinstance(event, row_event.UpdateRowsEvent):
                event_dict['action'] = 'update'
                event_dict.update(row['after_values'].items())
            elif isinstance(event, row_event.WriteRowsEvent):
                event_dict['action'] = 'insert'
                event_dict.update(row['values'].items())

        order_events.append(event_dict)

if len(order_events) > 0:

    try:
        # Export events to CSV
        keys = order_events[0].keys()
        local_filename = 'binlog_orders.csv'
        with open(local_filename, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys, delimiter='|')
            dict_writer.writerows(order_events)

        print('Done')

        # Close connection
        b_stream.close()

    except Exception as e:
        print('Failed!')
        raise Exception
else:
    print('There are no events.')



