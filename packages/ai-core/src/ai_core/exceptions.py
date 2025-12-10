class GraphProfileError(Exception):
    """Base exception for graph profile errors."""

    pass


class GraphProfileNotFoundError(GraphProfileError):
    """Raised when a graph profile is not found."""

    pass
