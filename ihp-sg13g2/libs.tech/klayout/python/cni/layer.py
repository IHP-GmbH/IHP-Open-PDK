
class Layer(object):

    tech = None
    layout = None

    def __init__(self, name, purpose = None):
        namePurpose = name if purpose is None else name + "." + purpose
        layer, datatype = Layer.tech.stream_layers()[namePurpose]

        self._name = namePurpose
        self._number = Layer.layout.layer(layer, datatype, namePurpose)
        self._purposeName = "" if purpose is None else purpose

    def getAttrs(self):
        raise Exception("Not implemented yet!")

    def getGridResolution(self):
        raise Exception("Not implemented yet!")

    def getLayerAbove(self):
        raise Exception("Not implemented yet!")

    def getLayerAbove(self, layerMaterial):
        raise Exception("Not implemented yet!")

    def getLayerBelow(self):
        raise Exception("Not implemented yet!")

    def getLayerBelow(self, layerMaterial):
        raise Exception("Not implemented yet!")

    def getLayerName(self):
        return self._name

    def getLayerNumber(self):
        return self._number

    def getMaterial(self):
        raise Exception("Not implemented yet!")

    def getPurposeName(self):
        raise Exception("Not implemented yet!")

    def getPurposeNumber(self):
        raise Exception("Not implemented yet!")

    def getRoutingDir(self):
        raise Exception("Not implemented yet!")

    def isAbove(self, layer):
        raise Exception("Not implemented yet!")

    def isMaskLayer(self):
        raise Exception("Not implemented yet!")

    @property
    def name(self):
        return self._name

    @property
    def number(self):
        return self._number

    @property
    def purposeName(self):
        return self._puyrposeName

    @property
    def purposeNumber(self):
        raise Exception("Not implemented yet!")



