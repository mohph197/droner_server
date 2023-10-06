from app.lib.mongodb import mongodb


def get_missions():
    collection = mongodb["missions"]

    return collection.find()
