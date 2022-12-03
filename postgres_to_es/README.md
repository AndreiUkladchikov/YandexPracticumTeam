Если нужен ETL отдельно:
- запустить Elasticsearch на порту 9200: 
docker run -p 9200:9200 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.7.0
- config/db_config - uncomment load_dotenv()
- создать state.json в корне папки postgres_to_es
- создать индексы - python create_etl.py
- перенести данные из Postgres - python main.py