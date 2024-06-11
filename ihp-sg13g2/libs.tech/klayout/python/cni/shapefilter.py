########################################################################
#
# Copyright 2024 IHP PDK Authors
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

from cni.layer import Layer

class ShapeFilter(object):
    """
    Creates an empty ShapeFilter object, which would be used to indicate that all layers should be
    considered in any bounding box or placement calculations


    Creates a ShapeFilter object, consisting of only a single layer. This single layer is the only
    layer which should be considered when the ShapeFilter object is passed to methods which perform
    bounding box and placement calculations.

    :param layer: Layer to filter
    :type layer: Layer


    Creates a ShapeFilter object, consisting of a list of Layer objects. These layers are the only
    layers which should be considered when the ShapeFilter is passed to methods which perform
    bounding box or placement calculations.

    :param layerList: Layers to filter
    :type layerList: LayerList


    Creates a ShapeFilter object, consisting of the Layer objects which are specified by the
    shapeFilter ShapeFilter object. These layers are the only layers which should be considered when
    the ShapeFilter is passed to methods which perform bounding box or placement calculations.

    :param shapeFilter: ShapeFilter to filter
    :type shapeFilter: ShapeFilter

    """

    def __init__(self, arg = None):
        self._layers = []

        if arg is not None:
            if type(arg) is Layer:
                self._layers.append(arg)
            elif type(arg) is list:
                self._layers.extend(arg)
            elif type(arg) is ShapeFilter:
                self = arg.copy.deepcopy();
            else:
                raise Exception(f"Not supported type '{type(arg)}'")

    def isIncluded(self, layer: Layer) -> bool:
        """
        Returns true if the layer parameter is a layer which is in the list of layers considered by
        the ShapeFilter object, and returns False otherwise.

        :param layer: Layer to check
        :type layer: Layer
        :rtype: bool

        """

        if len(self._layers) == 0:
            return True

        for item in self._layers:
            if layer.getLayerName() == item.getLayerName():
                return True

        return False
