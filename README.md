issues-monitor
==============

Script to be used with xfce4-genmon-plugin. It adds the github issues assigned to you to a panel item.

Installing
----------

1. Create a copy of `parameters.ini.dist` as `parameters.ini` in the same directory.
```bash
cp parameters.ini.dist parameters.ini
```
2. Create an API Token in GitHub and add it to `parameters.ini`.
3. Configure genmon-plugin so that it runs the `panel.sh` script.
