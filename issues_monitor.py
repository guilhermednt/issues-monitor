#!/usr/bin/env python

from __future__ import print_function
import os
import sys, getopt
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

def warning(*objs):
    print("WARNING: ", *objs, file=sys.stderr)

DIR = os.path.dirname(os.path.realpath(__file__))
configfile = DIR + '/config.ini'

argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv,"hc:",["config="])
except getopt.GetoptError as e:
    pprint.pprint(e)
    warning('issues_monitor.py -c <configfile>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print('issues_monitor.py -c <configfile>')
        sys.exit()
    elif opt in ("-c", "--config"):
        configfile = arg

config = SafeConfigParser()
config.read(configfile)
githubKey = config.get('github', 'api_key')
updateInterval = config.get('interval', 'issues_monitor')

APPINDICATOR_ID = 'issues_monitor'

class App:
    def __init__(self, indicator_id, githubKey):
        print('App init')
        self.indicator = appindicator.Indicator.new(indicator_id, os.path.abspath(DIR + '/fluidicon.png'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.githubKey = githubKey

        self.quit_event = threading.Event()
        threading.Thread(target=loop_sleep, args=(1, self.quit_event)).start()

    def get_indicator(self):
        print('app.get_indicator')
        return self.indicator

    def fetch_issues(self):
        print('app.fetch_issues')
        url = 'https://api.github.com/issues?filter=assigned'
        auth = {'Authorization': 'token ' + self.githubKey}
        response = requests.get(url, headers=auth)
        return response.json()

    def update_indicator(self):
        print('app.update_indicator')
        self.indicator.set_label('...', '...')
        issues = self.fetch_issues()
        count = len(issues)
        self.indicator.set_label(str(count), str(count + 1))
        menu = self.get_menu(self.indicator)
        self.issues_menu(self.get_menu(self.indicator), issues)
        
    def get_menu(self, indicator):
        print('app.get_menu')
        menu = indicator.get_menu()
        if isinstance(menu, gtk.Menu):
            return menu
        else:
            menu = gtk.Menu()
            menu.show_all()
            indicator.set_menu(menu)
            return menu

    def issues_menu(self, menu, issues):
        print('app.issues_menu')
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
        print('app.clear_menu')
        for i in menu.get_children():
            menu.remove(i)

    def issue_to_string(self, issue):
        print('app.issue_to_string')
        if 'repository' not in issue or 'full_name' not in issue['repository'] or 'number' not in issue or 'title' not in issue:
            print('invalid issue ??')
            return '-'
        return '[%s#%s] %s' % (issue['repository']['full_name'], issue['number'], issue['title'])

    def print_issues(self, issues):
        print('app.print_issues')
        for issue in issues:
            print(self.issue_to_string(issue))

    def open_issue(self, item, url):
        print('app.open_issue')
        global webbrowser
        webbrowser.open_new_tab(url);

    def quit(self, source):
        print('app.quit')
        global gtk
        self.quit_event.set()
        gtk.main_quit()
        exit()

def loop_sleep(arg1, quit_event):
    print('loop_sleep')
    global app, updateInterval
    while not quit_event.is_set():
        try:
            app
        except NameError as e:
            warning(e)
            quit_event.wait(1)
            continue
        else:
            try:
                app.update_indicator()
            except:
                print("Unexpected error:", sys.exc_info()[0])

        quit_event.wait(updateInterval)

    gtk.main_quit()
    exit()

githubKey = config.get('github', 'api_key')
app = App(APPINDICATOR_ID, githubKey)

def main():
    print('main')
    global app
    app.update_indicator()

    gdk.threads_init()
    gdk.threads_enter()
    gtk.main()
    gdk.threads_leave()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
