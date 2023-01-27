# ChatGPT QA System on Slack

ChatGPT QA System will reply your question on the thread, using ChatGPT, on Slack.

## version

* Python==3.9.2

## setup

1. prepare `conf/config.json`
   ```
   {
       "email": "hoge",
       "password": "hoge",
       "isMicrosoftLogin": true,
       "driver_exec_path": "hoge"
   }
   ```
2. prepare `.env`
   ```
   SLACK_CHANNEL_ID=hoge
   SLACK_ACCESS_TOKEN=hoge
   SLACK_BOT_ID=hoge
   CHATGPT_CONF_PATH=/path/to/config.json
   MIN_INTERVAL=5
   ```
3. prepare `bin/chromedriver`
4. prepare venv
   ```shell
   $ python3 -m venv .venv
   $ source .venv/bin/activate
   $ pip3 install -r requirements.txt
   ```
