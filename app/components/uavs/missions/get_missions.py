from app.lib.mongodb import mongodb


def get_missions():
    try:
        collection = mongodb.get_collection("missions")

        return collection.find()
    except:
        return list()
