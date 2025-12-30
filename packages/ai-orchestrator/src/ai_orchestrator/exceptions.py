class ChatTurnPlanError(Exception):
    """Exception raised when ChatTurnPlan.build() encounters an error during parsing or validation."""

    def __init__(self, code: str, message: str):
        """
        Initialize ChatTurnPlanError.

        Args:
            code: Error code (e.g., "GRAPH_PROFILE_NOT_FOUND").
            message: Error message describing what went wrong.
        """
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")
