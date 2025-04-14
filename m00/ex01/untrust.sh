docker exec -it postgres_db sed -i 's/trust/scram-sha-256/g' /var/lib/postgresql/data/pg_hba.conf
echo "Postgres authentication method changed to scram-sha-256"
echo " You may need to restart the container for the changes to take effect."