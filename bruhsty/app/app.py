import logging

from bruhsty.bot import BruhstyBot

from bruhsty import config
from bruhsty.config import UpdateType


def run(cfg: config.Config, logger: logging.Logger) -> None:
    bot = BruhstyBot(cfg.bot.token, logger)

    if cfg.bot.updates == UpdateType.POLLING:
        bot.start_polling(cfg.bot.polling.timeout)
    elif cfg.bot.updates == UpdateType.WEBHOOK:
        bot.start_webhook(
            host=cfg.bot.webhook.host,
        )
    else:
        raise AssertionError("Unknown update fetching type")
