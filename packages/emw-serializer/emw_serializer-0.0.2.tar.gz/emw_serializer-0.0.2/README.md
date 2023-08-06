# emw-serializer

- Basic serializer.
- Converts (nested) structures to `dict` or JSON string.
- Useful for API work.

## Usage
```
from emw_serializer import JsonSerializer


class Gakk:
    def __init__(self):
        self.a = 'a'
        self.b = 5


serializer = JsonSerializer()
thing_to_serialize = Gakk()
json = serializer.serialize(thing_to_serialize)
print(json)
```
will print
```
{
    "a": "a",
    "b": 5
}
```

## Capabilities
Caters for:
- `str`, `int`, `float`, `bool`
- `dict`, `list`, `set`
- `Enum`
- class properties
- object properties
- `@property` decorators
- `property()` function
