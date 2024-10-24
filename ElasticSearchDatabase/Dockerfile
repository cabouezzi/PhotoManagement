# Start from the official Elasticsearch image
FROM docker.elastic.co/elasticsearch/elasticsearch:8.10.0

# Set environment variables
ENV discovery.type=single-node
ENV ELASTIC_PASSWORD=elastic

# Copy any custom configuration files
# COPY ./elastic_config/elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml

# Expose the necessary ports
EXPOSE 9200

# Run Elasticsearch by default
CMD ["elasticsearch"]
