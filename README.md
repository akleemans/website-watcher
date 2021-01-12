# scrape-notify-bot

Get a Telegram notification when a certain term is present (or absent) on a website.

## Configuration

Copy `config_template.json` to config.json and replace Bot ID and chat ID by your own.

Then, configure your `sites` as follows:

* `url`: URL of the site to track.
* `selector`: Which part of the site to check. Enter any [CSS selector](https://developer.mozilla.org/de/docs/Web/CSS/CSS_Selectors) here. Leave blank for checking the whole site.
* `term`: Term to search for.
* `notify_on`: Either `present` or `absent` - what the condition should be to send out a notification.

## Run

First, install the dependencies: `lxml` and `cssselect` are needed for applying the CSS selector.

For making the bot work, add a cron job (or similar) to execute `python bot.py`.
