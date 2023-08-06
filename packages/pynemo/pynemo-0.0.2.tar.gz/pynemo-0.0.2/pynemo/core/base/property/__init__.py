from .boolean import BooleanProperty
from .floating import FloatProperty
from .integer import IntegerProperty
from .string import StringProperty


python_type_mapper = {
    bool: BooleanProperty,
    float: FloatProperty,
    int: IntegerProperty,
    str: StringProperty,
}
