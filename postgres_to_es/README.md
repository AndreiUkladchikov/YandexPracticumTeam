Если нужен ETL отдельно:
- запустить Elasticsearch на порту 9200: 
docker run -p 9200:9200 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.7.0
- создать индексы - python create_etl.py
- перенести данные из Postgres - python main.py
- config/db_config - uncomment load_dotenv()