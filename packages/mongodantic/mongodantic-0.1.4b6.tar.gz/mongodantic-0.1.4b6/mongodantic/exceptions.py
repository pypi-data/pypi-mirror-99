class BaseMongodanticException(Exception):
    pass


class NotDeclaredField(BaseMongodanticException):
    def __init__(self, field_name: str, fields: list, *args):
        self.field_name = field_name
        self.fields = fields
        super().__init__(*args)

    def __str__(self):
        return f"This field - {self.field_name} not declared in {self.fields}"


class InvalidArgument(BaseMongodanticException):
    pass


class ValidationError(BaseMongodanticException):
    pass


class MongoIndexError(BaseMongodanticException):
    pass


class MongoConnectionError(BaseMongodanticException):
    pass


class DuplicateQueryParamError(BaseMongodanticException):
    pass


class InvalidArgsParams(BaseMongodanticException):
    def __str__(self):
        return 'Arguments must be Query objects'
