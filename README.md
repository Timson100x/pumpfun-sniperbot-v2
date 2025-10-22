# Pumpfun Sniper Bot

🤖 **Automatisierter Kryptowährungs-Handelsbot für Pump.fun Token-Launches**

Ein fortgeschrittener Sniper-Bot für Solana, der neue Token-Launches auf Pump.fun überwacht und automatisch handelt. Mit Jupiter-Swaps, PnL-Tracking, Slippage-Kontrolle, Take-Profit/Stop-Loss und Telegram-Benachrichtigungen.

## ✨ Features

- 🚀 **Echtzeit-Monitoring** - WebSocket-Verbindung zu Pump.fun für sofortige Token-Launch-Erkennung
- 💱 **Jupiter Integration** - Automatische Swaps über Jupiter DEX Aggregator
- 📊 **PnL Tracking** - Überwachung offener Positionen mit Profit/Loss-Berechnung
- 🎯 **TP/SL Management** - Automatisches Take-Profit und Stop-Loss
- 📱 **Telegram Notifications** - Echtzeitbenachrichtigungen über alle Bot-Aktivitäten
- 🔧 **Konfigurierbar** - Anpassbare Parameter für Slippage, Buy-Amount, TP/SL
- 🛡️ **Robustes Error-Handling** - Automatische Wiederverbindung und Fehlerbehandlung
- 🏥 **Health Checks** - Periodische Statusmeldungen
- ⚡ **Autostart** - Automatischer Bot-Start beim Codespace-Launch

## 🚀 Quick Start (GitHub Codespaces)

### 1. Repository in Codespaces öffnen

1. Klicke auf den grünen "Code" Button
2. Wähle "Codespaces" Tab
3. Klicke "Create codespace on main"

### 2. Automatischer Start (empfohlen)

**Der Bot startet jetzt automatisch!** 🎉

Dank der `.devcontainer/devcontainer.json` Konfiguration:
- ✅ Abhängigkeiten werden automatisch installiert
- ✅ Bot startet im Hintergrund mit AUTOSTART=true
- ✅ Logs werden in `bot.log` geschrieben

**Bot-Status prüfen:**
```bash
# Logs anzeigen
tail -f bot.log

# Bot-Prozess prüfen
ps aux | grep main.py

# Bot stoppen (falls nötig)
pkill -f main.py
```

### 3. Manueller Start (optional)

Falls du den Bot manuell starten möchtest:
```bash
# Abhängigkeiten installieren
pip install -r requirements.txt

# Bot im Vordergrund starten
python main.py

# Oder im Hintergrund
nohup python main.py > bot.log 2>&1 &
```

## 🔧 Automatisierungs-Konfiguration

Die Autostart-Funktion wird durch folgende Dateien gesteuert:

### `.devcontainer/devcontainer.json`
```json
{
  "name": "Pump.fun Sniper Bot",
  "image": "mcr.microsoft.com/devcontainers/python:3.11",
  "postCreateCommand": "pip install -r requirements.txt",
  "postStartCommand": "nohup python main.py > bot.log 2>&1 &",
  "remoteEnv": {
    "AUTOSTART": "true"
  }
}
```

**Erklärung:**
- `postCreateCommand`: Installiert Dependencies beim ersten Codespace-Start
- `postStartCommand`: Startet den Bot automatisch bei jedem Codespace-Start
- `remoteEnv.AUTOSTART`: Setzt die Umgebungsvariable für automatischen Betrieb

**AUTOSTART deaktivieren:**

Falls du den automatischen Start nicht möchtest:
1. Öffne `.devcontainer/devcontainer.json`
2. Entferne die `postStartCommand` Zeile
3. Oder setze `AUTOSTART` auf `false`
4. Rebuild den Codespace (Cmd/Ctrl+Shift+P → "Rebuild Container")

## ⚙️ Konfiguration

### Test-Konfiguration (bereits im Code enthalten)

Der Bot enthält bereits Test-API-Keys für sofortiges Testen:

```python
HELIUS_API_KEY = "391fbbd3-9807-426c-8717-7e283baebb62"
TELEGRAM_BOT_TOKEN = "7804077648:AAGLkUo-XE-pZLjN0QjhsF2u4AKI9FRNzE8"
TELEGRAM_CHAT_ID = "1287390765"
PRIVATE_KEY = "MGuQArsL3fWTiv2hvcAwEBkxpDqJeVYMbGxkZLPRpump"
```

### Produktiv-Konfiguration

**⚠️ Für Live-Trading IMMER eigene Keys verwenden!**

1. **Helius API Key** (kostenlos)
   - Registriere dich auf [helius.dev](https://www.helius.dev/)
   - Erstelle einen API Key
   - Ersetze `HELIUS_API_KEY` im Code

2. **Telegram Bot**
   - Erstelle einen Bot über [@BotFather](https://t.me/botfather)
   - Kopiere den Token
   - Ersetze `TELEGRAM_BOT_TOKEN` im Code
   - Sende eine Nachricht an deinen Bot
   - Hole deine Chat-ID über: `https://api.telegram.org/bot<TOKEN>/getUpdates`
   - Ersetze `TELEGRAM_CHAT_ID` im Code

3. **Solana Wallet**
   - Generiere ein neues Keypair:
   ```bash
   solana-keygen new --no-passphrase -o wallet.json
   ```
   - Exportiere den Private Key:
   ```bash
   cat wallet.json
   ```
   - Ersetze `PRIVATE_KEY` im Code
   - ⚠️ **WICHTIG**: Fülle das Wallet mit SOL für Trading

### Handelsparameter anpassen

Öffne `main.py` und passe die Konfiguration an:

```python
# Bot-Konfiguration
SLIPPAGE_BPS = 500  # 5% Slippage
BUY_AMOUNT_SOL = 0.01  # Kaufbetrag in SOL
TAKE_PROFIT_PERCENT = 50  # 50% Take Profit
STOP_LOSS_PERCENT = 20  # 20% Stop Loss
CHECK_INTERVAL = 60  # PnL-Check alle 60 Sekunden
HEALTH_CHECK_INTERVAL = 600  # Statusmeldung alle 10 Minuten
```

## 📋 Voraussetzungen

- Python 3.11+
- GitHub Codespaces (empfohlen) oder lokales Setup
- Helius API Key (für Solana RPC)
- Telegram Bot (für Benachrichtigungen)
- Solana Wallet mit SOL-Guthaben

## 🔄 Workflow

1. **Token-Erkennung**: Bot verbindet sich mit Pump.fun WebSocket
2. **Automatischer Kauf**: Bei neuem Token automatischer Kaufversuch
3. **PnL-Monitoring**: Kontinuierliche Überwachung der Position
4. **TP/SL-Ausführung**: Automatischer Verkauf bei Erreichen der Schwellenwerte
5. **Telegram-Updates**: Benachrichtigungen über alle Aktivitäten

## 📊 Beispiel-Output

```
2024-01-15 10:30:15 | INFO | Network: Mainnet
2024-01-15 10:30:15 | INFO | Wallet: Fkm7vM1z6iXUNXqjXKYPBZVjJTNfMBT2D6yP5AWWNZn4
2024-01-15 10:30:16 | INFO | Connected to Pump.fun WebSocket
2024-01-15 10:31:42 | INFO | New token detected: PUMP (7xK...)
2024-01-15 10:31:43 | INFO | Attempting to buy PUMP...
2024-01-15 10:31:45 | INFO | Buy order executed for PUMP
```

## ⚠️ Disclaimer

**WICHTIG**: Dies ist experimentelle Software für Bildungszwecke.

- ⚠️ Trading birgt erhebliche Risiken
- 💰 Verwende nur Kapital, dessen Verlust du dir leisten kannst
- 🔒 Die enthaltenen Test-Keys sind NUR für Tests gedacht
- 🚫 Keine Garantie für Profite oder Funktionalität
- 📜 Verwende auf eigenes Risiko

## 🛠️ Entwicklung

### Code-Struktur

```
pumpfun-sniperbot-v2/
├── .devcontainer/
│   └── devcontainer.json  # Codespace-Konfiguration
├── main.py                # Hauptbot-Code
├── requirements.txt       # Python-Abhängigkeiten
└── README.md             # Diese Datei
```

### Beitragen

Contributions sind willkommen! Pull Requests und Issues gerne einreichen.

## 📄 Lizenz

MIT License - siehe LICENSE für Details

## 🔗 Links

- [Pump.fun](https://pump.fun)
- [Jupiter DEX](https://jup.ag)
- [Helius RPC](https://www.helius.dev/)
- [Solana Docs](https://docs.solana.com/)
- [Telegram Bot API](https://core.telegram.org/bots)

## 💬 Support

Bei Fragen oder Problemen:

1. Prüfe die Logs auf Fehlermeldungen (`tail -f bot.log`)
2. Stelle sicher, dass alle Dependencies installiert sind
3. Überprüfe die API-Keys und Konfiguration
4. Erstelle ein Issue auf GitHub

---

**Made with ❤️ for the Solana Community**
