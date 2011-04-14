import os

from datetime import datetime

from google.appengine.ext import db
from google.appengine.api import mail
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class GameLogEntry(db.Model):
  receive_time = db.DateTimeProperty()
  game_html = db.StringProperty()
  settings = db.StringProperty()

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
      log_entry.game_html = self.request.get('log')
      log_entry.settings = self.request.get('settings')
      db.put(log_entry)
      print log_entry.to_xml()

      self.response.headers['Content-Type'] = 'text/plain'
      self.response.out.write('OK')

    except Exception, e:
      message = mail.EmailMessage(sender='drheld@gmail.com',
                                  subject='A dominion logger error has occurred.') 
      message.to = 'drheld@gmail.com'
      message.body = str(e) + '\n\n\n' + traceback.format_exc() + \
                     '\n\nRequest:' + str(self.request)
      message.send()

      self.response.headers['Content-Type'] = 'text/plain'
      self.response.out.write('ERROR')

application = webapp.WSGIApplication(
    [('/', MainPage),
     ('/log_game', LogGame)],
    debug=True)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
