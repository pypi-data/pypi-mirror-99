import attr


@attr.dataclass(slots=True)
class DataKeyDoc:
    key: str
    doc_count: float
