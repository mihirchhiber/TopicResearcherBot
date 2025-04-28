import pymongo
from article import Article 

# Connect to MongoDB server
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["article_database"]
mycollection = mydb["articles"]

def insert_article(article: Article):
    """Insert an Article object into MongoDB."""
    try:
        mycollection.insert_one(article.to_dict())
    except Exception as e:
        print(f"Error inserting article: {e}")

def get_any_article() -> dict:
    """Get any one article."""
    return mycollection.find_one()

def get_article_using_title(title: str) -> dict:
    """Get article by title."""
    return mycollection.find_one({'title': title})

def get_all_articles() -> list:
    """Get all articles."""
    articles = []
    for post in mycollection.find():
        articles.append(post) 
    return articles

def delete_article_using_title(title: str):
    """Delete article by title."""
    try:
        result = mycollection.delete_one({'title': title})
        return result.deleted_count
    except Exception as e:
        print(f"Error deleting article: {e}")
        return 0