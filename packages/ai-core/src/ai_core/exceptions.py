class GraphProfileError(Exception):
    """Base exception for graph profile errors."""

    pass


class GraphProfileNotFoundError(GraphProfileError):
    """Raised when a graph profile is not found."""

    pass


class ModelProfileError(Exception):
    """Base exception for model profile errors."""

    pass


class ModelProfileNotFoundError(ModelProfileError):
    """Raised when a model profile is not found."""

    pass
