# Project Setup Guide

This guide assumes you're using a Mac and have the Apple Mail app installed. It will walk you through setting up a Python project that utilizes various APIs to automate tasks based on receiving specific emails. Please follow the steps carefully to ensure everything works correctly.

## Prerequisites

Before you begin, ensure that you have Python installed on your system. If you don't, please visit the [official Python website](https://www.python.org/downloads/) for installation instructions.

## Step 1: Install Required Libraries

Open your terminal and run the following command to install the necessary Python libraries:
```
pip install beautifulsoup4 requests openai
```

## Step 2: Configure Project Settings

Create a file named `config.py` in the root directory of your project. Fill it out with the following structure, replacing placeholder values with your actual information:

```python
EMAIL_ADDRESS = "your_email@something.com"  # Replace with your email address
EMAIL_PASSWORD = "your_app_password"  # Replace with your app password
OPENAI_API_KEY = "your_openai_api_key"  # Replace with your OpenAI API key
TELEGRAM_BOT_API = "your_telegram_bot_api"  # Replace with your Telegram Bot API
TELEGRAM_CHATID = "your_chat_id"  # Replace with your Telegram chat ID with your bot
USER_PHONE_NUMBER = "1234567890"  # Replace with your phone number
SLACK_BOT_OAUTH = "1234567890"      # Replace with your SLACK API

```

## Step 3: Obtaining API Keys and Passwords

1. Starting Septemeber of 2024 Google doesnt allow developers to access google accounts with just a gmail and password; you now need to adhere to OAuth 2.0, the industry-standard protocol for authorization. To get around this, we need to get an ‘app password.’ Follow the instructions in this link to get your app password: https://support.google.com/accounts/answer/185833?hl=en 

    Once you have the app password, put it into the EMAIL_PASSWORD in config.py

2. You will next need an OpenAI API Key if you dont already have one. This will require a credit card cince OpenAI’s pretrained models are not free :/ Follow the instructions with this link: https://www.howtogeek.com/885918/how-to-get-an-openai-api-key/ 

    Once you have the OpenAI API key, put it into the OPENAI_API_KEY in config.py

3. Next you’ll need a Telegram Bot API  and the bot itself. Follow the instructions here: https://stackoverflow.com/questions/43291868/where-to-find-the-telegram-api-key 

    Once you have the Telegram Bot API , put it into the TELEGRAM_BOT_API in config.py

4. Almost done, now you just need the chat id which tells telegram where you chat with your bot is. To get this, open telegram and in the search bar on the topleft corner, search for @getidsbot. Start a conversation or type in /start with this @getidsbot bot. It should return a message that looks like this:

```
Hello, User! I am a computer program that can chat (also known as a 'bot') and I can tell you something about you and the messages you send me.
Try it out, just forward me some messages ;)
Note from the developers:
This is a very early version of the bot. Therefore a few things (explainatory texts, etc.) are still missing. If you can code, here is the GitHub repo. If you don't know how to program, you can still help. Just tell us @wjclub.
👤 You
 ├ id: XXXXXXXXXX
 ├ is_bot: false
 ├ first_name: USer
 └ language_code: en (-)
```

    You want to grab the id: XXXXXXXXXX and replace TELEGRAM_CHATID in config.py

5. If you want to use, slack go to your workspace, in the main dropdown click 'tools & settings' -> manage apps. This will bring you to a browser in which you should select build from the top right. Click 'create new app' then click create from scratch. Add a name to the app and select the workspace you want your bot to exist in. You will get an API key for this bot which you should place in the config file. Then, in the browser again, go to 'OAuth and Permissions' section. Scroll down to scopes and under bot Token scopes add chat::write. Save and then go to 'Your Apps' and install the bot you just made. The last step is to navigate to the channel you want the bot to be in and type /invite @your-bot-name to invite your bot.

## Step 4: Automation

Ok, that’s it for the configuration. The last step is to make this program run everytime you get an email from dan@tldrnewsletter.com . The first step is to make a file in your project called run_daily_tech_brief.scpt and paste the following line into the file. Dont forget to replace ```/your/path/to/venv``` and ```/your/path/to``` with your paths:

```do shell script "source /your/path/to/venv/bin/activate && python3 /your/path/to/main.py"```


Next, open up the Apple Mail App and click ```Mail > Settings > Rules > Add Rule```. Go to ‘Perform the following actions: ‘ and select ```Run AppleScript```. The next field will ask you to select a script, select ‘Open in Finder’ and paste in the ```run_dailt_tech_brief.scpt``` file. Exit. Now, give your rule a name and set the following parameters. 
```
If [any] of the following conditions are met:
[From][contains][dan@tldrnewsletter.com]

Perform the following actions:
[Copy Message] to mailbox: [Inbox]
[Run Apple Script][run_daily_tech_brief]
```
Press Ok and you should be all set! Make sure your Apple System Preferances allow the Apple Script Editor and Apple Mail App to make changes and control your computer.
