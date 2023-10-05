import pusher

_pusher_client = pusher.Pusher(
  app_id='1682651',
  key='36d49d87aa68e5eaf8d6',
  secret='31b80ae4113ab60aece1',
  cluster='eu',
  ssl=True
)

def send_notification(event, data):
    _pusher_client.trigger('notifications', event, data)