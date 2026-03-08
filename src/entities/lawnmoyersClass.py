from dataclasses import dataclass

@dataclass(repr=False)
class Lawnmoyer:
    name: str = "Lawnmoyer"
    speed: float = 2.5

    def to_string(self) -> str:
        return self.name.upper()