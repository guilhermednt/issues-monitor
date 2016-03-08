import os
import pprint
import signal
import requests
import json
import webbrowser
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from tendo import singleton
from ConfigParser import SafeConfigParser

class App:
    def __init__(self, indicator_id, githubKey):
        self.indicator = appindicator.Indicator.new(indicator_id, os.path.abspath('fluidicon.png'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.githubKey = githubKey

    def get_indicator(self):
        return self.indicator

    def fetch_issues(self):
        url = 'https://api.github.com/issues?filter=assigned'
        auth = {'Authorization': 'token ' + self.githubKey}
        response = requests.get(url, headers=auth)
        return response.json()

    def update_indicator(self):
        issues = self.fetch_issues()
        count = len(issues)
        self.indicator.set_label(str(count), str(count + 1))
        self.indicator.set_menu(self.issues_menu(issues))

    def issues_menu(self, issues):
        global gtk
        menu = gtk.Menu()
        for issue in issues:
            item = gtk.MenuItem(self.issue_to_string(issue))
            item.connect('activate', self.open_issue, issue['html_url'])
            menu.append(item)
        menu.show_all()
        return menu

    def issue_to_string(self, issue):
        return '[%s#%s] %s' % (issue['repository']['full_name'], issue['number'], issue['title'])

    def print_issues(self, issues):
        for issue in issues:
            print self.issue_to_string(issue)

    def open_issue(self, item, url):
        global webbrowser
        webbrowser.open_new_tab(url);

me = singleton.SingleInstance()

config = SafeConfigParser()
config.read('config.ini')

githubKey = config.get('github', 'api_key')

APPINDICATOR_ID = 'issues_monitor'

def main():
    app = App(APPINDICATOR_ID, githubKey)
    indicator = app.get_indicator()
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    app.update_indicator()
    gtk.main()

def build_menu():
    menu = gtk.Menu()
    item_quit = gtk.MenuItem('Quit')
    item_quit.connect('activate', quit)
    menu.append(gtk.MenuItem('Teste'))
    menu.append(item_quit)
    menu.show_all()
    return menu

def quit(source):
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
