import requests


class Endpoints:
    def __init__(self, bot_token: str, public_key: str, debug: bool = False):
        self.url = "https://discord.com/api/v8"

        self.debug = debug
        self.bot_token = bot_token
        self.public_key = public_key
        self.application_id = self.get_bot_id()

        self.application = f"{self.url}/applications/{self.application_id}"
        self.webhook = f"{self.url}/webhooks/{self.application_id}"
        self.interaction = f"{self.url}/interactions"

    def query(self, url: str, method: str = "get", *args, **kwargs):
        headers = {
            "Authorization": self.bot_token,
            "Content-Type": "application/json"
        }

        r = getattr(requests, method.lower())(url, headers=headers, *args, **kwargs)

        if self.debug:
            print(f"{r}\n{r.content}")

        return r

    def get_bot_id(self):
        """ Get the Bot/Application ID """
        r = self.query(f"{self.url}/users/@me")
        data = r.json()
        return int(data["id"])

    def prepare_endpoint(self, endpoint: str, method: str, guild_id: int = None, data=None):
        if guild_id:
            url = f"{self.application}/guilds/{guild_id}"
        else:
            url = f"{self.application}"

        r = self.query(f"{url}{endpoint}", method, json=data if data else None)
        return r

    def get_commands(self, guild_id: int = None):
        """ Get all commands on the slash endpoint """
        r = self.prepare_endpoint("/commands", "GET", guild_id=guild_id)
        return r.json()

    def get_command(self, command_id: int, guild_id: int = None):
        """ Get slash command by snowflake ID """
        r = self.prepare_endpoint(f"/commands/{command_id}", "GET", guild_id=guild_id)
        return r.json()

    def create_command(self, data, guild_id: int = None):
        """ Create a new slash command """
        r = self.prepare_endpoint("/commands", "POST", data=data, guild_id=guild_id)
        return r

    def edit_command(self, command_id: int, data, guild_id: int = None):
        """ Edit a slash command """
        r = self.prepare_endpoint(f"/commands/{command_id}", "PATCH", data=data, guild_id=guild_id)
        return r

    def delete_command(self, command_id: int, guild_id: int = None):
        """ Edit a slash command """
        r = self.prepare_endpoint(f"/commands/{command_id}", "DELETE", guild_id=guild_id)
        return r

    def message(self, interaction_token: str, message_id: str = "@original"):
        return f"{self.webhook}/{interaction_token}/messages/{message_id}"

    def followup_message(self, interaction_token: str):
        return f"{self.webhook}/{interaction_token}"
