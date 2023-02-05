from clickhouse_driver import Client

client = Client(host='localhost') 

client.execute('SHOW DATABASES')
# [('_temporary_and_external_tables',), ('default',), ('system',)]