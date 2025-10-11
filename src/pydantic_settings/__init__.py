class SettingsConfigDict(dict):
    """Minimal placeholder for compatibility."""


class BaseSettings:
    """Simplified BaseSettings replacement."""

    def __init__(self, **data):
        # apply class defaults
        for name, value in self.__class__.__dict__.items():
            if name.startswith("_") or callable(value) or isinstance(value, property):
                continue
            setattr(self, name, value)
        # override with provided values
        for name, value in data.items():
            setattr(self, name, value)
