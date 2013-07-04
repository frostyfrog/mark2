import os
import random

from mk2.plugins import Plugin
from mk2.events import StatPlayerCount, Hook


class Alert(Plugin):
    interval = Plugin.Property(default=200)
    command  = Plugin.Property(default="say {message}")
    path     = Plugin.Property(default="alerts.txt")
    
    messages = []
    repeating = False
    empty = True

    def setup(self):
        self.register( self.emptyCheck, StatPlayerCount )

        self.register( self.server_started, Hook, public=True, name="reload-alert", doc='Reload all of the alerts from %s' % self.path )

    def server_started(self, event=None):
        if self.path and os.path.exists(self.path):
            f = open(self.path, 'r')
            for l in f:
                l = l.strip()
                if l:
                    self.messages.append(l)
            f.close()
            
            if self.messages and not self.repeating:
                self.console("Repeating interval: %d" % self.interval )
                self.repeating_task(self.repeater, self.interval)
                self.repeating = True
            if self.messages:
                self.console( "[Plugin] Alert: Successfully loaded %s" % self.path )
            else:
                self.console( "[Plugin] Alert: Failed to load %s" % self.path )

    def emptyCheck(self, event):
        if event.players_current > 0:
            self.empty = False
        else:
            self.empty = True

    def repeater(self, event):
        if not self.empty and self.messages:
            self.send_format(self.command, parseColors=True, message=random.choice(self.messages))
        elif not self.empty:
            self.console("[Plugin] Alert: No alerts loaded...")

# vim: set ai et ts=4 sw=4:
