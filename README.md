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

## 🚀 Quick Start (GitHub Codespaces)

### 1. Repository in Codespaces öffnen

1. Klicke auf den grünen "Code" Button
2. Wähle "Codespaces" Tab
3. Klicke "Create codespace on main"

### 2. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 3. Bot starten

```bash
python main.py
```

## ⚙️ Konfiguration

### Test-Konfiguration (bereits im Code enthalten)

Der Bot enthält bereits Test-API-Keys für sofortiges Testen:

```python
HELIUS_API_KEY = "391fbbd3-9807-426c-8717-7e283baebb62"
TELEGRAM_TOKEN = "8363468641:AAF8x1fLVo4ZMlLyFFYg5Ibw9_4gbReIv7I"
TELEGRAM_CHAT_ID = "6623899415"
WALLET_SECRET = [118, 120, 232, 76, 204, 84, 143, 91, ...] # Test-Wallet
```

### Umgebungsvariablen (optional)

Für die Produktion können eigene Keys über Umgebungsvariablen gesetzt werden:

```bash
export HELIUS_API_KEY="your-helius-api-key"
export TELEGRAM_TOKEN="your-telegram-bot-token"
export TELEGRAM_CHAT_ID="your-chat-id"
export WALLET_SECRET='[your,wallet,secret,array]'
export MAX_BUY_SOL="0.1"
export SLIPPAGE_BPS="500"
export TAKE_PROFIT_PERCENT="50.0"
export STOP_LOSS_PERCENT="30.0"
export USE_DEVNET="false"
```

## 📋 Parameter

| Parameter | Standard | Beschreibung |
|-----------|----------|-------------|
| `MAX_BUY_SOL` | 0.1 | Maximale SOL-Menge pro Trade |
| `SLIPPAGE_BPS` | 500 | Slippage in Basispunkten (500 = 5%) |
| `TAKE_PROFIT_PERCENT` | 50.0 | Take-Profit Schwelle in % |
| `STOP_LOSS_PERCENT` | 30.0 | Stop-Loss Schwelle in % |
| `USE_DEVNET` | false | Devnet für Tests verwenden |

## 🔧 Abhängigkeiten

- **solana** (>=0.30.2) - Solana Python SDK
- **solders** (>=0.18.1) - Solana Rust-basierte Tools
- **aiohttp** (>=3.9.0) - Async HTTP Client
- **websockets** (>=12.0) - WebSocket Support
- **requests** (>=2.31.0) - HTTP Library
- **python-telegram-bot** (>=20.0) - Telegram Bot API
- **python-dotenv** (>=1.0.0) - .env File Support

## 📱 Telegram Setup

### Test-Bot verwenden (bereits konfiguriert)

Der Bot nutzt bereits einen konfigurierten Test-Telegram-Bot. Keine weitere Einrichtung nötig!

### Eigenen Telegram Bot erstellen (optional)

1. Starte einen Chat mit [@BotFather](https://t.me/BotFather)
2. Sende `/newbot` und folge den Anweisungen
3. Kopiere den erhaltenen Token
4. Starte einen Chat mit deinem neuen Bot
5. Sende eine Nachricht
6. Hole deine Chat-ID: `https://api.telegram.org/bot<TOKEN>/getUpdates`
7. Setze die Werte in den Umgebungsvariablen

## 🔐 Helius RPC Setup

### Test-API verwenden (bereits konfiguriert)

Ein Test-Helius-API-Key ist bereits im Code enthalten.

### Eigenen API-Key erstellen (optional)

1. Registriere dich auf [Helius](https://www.helius.dev/)
2. Erstelle ein neues Projekt
3. Kopiere den API-Key
4. Setze `HELIUS_API_KEY` in den Umgebungsvariablen

## 💼 Wallet Setup

### Test-Wallet (bereits konfiguriert)

Ein Test-Wallet ist bereits konfiguriert:
- **Public Key**: `Fkm7vM1z6iXUNXqjXKYPBZVjJTNfMBT2D6yP5AWWNZn4`
- **Private Key**: Bereits im Code als Byte-Array

⚠️ **WICHTIG**: Dies ist ein Test-Wallet! Für echtes Trading einen eigenen Wallet erstellen!

### Eigenes Wallet erstellen (für Produktion)

```python
from solders.keypair import Keypair
import json

# Neues Wallet generieren
kp = Keypair()
print(f"Public Key: {kp.pubkey()}")
print(f"Secret Array: {json.dumps(list(bytes(kp)))}")
```

## 📊 Bot-Workflow

1. **Verbindung** - Bot verbindet sich mit Pump.fun WebSocket
2. **Monitoring** - Überwacht neue Token-Launches in Echtzeit
3. **Analyse** - Prüft Token anhand definierter Kriterien
4. **Ausführung** - Führt automatisch Buy-Orders via Jupiter aus
5. **Tracking** - Überwacht offene Positionen
6. **Management** - Triggert automatisch TP/SL
7. **Benachrichtigung** - Sendet Updates via Telegram

## 🔍 Logs

Der Bot loggt alle Aktivitäten:

```
2024-01-15 10:30:15 | INFO | Starting Pump.fun Sniper Bot...
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
├── main.py              # Hauptbot-Code
├── requirements.txt     # Python-Abhängigkeiten
└── README.md           # Diese Datei
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
1. Prüfe die Logs auf Fehlermeldungen
2. Stelle sicher, dass alle Dependencies installiert sind
3. Überprüfe die API-Keys und Konfiguration
4. Erstelle ein Issue auf GitHub

---

**Made with ❤️ for the Solana Community**
