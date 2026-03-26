from telegram.client import get_client
from utils.config_manager import get_config
from utils.errors import TSGError

_client = None

async def get_shared_client():
    global _client
    if _client is None:
        config = get_config()
        if not config["api_id"] or not config["api_hash"]:
            raise TSGError("Telegram API credentials not configured.")
        _client = get_client(config["api_id"], config["api_hash"])
        await _client.start()
    elif not getattr(_client, "is_connected", False):
        try:
            await _client.start()
        except Exception:
            pass
    return _client
