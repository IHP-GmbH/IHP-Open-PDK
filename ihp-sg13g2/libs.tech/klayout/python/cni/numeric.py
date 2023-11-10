
import re

class Numeric(float):
    _scaleFactors = "yzafpnumc%kKMGTPEZY"

    def __new__(cls, value):
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

        if type(value) is float or type(value) is int or type(value is Numeric):
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
        if scaleFactor is not None:
            if type(scaleFactor) is str:
                calcValue, numberPart, scaleFactor = Numeric._calcValue(self._numberPart + scaleFactor)
                return calcValue
        else:
            return self

    @property
    def scaleFactor(self):
        return self._scaleFactor

    @property
    def scale_factors(self):
        return [*Numeric._scaleFactors]

