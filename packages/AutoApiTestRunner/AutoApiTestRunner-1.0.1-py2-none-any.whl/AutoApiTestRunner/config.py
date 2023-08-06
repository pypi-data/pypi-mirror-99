from os import environ
from os.path import expanduser, exists
from json import load, dump

DEFAULT_GH_ORG = environ.get("DC_GH_ORG", "Shuttl-Tech")
DEFAULT_CACHE_FILE = "~/.autocli-cache"


class Config:
    def __init__(self, config_path="~/.autoclirc"):
        # These are values that aren't configurable at the moment
        self.cache_file = expanduser(DEFAULT_CACHE_FILE)

        self.config_path = expanduser(config_path)
        if not exists(self.config_path):
            self.attrs = {}
        else:
            self._load_from_file()

    def __getattr__(self, item):
        return self.attrs.get(item)

    def set(self, key, value):
        attrs = self.attrs.copy()
        attrs[key] = value
        self.update(**attrs)

    def __iter__(self):
        for k, v in self.attrs.items():
            yield k, v

    def _load_from_file(self):
        with open(self.config_path, "r") as c:
            self.attrs = load(c)

    def exists(self):
        return len(self.attrs) > 0

    def update(self, **kwargs):
        if "github_org" not in kwargs:
            kwargs["github_org"] = DEFAULT_GH_ORG

        for existing_key, existing_val in self:
            if existing_key not in kwargs:
                kwargs[existing_key] = existing_val

        with open(self.config_path, "w+") as c:
            dump(kwargs, c, indent=2, sort_keys=True)

        self._load_from_file()


config = Config()
