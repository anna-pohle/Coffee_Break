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
    "Deine Wasserflasche schaut mich vorwurfsvoll an 💧",
    "Blinzel-Check: Du starrst, nicht du arbeitest 😅",
    "10 Jumping Jacks! Oder zu viel verlangt? 😏",
    "Noch ein Kaffee oder zitterst du schon? ☕",
    "Gemüse heute? Oder zählen Gummibärchen? 🍎",
    "Sitzt du gerade oder hängst du? Kleiner Unterschied 😉",
    "Drei tiefe Atemzüge - ich warte! 🌬️",
    "Handgelenke schütteln! Ja, du siehst dabei weird aus.",
    "Frische Luft! Oder magst du CO2? 🪟",
    "Schultern bis zu den Ohren? Dachte ich mir.",
    "Küchen-Spaziergang! Wasser holen zählt als Sport 🚶",
    "Augen zu, kurz chillen. Du bist auf einem guten Weg!",
    "Snacktime! Belohnung ist Teil der Produktivität 😊",
    "Nacken dehnen - oder wartest du auf Verspannungen?",
    "Füße hoch! Du bist kein Laptop-Ständer.",
    "Grinsen für 5 Sekunden - selbst wenn's Fake ist 😊",
    "Kiefermassage! Ja wirklich, du beißt die Zähne zusammen.",
    "Katzen-Streck-Move: Arme hoch und gääähnen!",
    "Tanzen! 20 Sekunden, keine Zeugen 🎵",
    "Sitzhaltung: Königin/König, nicht Fragezeichen 👑",
    "Letztes Mal gelacht? Lustiges Video als Therapie?",
    "Treppen! Oder ist der Aufzug dein bester Freund? 😅",
    "Handy-Detox: 30 Sekunden nur du und deine Gedanken",
    "Kaffee als Event trinken, nicht als Benzin!",
    "Waden dehnen - du bist kein Bürostuhl-Fossil",
    "Selbst-Nackenmassage oder willst du warten bis's wehtut?",
    "Seitlich strecken! Links, rechts, und... entspannen.",
    "Zitronenwasser = fancy Hydration 🍋",
    "Achtsamkeit: Was siehst du? Was hörst du? Was fühlst du?",
    "Hände unter kaltes Wasser - instant Refresh!",
    "Augen-Urlaub: 20 Sekunden was Grünes anschauen 🌿",
    "Kniebeugen-Runde! Oder zu ambitioniert? 😏",
    "Beim Telefonieren rumlaufen = Multitasking done right",
    "Essen am Schreibtisch? Naja... könnte besser sein 😅",
    "Sauerstoff-Level kritisch! Fenster auf!",
    "Oberkörper-Twist! Links, rechts - du bist nicht festgeschraubt.",
    "Apfel > Energy Drink. Fight me. 🍎",
    "Chaos auf dem Schreibtisch = Chaos im Kopf?",
    "Augenmassage! Ganz zart, du bist kein Teig.",
    "Warmes Wasser über die Hände = Mini-Spa 💆",
    "Power Nap Zeit? 15 Minuten können Wunder wirken!",
    "Playlist-Wechsel! Selbe Songs = Zombie-Mode 🎵",
    "Bisschen durchs Zimmer laufen? Deine Beine existieren noch!",
    "Gesichts-Yoga klingt weird, hilft aber wirklich",
    "Datteln + Nussbutter = besseres Snickers 🥜",
    "Nächste Pause geplant? Oder hoffst du auf Spontan-Erleuchtung?",
    "Arme schütteln wie vor'm Boxkampf! 🥊",
    "Balance-Test: 10 Sekunden auf einem Bein - schaffst du's?",
    "Vitamin D tanken! Oder bist du Team Vampir? ☀️",
    "Kiefer entspannen - du kaust grad imaginären Kaugummi",
    "Gähnen wirkt - selbst wenn du's nur vortäuschst",
    "Wasserflasche Status: Leer. Aktion erforderlich!",
    "Katzen-Stretch! Rücken rund, dann durchstrecken 🐱",
    "Hände verschränken und nach vorne - knackt's? 😄",
    "Auf Zehenspitzen wippen - Mini-Workout!",
    "Musik-Stimmung ändern? Neue Vibes needed?",
    "Tief einatmen - mehr als das Mini-Atmen gerade",
    "Letzte echte Mahlzeit? Kaffee zählt nicht.",
    "Fußgelenke kreisen! Auch die haben Gefühle.",
    "Schreibtisch-Feng-Shui: 2 Minuten aufräumen = innere Ruhe",
    "Tagtraum-Pause! 10 Sekunden Kopfkino 🏖️",
    "Wasser trinken ist wie Blumen gießen - für dich!",
    "Schulterblätter zusammen und... relax!",
    "Kopf nach hinten - vorsichtig! Nicht übertreiben.",
    "Real talk: Wie geht's dir wirklich grade?",
    "Pausen machen ist kein Versagen, sondern smart 💙",
    "Nacken dehnen: Ohr zur Schulter, spürst du's?",
    "Finger-Gymnastik! Die tippen den ganzen Tag.",
    "Beine mal richtig strecken - Knie sind keine Dauerbeuger",
    "Schultern fallen lassen - du trägst grad die Welt",
    "Smile-Challenge: Einfach weil's die Laune hebt 😊",
    "Gurken-Wasser = Spa-Feeling for free! 🥒",
    "Augen-Training: Nah fokussieren, dann fern",
    "Unterarme entspannen - Tastatur ist kein Feind",
    "Letzter Screen-Break? Vor 3 Stunden? Echt jetzt?",
    "Beine unter'm Tisch ausstrecken - nobody's watching",
    "Sitz-Check: Rücken an Lehne? Füße am Boden?",
    "Energietief? Raus an die Luft hilft mehr als TikTok",
    "Tee-Zeremonie! Mach's mit Intention, nicht auf Auto-Pilot ☕",
    "Hände reiben, warm machen, aufs Gesicht - ahhhh",
    "Bewusst langsam atmen - nicht Speed-Atmen!",
    "Licht-Check: Zu dunkel? Zu grell? Goldilocks it!",
    "Triple-Threat: Snack + Wasser + Luft = Reset!",
    "Bildschirm-Helligkeit optimieren? Augen danken's dir",
    "Mal ohne Musik? Stille kann auch nice sein",
    "Nacken gut gestützt? Kopf wiegt 5kg, nur so!",
    "Daumen kreisen! Unterschätztes Körperteil.",
    "Future-You wird jetzt-You für die Pause danken",
    "Temperatur okay? Zu warm = instant Müdigkeit",
    "Handflächen auf Augen legen - instant Wellness 💆",
    "Wie lange sitzt du schon? Uff... lang, oder?",
    "Deine Haltung spricht Bände - welche Story erzählst du?",
    "Wasser pimpen: Minze, Ingwer, Limette - fancy!",
    "Tief seufzen erlaubt! Lungenlüften! 🌬️",
    "Füße kreisen lassen - die tragen dich durchs Leben!",
    "Fenster-Meditation: Einfach rausschauen, 30 Sekunden",
    "Snack-Mood: Süß oder salzig? Entscheide weise 😋",
    "Katze-Kuh-Move: Rücken rund, dann hohl 🐱🐄",
    "Umgebungs-Scan: Was brauchst du grade wirklich?",
    "Kopfmassage selbstgemacht - feels good!",
    "Bist du gerade produktiv oder nur busy? 🤔",
    "Wasserpause = Denkpause = beides wichtig!"
    ]

