import json

from enum import Enum


class BaseSerializer:
    def _serialize(self, something):
        if isinstance(something, Enum):
            return something.value

        if isinstance(something, dict):
            element = {}
            for key, value in something.items():
                element[key] = self._serialize(value)
            return element

        if hasattr(something, "__dict__"):
            element = {}
            for key in dir(something):
                if key.startswith("_"):
                    continue
                # if getattr(something, key) is None:
                #     continue
                if callable(getattr(something, key)):
                    continue
                element[key] = self._serialize(getattr(something, key))
            return element

        if isinstance(something, list):
            element = []
            for value in something:
                element.append(self._serialize(value))
            return element

        if isinstance(something, set):
            element = []
            for value in something:
                element.append(self._serialize(value))
            return element

        return something


class Serializer(BaseSerializer):
    def __init__(self):
        super().__init__()

    def serialize(self, something):
        return self._serialize(something)


class JsonSerializer(BaseSerializer):
    def __init__(self):
        super().__init__()

    def serialize(self, something):
        return json.dumps(self._serialize(something))
