from google.appengine.ext import db

class GameLogEntry(db.Model):
  receive_time = db.DateTimeProperty()
  version = db.StringProperty()
  settings = db.StringProperty()
  game_id = db.StringProperty()
  reporter = db.StringProperty()
  correct_score = db.BooleanProperty()
  player_json = db.TextProperty()
  game_log = db.BlobProperty()
