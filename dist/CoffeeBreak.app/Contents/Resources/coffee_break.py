#!/usr/bin/env python3
"""
CoffeeBreak - Dein freundlicher Selbstfürsorge-Buddy
Erinnert dich alle 2h aktiver Bildschirmzeit daran, auf dich zu achten.
"""

import rumps
import time
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import subprocess
import random

# Pfad für persistente Daten
APP_SUPPORT = Path.home() / "Library" / "Application Support" / "CoffeeBreak"
APP_SUPPORT.mkdir(parents=True, exist_ok=True)
STATE_FILE = APP_SUPPORT / "state.json"

# Freundliche Erinnerungen (wie von einem guten Freund)
REMINDERS = [
    "Hey, trink mal was! Wann hattest du das letzte Glas Wasser? 💧",
    "Kurz aufstehen und strecken? Dein Rücken wird's dir danken!",
    "Schau mal kurz aus dem Fenster. Ernsthaft, die Welt ist noch da! 🌤️",
    "Zeit für einen Kaffee? Oder vielleicht einen Tee? ☕️",
    "Schnapp dir einen Snack! Ein Apfel, Nüsse, whatever - Hauptsache was 🍎",
    "Handgelenke mal kreisen lassen? Du tippst schon ne Weile...",
    "Deep breath in... and out. Fühlst du das? Das ist Entspannung 🌬️",
    "Augen zu, Schläfen massieren, 10 Sekunden. Los, mach! 😌",
    "Schultern hoch, Schultern runter. Merkst du die Verspannung?",
    "Wie wär's mit einem kurzen Walk? Nur um den Block?",
    "Hände ausschütteln wie beim Sport. Fühlt sich doof an, hilft aber!",
    "Kopf nach links, nach rechts drehen. Ganz langsam, kein Stress.",
    "Trinkst du noch oder verdurstest du schon? 💦",
    "Augen zu und 20 Sekunden an was Schönes denken. Gönn dir!",
    "Füße hochlegen, 30 Sekunden chillen. You deserve it!",
    "Fenster auf, frische Luft rein! Oder ist dir zu kalt? 🪟",
    "Mal kurz lächeln? Auch wenn's weird ist - hebt die Stimmung! 😊",
    "Zeit für die 20-20-20 Regel: 20 Sek. auf was 20 Fuß weit schauen!",
    "Aufstehen und ein bisschen on the spot joggen? Blut in Wallung bringen!",
    "Nimm dir 2 Minuten für einen guten Song. Tanzen optional 🎵",
    "Rücken gerade, Bauch rein, Brust raus. Haltung, Baby!",
    "Snacktime! Was hast du Leckeres in der Küche?",
    "Kurz die Arme über dem Kopf strecken - wie ein Katzenbuckel!",
    "Augen weit auf und zu, ein paar Mal blinzeln. Bildschirm-Müdigkeit ade!",
    "5 tiefe Atemzüge. Einfach nur atmen, nichts weiter.",
    "Wasserflasche leer? Auf zur Küche! Bewegung + Hydration = Win 💪",
    "Mal die Waden dehnen? Einfach aufstehen und Fersen hoch.",
    "Sitzt du gerade gut? Check mal deine Haltung, seriously.",
    "Kurze Pause für ein paar Kniebeugen? Oder ist das zu viel verlangt? 😄",
    "Wann hast du das letzte Mal bewusst geatmet? Jetzt wär ein guter Moment!",
    "Mini-Meditation: 30 Sekunden nur deinen Atem beobachten 🧘",
    "Spaziergang zur Kaffeemaschine zählt auch als Bewegung!",
    "Müde Augen? Handflächen aneinander reiben und auf die Augen legen.",
    "Du arbeitest schon ne Weile - gönn dir 2 Minuten Nichtstun!",
    "Snack + Wasser + frische Luft = perfekte Kombo! 🎯",
    "Hals nach hinten neigen, Himmel anschauen (oder Decke). Feels good!",
    "Die Schulterblätter zusammenziehen - spürst du die Spannung?",
    "Kurzer Reality-Check: Wie geht's dir gerade? Ehrlich?",
    "Obst-Timer! Wann hast du heute was Gesundes gegessen? 🍊",
    "Bildschirm-Detox: 30 Sekunden aus dem Fenster starren.",
]


