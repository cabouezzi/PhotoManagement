<h1>Set up Elasticsearch Database</h1>

1. Create the elasticsearch network.
```docker network create elastic```

2. Set the password for the database in the Dockerfile. Default is "elastic"

3. Build the docker image from the Dockerfile in ./ElasticSearchDatabase
```docker build -t elasticdock ./ElasticSearchDatabase```

4. Run the docker container
```docker run --name es00 --net elastic -p 9200:9200 -it -m 1GB elasticdock```

5. After the server has finished setting up (~15-30 seconds), copy the https certificate to the host machine
```docker cp es00:/usr/share/elasticsearch/config/certs/http_ca.crt ./ElasticSearchDatabase/```

6. Test connection to the server
**NOTE: '-k' ignores certificate checks**
- Test connection (on unix)
```curl -k --cacert ./ElasticSearchDatabase/http_ca.crt -u elastic:<PASSWORD> https://localhost:9200```

- Test connection (on windows)
```curl.exe -k --cacert ./ElasticSearchDatabase/http_ca.crt -u elastic:<PASSWORD> https://localhost:9200```
