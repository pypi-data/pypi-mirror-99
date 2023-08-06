import inspect


class Command:
    """ No description available """
    def __init__(self, bot):
        self.bot = bot
        doc_desc = type(self).__doc__
        self.name = type(self).__name__.lower()
        self.description = inspect.cleandoc(doc_desc) if doc_desc else ""
        self.options = []
        self.command = {}
        self.id = None

        if not isinstance(self.name, str):
            raise TypeError("Command name must be a string")

    def prepare(self, bot):
        pass

    async def reply(self, bot):
        pass

    @property
    def raw(self):
        """ Display raw JSON """
        return self.command

    def build(self):
        """ Build the JSON command """
        self.prepare(self.bot)
        self.command["name"] = self.name
        self.command["description"] = self.description or "No description available"
        self.command["options"] = self.options
        return self.command


class Option:
    def __init__(self):
        self.options = []

    def build(self):
        return self.options

    def add_values(self, name: str, description: str, values: tuple, required: bool = True):
        choices = [
            {"name": name, "value": value}
            for name, value in values
        ]

        make_option = {
            "name": name, "description": description,
            "type": 3, "required": required, "choices": choices
        }

        self.options.append(make_option)
        return make_option
