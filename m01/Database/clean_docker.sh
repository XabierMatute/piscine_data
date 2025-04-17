docker system prune --volumes --force --all
docker container prune --force
docker volume prune --force
docker volume rm $(docker volume ls -q) #puede dar error
docker rm -f $(docker ps -a -q) # Elimina todos los contenedores?