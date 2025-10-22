#!/usr/bin/env python3
"""
Erweiterter Pump.fun Sniper Bot – Telegram-gesteuert
- Start/Stop via Telegram Kommandos (/startbot, /stopbot)
- Läuft Haupt-Tasks im Hintergrund und managed Lebenszyklus
"""
import os
import asyncio
import json
import logging
import websockets
import aiohttp
from typing import Dict, Any
from datetime import datetime

from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from solders.keypair import Keypair

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
log = logging.getLogger("pump_sniper_ext")

HELIUS_API_KEY = os.getenv("HELIUS_API_KEY", "")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
WALLET_SECRET = os.getenv("WALLET_SECRET", json.dumps([0]*64))
MAX_BUY_SOL = float(os.getenv("MAX_BUY_SOL", "0.1"))
SLIPPAGE_BPS = int(os.getenv("SLIPPAGE_BPS", "500"))
TAKE_PROFIT_PERCENT = float(os.getenv("TAKE_PROFIT_PERCENT", "50.0"))
STOP_LOSS_PERCENT = float(os.getenv("STOP_LOSS_PERCENT", "30.0"))
USE_DEVNET = os.getenv("USE_DEVNET", "false").lower() == "true"

class PumpSniperBot:
    def __init__(self):
        self.running = asyncio.Event()
        self.stop_signal = asyncio.Event()
        self.positions: Dict[str, Any] = {}
        self.trades_made = 0
        self.rpc_url = f"https://{'devnet' if USE_DEVNET else 'mainnet'}.helius-rpc.com/?api-key={HELIUS_API_KEY}"
        self.client: AsyncClient | None = None
        self.wallet = Keypair.from_bytes(bytes(json.loads(WALLET_SECRET)))
        self.bg_tasks: list[asyncio.Task] = []
        log.info(f"Wallet initialized: {self.wallet.pubkey()}")

    async def send_telegram(self, message: str):
        try:
            if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
                log.debug("Telegram not configured; skipping send.")
                return
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
            async with aiohttp.ClientSession() as session:
                await session.post(url, json=data)
        except Exception as e:
            log.error(f"Telegram send error: {e}")

    async def health_check(self):
        while self.running.is_set() and not self.stop_signal.is_set():
            try:
                await asyncio.sleep(300)
                msg = (
                    f"🔄 Health Check\n"
                    f"Status: {'Running' if self.running.is_set() else 'Stopped'}\n"
                    f"Trades: {self.trades_made}\n"
                    f"Positions: {len(self.positions)}"
                )
                await self.send_telegram(msg)
            except Exception as e:
                log.error(f"Health check error: {e}")

    async def monitor_pump_feed(self):
        ws_url = "wss://pumpportal.fun/api/data"
        while self.running.is_set() and not self.stop_signal.is_set():
            try:
                async with websockets.connect(ws_url) as ws:
                    await ws.send(json.dumps({"method": "subscribeNewToken"}))
                    log.info("Connected to Pump.fun WebSocket")
                    async for msg in ws:
                        if not self.running.is_set() or self.stop_signal.is_set():
                            break
                        data = json.loads(msg)
                        if data and 'mint' in data:
                            await self.handle_new_token(data)
            except Exception as e:
                if not self.running.is_set():
                    break
                log.error(f"WebSocket error: {e}")
                await asyncio.sleep(5)

    async def handle_new_token(self, token_data: Dict[str, Any]):
        try:
            mint = token_data.get('mint')
            symbol = token_data.get('symbol', 'UNKNOWN')
            log.info(f"New token detected: {symbol} ({mint})")
            await self.send_telegram(f"🚀 New Token\n{symbol} - {mint}")
            if await self.should_snipe(token_data):
                await self.execute_buy(mint, symbol)
        except Exception as e:
            log.error(f"Token handling error: {e}")

    async def should_snipe(self, token_data: Dict[str, Any]) -> bool:
        return True

    async def execute_buy(self, mint: str, symbol: str):
        try:
            log.info(f"Attempting to buy {symbol}...")
            async with aiohttp.ClientSession() as session:
                # Placeholder: integrate Jupiter here
                await asyncio.sleep(0.2)
            self.trades_made += 1
            self.positions[mint] = {
                'symbol': symbol,
                'buy_price': MAX_BUY_SOL,
                'amount': 0,
                'timestamp': datetime.now().isoformat()
            }
            await self.send_telegram(f"✅ Buy Executed\n{symbol} for {MAX_BUY_SOL} SOL")
        except Exception as e:
            log.error(f"Buy execution error: {e}")
            await self.send_telegram(f"❌ Buy Failed\n{symbol}: {e}")

    async def monitor_positions(self):
        while self.running.is_set() and not self.stop_signal.is_set():
            try:
                await asyncio.sleep(30)
                for mint, position in list(self.positions.items()):
                    await self.check_position(mint, position)
            except Exception as e:
                log.error(f"Position monitoring error: {e}")

    async def check_position(self, mint: str, position: Dict[str, Any]):
        try:
            pass
        except Exception as e:
            log.error(f"Position check error: {e}")

    async def start_core(self):
        if self.running.is_set():
            await self.send_telegram("ℹ️ Bot already running.")
            return
        self.stop_signal.clear()
        self.running.set()
        await self.send_telegram("🤖 Bot started.")
        self.client = AsyncClient(self.rpc_url, commitment=Confirmed)
        self.bg_tasks = [
            asyncio.create_task(self.monitor_pump_feed()),
            asyncio.create_task(self.monitor_positions()),
            asyncio.create_task(self.health_check()),
        ]

    async def stop_core(self):
        if not self.running.is_set():
            await self.send_telegram("ℹ️ Bot already stopped.")
            return
        await self.send_telegram("🛑 Stopping bot...")
        self.running.clear()
        self.stop_signal.set()
        for t in self.bg_tasks:
            t.cancel()
        self.bg_tasks.clear()
        try:
            if self.client:
                await self.client.close()
        finally:
            self.client = None
        await self.send_telegram("✅ Bot stopped.")

    async def telegram_webhook_loop(self):
        # Long-polling Telegram updates to receive commands
        if not TELEGRAM_TOKEN:
            log.warning("No TELEGRAM_TOKEN set; Telegram control disabled.")
            return
        last_update_id = None
        base = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
        async with aiohttp.ClientSession() as session:
            while not self.stop_signal.is_set():
                try:
                    params = {"timeout": 50}
                    if last_update_id is not None:
                        params["offset"] = last_update_id + 1
                    async with session.get(f"{base}/getUpdates", params=params, timeout=60) as resp:
                        if resp.status != 200:
                            await asyncio.sleep(2)
                            continue
                        payload = await resp.json()
                        for update in payload.get("result", []):
                            last_update_id = update.get("update_id", last_update_id)
                            message = update.get("message") or update.get("edited_message")
                            if not message:
                                continue
                            chat_id = str(message.get("chat", {}).get("id"))
                            text = (message.get("text") or "").strip()
                            if TELEGRAM_CHAT_ID and chat_id != str(TELEGRAM_CHAT_ID):
                                continue  # ignore other chats
                            await self.handle_telegram_command(text)
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    log.error(f"Telegram loop error: {e}")
                    await asyncio.sleep(2)

    async def handle_telegram_command(self, text: str):
        cmd = text.split()[0].lower()
        if cmd in ("/startbot", "startbot"):
            await self.start_core()
        elif cmd in ("/stopbot", "stopbot"):
            await self.stop_core()
        elif cmd in ("/status", "status"):
            await self.send_telegram(
                f"📊 Status: {'Running' if self.running.is_set() else 'Stopped'}\n"
                f"Trades: {self.trades_made}\nPositions: {len(self.positions)}"
            )
        else:
            await self.send_telegram("Befehle: /startbot, /stopbot, /status")

async def main():
    bot = PumpSniperBot()
    # Start Telegram control loop always
    tel_task = asyncio.create_task(bot.telegram_webhook_loop())
    # Optionally autostart bot if env set
    if os.getenv("AUTOSTART", "false").lower() == "true":
        await bot.start_core()
    try:
        # Keep process alive; wait until SIG via /stopbot then cancel
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass
    finally:
        tel_task.cancel()
        with contextlib.suppress(Exception):
            await tel_task

if __name__ == "__main__":
    import contextlib
    asyncio.run(main())
