from abc import abstractmethod, ABC


class Generator(ABC):
    """
    Abstract class for generating events for a provider
    """
    def __init__(self, config=None):
        self.config = config

    @abstractmethod
    def generate(self) -> None:
        return "Generated content"