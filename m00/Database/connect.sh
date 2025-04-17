source .env
your_login=$POSTGRES_USER
echo "Connecting to $POSTGRES_CONTAINER_NAME database as user $your_login..."

docker exec -it $POSTGRES_CONTAINER_NAME psql -U $your_login -d piscineds -h localhost -W