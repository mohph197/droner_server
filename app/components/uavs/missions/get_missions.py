from app.lib import mongodb


def get_mission():
    collection = mongodb["missions"]

    return collection.find()
