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

from __future__ import annotations

from cni.point import *
from cni.ulist import *

class PointList(ulist[Point]):

    def __init__(self, items = None) -> None:
        super().__init__(items)

    def compress(self, isClose = True) -> PointList:
        """
        Compresses this PointList, by removing any extra (coincident and/or collinear) points from
        this PointList. The optional isClosed parameter is used to indicate whether this set of
        points is meant to represent a closed shape or not. If all points are collinear, then the
        first and last points will be the result of compressing this PointList. If the first and
        last points are coincident, then only the first point is returned

        :param isClose: Whether represented shape is closed
        :type p1: boolean
        :return: see description above
        :rtype: PointList
        """

        if len(self) < 3:
            return self

        if self[0] == self[-1]:
            firstPointList = []
            firstPointList.append(self[0])
            self = firstPointList
            return self

        uniqueList = []
        [uniqueList.append(i) for i in self if i not in uniqueList]

        nonColinearList = []
        for index, value in enumerate(uniqueList):
            if index == 0 or index == len(uniqueList)-1:
                nonColinearList.append(value)
            else:
                if not Point.areColinearPoints(uniqueList[index-1], value, uniqueList[index+1]):
                    nonColinearList.append(value)

        self = nonColinearList
        return self

