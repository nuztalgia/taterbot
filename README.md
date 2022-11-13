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
to install/clone/**fork** this project and run your own personal TaterBot! 🌟

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
   ap**peel**ing name for your bot and click <kbd>Create</kbd>.

2. Now you should be on the **General Information** page for your app. Give it a
   cute profile picture and description - these will be visible to your Clowns!
   After **tating** care of those two things, you can move on from this page.

3. The next step is to add a "bot user" to your app, which allows it to appear
   in Discord similarly to other members. Navi**tate** to the **Bot** page using
   the sidebar menu on the left, then click the <kbd>Add Bot</kbd> button on the
   right.

4. After creating a bot user, you should see a <kbd>Reset Token</kbd> button.
   Click it to gener**tate** your bot token! 🎉

<hr>
</details>

<details>
<summary>
If you have a bot token but are unsure of how to proceed through the Botstrap
setup, click to expand this section.
</summary>
<hr>

1. At the initial prompt that asks `Would you like to add one now?`, type `yes`
   (or just `y`) and hit <kbd>Enter</kbd>.

2. Next, you'll be asked to enter your bot token (i.e. copy and paste it in).
   When you do, your input won't be visible on the screen - this is by design,
   to keep your token safe! Just trust that it's there, and hit <kbd>Enter</kbd>
   again.

3. If you entered your token correctly, you'll be prompted to run your bot. Go
   ahead and type `y`, then hit <kbd>Enter</kbd>.

<hr>
</details>

After you set up your token and your bot successfully authenti**tates** with
Discord, you should see this message:

```
TaterBot is online and ready!
```

Congratu**tations**, you're now the proud Potato parent of a tiny Tater tot! 👶

## Putting Down Roots

### 🥔 Instructions for the Potato

So your bot is online and ready, but where exactly is it? If you haven't added
it to any Discord servers yet, you should check your potato clock... because
it's time for your TaterBot to put down its roots! 🌞

<img align="right" src="https://user-images.githubusercontent.com/95021853/201503489-c583281a-659b-4fd9-b87d-a969267c1c2a.png" width=320>

Open up the [Developer Portal](https://discord.com/developers/applications/)
(again) and select your app. Navi**tate** to the **Bot** page using the sidebar
menu on the left, then scroll down a little bit. There are **two** switches that
you need to flip on this page:

- **Server Members Intent** - This should be turned **ON**.
- **Message Content Intent** - This should be turned **ON**.

Make sure to leave all the other switches as they originally were!

<img align="left" src="https://user-images.githubusercontent.com/95021853/201504285-7398b3ad-20c6-47f2-8b11-4414cbb4222f.png" width=320>

Next, click **OAuth2** in the sidebar menu on the left. It'll expand to reveal
two sub-pages - click the one labeled **URL Generator**. On this page, select
the `bot` checkbox, and another section will appear.

There are **seven** new checkboxes that you need to select in order for your
TaterBot to work, and they're all in the **Text Permissions** column:<br>
`Send Messages`, `Embed Links`, `Attach Files`, `Read Message History`,
`Use External Emojis`, `Add Reactions`, and `Use Slash Commands`.

Once you've selected all the appropriate permissions, click the <kbd>Copy</kbd>
button in the bottom-right corner of the page. Send the result (your TaterBot's
custom invite link) to a trusted Clown, then wait anxiously for them to accept
it. 🤡

### 🎪 Instructions for the Clowns

<img align="right" src="https://user-images.githubusercontent.com/95021853/201505432-1fb57038-b441-493e-a425-f2a199498df6.png" width=100>

A server admin for the Clowns will have to open the bot invite link provided by
the Potato in order to allow their TaterBot to facili**tate** communi**tation**.
Upon doing so, they should see a dialog that looks similar to the one in the
picture to the right - but with different names and icons, of course. (You _did_
give your bot a cute name and avatar like the instructions said to do... right?
😜)

The Clowns admin should verify that the requested permissions are
`Send Messages`, `Embed Links`, `Attach Files`, `Read Message History`,
`Add Reactions`, `Use External Emojis`, and last but not least,
`Use Application Commands`. They should then grant your TaterBot these
permissions and add it to the server by clicking the <kbd>Authorize</kbd>
button.

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
