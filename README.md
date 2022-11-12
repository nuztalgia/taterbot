<h1>
<picture><img src="https://github.com/nuztalgia/tater-bot/blob/main/tater_bot/assets/potato-purple-heart.png" width=32></picture>
TaterBot
</h1>

[![Botstrap](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fnuztalgia%2Fbotstrap%2Fmain%2F.github%2Fbadges%2Fbotstrap-on.json&logo=0)](https://github.com/nuztalgia/botstrap)
[![Project License](https://img.shields.io/github/license/nuztalgia/tater-bot?color=blue)](https://github.com/nuztalgia/tater-bot/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.10-blue)](https://github.com/nuztalgia/tater-bot/blob/main/pyproject.toml)
[![Build Status](https://img.shields.io/github/workflow/status/nuztalgia/tater-bot/Build)](https://github.com/nuztalgia/tater-bot/actions/workflows/build.yml)
[![CodeQL Status](https://img.shields.io/github/workflow/status/nuztalgia/tater-bot/CodeQL?label=codeQL)](https://github.com/nuztalgia/tater-bot/actions/workflows/codeql.yml)
[![CodeFactor](https://img.shields.io/codefactor/grade/github/nuztalgia/tater-bot/main?label=codefactor)](https://www.codefactor.io/repository/github/nuztalgia/tater-bot)

TaterBot is a personal Discord bot that serves as a cross-server spec**tater**
and communi**tater**. 🥔👾💗

It lets me (hereafter referred to as a "Potato") connect with a group of people
that I love dearly (hereafter referred to as "Clowns") even though my actual
Discord account is no longer in their server. Frankly, it's an overengineered
way for me to maintain boundaries and protect my mental health, because I'm my
own worst saboteur.

<b>TMI</b> (too much information) - Maybe.<br><b>LOL</b> (lots of love) -
Absolutely. 💜

Are you also a Potato looking to communi**tate** with a group of Clowns? Maybe
TaterBot can help you out. It's a shy bot that forms a very strong attachment to
its Potato, so it isn't publicly hosted anywhere - but you're more than welcome
to install/clone/fork this project and run your own instance of TaterBot. 🌱

## Adopting a TaterBot

First, you'll need to make sure you have a few things ready in order to properly
care for your TaterBot:

- **Python 3.10** - https://www.python.org/downloads/release/python-3108/
- `pip` (usually auto-installed with Python) -
  https://pip.pypa.io/en/stable/installation/
- `git` (just for installation; no need to know how to use it) -
  https://git-scm.com/downloads
- Basic familiarity with the
  [terminal or "command line"](https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Understanding_client-side_tools/Command_line#welcome_to_the_terminal)
  on your system

Do you meet the adoption requirements? If so, let's get this potato rolling!
**Install TaterBot** by using this command:

```
pip install -U git+https://github.com/nuztalgia/tater-bot.git
```

Once you've installed TaterBot, you can run it by using the following command
from any directory:

```
tater-bot
```

If everything was planted correctly, you should see something like this after
running the above command:

```
tater-bot: You currently don't have a saved development bot token.
Would you like to add one now? If so, type "yes" or "y":
```

A **bot token** is essentially the "key" to your bot's Discord account. It's
used for authorizing API requests and carries all of your bot's permissions,
which makes it a very sensitive piece of data. It should **never** be shared
with other people. For these reasons, TaterBot uses
[**Botstrap**](https://botstrap.readthedocs.io/) to safely encrypt/store tokens
and avoid potential security disas**taters**. 💥

Once you have your bot token ready, you can proceed through the Botstrap setup
by typing `yes` and hitting <kbd>Enter</kbd>.

## Development

Are you a fellow compu**tater** programmer? If so, you might be interested in
these commands:

```
git clone https://github.com/nuztalgia/tater-bot.git
cd tater-bot
pip install -e .
```

This will create an
[editable](https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs)
installation of TaterBot in your current environment. Any changes you make to
its code will immediately take effect when you run `tater-bot` locally.

[Contributions](https://github.com/nuztalgia/tater-bot/blob/main/.github/contributing.md)
to this project are very welcome, as long as they
[pass](https://results.pre-commit.ci/latest/github/nuztalgia/tater-bot/main)
[all](https://github.com/nuztalgia/tater-bot/actions/workflows/build.yml)
[the](https://github.com/nuztalgia/tater-bot/actions/workflows/codeql.yml)
[checks](https://www.codefactor.io/repository/github/nuztalgia/tater-bot) to
keep it green and healthy! 💚

## License

**Source Code:** Copyright © 2022
[Nuztalgia / Lovegood](https://github.com/nuztalgia). Released under the
[MIT License](https://github.com/nuztalgia/tater-bot/blob/main/LICENSE).

**Image Assets:** Included under [fair use](https://www.copyright.gov/fair-use/)
and **not** covered by the above license. See
[`assets/README.md`](https://github.com/nuztalgia/tater-bot/tree/main/tater_bot/assets)
for more details.
