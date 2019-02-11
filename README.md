# Webdo Bot

> Telegram bot for webdonalds.  
> Forked from [HelloDHLyn/tenri-bot](https://github.com/HelloDHLyn/tenri-bot).

## Development

### Prerequisites

  - Python 3.6 or later

### Environment Variables

  - `TELEGRAM_BOT_TOKEN`

### Run unittests

```sh
python -m unittest test/**.py
```

## Deploy

Use docker to start bot server.

```
docker build -t hellodhlyn/webdo-bot .
docker run -e "TELEGRAM_BOT_TOKEN=<your_bot_token>" hellodhlyn/webdo-bot
```
