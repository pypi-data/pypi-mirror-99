# Copyright (C) 2021 Raven Computing
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
Provides internal utility functions for Column operations.
"""

import raven.struct.dataframe.bytecolumn as bytecolumn
import raven.struct.dataframe.shortcolumn as shortcolumn
import raven.struct.dataframe.intcolumn as intcolumn
import raven.struct.dataframe.longcolumn as longcolumn
import raven.struct.dataframe.floatcolumn as floatcolumn
import raven.struct.dataframe.doublecolumn as doublecolumn
import raven.struct.dataframe.stringcolumn as stringcolumn
import raven.struct.dataframe.charcolumn as charcolumn
import raven.struct.dataframe.booleancolumn as booleancolumn
import raven.struct.dataframe.binarycolumn as binarycolumn

# pylint: disable=R0911, R0912

def is_numeric_fp(col):
    """Indicates whether the specified Column has a type name
    of float or double.

    Args:
        col: The Column to check

    Returns:
        A bool which indicates whether the specified Column is
        a FloatColumn, NullableFloatColumn, DoubleColumn,
        NullableDoubleColumn
    """
    return col.type_code() in (floatcolumn.FloatColumn.TYPE_CODE,
                               floatcolumn.NullableFloatColumn.TYPE_CODE,
                               doublecolumn.DoubleColumn.TYPE_CODE,
                               doublecolumn.NullableDoubleColumn.TYPE_CODE)

def column_from_typename(typename):
    """Constructs and returns a Column from the specified typename.

    The returned Column instance is a default (non-nullable) Column.

    Args:
        typename: The type name of the Column to return, as a str

    Returns:
        A Column instance from the specified type name,
        or None if the argument is not a valid type name
    """
    if typename == "byte":
        return bytecolumn.ByteColumn()
    elif typename == "short":
        return shortcolumn.ShortColumn()
    elif typename in ("int", "integer"):
        return intcolumn.IntColumn()
    elif typename == "long":
        return longcolumn.LongColumn()
    elif typename in ("string", "str"):
        return stringcolumn.StringColumn()
    elif typename == "float":
        return floatcolumn.FloatColumn()
    elif typename == "double":
        return doublecolumn.DoubleColumn()
    elif typename in ("char", "character"):
        return charcolumn.CharColumn()
    elif typename in ("boolean", "bool"):
        return booleancolumn.BooleanColumn()
    elif typename == "binary":
        return binarycolumn.BinaryColumn()
    else:
        return None

def column_of_type(type_code, length):
    """Creates a new Column instance with the specified type code.

    This function can be used to construct an empty column which has the
    same type as another column but is not a copy of that column's content
    and has the specified length. The returned Column will be initialized
    with default values if the length argument is positive.

    Args:
        type_code: The unique type code of the Column to create
        length: The initial length of the Column to create. Must be an int
    Returns:
        A Column of the specified type and length or None if
        the specified type code is unknown
    """
    if not isinstance(length, int):
        raise ValueError("Invalid length argument. Must be an int")

    if type_code == bytecolumn.ByteColumn.TYPE_CODE:
        return bytecolumn.ByteColumn(values=length)
    if type_code == shortcolumn.ShortColumn.TYPE_CODE:
        return shortcolumn.ShortColumn(values=length)
    if type_code == intcolumn.IntColumn.TYPE_CODE:
        return intcolumn.IntColumn(values=length)
    if type_code == longcolumn.LongColumn.TYPE_CODE:
        return longcolumn.LongColumn(values=length)
    if type_code == stringcolumn.StringColumn.TYPE_CODE:
        return stringcolumn.StringColumn(values=length)
    if type_code == floatcolumn.FloatColumn.TYPE_CODE:
        return floatcolumn.FloatColumn(values=length)
    if type_code == doublecolumn.DoubleColumn.TYPE_CODE:
        return doublecolumn.DoubleColumn(values=length)
    if type_code == charcolumn.CharColumn.TYPE_CODE:
        return charcolumn.CharColumn(values=length)
    if type_code == booleancolumn.BooleanColumn.TYPE_CODE:
        return booleancolumn.BooleanColumn(values=length)
    if type_code == binarycolumn.BinaryColumn.TYPE_CODE:
        return binarycolumn.BinaryColumn(values=length)
    if type_code == bytecolumn.NullableByteColumn.TYPE_CODE:
        return bytecolumn.NullableByteColumn(values=length)
    if type_code == shortcolumn.NullableShortColumn.TYPE_CODE:
        return shortcolumn.NullableShortColumn(values=length)
    if type_code == intcolumn.NullableIntColumn.TYPE_CODE:
        return intcolumn.NullableIntColumn(values=length)
    if type_code == longcolumn.NullableLongColumn.TYPE_CODE:
        return longcolumn.NullableLongColumn(values=length)
    if type_code == stringcolumn.NullableStringColumn.TYPE_CODE:
        return stringcolumn.NullableStringColumn(values=length)
    if type_code == floatcolumn.NullableFloatColumn.TYPE_CODE:
        return floatcolumn.NullableFloatColumn(values=length)
    if type_code == doublecolumn.NullableDoubleColumn.TYPE_CODE:
        return doublecolumn.NullableDoubleColumn(values=length)
    if type_code == charcolumn.NullableCharColumn.TYPE_CODE:
        return charcolumn.NullableCharColumn(values=length)
    if type_code == booleancolumn.NullableBooleanColumn.TYPE_CODE:
        return booleancolumn.NullableBooleanColumn(values=length)
    if type_code == binarycolumn.NullableBinaryColumn.TYPE_CODE:
        return binarycolumn.NullableBinaryColumn(values=length)

    # Default value for unknown type code
    return None

def type_code_byte_column():
    """Returns the constant type code of all ByteColumn instances

    Returns:
        The unique type code of all ByteColumns
    """
    return bytecolumn.ByteColumn.TYPE_CODE

def type_code_short_column():
    """Returns the constant type code of all ShortColumn instances

    Returns:
        The unique type code of all ShortColumns
    """
    return shortcolumn.ShortColumn.TYPE_CODE

def type_code_int_column():
    """Returns the constant type code of all IntColumn instances

    Returns:
        The unique type code of all IntColumns
    """
    return intcolumn.IntColumn.TYPE_CODE

def type_code_long_column():
    """Returns the constant type code of all LongColumn instances

    Returns:
        The unique type code of all LongColumns
    """
    return longcolumn.LongColumn.TYPE_CODE

def type_code_float_column():
    """Returns the constant type code of all FloatColumn instances

    Returns:
        The unique type code of all FloatColumns
    """
    return floatcolumn.FloatColumn.TYPE_CODE

def type_code_double_column():
    """Returns the constant type code of all DoubleColumn instances

    Returns:
        The unique type code of all DoubleColumns
    """
    return doublecolumn.DoubleColumn.TYPE_CODE

def type_code_string_column():
    """Returns the constant type code of all StringColumn instances

    Returns:
        The unique type code of all StringColumns
    """
    return stringcolumn.StringColumn.TYPE_CODE

def type_code_char_column():
    """Returns the constant type code of all CharColumn instances

    Returns:
        The unique type code of all CharColumns
    """
    return charcolumn.CharColumn.TYPE_CODE

def type_code_boolean_column():
    """Returns the constant type code of all BooleanColumn instances

    Returns:
        The unique type code of all BooleanColumns
    """
    return booleancolumn.BooleanColumn.TYPE_CODE

def type_code_binary_column():
    """Returns the constant type code of all BinaryColumn instances

    Returns:
        The unique type code of all BinaryColumns
    """
    return binarycolumn.BinaryColumn.TYPE_CODE

def type_code_nullable_byte_column():
    """Returns the constant type code of all NullableByteColumn instances

    Returns:
        The unique type code of all NullableByteColumns
    """
    return bytecolumn.NullableByteColumn.TYPE_CODE

def type_code_nullable_short_column():
    """Returns the constant type code of all NullableShortColumn instances

    Returns:
        The unique type code of all NullableShortColumns
    """
    return shortcolumn.NullableShortColumn.TYPE_CODE

def type_code_nullable_int_column():
    """Returns the constant type code of all NullableIntColumn instances

    Returns:
        The unique type code of all NullableIntColumns
    """
    return intcolumn.NullableIntColumn.TYPE_CODE

def type_code_nullable_long_column():
    """Returns the constant type code of all NullableLongColumn instances

    Returns:
        The unique type code of all NullableLongColumns
    """
    return longcolumn.NullableLongColumn.TYPE_CODE

def type_code_nullable_float_column():
    """Returns the constant type code of all NullableFloatColumn instances

    Returns:
        The unique type code of all NullableFloatColumns
    """
    return floatcolumn.NullableFloatColumn.TYPE_CODE

def type_code_nullable_double_column():
    """Returns the constant type code of all NullableDoubleColumn instances

    Returns:
        The unique type code of all NullableDoubleColumns
    """
    return doublecolumn.NullableDoubleColumn.TYPE_CODE

def type_code_nullable_string_column():
    """Returns the constant type code of all NullableStringColumn instances

    Returns:
        The unique type code of all NullableStringColumns
    """
    return stringcolumn.NullableStringColumn.TYPE_CODE

def type_code_nullable_char_column():
    """Returns the constant type code of all NullableCharColumn instances

    Returns:
        The unique type code of all NullableCharColumns
    """
    return charcolumn.NullableCharColumn.TYPE_CODE

def type_code_nullable_boolean_column():
    """Returns the constant type code of all NullableBooleanColumn instances

    Returns:
        The unique type code of all NullableBooleanColumns
    """
    return booleancolumn.NullableBooleanColumn.TYPE_CODE

def type_code_nullable_binary_column():
    """Returns the constant type code of all NullableBinaryColumn instances

    Returns:
        The unique type code of all NullableBinaryColumns
    """
    return binarycolumn.NullableBinaryColumn.TYPE_CODE

def default_value_string_column():
    """Returns the default value for StringColumns.

    Returns:
        The default value used by all non-nullable StringColumns
    """
    return stringcolumn.StringColumn.DEFAULT_VALUE

def default_value_char_column():
    """Returns the default value for CharColumns.

    Returns:
        The default value used by all non-nullable CharColumns
    """
    return charcolumn.CharColumn.DEFAULT_VALUE
