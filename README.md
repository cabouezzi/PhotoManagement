

## Database Documentation
For our database we wanted a simple and performent database that supports vector search.
We wanted a databse to support vector-search so we could best meet a users search requirments.

### Database Choices
We originally wanted to use Elasticsearch(https://www.elastic.co/) as our database because of its AI oriented search mechanisms
and strong vector-search capabilities. However, because Elasticsearch has a very feature rich set of tools
and use of Apache Lucene, we found that Elasticsearch would need to run as a seperate process. This created
issues such as SSL certificates resetting upon relauch and a long startup time. 

We chose to use ChromaDB(https://www.trychroma.com/) instead. This database installs as a python package and uses python's native sqllite3 module
in the background. ChromaDB is also designed from the ground up to support vector-search. A major advantage over Elasticsearch
is that there is no need for a seperate process, so startup times are faster and retrieval is faster. Because of these
advantages we chose ChromaDB over Elasticsearch.

