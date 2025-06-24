# website-watcher

Get a Telegram notification when a certain term is present (or absent) on a website.

## Configuration

Copy `config_template.json` to config.json and replace Bot ID and chat ID by your own.
See [this article](https://medium.com/@ManHay_Hong/how-to-create-a-telegram-bot-and-send-messages-with-python-4cf314d9fa3e)
on how to create a new Telegram bot.

Then, configure your `sites` as follows:

* `name`: Name of the watch
* `url`: URL of the site to track
* `selector`: Which part of the site to check. Enter any [CSS selector](https://developer.mozilla.org/de/docs/Web/CSS/CSS_Selectors) here. Leave blank to check the whole site
* `term`: Term to search for
* `notify_on`: Either `present` or `absent` - what the condition should be to send out a notification
* `enabled`: Boolean to indicate whether the site watch is enabled

After a notification was triggered, the site will be disabled.

## Run

First, install the dependencies: `lxml` and `cssselect` are needed for applying the CSS selector.

For making the bot work, add a cron job (or similar) to execute `python bot.py`.
