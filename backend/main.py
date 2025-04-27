# main.py

from fastapi import FastAPI, Query
from contextlib import asynccontextmanager
import backend.llm_articles as llm_articles

@asynccontextmanager
async def lifespan(app: FastAPI):
    llm_articles.load_llm()
    yield
    llm_articles.unload_llm()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def index():
    return {"name": "Mihir"}

@app.get("/query-articles")
def query_articles(
    parent_sites: list[str] = Query(..., description="List of sites to check for articles"),
    topics: list[str] = Query(..., description="List of topics to comb through")
):
    # Fetch articles
    recent_articles = llm_articles.get_recent_articles(parent_sites, topics, weeks=1, articlesPerWeek=1)

    # Process each article: clean and summarize
    for article in recent_articles:
        article["clean_content"] = llm_articles.clean_article_text(article["title"], article["content"])
        article["summary"] = llm_articles.summarize_article_text(article["title"], article["clean_content"])

    return {"articles": recent_articles}
