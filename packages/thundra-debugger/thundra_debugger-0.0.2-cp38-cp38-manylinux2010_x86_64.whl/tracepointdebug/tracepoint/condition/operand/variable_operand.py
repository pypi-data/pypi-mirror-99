from tracepointdebug.tracepoint.condition.operand.boolean_operand import BooleanOperand
from tracepointdebug.tracepoint.condition.operand.null_operand import NullOperand
from tracepointdebug.tracepoint.condition.operand.number_operand import NumberOperand
from tracepointdebug.tracepoint.condition.operand.object_operand import ObjectOperand
from tracepointdebug.tracepoint.condition.operand.operand import Operand
from tracepointdebug.tracepoint.condition.operand.string_operand import StringOperand
from tracepointdebug.tracepoint.condition.variable_value_provider import VariableValueProvider


class VariableOperand(Operand):

    def __init__(self, var_name):
        self.value_provider = VariableValueProvider(var_name)

    def create_variable_operand(self, var_value):
        if isinstance(var_value, bool):
            return BooleanOperand(self.value_provider)

        if isinstance(var_value, (int, float)):
            return NumberOperand(self.value_provider)

        if isinstance(var_value, str):
            return StringOperand(self.value_provider)

        if isinstance(var_value, object):
            return ObjectOperand(self.value_provider)

        return None

    def get_variable_operand(self, condition_context):
        value = self.value_provider.get_value(condition_context)
        if value is None:
            return NullOperand()
        return self.create_variable_operand(value)

    def get_value(self, condition_context):
        self.value_provider.get_value(condition_context)

    def eq(self, operand, condition_context):
        cur_operand = self.get_variable_operand(condition_context)
        if cur_operand is None:
            return False
        return cur_operand.eq(operand, condition_context)

    def ne(self, operand, condition_context):
        cur_operand = self.get_variable_operand(condition_context)
        if cur_operand is None:
            return False
        return cur_operand.ne(operand, condition_context)

    def lt(self, operand, condition_context):
        cur_operand = self.get_variable_operand(condition_context)
        if cur_operand is None:
            return False
        return cur_operand.lt(operand, condition_context)

    def le(self, operand, condition_context):
        cur_operand = self.get_variable_operand(condition_context)
        if cur_operand is None:
            return False
        return cur_operand.le(operand, condition_context)

    def gt(self, operand, condition_context):
        cur_operand = self.get_variable_operand(condition_context)
        if cur_operand is None:
            return False
        return cur_operand.gt(operand, condition_context)

    def ge(self, operand, condition_context):
        cur_operand = self.get_variable_operand(condition_context)
        if cur_operand is None:
            return False
        return cur_operand.ge(operand, condition_context)
