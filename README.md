
# 1. Photo Management

An application that provides an API for storing photos and interacting with them. Users will be able to add/delete photos from the library. There will be an UI displaying a selected photo and options to edit the photo. The library generates a text description of a selected image and uses a text to speech engine to play audio.

Features:
- Upload photo(s) to library by inputting a path to a jpg or png file or a directory containing jpg and png file types
- UI displays image and connects other features
- Edit photo’s brightness, hue, and saturation with input on UI
- Sort and return duplicate/similar photos (button to call function)
- Search and return photos matching text query (button to call function)
- Generate and play audio for text description (button to call function)
- Delete photos from client’s local database (will not delete files from client’s file directories)

Link to demo [here](https://drive.google.com/file/d/1hcS5-gKFppm3sKZi9WeGxWMw2y1--nUi/view?usp=share_link)

## 2. Installation Instructions

**Install poetry:**

```pip install poetry```


**Install dependencies with poetry:**

```poetry lock```

```poetry install```


**Download Ollama for your OS:**

Follow instructions to download and run Ollama at https://ollama.com/download and pull the vision LLM being used with `ollama pull llama3.2-vision:11b`.

run ollama on your computer as an application or through command
```ollama run ollama pull llama3.2-vision:11b```

> NOTE: If your computer cannot run the `llama3.2-vision:11b` model, you can try any other multimodal model such as `llava-llama3` model

**Embeddings Model:**
The multimodal embeddings model used with Chroma DB is an open-source implementation of OpenAI’s CLIP model. It can be downloaded from Huggingface (https://huggingface.co/laion/CLIP-ViT-B-32-laion2B-s34B-b79K) but will automatically be downloaded when the app starts, stored in `{HOME}/.cache/huggingface/hub`.

## 3. Configuration

Running the unit tests will skip over the tests involving the LLM’s due to high latency. To call the tests, instead of `python -m unittest`, run `CHAT=true python -m unittest`.

**NOTE:**

If your MacBook is using an Intel core processor, the newest pytorch version is not compatible with numpy 2.x and the program will not run. To fix this error you can

Install a 1.x version of numpy:

```poetry uninstall numpy```

```poetry install numpy==1.24.1```


## 4. Database Documentation

For our database we wanted a simple and performant database that supports vector search.

We wanted a database to support vector-search so we could best meet a user's search requirements.


### 4.1 Database Choices

We originally wanted to use [Elasticsearch](https://www.elastic.co/) as our database because of its AI oriented search mechanisms and strong vector-search capabilities. However, because Elasticsearch has a very feature rich set of tools and use of Apache Lucene, we found that Elasticsearch would need to run as a separate process. This created issues such as SSL certificates resetting upon relaunch and a long startup time.

We chose to use [ChromaDB](https://www.trychroma.com/) instead. This database installs as a python package and uses python's native sqlite3 module in the background. ChromaDB is also designed from the ground up to support vector-search. A major advantage over Elasticsearch is that there is no need for a separate process, so startup times are faster and retrieval is faster. Because of these advantages, we chose ChromaDB over Elasticsearch.


## 5. AI models

We use the [Ollama](https://ollama.com/) LLM to generate an image description by communicating with the LLM through backend implementation. Ollama runs in the background of a computer and accepts an input of an array of strings as messages. We chose Ollama because it is from a reputable open source media, Meta Open Source: AI.

## 6. Contribution

|---|---|
|---|---|
| Chaniel Abou-Ezzi | Search for photos using text description feature;  Code cross-checking;   Documentation;  Presentation; preparation  |
| Anh Le | Edit photos feature; UI development;  Code cross-checking; Documentation; Presentation; preparation |
| Anh Trinh | Duplicate detection feature; Code cross-checking;   Documentation;  Presentation; preparation;  |
| Joseph Schwab | Database handle; Code cross-checking;   Documentation;  Presentation; preparation |
| Kailin Luo | Generate and play audio description for photos feature; Code cross-checking;   Documentation;  Presentation; preparation  |