class CoffeeBreakApp(rumps.App):
    def __init__(self):
        super(CoffeeBreakApp, self).__init__(
            "☕️",
            title="☕️",
            quit_button=None  # Custom quit button
        )
        
        # State variables
        self.active_time = 0  # Sekunden aktiver Nutzung heute
        self.last_check = time.time()
        self.last_reminder = 0  # Timestamp der letzten Erinnerung
        self.paused_until = None  # Timestamp bis wann pausiert
        self.last_date = datetime.now().date()
        
        # Load state
        self.load_state()
        
        # Menu items
        self.menu = [
            rumps.MenuItem("Aktive Zeit: 0h 0m", callback=None),
            rumps.separator,
            rumps.MenuItem("Pause: 10 Minuten", callback=self.pause_10),
            rumps.MenuItem("Pause: 30 Minuten", callback=self.pause_30),
            rumps.MenuItem("Pause: 60 Minuten", callback=self.pause_60),
            rumps.separator,
            rumps.MenuItem("Über CoffeeBreak", callback=self.show_about),
            rumps.MenuItem("Beenden", callback=self.quit_app),
        ]
        
        # Start tracking timer
        self.timer = rumps.Timer(self.check_activity, 10)  # Check every 10 seconds
        self.timer.start()
    
    def load_state(self):
        """Lädt den gespeicherten Zustand"""
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, 'r') as f:
                    state = json.load(f)
                    saved_date = datetime.fromisoformat(state.get('date', '')).date()
                    
                    # Reset wenn neuer Tag
                    if saved_date == datetime.now().date():
                        self.active_time = state.get('active_time', 0)
                        self.last_reminder = state.get('last_reminder', 0)
                    else:
                        self.active_time = 0
                        self.last_reminder = 0
            except Exception as e:
                print(f"Error loading state: {e}")
    
    def save_state(self):
        """Speichert den aktuellen Zustand"""
        try:
            state = {
                'active_time': self.active_time,
                'last_reminder': self.last_reminder,
                'date': datetime.now().isoformat()
            }
            with open(STATE_FILE, 'w') as f:
                json.dump(state, f)
        except Exception as e:
            print(f"Error saving state: {e}")
    
    def get_idle_time(self):
        """Gibt die Idle-Zeit in Sekunden zurück"""
        try:
            output = subprocess.check_output(
                ['ioreg', '-c', 'IOHIDSystem'],
                stderr=subprocess.STDOUT
            ).decode('utf-8')
            
            for line in output.split('\n'):
                if 'HIDIdleTime' in line:
                    idle_time_ns = int(line.split('=')[1].strip())
                    return idle_time_ns / 1000000000  # Convert to seconds
            return 0
        except Exception as e:
            print(f"Error getting idle time: {e}")
            return 0
    
    def check_activity(self, _):
        """Prüft Aktivität und aktualisiert Counter"""
        current_time = time.time()
        
        # Check if new day
        if datetime.now().date() != self.last_date:
            self.active_time = 0
            self.last_reminder = 0
            self.last_date = datetime.now().date()
        
        # Check if user is active (idle < 30 seconds)
        idle_time = self.get_idle_time()
        
        if idle_time < 30:  # User ist aktiv
            time_passed = current_time - self.last_check
            self.active_time += time_passed
            
            # Update menu
            hours = int(self.active_time // 3600)
            minutes = int((self.active_time % 3600) // 60)
            self.menu["Aktive Zeit: 0h 0m"].title = f"Aktive Zeit: {hours}h {minutes}m"
            
            # Check if reminder needed (alle 2h = 7200 Sekunden)
            if self.active_time - self.last_reminder >= 7200:
                if not self.is_paused():
                    self.send_reminder()
                    self.last_reminder = self.active_time
        
        self.last_check = current_time
        self.save_state()
    
    def is_paused(self):
        """Prüft ob aktuell pausiert ist"""
        if self.paused_until is None:
            return False
        
        if time.time() < self.paused_until:
            return True
        else:
            self.paused_until = None
            return False
    
    def send_reminder(self):
        """Sendet eine freundliche Erinnerung"""
        message = random.choice(REMINDERS)
        
        # macOS Notification
        os.system(f'''
            osascript -e 'display notification "{message}" with title "CoffeeBreak ☕️" sound name "Glass"'
        ''')
    
    def pause_10(self, _):
        """Pausiert für 10 Minuten"""
        self.paused_until = time.time() + (10 * 60)
        rumps.notification(
            title="CoffeeBreak pausiert",
            subtitle="",
            message="Ich melde mich in 10 Minuten wieder! 🤫"
        )
    
    def pause_30(self, _):
        """Pausiert für 30 Minuten"""
        self.paused_until = time.time() + (30 * 60)
        rumps.notification(
            title="CoffeeBreak pausiert",
            subtitle="",
            message="Ich melde mich in 30 Minuten wieder! 🤫"
        )
    
    def pause_60(self, _):
        """Pausiert für 60 Minuten"""
        self.paused_until = time.time() + (60 * 60)
        rumps.notification(
            title="CoffeeBreak pausiert",
            subtitle="",
            message="Ich melde mich in 60 Minuten wieder! 🤫"
        )
    
    def show_about(self, _):
        """Zeigt Info-Dialog"""
        rumps.alert(
            title="CoffeeBreak ☕️",
            message="Dein freundlicher Selbstfürsorge-Buddy\n\n"
                   "Erinnert dich alle 2 Stunden aktiver Bildschirmzeit daran, "
                   "auf dich zu achten.\n\n"
                   "Made with ❤️"
        )
    
    def quit_app(self, _):
        """Beendet die App"""
        self.save_state()
        rumps.quit_application()


if __name__ == "__main__":
    CoffeeBreakApp().run()
