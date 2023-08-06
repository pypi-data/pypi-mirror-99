# discord_slash.py
Attempting to create a framework for Discord Slash commands... yes

# Installation
`pip install slashpy`

# Documentation
Coming soon™

# Why is it forced to a guild?
Because I hate having the 1 hour cache when testing the output of these shits, so while I test, it will be controlled by config.json on which guild_id it will make commands to. I will later in time make a more dynamic way to change between global and guild.

# Commands folder
- Class name = Command name
- Class doc = Command desc.
- async reply = The JSON sent back as reply to Discord's POST webhook
