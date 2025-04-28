import llm_articles
from database import insert_article, get_all_articles, get_article_topics_sites, delete_article_using_id
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query

@asynccontextmanager
async def lifespan(app: FastAPI):
    llm_articles.load_llm()
    yield
    llm_articles.unload_llm()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def index():
    return {"status": "200"}

@app.get("/query-articles")
def query_articles(
    parent_sites: list[str] = Query(..., description="List of sites to check for articles"),
    topics: list[str] = Query(..., description="List of topics to comb through")
):
    # Fetch articles
    recent_articles = llm_articles.get_recent_articles(parent_sites, topics, weeks=1, articlesPerWeek=2)

    # Process each article: clean and summarize
    for article in recent_articles:
        llm_articles.clean_article_text(article)
        llm_articles.summarize_article_text(article)
        insert_article(article)

    # Convert all Article objects to dicts for JSON response
    articles_response = [article.to_dict() for article in recent_articles]

    return {"articles": articles_response}

@app.get("/get-all-articles")
def return_all_articles():

    articles = get_all_articles()
    return {"articles": articles}

@app.get("/get-topics-and-sites")
def return_topics_and_sites():

    articles = get_article_topics_sites()
    return {"articles": articles}

@app.get("/delete-article/{article_id}")
def return_topics_and_sites(article_id: int):

    delete_article_using_id(article_id)
    return {"article removed": 200}
    
