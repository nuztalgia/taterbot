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
own worst sabo**tater**.

<b>TMI</b> (too much information) - Maybe.<br><b>LOL</b> (lots of love) -
Absolutely. 💜

Are you also a Potato looking to associ**tate** with a group of Clowns? Maybe
TaterBot can help you out. It's a shy bot that forms a very strong attachment to
its Potato, so it isn't publicly hosted anywhere - but you're more than welcome
to install/clone/fork this project and run your own personal TaterBot! 🌟

## Adopting a TaterBot

### 📜 Prerequisites

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

Do you meet the adoption requirements? If so, let's get this Potato rolling! 🥁

### 🌱 Installation & Usage

You can install and/or up**tate** TaterBot by using this command:

```
pip install -U git+https://github.com/nuztalgia/tater-bot.git
```

Once you've installed TaterBot, you can run it by using this command from any
directory:

```
tater-bot
```

<details>
<summary>
For information about the available command-line options, run
<code>tater-bot -h</code> (or click to expand this section).
</summary>
<br>

```
usage: tater-bot [-f] [-t] [-v] [--help] [<token id>]

  A Discord bot that serves as a cross-server spectater and communitater.
  Run "tater-bot" with no parameters to start the bot in development mode.

positional arguments:
  <token id>        The ID of the token to use to run the bot.
                    Valid options are "dev" and "prod".

options:
  -f, --force-sync  Force-sync all TaterBot app commands.
  -t, --tokens      View/manage your saved Discord bot tokens.
  -v, --version     Display the current bot version.
  -h, --help        Display this help message.
```

</details>

### 🔑 Onboarding & Security

If everything was planted correctly, you should see something like this after
running `tater-bot` for the first time:

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

<details>
<summary>
If you don't have a bot token and want more info on how to get one, click to
to expand this section.
</summary>
<hr>

1. To obtain a bot token, you'll first have to create a new **Discord App**. Go
   to the [Developer Portal](https://discord.com/developers/applications) and
   click the <kbd>New Application</kbd> button in the top-right corner. Enter an
   endearing name for your bot and click <kbd>Create</kbd>.

2. Now you should be on the **General Information** page for your app. Give it a
   cute profile picture and description - these will be visible to your Clowns!
   After **tating** care of those two things, you can move on from this page.

3. The next step is to add a "bot user" to your app, which allows it to appear
   in Discord similarly to other members. Navi**tate** to the **Bot** page using
   the sidebar menu on the left, then click the <kbd>Add Bot</kbd> button on the
   right.

4. After creating a bot user, you should see a <kbd>Reset Token</kbd> button.
   Click it to generate your new bot token! 🎉

<hr>
</details>

<details>
<summary>
Once you have a bot token, you can proceed through the Botstrap setup. Click to
expand this section for details.
</summary>
<hr>

1. At the initial prompt that asks `Would you like to add one now?`, type `yes`
   (or just `y`) and hit <kbd>Enter</kbd>.

2. Next, you'll be asked to enter your bot token (i.e. copy and paste it in).
   When you do, your input won't be visible on your screen - this is by design,
   to keep your token safe! Just trust that it's there, and hit <kbd>Enter</kbd>
   again.

3. If you entered your token correctly, you'll be prompted to run your bot. Go
   ahead and type `y`, then hit <kbd>Enter</kbd>.

<hr>
</details>

After your bot successfully authenti**tates** with Discord, you should see this
text on your screen:

```
TaterBot is online and ready!
```

Congratu**tations**, you're now a proud parent Potato! 👶

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
