import os
import re
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

class Debug(webapp.RequestHandler):
  def get(self):
    query = db.Query(GameLogEntry)
    query.filter('correct_score =', False)
    results = query.fetch(limit=1)

    if len(results) != 1:
      self.response.headers['Content-Type'] = 'text/plain'
      if (len(results) == 0):
        self.response.out.write('No bugs found...')
      else:
        self.response.out.write('More than one bug in one fetch. Huh?')
      return

    result = results[0]
    template_values = {}

    template_values['primary_key'] = result.key().name()
    template_values['version'] = result.version
    template_values['reporter'] = result.reporter
    template_values['receive_time'] = str(result.receive_time)
    template_values['settings'] = result.settings

    link_parts = re.search('game-([0-9]{6})([0-9]{2})-', result.game_id)
    url = 'http://dominion.isotropic.org/gamelog/'
    url += link_parts.group(1) + '/' + link_parts.group(2) + '/' + result.game_id
    game_link = '<a href="%s" id="game_link">%s</a>' % (url, url)
    template_values['game_link'] = game_link

    # Clean the html and dump it.
    game_html = result.game_html
    if game_html is None or game_html == "":
      game_html = zlib.decompress(result.game_log)
    game_html = re.sub(r'<img [^>]*>', r'<img src="">', game_html)
    game_html = re.sub(r'<embed [^>]*>', r'', game_html)
    template_values['game_log'] = game_html

    path = os.path.join(os.path.dirname(__file__), 'html/debug.html')
    self.response.out.write(template.render(path, template_values))


class DebugDel(webapp.RequestHandler):
  def get(self):
    self.redirect('/debug')

  def post(self):
    key = db.Key.from_path('GameLogEntry', self.request.get('key'));
    log_entry = db.get(key)
    db.delete(log_entry)
    self.redirect('/debug')


application = webapp.WSGIApplication(
    [
     ('/debug', Debug),
     ('/debug_del', DebugDel),
    ],
    debug=True)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
