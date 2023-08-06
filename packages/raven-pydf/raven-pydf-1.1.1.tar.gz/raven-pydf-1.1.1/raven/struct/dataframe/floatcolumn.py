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
Provides an implementation for FloatColumn and NullableFloatColumn
"""

from struct import pack

import numpy as np

import raven.struct.dataframe.core as dataframe
import raven.struct.dataframe.column as column
import raven.struct.dataframe._columnutils as utils

class FloatColumn(column.Column):
    """A Column holding float values (float32).
    This implementation DOES NOT support null values.
    """

    TYPE_CODE = 6

    def __init__(self, name=None, values=None):
        """Constructs a new FloatColumn.

        The constructed Column will have the specified name or is unlabeled
        if the specified name is None or empty.
        The constructed Column has the content of the specified list
        or numpy array. If the argument specifying the Column values is
        an int, then the constructed Column is initialized with the given
        length and all Column entries are set to default values.

        Args:
            name: The name of the FloatColumn as a string
            values: The content of the FloatColumn.
                Must be a list or numpy array with dtype float32, or an int
        """
        if values is None:
            values = np.empty(0, dtype=np.float32)

        if isinstance(values, list):
            for value in values:
                self._check_type(value)

            values = np.array(values, dtype=np.float32)

        elif isinstance(values, np.ndarray):
            if values.dtype != "float32":
                raise dataframe.DataFrameException(
                    ("Invalid argument array. Expected "
                     "float array (float32) but found {}".format(values.dtype)))

        elif isinstance(values, int):
            values = np.zeros(values, dtype=np.float32)
        else:
            raise dataframe.DataFrameException(
                ("Invalid argument array. Expected "
                 "list or numpy array but found {}".format(type(values))))

        super().__init__(name, values)

    def _check_type(self, value):
        if value is None:
            raise dataframe.DataFrameException(
                ("Invalid argument. "
                 "FloatColumn cannot use None values"))

        if not isinstance(value, float) and not isinstance(value, np.float32):
            raise dataframe.DataFrameException(
                ("Invalid argument. Expected "
                 "float (float32) but found {}".format(type(value))))

    def get_value(self, index):
        """Gets the float value at the specified index

        Args:
            index: The index of the value to get

        Returns:
            The float value at the specified index. Is never None

        Raises:
            ValueError: If the specified index is out of bounds
        """
        self._check_bounds(index)
        return float(self._values[index])

    def type_code(self):
        return FloatColumn.TYPE_CODE

    def type_name(self):
        return "float"

    def is_nullable(self):
        return False

    def is_numeric(self):
        return True

    def get_default_value(self):
        return 0.0

    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    # pylint: disable=invalid-name
    def convert_to(self, typecode):
        converted = None
        if typecode == utils.type_code_byte_column():
            converted = dataframe.DataFrame.ByteColumn(values=self._values.astype(np.int8))
        elif typecode == utils.type_code_short_column():
            converted = dataframe.DataFrame.ShortColumn(values=self._values.astype(np.int16))
        elif typecode == utils.type_code_int_column():
            converted = dataframe.DataFrame.IntColumn(values=self._values.astype(np.int32))
        elif typecode == utils.type_code_long_column():
            converted = dataframe.DataFrame.LongColumn(values=self._values.astype(np.int64))
        elif typecode == utils.type_code_string_column():
            vals = self._values.astype(np.object)
            for i, x in np.ndenumerate(vals):
                vals[i] = str(x)

            converted = dataframe.DataFrame.StringColumn(values=vals)
        elif typecode == FloatColumn.TYPE_CODE:
            converted = self.clone()
        elif typecode == utils.type_code_double_column():
            converted = dataframe.DataFrame.DoubleColumn(values=self._values.astype(np.float64))
        elif typecode == utils.type_code_char_column():
            vals = self._values.astype(np.uint8)
            for i, x in np.ndenumerate(vals):
                vals[i] = ord(str(x)[0])

            converted = dataframe.DataFrame.CharColumn(values=vals)
        elif typecode == utils.type_code_boolean_column():
            converted = dataframe.DataFrame.BooleanColumn(values=self._values.astype(np.bool))
        elif typecode == utils.type_code_binary_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                vals[i] = bytearray(pack(">f", x))

            converted = dataframe.DataFrame.BinaryColumn(values=vals)
        elif typecode == utils.type_code_nullable_byte_column():
            vals = self._values.astype(np.int8)
            converted = dataframe.DataFrame.NullableByteColumn(values=vals.astype(np.object))
        elif typecode == utils.type_code_nullable_short_column():
            vals = self._values.astype(np.int16)
            converted = dataframe.DataFrame.NullableShortColumn(values=vals.astype(np.object))
        elif typecode == utils.type_code_nullable_int_column():
            vals = self._values.astype(np.int32)
            converted = dataframe.DataFrame.NullableIntColumn(values=vals.astype(np.object))
        elif typecode == utils.type_code_nullable_long_column():
            vals = self._values.astype(np.int64)
            converted = dataframe.DataFrame.NullableLongColumn(values=vals.astype(np.object))
        elif typecode == utils.type_code_nullable_string_column():
            vals = self._values.astype(np.object)
            for i, x in np.ndenumerate(vals):
                vals[i] = str(x)

            converted = dataframe.DataFrame.NullableStringColumn(values=vals)
        elif typecode == NullableFloatColumn.TYPE_CODE:
            vals = self._values.astype(np.object)
            converted = NullableFloatColumn(values=vals)
        elif typecode == utils.type_code_nullable_double_column():
            vals = self._values.astype(np.float64)
            vals = vals.astype(np.object)
            converted = dataframe.DataFrame.NullableDoubleColumn(values=vals)
        elif typecode == utils.type_code_nullable_char_column():
            vals = self._values.astype(np.object)
            for i, x in np.ndenumerate(vals):
                vals[i] = ord(str(x)[0])

            converted = dataframe.DataFrame.NullableCharColumn(values=vals)
        elif typecode == utils.type_code_nullable_boolean_column():
            vals = self._values.astype(np.bool)
            vals = vals.astype(np.object)
            converted = dataframe.DataFrame.NullableBooleanColumn(values=vals)
        elif typecode == utils.type_code_nullable_binary_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                vals[i] = bytearray(pack(">f", x))

            converted = dataframe.DataFrame.NullableBinaryColumn(values=vals)
        else:
            raise dataframe.DataFrameException(
                "Unknown column type code: {}".format(typecode))

        # pylint: disable=protected-access
        converted._name = self._name
        return converted

    def _create_array(self, size=0):
        return np.zeros(size, dtype=np.float32)

class NullableFloatColumn(column.Column):
    """A Column holding nullable float values.
    Any values not explicitly set are considered None.
    """

    TYPE_CODE = 15

    def __init__(self, name=None, values=None):
        """Constructs a new NullableFloatColumn.

        The constructed Column will have the specified name or is unlabeled
        if the specified name is None or empty.
        The constructed Column has the content of the specified list
        or numpy array. If the argument specifying the Column values is
        an int, then the constructed Column is initialized with the given
        length and all Column entries are set to default values.

        Args:
            name: The name of the NullableFloatColumn as a string
            values: The content of the NullableFloatColumn.
                Must be a list or numpy array with dtype object, or an int
        """
        if values is None:
            values = np.empty(0, dtype=np.object)

        if isinstance(values, list):
            for value in values:
                self._check_type(value)

            values = np.array(values, dtype=np.object)

        elif isinstance(values, np.ndarray):
            if values.dtype != "object":
                raise dataframe.DataFrameException(
                    ("Invalid argument array. Expected "
                     "float array (object) but found {}".format(values.dtype)))

            for value in values:
                self._check_type(value)

        elif isinstance(values, int):
            values = np.empty(values, dtype=np.object)
        else:
            raise dataframe.DataFrameException(
                ("Invalid argument array. Expected "
                 "list or numpy array but found {}".format(type(values))))

        super().__init__(name, values)

    def _check_type(self, value):
        if value is not None:
            if not isinstance(value, float) and not isinstance(value, np.float32):
                raise dataframe.DataFrameException(
                    ("Invalid argument. Expected "
                     "float (float32) but found {}".format(type(value))))

    def get_value(self, index):
        """Gets the float value at the specified index

        Args:
            index: The index of the value to get

        Returns:
            The float value at the specified index. May be None

        Raises:
            ValueError: If the specified index is out of bounds
        """
        self._check_bounds(index)
        val = self._values[index]
        if val is None:
            return None
        else:
            return float(val)

    def type_code(self):
        return NullableFloatColumn.TYPE_CODE

    def type_name(self):
        return "float"

    def is_nullable(self):
        return True

    def is_numeric(self):
        return True

    def get_default_value(self):
        return None

    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    # pylint: disable=invalid-name
    def convert_to(self, typecode):
        converted = None
        if typecode == utils.type_code_byte_column():
            vals = np.empty([self._values.shape[0]], dtype=np.int8)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = int(np.int8(x))
                else:
                    vals[i] = 0

            converted = dataframe.DataFrame.ByteColumn(values=vals)
        elif typecode == utils.type_code_short_column():
            vals = np.empty([self._values.shape[0]], dtype=np.int16)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = int(np.int16(x))
                else:
                    vals[i] = 0

            converted = dataframe.DataFrame.ShortColumn(values=vals)
        elif typecode == utils.type_code_int_column():
            vals = np.empty([self._values.shape[0]], dtype=np.int32)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = int(np.int32(x))
                else:
                    vals[i] = 0

            converted = dataframe.DataFrame.IntColumn(values=vals)
        elif typecode == utils.type_code_long_column():
            vals = np.empty([self._values.shape[0]], dtype=np.int64)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = int(np.int64(x))
                else:
                    vals[i] = 0

            converted = dataframe.DataFrame.LongColumn(values=vals)
        elif typecode == utils.type_code_string_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = str(x)
                else:
                    vals[i] = utils.default_value_string_column()

            converted = dataframe.DataFrame.StringColumn(values=vals)
        elif typecode == FloatColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.float32)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = float(np.float32(x))
                else:
                    vals[i] = 0.0

            converted = FloatColumn(values=vals)
        elif typecode == utils.type_code_double_column():
            vals = np.empty([self._values.shape[0]], dtype=np.float64)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = float(np.float64(x))
                else:
                    vals[i] = 0.0

            converted = dataframe.DataFrame.DoubleColumn(values=vals)
        elif typecode == utils.type_code_char_column():
            vals = np.zeros([self._values.shape[0]], dtype=np.uint8)
            ord_default = ord(utils.default_value_char_column())
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = ord(str(x)[0])
                else:
                    vals[i] = ord_default

            converted = dataframe.DataFrame.CharColumn(values=vals)
        elif typecode == utils.type_code_boolean_column():
            vals = np.empty([self._values.shape[0]], dtype=np.bool)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = (x != 0.0)
                else:
                    vals[i] = False

            converted = dataframe.DataFrame.BooleanColumn(values=vals)
        elif typecode == utils.type_code_binary_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = bytearray(pack(">f", x))
                else:
                    vals[i] = bytearray(pack(">f", 0.0))

            converted = dataframe.DataFrame.BinaryColumn(values=vals)
        elif typecode == utils.type_code_nullable_byte_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                vals[i] = int(np.int8(x)) if x is not None else None

            converted = dataframe.DataFrame.NullableByteColumn(values=vals)
        elif typecode == utils.type_code_nullable_short_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                vals[i] = int(np.int16(x)) if x is not None else None

            converted = dataframe.DataFrame.NullableShortColumn(values=vals)
        elif typecode == utils.type_code_nullable_int_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                vals[i] = int(np.int32(x)) if x is not None else None

            converted = dataframe.DataFrame.NullableIntColumn(values=vals)
        elif typecode == utils.type_code_nullable_long_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                vals[i] = int(np.int64(x)) if x is not None else None

            converted = dataframe.DataFrame.NullableLongColumn(values=vals)
        elif typecode == utils.type_code_nullable_string_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = str(x)
                else:
                    vals[i] = None

            converted = dataframe.DataFrame.NullableStringColumn(values=vals)
        elif typecode == NullableFloatColumn.TYPE_CODE:
            converted = self.clone()
        elif typecode == utils.type_code_nullable_double_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = float(np.float64(x))
                else:
                    vals[i] = None

            converted = dataframe.DataFrame.NullableDoubleColumn(values=vals)
        elif typecode == utils.type_code_nullable_char_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = ord(str(x)[0])
                else:
                    vals[i] = None

            converted = dataframe.DataFrame.NullableCharColumn(values=vals)
        elif typecode == utils.type_code_nullable_boolean_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = (x != 0.0)
                else:
                    vals[i] = None

            converted = dataframe.DataFrame.NullableBooleanColumn(values=vals)
        elif typecode == utils.type_code_nullable_binary_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = bytearray(pack(">f", x))
                else:
                    vals[i] = None

            converted = dataframe.DataFrame.NullableBinaryColumn(values=vals)
        else:
            raise dataframe.DataFrameException(
                "Unknown column type code: {}".format(typecode))

        # pylint: disable=protected-access
        converted._name = self._name
        return converted

    def _create_array(self, size=0):
        return np.empty(size, dtype=np.object)