TIMER_ICONS = [
        [0, "🐈"], # 🦊 🌪️ 🥟 🥜 🧟 ☕️ 🥟 👀 🔥 🌙 💀 🐈 🐈‍⬛ 🐅 🐆
        [900, "🐈‍⬛"], # 15 minutes
        [1800, "🐅"], # 30 minutes
        [2700, "🐆"], # 45 minutes
        [3600, "🦊"], # 1 hour
        [3600+1800, "☕️"], # 1 hour 30 minutes
        [7200, "👀"], # 2 hours
        [10800, "🥟"], # 3 hours
        [14400, "🏃🏽‍♂️‍➡️"], # 4 hours
        [18000, "🧟"], # 5 hours
        [21600, "🔥"], # 6 hours
        [25200, "🌙"], # 7 hours
        [28800, "💀"], # 8 hours
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
        
        # Update icon based on active time
        self.update_icon()
        
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
    
    def update_icon(self):
        """Aktualisiert das Symbol basierend auf der aktiven Zeit"""
        for icon in TIMER_ICONS:
            if self.active_time >= icon[0]:
                self.title = icon[1]
    
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
            self.update_icon()  # Reset icon for new day
        
        # Check if user is active (idle < 30 seconds)
        idle_time = self.get_idle_time()
        
        if idle_time < 30:  # User ist aktiv
            time_passed = current_time - self.last_check
            self.active_time += time_passed
            
            # Update menu
            hours = int(self.active_time // 3600)
            minutes = int((self.active_time % 3600) // 60)
            self.menu["Aktive Zeit: 0h 0m"].title = f"Aktive Zeit: {hours}h {minutes}m"
            
            # Update icon based on active time
            self.update_icon()
            
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
