#!/bin/bash

# CoffeeBreak Installation Script
# Installiert die App und richtet Autostart ein

set -e  # Exit on error

echo "☕️  CoffeeBreak Installation"
echo "================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 ist nicht installiert!"
    echo "Bitte installiere Python 3 von https://www.python.org"
    exit 1
fi

echo "✅ Python 3 gefunden"
echo ""

# Create virtual environment
echo "📦 Erstelle virtuelle Python-Umgebung..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installiere Dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Clean previous builds
echo "🧹 Räume alte Builds auf..."
rm -rf build dist 2>/dev/null || true
sudo rm -rf /Applications/CoffeeBreak.app 2>/dev/null || true

# Build app (standalone, not alias mode)
echo "🔨 Baue CoffeeBreak.app..."
python setup.py py2app

# Copy to Applications
echo "📂 Kopiere nach /Applications..."
sudo cp -R dist/CoffeeBreak.app /Applications/
sudo chmod -R 755 /Applications/CoffeeBreak.app

# Create LaunchAgent directory
echo "🚀 Richte Autostart ein..."
LAUNCH_AGENT_DIR="$HOME/Library/LaunchAgents"
LAUNCH_AGENT_FILE="$LAUNCH_AGENT_DIR/com.coffeebreak.app.plist"

mkdir -p "$LAUNCH_AGENT_DIR"

# Unload if already exists
launchctl unload "$LAUNCH_AGENT_FILE" 2>/dev/null || true

# Create LaunchAgent
cat > "$LAUNCH_AGENT_FILE" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.coffeebreak.app</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/open</string>
        <string>/Applications/CoffeeBreak.app</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
EOF

# Load LaunchAgent
launchctl load "$LAUNCH_AGENT_FILE"

# Start app now
echo "🎬 Starte CoffeeBreak..."
open /Applications/CoffeeBreak.app

echo ""
echo "================================"
echo "✅ Installation erfolgreich!"
echo ""
echo "🎉 CoffeeBreak läuft jetzt!"
echo ""
echo "Du solltest eine Kaffeetasse ☕️ in der Menüleiste sehen."
echo "Die App startet automatisch bei jedem Login."
echo ""
echo "WICHTIG - Berechtigungen:"
echo "========================="
echo "1. Gehe zu: Systemeinstellungen → Datenschutz & Sicherheit"
echo "2. Aktiviere unter 'Benachrichtigungen': CoffeeBreak"
echo "3. Falls macOS nach Berechtigungen fragt: Erlauben!"
echo ""
echo "Viel Spaß und pass auf dich auf! ☕️❤️"
echo ""