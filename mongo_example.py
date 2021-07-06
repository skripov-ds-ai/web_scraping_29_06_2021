from pprint import pprint
from bson import ObjectId
from pymongo import MongoClient

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "posts"
MONGO_COLLECTION = "news_posts"

# client = MongoClient(MONGO_HOST, MONGO_PORT)
# # ...
# client.close()
#
# with MongoClient(MONGO_HOST, MONGO_PORT) as client:
#     pass


def print_mongo_docs(cursor):
    for doc in cursor:
        pprint(doc)


# CRUD
# 1. Create
# 2. Read
# 3. Update
# 4. Delete

with MongoClient(MONGO_HOST, MONGO_PORT) as client:
    post_doc = {
        "title": "Using MongoDB",
        "rating": 1,
    }
    posts = [
        {
            "title": "Using SQL",
            "rating": 9,
        },
        {"title": "Example of BeautifulSoup4"},
    ]
    post_doc_with_predeclared_id = {
        "title": "How to scrape",
        "rating": -1,
        "_id": ObjectId("60e48695b4957574a1e94e06"),
    }

    db = client[MONGO_DB]
    news = db[MONGO_COLLECTION]
    # 1. Create
    # news.insert_one(post_doc)
    news.insert_many(posts)
    # news.insert_one(post_doc_with_predeclared_id)
    # Optional research
    # news.insert(...)

    # 2. Read
    # cursor = news.find()
    # transform to list
    # data = []
    # for doc in cursor:
    #     data.append(doc)
    # data = list(cursor)
    # pprint(data)

    # cursor = news.find()
    # cursor = news.find({})
    # print()
    # print_mongo_docs(cursor)
    # print()

    # cursor = news.find({
    #     "title": "Using MongoDB",
    #     "rating": 1,
    # })
    # print_mongo_docs(cursor)

    # $gt, $lt, $gte, $lte, $eq, $ne
    # cursor = news.find({
    #     "rating": {"$gt": 0}
    # })
    # print_mongo_docs(cursor)

    # rating == -1 or rating > 1
    # cursor = news.find({
    #     "$or": [
    #         {
    #             "rating": {"$eq": -1}
    #         },
    #         {
    #             "rating": {"$gt": 1}
    #         }
    #     ]
    # })
    # print_mongo_docs(cursor)
    # $in, $not, $and

    # limit; top-2
    # cursor = news.find({
    #     "rating": {"$gt": 0}
    # }).limit(2)
    # print_mongo_docs(cursor)

    # sort; 1 or -1
    # cursor = news.find({
    #     "rating": {"$gt": 0}
    # }).sort("rating", direction=-1)
    # print_mongo_docs(cursor)

    # sort; 1 or -1; with top-2
    # cursor = news.find({
    #     "rating": {"$gt": 0}
    # }).sort("rating", direction=-1).limit(2)
    # print_mongo_docs(cursor)

    # aggregate; for example, for searching by month etc(about datetime)

    # 3. Update
    # find_condition = {
    #     "rating": 9,
    # }
    # update_data = {
    #     "$set": {
    #         "title": "New title for rating = 9",
    #         "number_of_views": 100,
    #     }
    # }
    # update_data = {
    #     "$unset": {
    #         "title": None
    #     }
    # }
    # news.update_one(find_condition, update_data)
    # find_condition = {
    #     "title": "Using MongoDB"
    # }
    # update_data = {
    #     "$set": {
    #         "number_of_views": 999,
    #     }
    # }
    # news.update_many(find_condition, update_data)
    # Optional; $inc

    # find_condition = {
    #     "rating": -1,
    # }
    # replace_data = {
    #     "number_of_views": 998,
    # }
    # news.replace_one(find_condition, replace_data)

    # 4. Delete
    # find_condition = {
    #     "number_of_views": 999
    # }
    # news.delete_one(find_condition)
    # news.delete_many(find_condition)

    # Warning!
    # news.delete_many({})
    # drop collection
    # news.drop()
    # drop database
    # client.drop_database(MONGO_DB)
