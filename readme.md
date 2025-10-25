# ☕️ CoffeeBreak - Dein Selbstfürsorge-Buddy

Eine freundliche macOS-App, die dich alle 2 Stunden aktiver Bildschirmnutzung daran erinnert, auf dich zu achten.

## 🎁 Das kann die App

- ⏱️ Trackt aktive Bildschirmnutzung (nicht nur "Mac ist an")
- 💬 Schickt alle 2h freundliche Erinnerungen (Wasser trinken, stretchen, etc.)
- ⏸️ Pausierbar für 10, 30 oder 60 Minuten (perfekt für Meetings!)
- ☕️ Sitzt diskret in der Menüleiste
- 🚀 Startet automatisch beim Login
- 🔄 Reset täglich um Mitternacht

## 📦 Installation (Super einfach!)

### Schritt 1: Download & Entpacken

1. Lade den `CoffeeBreak` Ordner herunter
2. Entpacke ihn irgendwo (z.B. auf dem Schreibtisch)

### Schritt 2: Terminal öffnen

1. Öffne die **Terminal**-App (Spotlight: `⌘ + Space`, dann "Terminal" eingeben)
2. Gehe in den CoffeeBreak-Ordner:
   ```bash
   cd ~/Desktop/CoffeeBreak
   ```
   (Anpassen, falls der Ordner woanders liegt!)

### Schritt 3: Installation starten

```bash
chmod +x setup.sh
./setup.sh
```

Das Script macht alles automatisch:
- ✅ Installiert benötigte Python-Pakete
- ✅ Baut die App
- ✅ Kopiert sie nach `/Applications`
- ✅ Richtet Autostart ein
- ✅ Startet die App

**Dauert ca. 2-3 Minuten!**

### Schritt 4: Berechtigungen erteilen

⚠️ **WICHTIG!** Damit die App funktioniert:

1. Gehe zu: **Systemeinstellungen → Datenschutz & Sicherheit**
2. Aktiviere unter **Benachrichtigungen**: `CoffeeBreak`
3. Falls macOS Berechtigungen abfragt: **"Erlauben"** klicken

## 🎯 Benutzung

### Das Menüleisten-Icon (☕️)

Klicke auf die Kaffeetasse in der Menüleiste, um:
- 📊 Deine aktive Zeit heute zu sehen
- ⏸️ Benachrichtigungen zu pausieren (10/30/60 Min)
- ℹ️ Infos über die App zu lesen
- ❌ Die App zu beenden

### Erinnerungen

Alle 2 Stunden aktiver Nutzung bekommst du eine freundliche Notification wie:

- *"Hey, trink mal was! Wann hattest du das letzte Glas Wasser? 💧"*
- *"Kurz aufstehen und strecken? Dein Rücken wird's dir danken!"*
- *"Schau mal kurz aus dem Fenster. Ernsthaft, die Welt ist noch da! 🌤️"*

### Pause-Funktion

Meeting oder Deep Work? Kein Problem:
- Klick auf die Kaffeetasse
- Wähle `Pause: 10/30/60 Minuten`
- Die App meldet sich danach wieder

**Der Timer läuft im Hintergrund weiter!**

## 🔧 Technische Details

- **Sprache**: Python 3
- **Framework**: rumps (Menüleisten-Apps)
- **Tracking**: IOKit Idle Time Detection
- **Speicherort**: `~/Library/Application Support/CoffeeBreak/`

## 🐛 Probleme?

### App startet nicht
```bash
# Manuell starten zum Debuggen:
/Applications/CoffeeBreak.app/Contents/MacOS/CoffeeBreak
```

### Keine Benachrichtigungen
→ Check Systemeinstellungen → Datenschutz & Sicherheit → Benachrichtigungen

### Autostart funktioniert nicht
```bash
# LaunchAgent neu laden:
launchctl unload ~/Library/LaunchAgents/com.coffeebreak.app.plist
launchctl load ~/Library/LaunchAgents/com.coffeebreak.app.plist
```

### App deinstallieren
```bash
# App löschen:
rm -rf /Applications/CoffeeBreak.app

# Autostart entfernen:
launchctl unload ~/Library/LaunchAgents/com.coffeebreak.app.plist
rm ~/Library/LaunchAgents/com.coffeebreak.app.plist

# Daten löschen:
rm -rf ~/Library/Application\ Support/CoffeeBreak
```

## 💝 Für den Beschenkten

Hey! Deine Freunde haben sich Gedanken gemacht und dir diese App geschenkt, weil sie wollen, dass du auf dich achtest. 

Die App nervt nicht - sie erinnert dich nur freundlich daran, dass du auch ein Mensch bist mit Bedürfnissen. 💙

Und hey: Du kannst die Erinnerungen jederzeit pausieren, wenn's gerade nicht passt. Kein Stress!

---

**Made with ☕️ and ❤️**

*P.S.: Der Code ist Open Source - du kannst die Erinnerungstexte in `coffee_break.py` nach Belieben anpassen!*
