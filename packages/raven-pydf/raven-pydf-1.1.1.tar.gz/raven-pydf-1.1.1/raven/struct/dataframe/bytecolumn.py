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
Provides an implementation for ByteColumn and NullableByteColumn
"""

import numpy as np

import raven.struct.dataframe.core as dataframe
import raven.struct.dataframe.column as column
import raven.struct.dataframe._columnutils as utils

class ByteColumn(column.Column):
    """A Column holding byte values (int8).
    This implementation DOES NOT support null values.
    """

    TYPE_CODE = 1

    def __init__(self, name=None, values=None):
        """Constructs a new ByteColumn.

        The constructed Column will have the specified name or is unlabeled
        if the specified name is None or empty.
        The constructed Column has the content of the specified list
        or numpy array. If the argument specifying the Column values is
        an int, then the constructed Column is initialized with the given
        length and all Column entries are set to default values.

        Args:
            name: The name of the ByteColumn as a string
            values: The content of the ByteColumn.
                Must be a list or numpy array with dtype int8, or an int
        """
        if values is None:
            values = np.empty(0, dtype=np.int8)

        if isinstance(values, list):
            for value in values:
                self._check_type(value)

            values = np.array(values, dtype=np.int8)

        elif isinstance(values, np.ndarray):
            if values.dtype != "int8":
                raise dataframe.DataFrameException(
                    ("Invalid argument array. Expected "
                     "byte array (int8) but found {}".format(values.dtype)))

        elif isinstance(values, int):
            values = np.zeros(values, dtype=np.int8)
        else:
            raise dataframe.DataFrameException(
                ("Invalid argument array. Expected "
                 "list or numpy array but found {}".format(type(values))))

        super().__init__(name, values)

    def _check_type(self, value):
        if value is None:
            raise dataframe.DataFrameException(
                ("Invalid argument. "
                 "ByteColumn cannot use None values"))

        if isinstance(value, int):
            if (value < -128) or (value > 127):
                raise dataframe.DataFrameException(
                    "Out of range byte (int8): {}".format(value))

        elif not isinstance(value, np.int8):
            raise dataframe.DataFrameException(
                ("Invalid argument. Expected "
                 "byte (int8) but found {}".format(type(value))))

    def get_value(self, index):
        """Gets the byte value at the specified index

        Args:
            index: The index of the value to get

        Returns:
            The byte value at the specified index. Is never None

        Raises:
            ValueError: If the specified index is out of bounds
        """
        self._check_bounds(index)
        return int(self._values[index])

    def type_code(self):
        return ByteColumn.TYPE_CODE

    def type_name(self):
        return "byte"

    def is_nullable(self):
        return False

    def is_numeric(self):
        return True

    def get_default_value(self):
        return 0

    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    # pylint: disable=invalid-name
    def convert_to(self, typecode):
        converted = None
        if typecode == ByteColumn.TYPE_CODE:
            converted = self.clone()
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
        elif typecode == utils.type_code_float_column():
            converted = dataframe.DataFrame.FloatColumn(values=self._values.astype(np.float32))
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
                vals[i] = bytearray(int(x).to_bytes(1, byteorder="big", signed=True))

            converted = dataframe.DataFrame.BinaryColumn(values=vals)
        elif typecode == NullableByteColumn.TYPE_CODE:
            converted = NullableByteColumn(values=self._values.astype(np.object))
        elif typecode == utils.type_code_nullable_short_column():
            converted = dataframe.DataFrame.NullableShortColumn(
                values=self._values.astype(np.object))

        elif typecode == utils.type_code_nullable_int_column():
            converted = dataframe.DataFrame.NullableIntColumn(values=self._values.astype(np.object))
        elif typecode == utils.type_code_nullable_long_column():
            converted = dataframe.DataFrame.NullableLongColumn(
                values=self._values.astype(np.object))

        elif typecode == utils.type_code_nullable_string_column():
            vals = self._values.astype(np.object)
            for i, x in np.ndenumerate(vals):
                vals[i] = str(x)

            converted = dataframe.DataFrame.NullableStringColumn(values=vals)
        elif typecode == utils.type_code_nullable_float_column():
            vals = self._values.astype(np.float32)
            vals = vals.astype(np.object)
            converted = dataframe.DataFrame.NullableFloatColumn(values=vals)
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
                vals[i] = bytearray(int(x).to_bytes(1, byteorder="big", signed=True))

            converted = dataframe.DataFrame.NullableBinaryColumn(values=vals)
        else:
            raise dataframe.DataFrameException(
                "Unknown column type code: {}".format(typecode))

        # pylint: disable=protected-access
        converted._name = self._name
        return converted

    def _create_array(self, size=0):
        return np.zeros(size, dtype=np.int8)

class NullableByteColumn(column.Column):
    """A Column holding nullable byte values.
    Any values not explicitly set are considered None.
    """

    TYPE_CODE = 10

    def __init__(self, name=None, values=None):
        """Constructs a new NullableByteColumn.

        The constructed Column will have the specified name or is unlabeled
        if the specified name is None or empty.
        The constructed Column has the content of the specified list
        or numpy array. If the argument specifying the Column values is
        an int, then the constructed Column is initialized with the given
        length and all Column entries are set to default values.

        Args:
            name: The name of the NullableByteColumn as a string
            values: The content of the NullableByteColumn.
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
                     "byte array (object) but found {}".format(values.dtype)))

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
        if isinstance(value, int):
            if (value < -128) or (value > 127):
                raise dataframe.DataFrameException(
                    "Out of range byte (int8): {}".format(value))

        elif value is not None and not isinstance(value, np.int8):
            raise dataframe.DataFrameException(
                ("Invalid argument. Expected "
                 "byte (int8) but found {}".format(type(value))))

    def get_value(self, index):
        """Gets the byte value at the specified index

        Args:
            index: The index of the value to get

        Returns:
            The byte value at the specified index. May be None

        Raises:
            ValueError: If the specified index is out of bounds
        """
        self._check_bounds(index)
        val = self._values[index]
        if val is None:
            return None
        else:
            return int(val)

    def type_code(self):
        return NullableByteColumn.TYPE_CODE

    def type_name(self):
        return "byte"

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
        if typecode == ByteColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.int8)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = int(x)
                else:
                    vals[i] = 0

            converted = ByteColumn(values=vals)
        elif typecode == utils.type_code_short_column():
            vals = np.empty([self._values.shape[0]], dtype=np.int16)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = int(x)
                else:
                    vals[i] = 0

            converted = dataframe.DataFrame.ShortColumn(values=vals)
        elif typecode == utils.type_code_int_column():
            vals = np.empty([self._values.shape[0]], dtype=np.int32)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = int(x)
                else:
                    vals[i] = 0

            converted = dataframe.DataFrame.IntColumn(values=vals)
        elif typecode == utils.type_code_long_column():
            vals = np.empty([self._values.shape[0]], dtype=np.int64)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = int(x)
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
        elif typecode == utils.type_code_float_column():
            vals = np.empty([self._values.shape[0]], dtype=np.float32)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = float(x)
                else:
                    vals[i] = 0.0

            converted = dataframe.DataFrame.FloatColumn(values=vals)
        elif typecode == utils.type_code_double_column():
            vals = np.empty([self._values.shape[0]], dtype=np.float64)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = float(x)
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
                    vals[i] = (x != 0)
                else:
                    vals[i] = False

            converted = dataframe.DataFrame.BooleanColumn(values=vals)
        elif typecode == utils.type_code_binary_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = bytearray(int(x).to_bytes(1, byteorder="big", signed=True))
                else:
                    vals[i] = bytearray(int(0).to_bytes(1, byteorder="big", signed=True))

            converted = dataframe.DataFrame.BinaryColumn(values=vals)
        elif typecode == NullableByteColumn.TYPE_CODE:
            converted = self.clone()
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
        elif typecode == utils.type_code_nullable_float_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = float(x)
                else:
                    vals[i] = None

            converted = dataframe.DataFrame.NullableFloatColumn(values=vals)
        elif typecode == utils.type_code_nullable_double_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = float(x)
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
                    vals[i] = (x != 0)
                else:
                    vals[i] = None

            converted = dataframe.DataFrame.NullableBooleanColumn(values=vals)
        elif typecode == utils.type_code_nullable_binary_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = bytearray(int(x).to_bytes(1, byteorder="big", signed=True))
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
