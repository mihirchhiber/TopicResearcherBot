import pymongo
from article import Article

# Connect to MongoDB server
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# Create (or switch to) a database
mydb = myclient["article_database"]

mycollection = mydb["articles"]

def insert_article(article):
    mycollection.insert_one(article)

def get_any_article():
    return mycollection.find_one()

def get_article_using_id(id):
    return mycollection.find_one({'title': id})

def get_all_articles():
    articles = []
    for post in mycollection.find():
        articles.insert(post)
    return articles

def delete_article_using_id(id):
    mycollection.delete_one({'title': id})