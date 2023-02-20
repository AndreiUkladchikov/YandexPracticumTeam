#!/bin/sh

echo '-> настроим серверы конфигурации'
docker exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}, {_id: 1, host: \"mongocfg2\"}, {_id: 2, host: \"mongocfg3\"}]})" | mongosh'

echo ''
echo ''
echo '-> проверим статус, выполнив команду на первом сервере конфигурации'
docker exec -it mongocfg1 bash -c 'echo "rs.status()" | mongosh'

echo ''
echo ''
echo '-> соберём набор реплик первого шарда'
docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}, {_id: 1, host: \"mongors1n2\"}, {_id: 2, host: \"mongors1n3\"}]})" | mongosh'

echo ''
echo ''
echo '-> проверить статус реплик'
docker exec -it mongors1n1 bash -c 'echo "rs.status()" | mongosh'

echo ''
echo ''
echo '-> познакомим шард с маршрутизаторами'
docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongosh'

echo ''
echo ''
echo '-> инициализируем реплики второго шарда'
docker exec -it mongors2n1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}, {_id: 1, host: \"mongors2n2\"}, {_id: 2, host: \"mongors2n3\"}]})" | mongosh'

echo ''
echo ''
echo '-> добавим их в кластер'
docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors2/mongors2n1\")" | mongosh'

echo ''
echo ''
echo '-> проверить статус реплик и шардов'
docker exec -it mongos1 bash -c 'echo "sh.status()" | mongosh'

echo ''
echo ''
echo '-> Создадим тестовую БД'
docker exec -it mongors1n1 bash -c 'echo "use someTestDb" | mongosh'

echo ''
echo ''
echo '-> Включим шардирование'
docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"someTestDb\")" | mongosh'

echo ''
echo ''
echo '-> создать тестовую коллекцию'
docker exec -it mongos1 bash -c 'echo "db.createCollection(\"someTestDb.testCollection\")" | mongosh'

echo ''
echo ''
echo '-> Настроим шардирование по полю film_id'
docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"someTestDb.testCollection\", {\"film_id\": \"hashed\"})" | mongosh'

echo '-> Проверьте подтверждение о том, что теперь на коллекции подключено шардирование!!!'
