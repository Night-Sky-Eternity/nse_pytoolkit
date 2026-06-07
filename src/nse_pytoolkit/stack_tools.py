# nse_pytoolkit/stack_tools.py

class StackFrame[T]:
    """
    the stack frame is a node of a linked list that represents any chain of dependence to a parent.
    it is used to implement the context stack and the reentry counter.
    but also can be used to implement any other stack-like data structure that needs to keep track of the parent-child relationship.
    additionally is also allows branching like when a thread is forked and the child thread needs to keep track of the parent thread's context before the fork.
    """
    value: T
    parent: StackFrame[T] | None

    __slots__ = ("parent", "value")

    def __init__(self, value: T, parent: StackFrame[T] | None = None) -> None:
        self.value = value
        self.parent = parent

    @property
    def root(self) -> StackFrame[T]:
        frame = self
        while frame.parent is not None:
            frame = frame.parent
        return frame

    def pop(self) -> StackFrame[T] | None:
        return self.parent

    def push(self, value: T) -> StackFrame[T]:
        return StackFrame(value, self)
