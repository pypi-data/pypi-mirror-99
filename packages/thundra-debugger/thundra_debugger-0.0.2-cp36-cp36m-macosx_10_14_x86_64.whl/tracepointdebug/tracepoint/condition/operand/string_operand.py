from tracepointdebug.tracepoint.condition.operand.typed_operand import TypedOperand


class StringOperand(TypedOperand):

    def __init__(self, value_provider):
        super().__init__(str, value_provider)

    def is_eq(self, value, condition_context):
        cur_val = self.get_value(condition_context)
        return cur_val == value

    def is_ne(self, value, condition_context):
        cur_val = self.get_value(condition_context)
        return cur_val != value
