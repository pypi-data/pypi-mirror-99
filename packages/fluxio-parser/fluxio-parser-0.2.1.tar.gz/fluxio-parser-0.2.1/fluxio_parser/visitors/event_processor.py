"""Contains the EventProcessorVisitor class"""

import ast
from typing import Any


class EventProcessorVisitor(ast.NodeVisitor):
    """AST node visitor that parses an EventProcessor class in a .sfn file.

    The goal is to splice the class into a package's entry point module.

    Example EventProcessor class::

        class MyEventProcessor(EventProcessor):
            pass

    """

    def __init__(self, node: Any) -> None:
        """Initializer

        Args:
            node: AST node of the event processor class. Stored here for downstream
                processing.

        """
        super().__init__()
        self.node = node
