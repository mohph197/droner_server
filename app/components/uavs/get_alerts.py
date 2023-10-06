from app.lib.mongodb import mongodb


def get_alerts():
    to_return = list(mongodb["alerts"].find().sort({"timestamp": -1}))

    mongodb["alerts"].update_many({"seen": False}, {"$set": {"seen": True}})

    return to_return
