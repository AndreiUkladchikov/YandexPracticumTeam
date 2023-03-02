#!/bin/sh

configure_sharding () {
    echo '-> настроим серверы конфигурации'
    docker exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}, {_id: 1, host: \"mongocfg2\"}, {_id: 2, host: \"mongocfg3\"}]})" | mongosh'

    echo ''
    echo '-> проверим статус, выполнив команду на первом сервере конфигурации'
    docker exec -it mongocfg1 bash -c 'echo "rs.status()" | mongosh'

    echo ''
    echo '-> соберём набор реплик первого шарда'
    docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}, {_id: 1, host: \"mongors1n2\"}, {_id: 2, host: \"mongors1n3\"}]})" | mongosh'

    echo ''
    echo '-> проверить статус реплик'
    docker exec -it mongors1n1 bash -c 'echo "rs.status()" | mongosh'

    echo ''
    echo '-> познакомим шард с маршрутизаторами'
    docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongosh'

    echo ''
    echo '-> инициализируем реплики второго шарда'
    docker exec -it mongors2n1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}, {_id: 1, host: \"mongors2n2\"}, {_id: 2, host: \"mongors2n3\"}]})" | mongosh'

    echo ''
    echo '-> добавим их в кластер'
    docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors2/mongors2n1\")" | mongosh'

    echo ''
    echo '-> проверить статус реплик и шардов'
    docker exec -it mongos1 bash -c 'echo "sh.status()" | mongosh'

    echo ''
    echo '-> Создадим БД ugsDB'
    docker exec -it mongors1n1 bash -c 'echo "use ugsDB" | mongosh'

    echo ''
    echo '-> Включим шардирование'
    docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"ugsDB\")" | mongosh'

    echo ''
    echo '-> создать тестовую коллекцию likesAndReviews'
    docker exec -it mongos1 bash -c 'echo "db.createCollection(\"ugsDB.likesAndReviews\")" | mongosh'

    echo ''
    echo '-> создать тестовую коллекцию watchLater'
    docker exec -it mongos1 bash -c 'echo "db.createCollection(\"ugsDB.watchLater\")" | mongosh'

    echo ''
    echo '-> Настроим шардирование по полю film_id для коллекции likesAndReviews'
    docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"ugsDB.likesAndReviews\", {\"film_id\": \"hashed\"})" | mongosh'

    echo ''
    echo '-> Настроим шардирование по полю user_id для коллекции watchLater'
    docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"ugsDB.watchLater\", {\"user_id\": \"hashed\"})" | mongosh'

    echo ''
    echo '-> Проверьте подтверждение о том, что теперь на коллекции подключено шардирование!!!'
}

configure_sharding
