import os
import traceback
import zlib

from datetime import datetime

from google.appengine.api import users
from google.appengine.api import mail

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

# Local imports.
from game_log_entry import GameLogEntry

class MainPage(webapp.RequestHandler):
  def get(self):
    template_values = {}
    path = os.path.join(os.path.dirname(__file__), 'html/index.html')
    self.response.out.write(template.render(path, template_values))


class LogGame(webapp.RequestHandler):
  def get(self):
    self.redirect('/')

  def post(self):
    try:
      time = datetime.utcnow()
      log_key = '%s06%d' % (time.strftime('%s'), time.microsecond)
      log_entry = GameLogEntry(key_name=log_key)
      log_entry.receive_time = time
      log_entry.version = self.request.get('version')
      log_entry.settings = self.request.get('settings')
      log_entry.game_id = self.request.get('game_id')
      log_entry.reporter = self.request.get('reporter')
      log_entry.correct_score = (self.request.get('correct_score') == 'true')
      log_entry.game_log = zlib.compress(self.request.get('log').encode('utf-8'))
      db.put(log_entry)

      self.response.headers['Content-Type'] = 'text/plain'
      self.response.out.write('OK\n')

    except Exception, e:
      message = mail.EmailMessage(sender='drheld@gmail.com',
                                  subject='A dominion logger error has occurred.')
      message.to = 'drheld@gmail.com'
      message.body = str(e) + '\n\n\n' + traceback.format_exc() + \
                     '\n\nRequest:' + str(self.request)
      message.send()

      self.response.headers['Content-Type'] = 'text/plain'
      self.response.out.write('ERROR')


class FetchGame(webapp.RequestHandler):
  def get(self):
    self.redirect('/')

  def post(self):
    key = db.Key.from_path('GameLogEntry', self.request.get('key'));
    log_entry = db.get(key)

    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write(log_entry.game_html)


class Login(webapp.RequestHandler):
  def get(self):
    user = users.get_current_user()
    if user:
      greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" %
                  (user.nickname(), users.create_logout_url("/")))
    else:
      greeting = ("<a href=\"%s\">Sign in or register</a>." %
                  users.create_login_url("/"))

    self.response.out.write("<html><body>%s</body></html>" % greeting)


application = webapp.WSGIApplication(
    [
     ('/', MainPage),
     ('/log_game', LogGame),
     ('/fetch_game', FetchGame),
     ('/login', Login),
    ],
    debug=True)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
