from google.appengine.ext import db

class GameLogEntry(db.Expando):
  receive_time = db.DateTimeProperty()
  version = db.StringProperty()
  settings = db.StringProperty()
  game_id = db.StringProperty()
  reporter = db.StringProperty()
  correct_score = db.BooleanProperty()
  test_case = db.BooleanProperty()
  state_strings = db.BlobProperty()
  game_log = db.BlobProperty()
