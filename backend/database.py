import pymongo
from article import Article

# MongoDB connection setup
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["article_database"]
mycollection = mydb["articles"]

def remove_duplicates(lst_of_dicts):
    """
    Remove duplicate dictionaries from a list based on their content.

    Args:
        lst_of_dicts (list): List of dictionaries.

    Returns:
        list: List of unique dictionaries.
    """
    seen = set()
    unique = []
    for d in lst_of_dicts:
        dict_tuple = tuple((k, tuple(v)) for k, v in sorted(d.items()))
        if dict_tuple not in seen:
            seen.add(dict_tuple)
            unique.append(d)
    return unique

def insert_article(article: Article):
    """
    Insert an Article object into MongoDB.
    """
    try:
        mycollection.insert_one(article.to_dict())
    except Exception as e:
        print(f"Error inserting article: {e}")

def get_article_topics_sites() -> dict:
    """
    Get distinct topics and sites from all articles.
    """
    articles = []
    for post in mycollection.find({}, {"topics": 1, "sites": 1, "_id": 0}):
        articles.append(post)
    return remove_duplicates(articles)

def get_article_using_topics_and_sites(topics: list, sites: list) -> dict:
    """
    Retrieve articles matching given topics and sites.
    """
    articles = []
    for post in mycollection.find({'topics': topics, 'sites': sites}, {"_id": 0}):
        articles.append(post)
    return articles

def get_all_articles() -> list:
    """
    Retrieve all articles.
    """
    articles = []
    for post in mycollection.find({}, {"_id": 0}):
        articles.append(post)
    return articles

def delete_article_using_id(id: int):
    """
    Delete an article by its unique ID.
    """
    try:
        result = mycollection.delete_many({'id': id})
        return result.deleted_count
    except Exception as e:
        print(f"Error deleting article: {e}")
        return 0

def delete_article_using_topics_and_sites(topics: list, sites: list):
    """
    Delete articles matching the given topics and sites.
    """
    try:
        result = mycollection.delete_many({'topics': topics, 'sites': sites})
        return result.deleted_count
    except Exception as e:
        print(f"Error deleting article: {e}")
        return 0
