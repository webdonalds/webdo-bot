[![](https://img.shields.io/circleci/project/github/hellodhlyn/webdo-bot.svg?style=for-the-badge&logo=circleci&maxAge=3600)](https://circleci.com/gh/hellodhlyn/webdo-bot)
[![](https://img.shields.io/github/languages/top/hellodhlyn/webdo-bot.svg?style=for-the-badge&colorB=375eab&maxAge=3600)](#)

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
