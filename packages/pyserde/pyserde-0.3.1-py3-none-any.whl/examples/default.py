from dataclasses import dataclass, field
from typing import Dict

from serde import deserialize, serialize
from serde.json import from_json, to_json


@deserialize
@serialize
@dataclass
class Foo:
    i: int = 10
    s: str = 'foo'
    f: float = field(default=100.0)  # Use dataclass field.
    b: bool = field(default=True)
    d: Dict[str, int] = field(default_factory=dict)


def main():
    h = Foo()
    print(f"Into Json: {to_json(h)}")

    s = '{}'
    print(f"From Json: {from_json(Foo, s)}")


if __name__ == '__main__':
    main()
