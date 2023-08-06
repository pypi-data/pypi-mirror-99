# The Concierge

The Concierge allows you to create a simple project for the development of a ready-to-use Telegram Bot.

The Concierge hides all the configuration part and allows you to use all your imagination in the business logic of the Telegram Bot.

All you have to do is put the handlers in the *handlers* folder and specify them in the *settings* file.

## Requirements

The Concierge is based on the Telethon package. It is a very useful Python package that allows you to use a Telegram MTProto API.

The purpose of The Concierge is to create a simple and flexible template for rapid prototyping of a Telegram Bot based on Telethon package.

Below, a list of all required packages:

* [Telethon](https://github.com/LonamiWebs/Telethon)

    ```pip install telethon```

* [TheConcierge](https://github.com/luigimalaguti/TheConcierge)

    ```pip install theconcierge```

## Quick-start

Before you start programming your bot, you need to get the Telegram App API Id and App API Hash. You can retrieve these data on the [official Telegram website](https://my.telegram.org) when you create an application. For more info see the following [link](https://core.telegram.org/api/obtaining_api_id).

To get the token needed for the bot, you can visit the official telegram website which explains how to use [BotFather](https://core.telegram.org/bots#6-botfather).

Perfect, now you can start programming your Bot.

The structure of your project is as follows:

```
<PROJECT ROOT>
    |
    +-- handlers
    |   +-- <SOME HANDLER>.py
    +-- settings
    |   +-- settings.json
    +-- <MAIN>.py
```

### Handlers

The *handlers* folder contains all the handlers that the bot needs to work.

An handler is a function that will execute when it occurs some events, example a *NewMessage*, *ChatAction* and other (the events is specified into *Telethon* package, see your [documentation](https://docs.telethon.dev/en/latest/) for more details).

Simple handler look like this:

```python
@events.register(events.NewMessage(pattern="(?i)hi|hello"))
async def random_handler(event):
    await event.respond("Hey!")
```

One important note is that Telethon is based on *asyncio* package that allow you run Telegram Bot in async mode, then you must defined your handler function with ```async``` and use *event* methods with ```await```.  
All is explained on official Telethon documentation.

### Settings

The *settings* folder is not request by Telethon, but by The Concierge.

Inside the *settings* folder there is the *settings.json* file which contains all the data necessary for The Concierge to register all the handlers automatically, simply by specifying the name of the module and the functions in question.

An example:

```json
...

"handlers": {
    "echo": [
        "simple_echo_handler",
        "complex_echo_handler"
    ],
    "welcome": [
        "welcome_italy",
        "walcome_english"
    ]
}

...
```

Note: All handlers in the setting.json will load, if an handler isn't into settings.json, this handler won't load.

In settings.json there is also a field *system* where you can insert your **api_id**, **api_hash** and **bot_token**. The Concierge will load them automatically.

Finally there is a *app* field into settings.json for all data app that you can needed.

### Main

The *main* is the file where you can launch you bot.

```python
from theconcierge import TheConcierge

def main():
    concierge = TheConcierge()
    concierge.start_bot()

main()
```

This is the bare minimum needed to launch your Telegram Bot based on Telethon and The Concierge.
