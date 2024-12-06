## 1. Photo Management
An application that provides an API for storing photos and interacting with them. Users will be able to add/delete photos from the library. There will be options to find similar/duplicate photos and edit photos. The library will be able to generate a text description of a selected image and uses a text to speech engine to play audio.

## 2. Installation Instructions

## 3. Configuration 

## 4. Database Documentation
For our database we wanted a simple and performent database that supports vector search.
We wanted a databse to support vector-search so we could best meet a users search requirments.

## 4.1 Database Choices
We originally wanted to use Elasticsearch(https://www.elastic.co/) as our database because of its AI oriented search mechanisms
and strong vector-search capabilities. However, because Elasticsearch has a very feature rich set of tools
and use of Apache Lucene, we found that Elasticsearch would need to run as a seperate process. This created
issues such as SSL certificates resetting upon relauch and a long startup time. 

We chose to use ChromaDB(https://www.trychroma.com/) instead. This database installs as a python package and uses python's native sqllite3 module
in the background. ChromaDB is also designed from the ground up to support vector-search. A major advantage over Elasticsearch
is that there is no need for a seperate process, so startup times are faster and retrieval is faster. Because of these
advantages we chose ChromaDB over Elasticsearch.

## 5. AI models