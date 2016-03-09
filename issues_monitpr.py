import os
import pprint
import signal
import requests
import threading
import webbrowser
from tendo import singleton
from gi.repository import Gtk as gtk, Gdk as gdk
from ConfigParser import SafeConfigParser
from gi.repository import AppIndicator3 as appindicator

me = singleton.SingleInstance()

config = SafeConfigParser()
config.read('config.ini')
githubKey = config.get('github', 'api_key')

APPINDICATOR_ID = 'issues_monitor'

class App:
    def __init__(self, indicator_id, githubKey):
        self.indicator = appindicator.Indicator.new(indicator_id, os.path.abspath('fluidicon.png'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.githubKey = githubKey

        self.quit_event = threading.Event()
        threading.Thread(target=loop_sleep, args=(1, self.quit_event)).start()

    def get_indicator(self):
        return self.indicator

    def fetch_issues(self):
        url = 'https://api.github.com/issues?filter=assigned'
        auth = {'Authorization': 'token ' + self.githubKey}
        response = requests.get(url, headers=auth)
        return response.json()

    def update_indicator(self):
        self.indicator.set_label('...', '...')
        issues = self.fetch_issues()
        count = len(issues)
        self.indicator.set_label(str(count), str(count + 1))
        menu = self.get_menu(self.indicator)
        self.issues_menu(self.get_menu(self.indicator), issues)
        
    def get_menu(self, indicator):
        menu = indicator.get_menu()
        if isinstance(menu, gtk.Menu):
            return menu
        else:
            menu = gtk.Menu()
            menu.show_all()
            indicator.set_menu(menu)
            return menu

    def issues_menu(self, menu, issues):
        global gtk
        self.clear_menu(menu)
        for issue in issues:
            item = gtk.MenuItem(self.issue_to_string(issue))
            item.connect('activate', self.open_issue, issue['html_url'])
            menu.append(item)
            item.show()

        item = gtk.SeparatorMenuItem()
        menu.append(item)
        item.show()

        item = gtk.MenuItem('Quit')
        item.connect('activate', self.quit)
        menu.append(item)
        item.show()

        menu.show_all()
        return menu

    def clear_menu(self, menu):
        for i in menu.get_children():
            menu.remove(i)

    def issue_to_string(self, issue):
        return '[%s#%s] %s' % (issue['repository']['full_name'], issue['number'], issue['title'])

    def print_issues(self, issues):
        for issue in issues:
            print self.issue_to_string(issue)

    def open_issue(self, item, url):
        global webbrowser
        webbrowser.open_new_tab(url);

    def quit(self, source):
        global gtk
        self.quit_event.set()
        gtk.main_quit()
        exit()

def loop_sleep(arg1, quit_event):
    global app
    while not quit_event.is_set():
        try:
            app
        except NameError as e:
            pprint.pprint(e)
            quit_event.wait(1)
            continue
        else:
            app.update_indicator()

        quit_event.wait(30)

    gtk.main_quit()
    exit()

githubKey = config.get('github', 'api_key')
app = App(APPINDICATOR_ID, githubKey)

def main():
    global app
    app.update_indicator()

    gdk.threads_init()
    gdk.threads_enter()
    gtk.main()
    gdk.threads_leave()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
