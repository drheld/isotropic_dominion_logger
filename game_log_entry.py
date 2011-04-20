from google.appengine.ext import db

class GameLogEntry(db.Model):
  receive_time = db.DateTimeProperty()
  settings = db.StringProperty()
  game_id = db.StringProperty()
  reporter = db.StringProperty()
  correct_score = db.BooleanProperty()
  game_html = db.TextProperty()
