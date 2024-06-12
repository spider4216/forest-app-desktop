import gi
from gi.repository import GLib
import subprocess

import dbus
from dbus.mainloop.glib import DBusGMainLoop

import tkinter as tk
from tkinter import messagebox
from pygame import mixer

import time

mixer.init()
recording = mixer.Sound('/usr/share/sounds/freedesktop/stereo/alarm-clock-elapsed.oga')
timeoutSound = mixer.Sound('/usr/share/sounds/freedesktop/stereo/service-login.oga')

root = tk.Tk()
root.withdraw()

def notifications(bus, message):
  keys = ["app_name", "replaces_id", "app_icon", "summary",
          "body", "actions", "hints", "expire_timeout"]
  args = message.get_args_list()
  if len(args) == 8:
    notification = dict([(keys[i], args[i]) for i in range(8)])
    if not notification.get('hints'):
      return

    if not notification.get('hints').get('sender-pid'):
      return

    if notification.get('body') == "You have grown a healthy tree." and notification.get('summary') == 'Congratulations!':
      recording.play()

      askRes = messagebox.askquestion(
        message="You have grown a healthy tree. Do you want to short break?",
        title="Congratulations!"
      )

      if askRes == "yes":
        subprocess.Popen(["/usr/bin/stopwatch", "-backward", "000:05:00.000"])
        time.sleep(5 * 60)
        timeoutSound.play()
      else:
        subprocess.call(["/usr/bin/stopwatch", "-backward", "000:15:00.000"])
        time.sleep(15 * 60)
        timeoutSound.play()

DBusGMainLoop(set_as_default=True)

bus = dbus.SessionBus()
bus.add_match_string_non_blocking("eavesdrop=true, interface='org.freedesktop.Notifications', member='Notify'")
bus.add_message_filter(notifications)

#mainloop = glib.MainLoop()
mainloop = GLib.MainLoop()
mainloop.run()
