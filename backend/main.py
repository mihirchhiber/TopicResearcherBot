import llm_articles
from database import (
    insert_article, get_all_articles, get_article_topics_sites,
    delete_article_using_id, get_article_using_topics_and_sites,
    delete_article_using_topics_and_sites
)
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager to load and unload the LLM during the app lifespan.
    """
    llm_articles.load_llm()
    yield
    llm_articles.unload_llm()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def index():
    """
    Root endpoint to check server status.
    """
    return {"status": "200"}

@app.get("/query-articles")
def query_articles(
    parent_sites: list[str] = Query(..., description="List of sites to check for articles"),
    topics: list[str] = Query(..., description="List of topics to search for")
):
    """
    Fetch, clean, summarize, and insert articles from given sites and topics.
    """
    recent_articles = llm_articles.get_recent_articles(parent_sites, topics, weeks=1, articlesPerWeek=3)

    for article in recent_articles:
        llm_articles.clean_article_text(article)
        llm_articles.summarize_article_text(article)
        insert_article(article)

    articles_response = [article.to_dict() for article in recent_articles]
    return {"articles": articles_response}

@app.get("/get-all-articles")
def return_all_articles():
    """
    Return all articles stored in the database.
    """
    articles = get_all_articles()
    return {"articles": articles}

@app.get("/get-topics-and-sites")
def return_topics_and_sites():
    """
    Return distinct topics and sites combinations from stored articles.
    """
    articles = get_article_topics_sites()
    return {"articles": articles}

@app.get("/delete-article/{article_id}")
def delete_article(article_id: int):
    """
    Delete an article from the database using its ID.
    """
    delete_article_using_id(article_id)
    return {"article removed": 200}

@app.get("/get-articles-using-topics-and-sites")
def get_articles_using_topics_and_sites(
    topics: list[str] = Query(..., description="List of topics"),
    sites: list[str] = Query(..., description="List of sites")
):
    """
    Retrieve articles filtered by topics and sites.
    """
    articles = get_article_using_topics_and_sites(topics, sites)
    return {"articles": articles}

@app.get("/delete-articles-using-topics-and-sites")
def delete_articles_using_topics_and_sites(
    topics: list[str] = Query(..., description="List of topics"),
    sites: list[str] = Query(..., description="List of sites")
):
    """
    Delete articles based on matching topics and sites.
    """
    delete_article_using_topics_and_sites(topics, sites)
    return {"article removed": 200}
