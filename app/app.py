"""Define the main application"""


class Container[T]:
    def __init__(self, **kwargs: T):
        self.__dict__.update(kwargs)

    def __getattr__(self, item: str) -> T:
        return self.__dict__[item]


class App:
    def __init__(self):
        pass

    def build_app(self):
        pass
