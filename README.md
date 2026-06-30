# Midea PortaSplit Monitor

Automatischer Deal-Tracker für die Midea PortaSplit Klimaanlage.

## Features

- ✅ Preisüberwachung (< 900 €)
- ✅ Verfügbarkeitsprüfung
- ✅ Keine doppelten Alerts
- ✅ Telegram Benachrichtigung
- ✅ Läuft komplett auf GitHub Actions

---

## 🚀 Setup

### 1. Repo erstellen

- Neues GitHub Repository erstellen
- Code hochladen

---

### 2. Telegram Bot erstellen

1. Öffne: https://t.me/BotFather
2. `/start`
3. `/newbot`
4. Token kopieren

Chat ID holen:
- Bot anschreiben
- https://api.telegram.org/bot<TOKEN>/getUpdates

---

### 3. Secrets setzen

GitHub → Settings → Secrets:

``
TELEGRAM_TOKEN TELEGRAM_CHAT_ID

---

### 4. Workflow aktivieren

- Actions Tab öffnen
- Workflow starten oder automatisch warten

---

## ⏱ Zeitplan

Alle 6 Stunden:
0 */6 * * *

---

## 📦 Erweiterbarkeit

- Neue Shops → `shops/`
- Neue Produkte → `config.py`
- Email Support → `notifier.py`

---

## ⚠️ Hinweise

- Idealo ist Hauptquelle
- Einige Shops blockieren Scraping → später mit Playwright erweitern
