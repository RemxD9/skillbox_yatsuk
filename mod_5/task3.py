class BlockErrors:
    def __init__(self, ignored_errors):
        self.ignored_errors = ignored_errors

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type and any(issubclass(exc_type, e) for e in self.ignored_errors):
            return True  # Игнорируем ошибку
        return False
