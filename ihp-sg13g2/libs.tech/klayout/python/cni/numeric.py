########################################################################
#
# Copyright 2023 IHP PDK Authors
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#    https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
########################################################################

import re

class Numeric(float):
    """
    The Numeric class is used to create a floating point number from a string
    representation, such as “10ns”. This string representation is composed of two parts: 1) a
    number part and 2) a scale factor part. Thus, this Numeric class can be used to represent a
    floating point number as a floating point number along with a scaling factor. Since this
    Numeric class is derived from the base Python float class, it can be used just like a
    regular floating point number in any numerical computation.\n
    The number part of this Numeric class string representation can be any valid Python
    integer or floating point number; this Python floating point number can be represented
    using standard scientific notation, such as “1.23e-4”. The scaling factor part of this
    Numeric class string representation must be one of the following pre-defined scaling
    factor string values:

    +---------------+------------------+-------------+
    |  Character    |  Name            |  Multiplier |
    +===============+==================+=============+
    |  Y            |  Yotta           |  1e24       |
    +---------------+------------------+-------------+
    |  Z            |  Zetta           |  1e21       |
    +---------------+------------------+-------------+
    |  E            |  Exa             |  1e18       |
    +---------------+------------------+-------------+
    |  P            |  Peta            |  1e15       |
    +---------------+------------------+-------------+
    |  T            |  Tera            |  1e12       |
    +---------------+------------------+-------------+
    |  G            |  Giga            |  1e09       |
    +---------------+------------------+-------------+
    |  M            |  Mega            |  1e06       |
    +---------------+------------------+-------------+
    |  K or k       |  Kilo            |  1e03       |
    +---------------+------------------+-------------+
    |  ‘’           |  no scale factor |  1.0        |
    +---------------+------------------+-------------+
    |  %            |  percent         |  1e-2       |
    +---------------+------------------+-------------+
    |  c            |  centi           |  1e-2       |
    +---------------+------------------+-------------+
    |  m            |  milli           |  1e-3       |
    +---------------+------------------+-------------+
    |  u            |  micron          |  1e-6       |
    +---------------+------------------+-------------+
    |  n            |  nano            |  1e-9       |
    +---------------+------------------+-------------+
    |  p            |  pico            |  1e-12      |
    +---------------+------------------+-------------+
    |  f            |  femto           |  1e-15      |
    +---------------+------------------+-------------+
    |  a            |  atto            |  1e-18      |
    +---------------+------------------+-------------+
    |  z            |  zepto           |  1e-21      |
    +---------------+------------------+-------------+
    |  y            |  yocto           |  1e-24      |
    +---------------+------------------+-------------+

    Note that any characters after the first character in the scaling factor are simply ignored.
    Thus, the scaling factor “mVolt” is the same as “m”. This capability can be used to create
    more descriptive scaling factors.

    Numeric(int | float | string) – creates a Numeric object, based upon the specified number
    or string. The string must be a string of the form <number><scaleFactor>, where the
    <scaleFactor> is one of the pre-defined scaling factors in the above table of scaling factor
    strings. That is, this string representation must be composed of a number part and a
    scaling factor part, where the scaling factor is a pre-defined scaling factor string.

    """

    _scaleFactors = "yzafpnumc%kKMGTPEZY"

    def __new__(cls, value):
        """
        Numeric(int | float | string) – creates a Numeric object, based upon the specified number
        or string. The string must be a string of the form <number><scaleFactor>, where the
        <scaleFactor> is one of the pre-defined scaling factors in the above table of scaling factor
        strings. That is, this string representation must be composed of a number part and a
        scaling factor part, where the scaling factor is a pre-defined scaling factor string.

        """
        calcValue, numberPart, scaleFactor = cls._calcValue(value)
        instance = super().__new__(cls, calcValue)
        instance._scaleFactor = scaleFactor
        instance._numberPart = numberPart
        return instance

    @classmethod
    def _calcValue(cls, value):
        number = 0
        exp = 0
        numberPart = value
        scaleFactor = ""

        if type(value) is float or type(value) is int or type(value) is Numeric:
            return float(value), numberPart, scaleFactor

        match = re.fullmatch(r'([0-9.+\-e]+)([' + cls._scaleFactors + r'])?(\S*)?', value)

        if match:
            numberPart = match.group(1)

            if match.group(2) != None:
                scale = match.group(2)
                scaleFactor = scale;

                if scale == "c" or scale == "%":
                    exp = -2
                else:
                    if scale == "k":
                        scale = "K"

                    exp = -1

                    for i in cls._scaleFactors.replace('c', '').replace('%', ' ').replace('k', ''):
                        exp += 1
                        if i is scale:
                            break

                    exp = (exp - 8) * 3

        try:
            number = float(numberPart)
        except:
            raise ValueError

        return number * (10**exp), numberPart, scaleFactor

    def scaleFormat(self, scaleFactor = None):
        """
        Returns the floating point number formatted
        using the specified scaleFactor scaling value. If this scaleFactor parameter is not
        specified, then the floating point number is returned using the scale factor which was
        used when the Numeric class object was created.

        :param scaleFactor: Optional scaling factor to use.
        :type scaleFactor: string or None
        :return: new scaled Numeric object
        :rtype: Numeric

        """
        if scaleFactor is not None:
            if type(scaleFactor) is str:
                calcValue, numberPart, scaleFactor = Numeric._calcValue(self._numberPart + scaleFactor)
                return calcValue
        else:
            return self

    @property
    def scaleFactor(self):
        """
        The default (original) scale factor

        """
        return self._scaleFactor

    @property
    def scale_factors(self):
        """
        List of all available scaling factors, along with their values

        """
        return [*Numeric._scaleFactors]

