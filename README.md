lab_4_distributed_systems

cd examples/example_app
docker build . -t rjomba_keker
cd ../../
docker stack deploy -c .\redis\docker-compose.yml \
-c .\postgres\docker-compose.yml \ 
-c .\rabbit\docker-compose.yml  \
-c .\examples\example_app\docker-compose.yml test_stack


Можно как-то цепляться через docker service, позже вышлю апдейт
