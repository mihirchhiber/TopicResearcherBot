# TopicResearcherBot

**TopicResearcherBot** is an intelligent assistant designed to streamline the process of researching and analyzing online content. It uses LLMs (via LangChain and Ollama) to automate topic-based article discovery, content cleaning, and summarization. This tool is ideal for researchers, analysts, and content teams who want fast, structured insights from recent web articles.

---

## Features

- **Automated Web Search:** Uses Google Custom Search API to find recent articles related to specific topics and sites.
- **Article Scraping:** Extracts content from article pages using BeautifulSoup and custom rules to avoid noisy or irrelevant data.
- **LLM-based Cleaning:** Leverages LLMs to isolate and retain only the core article body, removing ads, UI elements, and boilerplate.
- **Summarization:** Uses a second LLM pass to generate concise summaries of the cleaned content.
- **Structured Storage:** Articles are stored in a MongoDB database for easy retrieval, filtering, and deletion.
- **Batch Article Retrieval:** Supports multi-week historical searches and batch retrieval per topic-site pair.

---

## Components

### `article.py`
Defines the `Article` class with fields like:
- `id`
- `topics`
- `sites`
- `title`
- `url`
- `source`
- `content`
- `clean_content`
- `summary`

### `database.py`
Handles MongoDB operations for:
- Storing new articles
- Retrieving and deleting existing ones
- Removing duplicates based on title and content hash

### `llmarticles.py`
Core script that:
- Searches and scrapes articles via Google CSE
- Cleans noisy text using LLM prompts
- Summarizes content with LangChain + Ollama
- Manages LLM memory and prompts for efficiency

---

## Usage

1. **Define Topics & Sites**  
   Configure your topics and target news sites.

2. **Run Retrieval**  
   Use `get_recent_articles(topics, sites)` to perform the search and scraping.

3. **Clean & Summarize**  
   Each article goes through `clean_article_text()` and `summarize_article_text()` functions for post-processing.

4. **View/Manage Data**  
   Use database functions to filter or delete articles as needed.

---

## Tech Stack

- Python
- LangChain
- Ollama or Groq AI (LLM backend)
- MongoDB
- Google Custom Search API
- BeautifulSoup
