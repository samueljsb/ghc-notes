import attrs


@attrs.frozen
class Definition:
    title: str

    # location
    file: str
    line: int


@attrs.frozen
class Reference:
    title: str

    # location
    file: str
    line: int
