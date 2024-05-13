docker compose up init-airflow -d

sleep 10

docker compose up -d

sleep 10

cd airbyte 

if [ -f "docker-compose.yaml" ]; then
  docker compose up -d
else
  ./run-ab-platform.sh
fi