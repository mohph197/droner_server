from app.lib.mongodb import mongodb


def get_missions():
    try:
        collection = mongodb.get_collection("missions")

        items = list(collection.find())

        for item in items:
            del item["_id"]

        return items
    except:
        return list()
