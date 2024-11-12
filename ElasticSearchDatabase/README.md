<h1>Set up Elasticsearch Database</h1>

1. Create the elasticsearch network.
```docker network create elastic```

2. Set the password for the database in .env. Default is "elastic"
3. Set the password for Kibana in .env. Default is "elastic"

3. Run docker-compose.yml
```docker compose up``

4. After the server has finished setting up (~15-30 seconds), copy the https certificate to the host machine
```docker cp elasticsearchdatabase-es01-1:/usr/share/elasticsearch/config/certs/ca/ca.crt .```

5. Test connection to the server
- Test connection (on unix)
```curl --cacert ./ca.crt -u elastic:<PASSWORD> https://localhost:9200```

- Test connection (on windows)
```curl.exe --cacert ./ca.crt -u elastic:<PASSWORD> https://localhost:9200```

<h2>Closing/Removing the server</h2>

- To delete the containers run
```docker compose down```

- To also delete the volumes use the ```-v``` flag


