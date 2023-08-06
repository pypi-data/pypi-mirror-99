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
Provides an implementation for BinaryColumn and NullableBinaryColumn
"""

from struct import unpack

import numpy as np

import raven.struct.dataframe.core as dataframe
import raven.struct.dataframe.column as column
import raven.struct.dataframe._columnutils as utils

class BinaryColumn(column.Column):
    """A Column holding binary values (bytearray).
    This implementation DOES NOT support null values.
    """

    TYPE_CODE = 19

    def __init__(self, name=None, values=None):
        """Constructs a new BinaryColumn.

        The constructed Column will have the specified name or is unlabeled
        if the specified name is None or empty.
        The constructed Column has the content of the specified list
        or numpy array. If the argument specifying the Column values is
        an int, then the constructed Column is initialized with the given
        length and all Column entries are set to default values.

        Args:
            name: The name of the BinaryColumn as a string
            values: The content of the BinaryColumn.
                Must be a list or numpy array with dtype object, or an int
        """
        if values is None:
            values = self._create_array()

        if isinstance(values, list):
            for value in values:
                if value is None:
                    raise dataframe.DataFrameException("BinaryColumn cannot use None values")
                if not isinstance(value, bytearray):
                    raise dataframe.DataFrameException("List must only contain bytearrays")

            # create and set values manually because numpy changes bytearray
            # objects to ndarray types when all bytearrays have equal length
            tmp = np.empty(len(values), dtype="object")
            for i, value in enumerate(values):
                tmp[i] = value

            values = tmp

        elif isinstance(values, np.ndarray):
            if values.dtype != "object":
                raise dataframe.DataFrameException(
                    ("Invalid argument array. Expected "
                     "bytearray array (object) but found {}".format(values.dtype)))

            for value in values:
                self._check_type(value)

        elif isinstance(values, int):
            values = self._create_array(size=values)
        else:
            raise dataframe.DataFrameException(
                ("Invalid argument array. Expected "
                 "list or numpy array but found {}".format(type(values))))

        super().__init__(name, values)

    def _check_type(self, value):
        if value is None:
            raise dataframe.DataFrameException(
                ("Invalid argument. "
                 "BinaryColumn cannot use None values"))

        if not isinstance(value, bytearray):
            raise dataframe.DataFrameException(
                ("Invalid argument. Expected "
                 "bytearray but found {}".format(type(value))))

    def capacity(self):
        return self._values.shape[0] if self._values is not None else 0

    def type_code(self):
        return BinaryColumn.TYPE_CODE

    def type_name(self):
        return "binary"

    def is_nullable(self):
        return False

    def is_numeric(self):
        return False

    def get_default_value(self):
        return bytearray.fromhex("00")

    def clone(self):
        """Creates and returns a copy of this BinaryColumn

        Returns:
            A copy of this BinaryColumn
        """
        val = self._create_array(self.capacity())
        for i in range(self.capacity()):
            val[i] = self._values[i][:]

        copy = BinaryColumn(values=val)
        copy._name = self._name
        return copy

    def __hash__(self):
        return hash(
            (self._name,
             (x.hex() if x is not None else None for x in self._values.tolist())
            ))

    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    # pylint: disable=invalid-name
    def convert_to(self, typecode):
        converted = None
        if typecode == utils.type_code_byte_column():
            vals = np.empty([self._values.shape[0]], dtype=np.int8)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) > 0:
                    vals[i] = x[0]
                else:
                    vals[i] = 0

            converted = dataframe.DataFrame.ByteColumn(values=vals)
        elif typecode == utils.type_code_short_column():
            vals = np.empty([self._values.shape[0]], dtype=np.int16)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) >= 2:
                    vals[i] = int.from_bytes(x[0:2], byteorder="big", signed=True)
                else:
                    vals[i] = 0

            converted = dataframe.DataFrame.ShortColumn(values=vals)
        elif typecode == utils.type_code_int_column():
            vals = np.empty([self._values.shape[0]], dtype=np.int32)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) >= 4:
                    vals[i] = int.from_bytes(x[0:4], byteorder="big", signed=True)
                else:
                    vals[i] = 0

            converted = dataframe.DataFrame.IntColumn(values=vals)
        elif typecode == utils.type_code_long_column():
            vals = np.empty([self._values.shape[0]], dtype=np.int64)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) >= 8:
                    vals[i] = int.from_bytes(x[0:8], byteorder="big", signed=True)
                else:
                    vals[i] = 0

            converted = dataframe.DataFrame.LongColumn(values=vals)
        elif typecode == utils.type_code_string_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = x.hex()
                else:
                    vals[i] = utils.default_value_string_column()

            converted = dataframe.DataFrame.StringColumn(values=vals)
        elif typecode == utils.type_code_float_column():
            vals = np.empty([self._values.shape[0]], dtype=np.float32)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) >= 4:
                    vals[i] = unpack(">f", x[0:4])[0]
                else:
                    vals[i] = 0.0

            converted = dataframe.DataFrame.FloatColumn(values=vals)
        elif typecode == utils.type_code_double_column():
            vals = np.empty([self._values.shape[0]], dtype=np.float64)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) >= 8:
                    vals[i] = unpack(">d", x[0:8])[0]
                else:
                    vals[i] = 0.0

            converted = dataframe.DataFrame.DoubleColumn(values=vals)
        elif typecode == utils.type_code_char_column():
            vals = np.empty([self._values.shape[0]], dtype=np.uint8)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) > 0:
                    vals[i] = int(x[0])
                else:
                    vals[i] = 0

            converted = dataframe.DataFrame.CharColumn(values=vals)
        elif typecode == utils.type_code_boolean_column():
            vals = np.empty([self._values.shape[0]], dtype=np.bool)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    is_zero = True
                    for y in x:
                        if y != 0:
                            is_zero = False
                            break

                    vals[i] = not is_zero
                else:
                    vals[i] = False

            converted = dataframe.DataFrame.BooleanColumn(values=vals)
        elif typecode == BinaryColumn.TYPE_CODE:
            converted = self.clone()
        elif typecode == utils.type_code_nullable_byte_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) > 0:
                    vals[i] = x[0]
                else:
                    vals[i] = None

            converted = dataframe.DataFrame.NullableByteColumn(values=vals)
        elif typecode == utils.type_code_nullable_short_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) >= 2:
                    vals[i] = int.from_bytes(x[0:2], byteorder="big", signed=True)
                else:
                    vals[i] = None

            converted = dataframe.DataFrame.NullableShortColumn(values=vals)
        elif typecode == utils.type_code_nullable_int_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) >= 4:
                    vals[i] = int.from_bytes(x[0:4], byteorder="big", signed=True)
                else:
                    vals[i] = None

            converted = dataframe.DataFrame.NullableIntColumn(values=vals)
        elif typecode == utils.type_code_nullable_long_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) >= 8:
                    vals[i] = int.from_bytes(x[0:8], byteorder="big", signed=True)
                else:
                    vals[i] = None

            converted = dataframe.DataFrame.NullableLongColumn(values=vals)
        elif typecode == utils.type_code_nullable_string_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = x.hex()
                else:
                    vals[i] = None

            converted = dataframe.DataFrame.NullableStringColumn(values=vals)
        elif typecode == utils.type_code_nullable_float_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) >= 4:
                    vals[i] = unpack(">f", x[0:4])[0]
                else:
                    vals[i] = None

            converted = dataframe.DataFrame.NullableFloatColumn(values=vals)
        elif typecode == utils.type_code_nullable_double_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) >= 8:
                    vals[i] = unpack(">d", x[0:8])[0]
                else:
                    vals[i] = None

            converted = dataframe.DataFrame.NullableDoubleColumn(values=vals)
        elif typecode == utils.type_code_nullable_char_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) > 0:
                    vals[i] = int(x[0])
                else:
                    vals[i] = None

            converted = dataframe.DataFrame.NullableCharColumn(values=vals)
        elif typecode == utils.type_code_nullable_boolean_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    is_zero = True
                    for y in x:
                        if y != 0:
                            is_zero = False
                            break

                    vals[i] = not is_zero
                else:
                    vals[i] = None

            converted = dataframe.DataFrame.NullableBooleanColumn(values=vals)
        elif typecode == NullableBinaryColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) > 0:
                    b = bytearray(len(x))
                    b[:] = x
                    vals[i] = b
                else:
                    vals[i] = None

            converted = NullableBinaryColumn(values=vals)
        else:
            raise dataframe.DataFrameException(
                "Unknown column type code: {}".format(typecode))

        # pylint: disable=protected-access
        converted._name = self._name
        return converted

    def _create_array(self, size=0):
        array = np.empty(size, dtype=np.object)
        for i in range(size):
            array[i] = self.get_default_value()

        return array

class NullableBinaryColumn(column.Column):
    """A Column holding nullable binary values (bytearray).
    Any values not explicitly set are considered None.
    """

    TYPE_CODE = 20

    def __init__(self, name=None, values=None):
        """Constructs a new NullableBinaryColumn.

        The constructed Column will have the specified name or is unlabeled
        if the specified name is None or empty.
        The constructed Column has the content of the specified list
        or numpy array. If the argument specifying the Column values is
        an int, then the constructed Column is initialized with the given
        length and all Column entries are set to default values.

        Args:
            name: The name of the NullableBinaryColumn as a string
            values: The content of the NullableBinaryColumn.
                Must be a list or numpy array with dtype object, or an int
        """
        if values is None:
            values = self._create_array()

        if isinstance(values, list):
            for value in values:
                self._check_type(value)

            # create and set values manually because numpy changes bytearray
            # objects to ndarray types when all bytearrays have equal length
            tmp = np.empty(len(values), dtype=object)
            for i, value in enumerate(values):
                tmp[i] = value

            values = tmp

        elif isinstance(values, np.ndarray):
            if values.dtype != "object":
                raise dataframe.DataFrameException(
                    ("Invalid argument array. Expected "
                     "byte array (object) but found {}".format(values.dtype)))

            for value in values:
                self._check_type(value)

        elif isinstance(values, int):
            values = self._create_array(size=values)
        else:
            raise dataframe.DataFrameException(
                ("Invalid argument array. Expected "
                 "list or numpy array but found {}".format(type(values))))

        super().__init__(name, values)

    def _check_type(self, value):
        if value is not None:
            if not isinstance(value, bytearray):
                raise dataframe.DataFrameException(
                    ("Invalid argument. Expected "
                     "bytearray but found {}".format(type(value))))

    def capacity(self):
        return self._values.shape[0] if self._values is not None else 0

    def type_code(self):
        return NullableBinaryColumn.TYPE_CODE

    def type_name(self):
        return "binary"

    def is_nullable(self):
        return True

    def is_numeric(self):
        return False

    def get_default_value(self):
        return None

    def clone(self):
        """Creates and returns a copy of this NullableBinaryColumn

        Returns:
            A copy of this NullableBinaryColumn
        """
        val = self._create_array(self.capacity())
        for i in range(self.capacity()):
            val[i] = self._values[i][:] if self._values[i] is not None else None

        copy = NullableBinaryColumn(values=val)
        copy._name = self._name
        return copy

    def __hash__(self):
        return hash(
            (self._name,
             (x.hex() if x is not None else None for x in self._values.tolist())
            ))

    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
    # pylint: disable=invalid-name
    def convert_to(self, typecode):
        converted = None
        if typecode == utils.type_code_byte_column():
            vals = np.empty([self._values.shape[0]], dtype=np.int8)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) > 0:
                    vals[i] = x[0]
                else:
                    vals[i] = 0

            converted = dataframe.DataFrame.ByteColumn(values=vals)
        elif typecode == utils.type_code_short_column():
            vals = np.empty([self._values.shape[0]], dtype=np.int16)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) >= 2:
                    vals[i] = int.from_bytes(x[0:2], byteorder="big", signed=True)
                else:
                    vals[i] = 0

            converted = dataframe.DataFrame.ShortColumn(values=vals)
        elif typecode == utils.type_code_int_column():
            vals = np.empty([self._values.shape[0]], dtype=np.int32)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) >= 4:
                    vals[i] = int.from_bytes(x[0:4], byteorder="big", signed=True)
                else:
                    vals[i] = 0

            converted = dataframe.DataFrame.IntColumn(values=vals)
        elif typecode == utils.type_code_long_column():
            vals = np.empty([self._values.shape[0]], dtype=np.int64)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) >= 8:
                    vals[i] = int.from_bytes(x[0:8], byteorder="big", signed=True)
                else:
                    vals[i] = 0

            converted = dataframe.DataFrame.LongColumn(values=vals)
        elif typecode == utils.type_code_string_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = x.hex()
                else:
                    vals[i] = utils.default_value_string_column()

            converted = dataframe.DataFrame.StringColumn(values=vals)
        elif typecode == utils.type_code_float_column():
            vals = np.empty([self._values.shape[0]], dtype=np.float32)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) >= 4:
                    vals[i] = unpack(">f", x[0:4])[0]
                else:
                    vals[i] = 0.0

            converted = dataframe.DataFrame.FloatColumn(values=vals)
        elif typecode == utils.type_code_double_column():
            vals = np.empty([self._values.shape[0]], dtype=np.float64)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) >= 8:
                    vals[i] = unpack(">d", x[0:8])[0]
                else:
                    vals[i] = 0.0

            converted = dataframe.DataFrame.DoubleColumn(values=vals)
        elif typecode == utils.type_code_char_column():
            vals = np.empty([self._values.shape[0]], dtype=np.uint8)
            ord_default = ord(utils.default_value_char_column())
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) > 0:
                    vals[i] = int(x[0])
                else:
                    vals[i] = ord_default

            converted = dataframe.DataFrame.CharColumn(values=vals)
        elif typecode == utils.type_code_boolean_column():
            vals = np.empty([self._values.shape[0]], dtype=np.bool)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    is_zero = True
                    for y in x:
                        if y != 0:
                            is_zero = False
                            break

                    vals[i] = not is_zero
                else:
                    vals[i] = False

            converted = dataframe.DataFrame.BooleanColumn(values=vals)
        elif typecode == BinaryColumn.TYPE_CODE:
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) > 0:
                    b = bytearray(len(x))
                    b[:] = x
                    vals[i] = b
                else:
                    vals[i] = bytearray(b"\x00")

            converted = BinaryColumn(values=vals)
        elif typecode == utils.type_code_nullable_byte_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) > 0:
                    vals[i] = x[0]
                else:
                    vals[i] = None

            converted = dataframe.DataFrame.NullableByteColumn(values=vals)
        elif typecode == utils.type_code_nullable_short_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) >= 2:
                    vals[i] = int.from_bytes(x[0:2], byteorder="big", signed=True)
                else:
                    vals[i] = None

            converted = dataframe.DataFrame.NullableShortColumn(values=vals)
        elif typecode == utils.type_code_nullable_int_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) >= 4:
                    vals[i] = int.from_bytes(x[0:4], byteorder="big", signed=True)
                else:
                    vals[i] = None

            converted = dataframe.DataFrame.NullableIntColumn(values=vals)
        elif typecode == utils.type_code_nullable_long_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) >= 8:
                    vals[i] = int.from_bytes(x[0:8], byteorder="big", signed=True)
                else:
                    vals[i] = None

            converted = dataframe.DataFrame.NullableLongColumn(values=vals)
        elif typecode == utils.type_code_nullable_string_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    vals[i] = x.hex()
                else:
                    vals[i] = None

            converted = dataframe.DataFrame.NullableStringColumn(values=vals)
        elif typecode == utils.type_code_nullable_float_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) >= 4:
                    vals[i] = unpack(">f", x[0:4])[0]
                else:
                    vals[i] = None

            converted = dataframe.DataFrame.NullableFloatColumn(values=vals)
        elif typecode == utils.type_code_nullable_double_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) >= 8:
                    vals[i] = unpack(">d", x[0:8])[0]
                else:
                    vals[i] = None

            converted = dataframe.DataFrame.NullableDoubleColumn(values=vals)
        elif typecode == utils.type_code_nullable_char_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None and len(x) > 0:
                    vals[i] = int(x[0])
                else:
                    vals[i] = None

            converted = dataframe.DataFrame.NullableCharColumn(values=vals)
        elif typecode == utils.type_code_nullable_boolean_column():
            vals = np.empty([self._values.shape[0]], dtype=np.object)
            for i, x in np.ndenumerate(self._values):
                if x is not None:
                    is_zero = True
                    for y in x:
                        if y != 0:
                            is_zero = False
                            break

                    vals[i] = not is_zero
                else:
                    vals[i] = None

            converted = dataframe.DataFrame.NullableBooleanColumn(values=vals)
        elif typecode == NullableBinaryColumn.TYPE_CODE:
            converted = self.clone()
        else:
            raise dataframe.DataFrameException(
                "Unknown column type code: {}".format(typecode))

        # pylint: disable=protected-access
        converted._name = self._name
        return converted

    def _create_array(self, size=0):
        return np.empty(size, dtype=np.object)
