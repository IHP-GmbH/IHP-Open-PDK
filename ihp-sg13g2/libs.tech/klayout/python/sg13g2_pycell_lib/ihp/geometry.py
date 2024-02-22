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

__version__ = "$Revision: #3 $"

from cni.dlo import *
from cni.geo import fgOr
from cni.geo import fgAnd
from cni.geo import fgXor
from cni.geo import fgNot
from cni.geo import fgMerge
from .utility_functions import *
from math import *

#***********************************************************************************************************************
# nth
#***********************************************************************************************************************
def nth(index, mlist):
    if type(mlist) is Box:
        if index == 0 :
            lw = mlist.lowerLeft()
            x1 = lw.getX();
            return x1
        elif index == 1:
            lw = mlist.lowerLeft()
            y1 = lw.getY();
            return y1
        elif index == 2:
            ur = mlist.upperRight()
            x2 = ur.getX();
            return x2
        elif index == 3:
            ur = mlist.upperRight()
            y2 = ur.getY();
            return y2

    return mlist[index]

#***********************************************************************************************************************
# dbDeleteObject
#***********************************************************************************************************************
def dbDeleteObject(obj):
    obj.destroy()

#***********************************************************************************************************************
# dbLayerOr
#***********************************************************************************************************************
def dbLayerOr(layerId, id1, id2 = None):
    if type(layerId) == str :
        layerId = Layer(layerId)

    if id2 == None :
        id2 = id1

    idOr = id1.fgOr(id2, layerId)

    return idOr

#***********************************************************************************************************************
# dbLayerOrList
#***********************************************************************************************************************
def dbLayerOrList(layerId, shapes):
    if type(layerId) == str :
        layerId = Layer(layerId)

    id1 = shapes[0]
    for index in range(1, listlen(shapes)) :
        id2 = nth(index, shapes)
        idOr = dbLayerOr(layerId, id1, id2)
        if index > 0 :
            dbDeleteObject(id1)
        id1 = idOr

    return idOr

#***********************************************************************************************************************
# dbLayerAnd
#***********************************************************************************************************************
def dbLayerAnd(layerId, id1, id2):
    if type(layerId) == str :
        layerId = Layer(layerId)

    idAnd = id1.fgAnd(id2, layerId)

    return idAnd

#***********************************************************************************************************************
# dbLayerAndList
#***********************************************************************************************************************
def dbLayerAndList(layerId, shapes):
    if type(layerId) == str :
        layerId = Layer(layerId)

    idAnd = shapes[0]
    for id in shapes[1:] :
        idAnd = fgAnd(idAnd, id, layerId)

    return idAnd

#***********************************************************************************************************************
# dbLayerXor
#***********************************************************************************************************************
def dbLayerXor(layerId, id1, id2):
    if type(layerId) == str :
        layerId = Layer(layerId)

    xorId = id1.fgXor(id2, layerId)

    return xorId

#***********************************************************************************************************************
# dbLayerXorList
#***********************************************************************************************************************
def dbLayerXorList(layerId, shapes):
    if type(layerId) == str :
        layerId = Layer(layerId)

    xorId = shapes[0]
    for id in shapes[1:] :
        xorId = fgXor(xorId, id, layerId)

    return xorId

#***********************************************************************************************************************
# dbLayerNot
#***********************************************************************************************************************
def dbLayerNot(layerId, id1, id2):
    if type(layerId) == str :
        layerId = Layer(layerId)

    notId = id1.fgNot(id2, layerId)

    return notId

#***********************************************************************************************************************
# dbLayerNotList
#***********************************************************************************************************************
def dbLayerNotList(layerId, shapes):
    if type(layerId) == str :
        layerId = Layer(layerId)

    notId = shapes[0]
    for id in shapes[1:] :
        notId = fgNot(notId, id, layerId)

    return notId

#***********************************************************************************************************************
# dbLayerMerge
#***********************************************************************************************************************
def dbLayerMerge(self, layerId):
    if type(layerId) == str :
        layerId = Layer(layerId)

    shapes = self.getLeafComps()
    mergeId = shapes[0].fgMerge(layerId)

    return mergeId

#***********************************************************************************************************************
# dbCopyShape
#***********************************************************************************************************************
def dbLayerSize(self, layerId, shapes, size, numPoints, grid = 0) :
    for id in shapes :
        id.fgSize(ShapeFilter(), size, layerId, grid)

#***********************************************************************************************************************
# dbCopyShape
#***********************************************************************************************************************
def dbCopyShape(fig, pnt, rot):
    copyId = fig.clone()

    dbMoveFig(copyId, pnt, rot)

    return copyId

#***********************************************************************************************************************
# dbMoveFig
#***********************************************************************************************************************
def dbMoveFig(fig, pnt, rot) :
    if rot :
        fig.transform(Transform(0, 0, strToOrient(rot)))

    if pnt :
        fig.moveBy(pnt.x, pnt.y)

#***********************************************************************************************************************
# dbLayerInside
#   layer - new layer for cloned shape
#***********************************************************************************************************************
def dbLayerInside(self, layer, idlist, id):

    if type(layer) == str :
        layer = Layer(layer)

    pnts = id.getPoints()

    mlist = list()
    for item in idlist :
        if type(item) == Rect :
            if pnts.containsPoint(Point(item.left, item.bottom)) and pnts.containsPoint(Point(item.left, item.top)) and pnts.containsPoint(Point(item.right, item.bottom)) and pnts.containsPoint(Point(item.right, item.top)) :
                it = item.clone()
                it.layer = layer
                mlist.append(it)
        else :
            pnts1 = item.getPoints()
            yes = False
            for pnt in pnts1 :
                if pnts.containsPoint(pnt) :
                    yes = True
                else :
                    yes = False
                    break

            if yes :
                it = item.clone()
                it.layer = layer
                mlist.append(it)

        #idOr = id.fgOr(item, layer)
        #if len(idOr.getComps()) == 1 :
        #    shape = idOr.getComp(0)
        #    if shape.getNumPoints() == 3 :
        #        mlist.append(item.clone())
        #
        #idOr.destroy()

    return mlist

#***********************************************************************************************************************
# dbLayerOutside
#***********************************************************************************************************************
def dbLayerOutside(self, layer, idlist, id):
    if type(layer) == str :
        layer = Layer(layer)

    if type(id) == Rect :
        pnts = PointList([Point(id.left, id.bottom), Point(id.left, id.top), Point(id.right, id.bottom), Point(id.right, id.top)])
    else :
        pnts = id.getPoints()

    mlist = list()
    for item in idlist :
        if type(item) == Rect :
            if pnts.containsPoint(Point(item.left, item.bottom)) and pnts.containsPoint(Point(item.left, item.top)) and pnts.containsPoint(Point(item.right, item.bottom)) and pnts.containsPoint(Point(item.right, item.top)) :
                pass
            else :
                mlist.append(item.clone())
        else :
            pnts1 = item.getPoints()
            yes = False
            for pnt in pnts1 :
                if pnts.containsPoint(pnt) :
                    yes = False
                    break
                else :
                    yes = True

            if yes :
                it = item.clone()
                it.layer = layer
                mlist.append(it)

    return mlist

#***********************************************************************************************************************
# dbCreateRect
#***********************************************************************************************************************
def dbCreateRect(self, layerId, bBox):
    if type(layerId) == str :
        layerId = Layer(layerId)

    rectId = Rect(layerId, bBox)
    return rectId

#***********************************************************************************************************************
# dbCreatePolygon
#***********************************************************************************************************************
def dbCreatePolygon(self, layerId, pointList):
    if type(layerId) is str :
        layerId = Layer(layerId)

    if type(pointList) is list :
        points = PointList()

        pointIndex = 0
        pointValue = 0
        for p in pointList :
            if pointIndex == 0 :
                pointValue = p
            elif pointIndex == 1 :
                point = Point(pointValue, p)
                points.append(point)
                pointIndex = -1

            pointIndex = pointIndex + 1

        pointList = points.compress()
    else :
        pointList = pointList.compress()

    polyId = Polygon(layerId, pointList)
    return polyId

#***********************************************************************************************************************
# dbCreatePath
#***********************************************************************************************************************
def dbCreatePath(self, layerId, pointList, width, style=PathStyle.TRUNCATE):
    if type(layerId) == str :
        layerId = Layer(layerId)

    pointList = pointList.compress()

    pathId = Path(layerId, width, pointList, style)
    return pathId

#***********************************************************************************************************************
# dbCreateDonut
#***********************************************************************************************************************
def dbCreateDonut(self, layerId, pnt, outRad, inRad):
    if type(layerId) == str :
        layerId = Layer(layerId)

    donutId = Donut(layerId, pnt, outRad, inRad)
    return donutId

#***********************************************************************************************************************
# dbCreateEllipse
#***********************************************************************************************************************
def dbCreateEllipse(self, layerId, bbox):
    if type(layerId) == str :
        layerId = Layer(layerId)

    ellipseId = Ellipse(layerId, bbox)

    return ellipseId

#***********************************************************************************************************************
# dbConvertEllipseToPolygon
#***********************************************************************************************************************
def dbConvertEllipseToPolygon(self, ellipse, numPoints, grid):
    points = Ellipse.genPolygonPoints(ellipse.getBBox(), numPoints, grid)
    polyId = dbCreatePolygon(self, ellipse.layer, points)

    return polyId

#***********************************************************************************************************************
# dbCreateLabel
#***********************************************************************************************************************
def dbCreateLabel(self, layerId, point, text, align, rotation, font, size):
    text = Text(layerId, text, point, size)

    text.setAlignment(strToAlignt(align))
    text.setOrientation(strToOrient(rotation))

    """
    rect = text.getBBox()
    lw = rect.lowerLeft()
    ur = rect.upperRight()

    x1 = lw.getX()
    x2 = ur.getX()
    y1 = lw.getY()
    y2 = ur.getY()

    if y1 > y2:
        temp = y1
        y1 = y2
        y2 = temp

    if x1 > x2:
        temp = x1
        x1 = x2
        x2 = temp

    shiftX = (x2-x1)/2
    shiftY = (y2-y1)/2
    text.setFont(font)
    text.setAlignment(align)

    if rotation is "R0":
        text.setOrientation(Orientation.R0)
        text.setOrigin(Point(x1-shiftX, y2+shiftY))
    elif rotation is "R90":
        text.setOrigin(Point(x1-shiftY, y2-shiftX))
        text.setOrientation(Orientation.R90)
    """
    return text

#***********************************************************************************************************************
# dbCreateNet
#***********************************************************************************************************************
def dbCreateNet(name, typ=SignalType.SIGNAL):
    net = Net.find(name)
    if not net :
        net = Net(name, typ)

    return net

#***********************************************************************************************************************
# dbCreateTerm
#***********************************************************************************************************************
def dbCreateTerm(self, name, typ=TermType.INPUT_OUTPUT):
    term = Term.find(name)
    if not term :
        term = self.addTerm(name, typ)

    return term

#***********************************************************************************************************************
# dbCreatePin
#***********************************************************************************************************************
def dbCreatePin(self, name, shape):
    pin = self.addPin(name, name, shape.getBBox(shape.layer), shape.layer)
    if not (shape.getNet() or shape.getPin()) :
        pin.addShape(shape)

    return pin

#***********************************************************************************************************************
# MkPin
#***********************************************************************************************************************
def MkPin(self, termName, termIndex, bBox, layerId, label=False, labelHight = -1):
    if type(layerId) == str :
        layerId = Layer(layerId, 'pin')

    bBox = bBox.fix()

    self.addPin(termName, termName, bBox, layerId)

    pcInst = dbCreateRect(self, layerId, bBox) # 17.6.11 GG

    # pin label
    if label and termName :
        if labelHight == -1 :
            pcLabelHeight = 0.5*min(bBox.getWidth(), abs(bBox.getHeight()))
        else :
            pcLabelHeight = labelHight
        dbCreateLabel(self, layerId, bBox.getCenter(), termName, 'centerCenter', 'R0', Font.EURO_STYLE, pcLabelHeight)

#***********************************************************************************************************************
# dbCreateVia
#***********************************************************************************************************************
def dbCreateVia(self, ViaDef, pnt, rot, params):
    via = StdVia(ViaDef.getName())

    via.setOrientation(strToOrient(rot))
    via.setOrigin(pnt)

    vp = via.getParams()
    if 'cutLayer' in params :
        cutLayer = params['cutLayer']
    else :
        cutLayer = vp.cutLayer
    if 'cutSize' in params :
        cutSize = params['cutSize']
    else :
        cutSize = vp.cutSize
    if 'cutSpace' in params :
        cutSpace = params['cutSpace']
    else :
        cutSpace = vp.cutSpace
    if 'implant1Ext' in params :
        implant1Ext = params['implant1Ext']
    else :
        implant1Ext = vp.implant1Ext
    if 'implant2Ext' in params :
        implant2Ext = params['implant2Ext']
    else :
        implant2Ext = vp.implant2Ext
    if 'layer1Ext' in params :
        layer1Ext = params['layer1Ext']
    else :
        layer1Ext = vp.layer1Ext
    if 'layer1Offset' in params :
        layer1Offset = params['layer1Offset']
    else :
        layer1Offset = vp.layer1Offset
    if 'layer2Ext' in params :
        layer2Ext = params['layer2Ext']
    else :
        layer2Ext = vp.layer2Ext
    if 'layer2Offset' in params :
        layer2Offset = params['layer2Offset']
    else :
        layer2Offset = vp.layer2Offset
    if 'numHVCuts' in params :
        numHVCuts = params['numHVCuts']
    else :
        numHVCuts = vp.numHVCuts
    if 'originOffset' in params :
        originOffset = params['originOffset']
    else :
        originOffset = vp.originOffset

    vp = ViaParam(vp,
                  layer1Ext,
                  layer2Ext,
                  implant1Ext,
                  implant2Ext,
                  layer1Offset,
                  layer2Offset,
                  originOffset,
                  cutSpace,
                  cutSize,
                  cutLayer,
                  numHVCuts)

    via.setParams(vp)

    return via

#***********************************************************************************************************************
# DrawRing
#***********************************************************************************************************************
def DrawRing(self, layer, rl, rr, rb, rt, rw, rh) :
    dbCreatePolygon(self, layer, PointList([Point(rl,rb), Point(rr,rb),
                                            Point(rr,rt), Point(rl,rt),
                                            Point(rl,rb+rh), Point(rl+rw,rb+rh),
                                            Point(rl+rw,rt-rh), Point(rr-rw,rt-rh),
                                            Point(rr-rw,rb+rh), Point(rl,rb+rh)]))

#***********************************************************************************************************************
# ihpBuildCont
#***********************************************************************************************************************
def ihpBuildCont(self, layer1, layer2, layer3, width1, width3, length3, pathpnts, terminal, pinlabel,
                       layer2_enc, offset, chop, layer3_space) :

    # pinlabel is a boolean that determines whether a label will be created
    # terminal is the pin name string

    bBox = Box(pathpnts.left-(width1/2), pathpnts.bottom, pathpnts.right+(width1/2), pathpnts.top)

    if terminal :
        do_pins = True
    else :
        do_pins = False


    # paths in layers 1&2 with subrectanges in layer3 and label in layer2
    if (layer3 and layer2 and layer1 and (layer1 != layer2)) :
        fig = dbCreateRect(self, layer2, bBox)
        pin_fig = dbCreateRect(self, layer2, Box(bBox.left+layer2_enc, bBox.bottom+layer2_enc, bBox.right-layer2_enc, bBox.top-layer2_enc))

        contactArray(self, layer2, layer3,
                     bBox.left, bBox.bottom, bBox.right, bBox.top,
                     layer2_enc, offset, width3, layer3_space)

    else : # paths in layers 1&2 with no subrectanges and label in layer2
        if ( (not layer3) and layer2 and layer1 and (layer1 != layer2) ) :
            fig = dbCreateRect(self, layer1, bBox)
            pin_fig = dbCreateRect(self, layer2, Box(bBox.left+layer2_enc, bBox.bottom+layer2_enc, bBox.right-layer2_enc, bBox.top-layer2_enc))

        else : # path in layer2 and rectangles in layer3 (one layer path and subrectangles)
            if( (not layer1) and (layer3 != layer2) ) :
                fig = dbCreateRect(self, layer2, bBox)
                pin_fig = fig
                contactArray(self, layer2, layer3,
                             bBox.left, bBox.bottom, bBox.right, bBox.top,
                             layer2_enc, offset, width3, layer3_space)

            else : # paths in layer 1 (one layer path)
                if layer1 != layer2 :
                    fig = dbCreateRect(self, layer1, bBox)
                    pin_fig = fig

    return [pin_fig, fig]

#***********************************************************************************************************************
# buildCont
#***********************************************************************************************************************
def buildCont(self, layer1, layer2, layer3, width1, width3, length3, pathpnts, terminal, pinlabel, layer2_enc, offset, chop, layer3_space) :
    # pinlabel is a boolean that determines whether a label will be created
    # terminal is the pin name string

    if terminal :
        do_pins = True
    else :
        do_pins = False

    if pathpnts[0].x > pathpnts[1].x :
        x = pathpnts[0].x
        pathpnts[0].x = pathpnts[1].x
        pathpnts[1].x = x
    if pathpnts[0].y > pathpnts[1].y :
        y = pathpnts[0].y
        pathpnts[0].y = pathpnts[1].y
        pathpnts[1].y = y

    if pathpnts[0].x == pathpnts[1].x :
        pathl = abs(pathpnts[0].y - pathpnts[1].y)
        hor = False
    elif pathpnts[0].y == pathpnts[1].y :
        pathl = abs(pathpnts[0].x - pathpnts[1].x)
        hor = True
    else :
        print('Warning: Incline path is not allowed for buildCont procedure')
        return

    count = pathl/(length3+layer3_space+offset)
    if  count - int(count) > 0.5 :
        count = int(count) + 1
    start = 0
    if pinlabel :
        start = 1

    # paths in layers 1&2 with subrectanges in layer3 and label in layer2
    if layer3 and layer2 and layer1 and (layer1 != layer2) :
        # rodCreatePath
        fig = dbCreatePath(self, layer1, pathpnts, width1)
        if pinlabel :
            if hor :
                MkPin(self, terminal, 0, Box((pathpnts[0].x+offset), pathpnts[0].y-width3/2, (pathpnts[0].x+offset)+width3, pathpnts[0].y+width3/2), layer2, pinlabel, layer2, length3)
            else :
                MkPin(self, terminal, 0, Box(pathpnts[0].x-width3/2, (pathpnts[0].y+offset), pathpnts[0].x+width3/2, (pathpnts[0].y+offset)+length3), layer2, pinlabel, layer2, length3)

        # subRect
        box = fig.getBBox()
        if hor :
            box.expandDir(Direction.WEST, -offset)
            box.expandDir(Direction.EAST, -offset)
        else :
            box.expandDir(Direction.NORTH, -offset)
            box.expandDir(Direction.SOUTH, -offset)
        Rect.fillBBoxWithRects(layer3, box, width3, length3, layer3_space, layer3_space, GapStyle.DISTRIBUTE)

        # rodCreateRect
        pin_fig = list()
        if do_pins :
            pin = MkPin(self, terminal, 0, fig.bbox.expand(-layer2_enc), layer1)
        else :
            pin = dbCreateRect(self, layer1, fig.bbox.expand(-layer2_enc))
        pin_fig.append(pin)

        #rodAlign(?alignObj, pin_fig, ?alignHandle, "centerCenter", ?refObj, fig, ?refHandle, "centerCenter")
    else :   # paths in layers 1&2 with no subrectanges and label in layer2
        if not layer3 and layer2 and layer1 and (layer1 != layer2) :
            # rodCreatePath
            fig = dbCreatePath(self, layer1, pathpnts, width1)
            if pinlabel :
                if hor :
                    MkPin(self, terminal, 0, Box((pathpnts[0].x+offset), pathpnts[0].y-width3/2, (pathpnts[0].x+offset)+width3, pathpnts[0].y+width3/2), layer2, pinlabel, layer2, length3, 'R0', 'centerLeft', Font.ROMAN)
                else :
                    MkPin(self, terminal, 0, Box(pathpnts[0].x-width3/2, (pathpnts[0].y+offset), pathpnts[0].x+width3/2, (pathpnts[0].y+offset)+length3), layer2, pinlabel, layer2, length3, 'R0', 'centerLeft', Font.ROMAN)

            # encSubPath
            dbCreatePath(self, layer2, pathpnts, width1-(2*layer2_enc))

            # rodCreateRect
            pin_fig = list()
            if do_pins :
                pin = MkPin(self, terminal, 0, fig.bbox, layer1)
            else :
                pin = dbCreateRect(self, layer1, fig.bbox)
            pin_fig.append(pin)

            #rodAlign(?alignObj, pin_fig, ?alignHandle, "centerCenter", ?refObj, fig, ?refHandle, "centerCenter")
        else :   # path in layer2 and rectangles in layer3 (one layer path and subrectangles)
            if not layer1 and layer3 != layer2 :
                # rodCreatePath
                fig = dbCreatePath(self, layer2, pathpnts, width1)
                if pinlabel :
                    if hor :
                        MkPin(self, terminal, 0, Box((pathpnts[0].x+offset), pathpnts[0].y-width3/2, (pathpnts[0].x+offset)+width3, pathpnts[0].y+width3/2), layer2)
                    else :
                        MkPin(self, terminal, 0, Box(pathpnts[0].x-width3/2, (pathpnts[0].y+offset), pathpnts[0].x+width3/2, (pathpnts[0].y+offset)+length3), layer2)

                # subRect
                box = fig.getBBox()
                if hor :
                    box.expandDir(Direction.WEST, -offset)
                    box.expandDir(Direction.EAST, -offset)
                else :
                    box.expandDir(Direction.NORTH, -offset)
                    box.expandDir(Direction.SOUTH, -offset)
                Rect.fillBBoxWithRects(layer3, box, width3, length3, layer3_space, layer3_space, GapStyle.DISTRIBUTE)

                # rodCreateRect
                pin_fig = list()
                if do_pins :
                    pin = MkPin(self, terminal, 0, fig.bbox, layer2)
                else :
                    pin = dbCreateRect(self, layer2, fig.bbox)
                pin_fig.append(pin)

                #rodAlign(?alignObj, pin_fig, ?alignHandle, "centerCenter", ?refObj, fig, ?refHandle, "centerCenter")
            else :   # paths in layer 1 (one layer path)
                if layer1 != layer2 :
                    # rodCreatePath
                    fig = dbCreatePath(self, layer1, pathpnts, width1)
                    if pinlabel :
                        if hor :
                            MkPin(self, terminal, 0, Box((pathpnts[0].x+offset), pathpnts[0].y-width3/2, (pathpnts[0].x+offset)+width3, pathpnts[0].y+width3/2), layer1)
                        else :
                            MkPin(self, terminal, 0, Box(pathpnts[0].x-width3/2, (pathpnts[0].y+offset), pathpnts[0].x+width3/2, (pathpnts[0].y+offset)+length3), layer1)

                    # rodCreateRect
                    pin_fig = list()
                    if do_pins :
                        pin = MkPin(self, terminal, 0, fig.bbox, layer1)
                    else :
                        pin = dbCreateRect(self, layer1, fig.bbox)
                    pin_fig.append(pin)

                    #rodAlign(?alignObj, pin_fig, ?alignHandle, "centerCenter", ?refObj, fig, ?refHandle, "centerCenter")

    return [pin_fig, fig]

#***********************************************************************************************************************
# MetalCont
#***********************************************************************************************************************
def MetalCont(self, p1_x, p1_y, p2_x, p2_y, _layer2, _layer3, _width1, _width3, _length3, _offset, _layer3_space) :
    pathLayer = _layer2
    width = _width1
    subRectLayer = _layer3
    srect_w = _width3
    srect_l = _length3
    srect_o = _offset
    srect_space = _layer3_space
    boxRectLayer = _layer2
    boxRectDelta = 0.0

    mlist = ulist[Rect]()
    __w2 = width/2
    if p1_x == p2_x :
        x_left  = p1_x-__w2
        x_right = p1_x+__w2
        if p1_y < p2_y :
            y_bot = p1_y
            y_top = p2_y
        else :
            y_bot = p2_y
            y_top = p1_y

        _sw2 = srect_w/2
        _yl = p1_x-_sw2
        _xr = p1_x+_sw2
        _yges = y_top-y_bot-2*srect_o
        _nrect = floor((_yges+srect_space)/(srect_l+srect_space))

        if _nrect > 1 :    # calculate new space and do a loop
            _rsp = (_yges-_nrect*srect_l)/(_nrect-1)
            _yy = y_bot+srect_o
            while _yy+srect_l <= y_top-srect_o+0.0001 :
                id = dbCreateRect(self, subRectLayer, Box(tog(_yl), tog(_yy), tog(_xr), tog(_yy+srect_l)))
                mlist.append(id )
                _yy = _yy+srect_l+_rsp

        else :
                if _nrect == 1 :  # center a single rect
                    _ymb = (y_top+y_bot-srect_l)/2
                    id = dbCreateRect(self, subRectLayer, Box(tog(_yl), tog(_ymb), tog(_xr), tog(_ymb+srect_l)))
                    mlist.append(id)

    else :
        if p1_y == p2_y :
            y_bot = p1_y-__w2
            y_top = p1_y+__w2
            if p1_x < p2_x :
                x_left = p1_x
                x_right = p2_x
            else :
                x_left = p2_x
                x_right = p1_x

            _sw2 = srect_w/2
            _yb = p1_y-_sw2
            _yt = p1_y+_sw2
            _xges = x_right-x_left-2*srect_o
            _nrect = floor((_xges+srect_space)/(srect_l+srect_space))

            if _nrect > 1  :   # calculate new space and do a loop
                _rsp = (_xges-_nrect*srect_l)/(_nrect-1)
                _xx = x_left+srect_o
                while _xx+srect_l <= x_right-srect_o+0.0001 :
                    id = dbCreateRect(self, subRectLayer, Box(tog(_xx), tog(_yb), tog(_xx+srect_l), tog(_yt)))
                    mlist.append(id)
                    _xx = _xx+srect_l+_rsp

            else :
                if _nrect == 1  :  # center a single rect
                    _xml = (x_left+x_right-srect_l)/2
                    id = dbCreateRect(self, subRectLayer, Box(tog(_xml), tog(_yb), tog(_xml+srect_l), tog(_yt)))
                    mlist.append(id)

        else :
            return mlist

    if pathLayer != ""  :
        id = dbCreateRect(self, pathLayer, Box(tog(x_left), tog(y_bot), tog(x_right), tog(y_top)))
        mlist.append(id)

    return mlist

#***********************************************************************************************************************
# DrawContArray
#***********************************************************************************************************************
def DrawContArray(self, layer, bbox, size, space, over):
    epsilon = self.techparams['epsilon1']

    bbox = bbox.fix()

    x1 = bbox.left
    x2 = bbox.right
    y1 = bbox.bottom
    y2 = bbox.top

    xanz = fix((x2-x1-2*over+space+epsilon)/(size+space))
    yanz = fix((y2-y1-2*over+space+epsilon)/(size+space))

    name = self.tech.name().split()[0]
    if name == 'SG13_dev' :
        cont_layer = 'Cont'
        cont_dist_big = self.techparams['Cnt_b1']
        cont_dist_big_nr = self.techparams['Cnt_b1_nr']

        # now check, if it is cont and more than 4 rows/lines
        if layer.name==cont_layer and xanz>=cont_dist_big_nr and yanz>=cont_dist_big_nr :
            # it has to be bigger space between contacts
            space = cont_dist_big
            # it has to be bigger space between contacts
            xanz = fix((x2-x1-2*over+space+epsilon)/(size+space))
            yanz = fix((y2-y1-2*over+space+epsilon)/(size+space))

    xmin = xanz*(size+space)-space+2*over
    ymin = yanz*(size+space)-space+2*over
    xoff = (x2-x1-xmin)/2
    xoff = GridFix(xoff)
    yoff = (y2-y1-ymin)/2
    yoff = GridFix(yoff)

    for j in range(int(yanz)):
        for i in range(int(xanz)):
            dbCreateRect(self, layer, Box(x1+xoff+over+(size+space)*i, y1+yoff+over+(size+space)*j,
                                          x1+xoff+over+(size+space)*i+size, y1+yoff+over+(size+space)*j+size))

    return Box(x1+xoff+over, y1+yoff+over,
               x1+xoff+over+xanz*size+(xanz-1)*space,
               y1+yoff+over+yanz*size+(yanz-1)*space)

#***********************************************************************************************************************
# contactArray
#***********************************************************************************************************************
def contactArray(self, pathLayer, contLayer, xl, yl, xh, yh, ox, oy, ws, ds):
    eps = self.tech.getTechParams()['epsilon1']

    w = xh-xl
    h = yh-yl

    mlist = list()

    nx = floor((w-ox*2+ds)/(ws+ds)+eps)
    if (nx <= 0) :
        return mlist

    dsx = 0
    if (nx == 1) :
        dsx = 0
    else :
        dsx = (w-ox*2-ws*nx)/(nx-1)

    ny = floor((h-oy*2+ds)/(ws+ds)+eps)
    if (ny <= 0) :
        return mlist

    dsy = 0
    if (ny == 1) :
        dsy = 0
    else :
        dsy = (h-oy*2-ws*ny)/(ny-1)

    x = 0
    if (nx == 1) :
        x = (w-ws)/2
    else :
        x = ox

    if pathLayer :
        mlist.append(dbCreateRect(self, pathLayer, Box(xl, yl, xh, yh)))

    for i in range(int(nx)) :
    #for(i=1; i<=nx; i++) {
        y = 0
        if ny == 1 :
            y = (h-ws)/2
        else :
            y = oy

        for j in range(int(ny)) :
        #for(j=1; j<=ny; j++) {
            mlist.append(dbCreateRect(self, contLayer, Box(xl+tog(x), yl+tog(y), xl+tog(x+ws), yl+tog(y+ws))))
            y = y+ws+dsy

        x = x+ws+dsx

    if pathLayer :
        mlist.append(dbCreateRect(self, pathLayer, Box(xl, yl, xh, yh)))

    return mlist


#***********************************************************************************************************************
# DrawContRowMid
#***********************************************************************************************************************
def DrawContRowMid(self, layer, x0, y0, x1, y1, size, space, drawMid, GRID, EPSILON):
    IGRID = 1/GRID

    dx = 0.0
    dy = 0.0
    xShift = 0.0
    yShift = 0.0

    x0 = int(x0*IGRID+EPSILON)*GRID
    x1 = int(x1*IGRID+EPSILON)*GRID
    y0 = int(y0*IGRID+EPSILON)*GRID
    y1 = int(y1*IGRID+EPSILON)*GRID

    if (x1-x0 > 0.0):
      dx = size+space

    if (x1-x0 < 0.0):
      dx = -(size+space)

    if (y1-y0 > 0.0):
      dy = size+space

    if (y1-y0 < 0.0):
      dy = -(size+space)

    if (nonzero(dx) and nonzero(dy)):
      delta = int(space*(1.0-1.0/math.sqrt(2.0)-0.01)*IGRID-EPSILON)*GRID
      if (dx > 0.0):
        dx = dx-delta
      else:
        dx = dx+delta

      if (dy > 0.0):
        dy = dy-delta
      else:
        dy = dy+delta

    xofs = 0.0
    yofs = 0.0

    if ((dy > 0.0) and iszero(dx)):
      xofs = int(-size/2.0*IGRID+EPSILON)*GRID
      yofs = 0.0
      xShift = 0.0
      yShift = 1

    if ((dx > 0.0) and (dy>0.0)):
      xofs = 0.0
      yofs = 0.0
      xShift = 1.0
      yShift = 1.0

    if ((dx > 0.0) and iszero(dy)):
      xofs = 0.0
      yofs = int(-size/2.0*IGRID+EPSILON)*GRID
      xShift = 1.0
      yShift = 0.0

    if ((dx > 0.0) and (dy < 0.0)):
      xofs = 0.0
      yofs = int(-size*IGRID+EPSILON)*GRID
      xShift = 1.0
      yShift = -1.0

    if ((dy < 0.0) and iszero(dx)):
      xofs = int(-size/2.0*IGRID+EPSILON)*GRID
      yofs = -size
      xShift = 0.0
      yShift = -1.0

    if ((dy < 0.0) and (dx < 0.0)):
      xofs = -size
      yofs = -size
      xShift = -1.0
      yShift = -1.0

    if ((dx < 0.0) and iszero (dy)):
      xofs = -size # -fix(size/3.0*IGRID)*GRID
      yofs = int(-size/2.0*IGRID+EPSILON)*GRID
      xShift = -1.0
      yShift = 0.0

    if ((dx < 0.0) and (dy > 0.0)):
      xofs = -size
      yofs = 0.0
      xShift = -1.0
      yShift = 1.0

    len = max (abs(x1-x0), abs(y1-y0))
    orglen = len
    len = len-space
    sstep = max(abs(dx), abs(dy))
    anz = int((len+(sstep-size)+EPSILON)/sstep)
    ovhd = orglen - (anz-1)*sstep - size

    if drawMid:
      x0 = Snap(x0+(xShift*ovhd/2))
      y0 = Snap(y0+(yShift*ovhd/2))

    for i in range (anz):
      dbCreateRect(self, layer, Box(xofs+x0+dx*i, yofs+y0+dy*i, xofs+x0+dx*i+size, yofs+y0+dy*i+size))

#***********************************************************************************************************************
# myBox: safe version of Box that works with x2,y2 smaller also
#***********************************************************************************************************************
def myBox(x1,y1,x2,y2):
    if x1<x2:
        xmin=x1
        xmax=x2
    else:
        xmin=x2
        xmax=x1

    if y1<y2:
        ymin=y1
        ymax=y2
    else:
        ymin=y2
        ymax=y1

    return Box(xmin,ymin,xmax,ymax)

#***********************************************************************************************************************
# ResizeBBox
#***********************************************************************************************************************
def ResizeBBox(bBox, value):
    return bBox.expand(value)

#***********************************************************************************************************************
# dbReplaceProp
#***********************************************************************************************************************
def dbReplaceProp(self, name, value):
    self.props[name] = value

#***********************************************************************************************************************
# dbDeleteObject
#***********************************************************************************************************************
def dbDeleteObject(self):
    self.destroy()

#***********************************************************************************************************************
# DrawFillers
#
# procedure filler in given area
## arguments:
## - xl,yl,xh,yh   (rectangle to be filled)
## - ws,hs (filler width, height)
## - dx,dy (space between fillers)
#***********************************************************************************************************************
def DrawFillers(self, layer, xl, yl, xh, yh, ws, hs, dx, dy, dir, offset, retlist):
    #Rect.fillBBoxWithRects(layer, Box(xl, yl, xh, yh), ws, hs, dx, dy)
    #return

    if type(layer) == str :
        layer = Layer(layer)

    idlist = list()
    W = xh-xl
    H = yh-yl
    nry = floor((H+dy)/(hs+dy))

    if nry > 1 : # vertical space between fillers
        hns = (H-nry*hs)/(nry-1)
    else :
        hns = 0.

    nrx = floor((W+dx)/(ws+dx))
    if nrx > 1 :    # horizontal space between fillers
        wns = (W-nrx*ws)/(nrx-1)
    else :
        wns = 0.

    if dir == 'u' :
        if nrx >= nry :
            dir = 'h'
        else :
            dir = 'v'

    if dir == 'h'  :  # row-wise
        if offset > 0 :
            off = (ws+dx)*0.5
        else :
            off = 0.

        y = yl
        for i in range(1, int(nry)+1) :
            togy = tog(y)
            x = xl
            nr = nrx
            if offset != 0 and evenp(i+offset-1) and nr > 1 :
                nr = nr-1
                x = x+off

            for j in range(1, int(nr)+1) :
                togx = tog(x)
                id = dbCreateRect(self, layer, Box(togx, togy, togx+ws, togy+hs))
                if retlist :
                    cons(idlist, id)
                x = x+wns+ws

            y = y+hns+hs

    else : # column-wise
        if offset > 0 :
            off = (hs+dy)*0.5
        else :
            0
        x = xl
        for i in range(1, int(nrx)+1) :
            togx = tog(x)
            y = yl
            nr = nry
            if offset != 0 and evenp(i+offset-1) :
                nr = nr-1
                y = y+off

            for j in range(1, int(nr)+1) :
                togy = tog(y)
                id = dbCreateRect(self, layer, Box(togx, togy, togx+ws, togy+hs))
                if retlist :
                    cons(idlist, id)
                y = y+hns+hs

            x = x+wns+ws

    # if

    return idlist

#***********************************************************************************************************************
# generateCorner
#***********************************************************************************************************************
def generateCorner(self, corner_startx, corner_starty, corner_width, corner_length, corner_steps, corner_end, offset, layer):
    item_list = list()
    for cnt in range(corner_steps) :
        rect = dbCreateRect(self, Layer(layer, 'drawing'), Box(corner_startx - corner_width * (cnt + 1), corner_starty + offset + (corner_length - corner_width) * cnt,
                                                                   corner_startx - corner_width * cnt, corner_starty+corner_length + offset  + (corner_length-corner_width) * cnt))
        cons(item_list, rect)

    rect = dbCreateRect(self, Layer(layer, 'drawing'), Box(corner_startx - corner_width * (corner_steps + 1), corner_starty + offset  + (corner_length - corner_width) * corner_steps,
                                                               corner_startx - corner_width * corner_steps, corner_end))
    cons(item_list, rect)

    return item_list

#***********************************************************************************************************************
# combineLayerAndDelete
#***********************************************************************************************************************
def combineLayerAndDelete(self, item_list, groupId, layer):

    shapes = dbLayerOrList(Layer(layer, 'drawing'), item_list)

    size = len(shapes.getComps())
    for i in range(size) :
        cons(groupId, shapes.getComp(i))

    for item in item_list :
        item.destroy()

    return groupId

#***********************************************************************************************************************
# ihpCopyFig
#***********************************************************************************************************************
def ihpCopyFig(groupId, pnt, rot):
    newList = list()
    for item in groupId :
        cons(newList, dbCopyShape(item, pnt, rot))

    return newList

#**************************************************************************************************************
# bondpadOctagonPoints
#**************************************************************************************************************
def bondpadOctagonPoints(rx, ry, off):
    return PointList([Point(-rx    , -ry+off), Point(-rx    , ry-off ),
                      Point(-rx+off, ry     ), Point(rx-off , ry     ),
                      Point(rx     , ry-off ), Point(rx     , -ry+off),
                      Point(rx-off , -ry    ), Point(-rx+off, -ry    )])

#**************************************************************************************************************
# bondpadOctagonRingPoints
#**************************************************************************************************************
def bondpadOctagonRingPoints(rx, ry, off, rxi, ryi, offi):
    return PointList([Point(-rx      , 0        ), Point(-rx      , ry-off   ),
                      Point(-rx+off  , ry       ), Point(rx-off   , ry       ),
                      Point(rx       , ry-off   ), Point(rx       , -ry+off  ),
                      Point(rx-off   , -ry      ), Point(-rx+off  , -ry      ),
                      Point(-rx      , -ry+off  ), Point(-rx      , 0        ),
                      Point(-rxi     , 0        ), Point(-rxi     , -ryi+offi),
                      Point(-rxi+offi, -ryi     ), Point(rxi-offi , -ryi     ),
                      Point(rxi      , -ryi+offi), Point(rxi      , ryi-offi ),
                      Point(rxi-offi , ryi      ), Point(-rxi+offi, ryi      ),
                      Point(-rxi     , ryi-offi ), Point(-rxi     , 0        )])

#**************************************************************************************************************
# bondpadStretchedCircle
#**************************************************************************************************************
def bondpadStretchedCircle(self, layer, rx, ry, grid):
    if type(layer) == str :
        layer = Layer(layer)

    if rx == ry :
        id1 = dbCreateEllipse(self, layer, Box(-rx, -rx, rx, rx))
        id  = dbConvertEllipseToPolygon(self, id1, 64, grid)
        return id

    if rx > ry :
        id1 = dbCreateEllipse(self, layer, Box(-rx, -ry -rx+ry*2, ry))
        id2 = dbCreateEllipse(self, layer, Box(rx-ry*2, -ry, rx, ry))
        id3 = dbCreateRect(self, layer, Box(ry-rx, -ry, rx-ry, ry))
        id = dbLayerOrList(layer, [id1, id2, id3])
        dbDeleteObject(id1)
        dbDeleteObject(id2)
        dbDeleteObject(id3)
        return id[0]

    id1 = dbCreateEllipse(self, layer, Box(-rx, -ry, rx, -ry+rx*2))
    id2 = dbCreateEllipse(self, layer, Box(-rx, ry-rx*2, rx, ry))
    id3 = dbCreateRect(self, layer, Box(-rx, rx-ry, rx, ry-rx))
    id = dbLayerOr(layer, [id1, id2, id3])
    dbDeleteObject(id1)
    dbDeleteObject(id2)
    dbDeleteObject(id3)

    return id[0]

#***********************************************************************************************************************
# geoMerge
#***********************************************************************************************************************
def geoMerge(self, layer) :
    if type(layer) == str :
        layer = Layer(layer)

    idlst = list()
    shapes = self.getLeafComps()
    for id in shapes :
        if id.layer == layer :
            idlst.append(id)

    if idlst :
        dbLayerOrList(layer, idlst)
        for id in idlst :
            id.destroy()

#***********************************************************************************************************************
# geoRing
#***********************************************************************************************************************
def geoRing(self, layer, rl, rr, rb, rt, rw, rh):
    if type(layer) == str :
        layer = Layer(layer)

    dbCreatePolygon(self, layer, PointList([Point(rl-rw, rb-rw), Point(rr+rw, rb-rw), Point(rr+rw, rt+rh), Point(rl-rw, rt+rh), Point(rl-rw, rb),
                                            Point(rl, rb), Point(rl, rt), Point(rr, rt), Point(rr, rb), Point(rl-rw, rb), Point(rl-rw, rb-rw)]))

#**************************************************************************************************************
# ihpGetRectHash
#**************************************************************************************************************
def ihpGetRectHash(g_value) :
    mlist = list()
    mlist.append(g_value)
    mlist.append(10001)
    return mlist

#**************************************************************************************************************
# ihpGetAskewHash
#**************************************************************************************************************
def ihpGetAskewHash(g_value) :
    mlist = list()
    mlist.append(g_value)
    mlist.append(10002)
    return mlist

#**************************************************************************************************************
# ihpGetOptionPair
#**************************************************************************************************************
def ihpGetOptionPair(g_index, g_options) :
    pair = list()
    iterIndex = 0

    for i in range(fix(listlen(g_options))) :
        if iterIndex == g_index :
            if (i+1) < listlen(g_options) :
                pair = pylist(nth(i, g_options), nth(i+1, g_options))
                return pair

        if isOdd(i) :
            iterIndex = iterIndex + 1

    return pair

#**************************************************************************************************************
# ihpIsRectOpt
#**************************************************************************************************************
def ihpIsRectOpt(g_index, g_options) :
    rValue = 0
    if (g_options != 0) and (g_index < listlen(g_options)) :
        testOpt = ihpGetOptionPair(g_index, g_options)
        if listlen(testOpt) == 2 :
            testHash = nth(1, testOpt);
            hashValue = nth(1, ihpGetRectHash(0));

            if testHash == hashValue :
                rValue = 1;



    return rValue;

#**************************************************************************************************************
# ihpIsAskewOpt
#**************************************************************************************************************
def ihpIsAskewOpt(g_index, g_options) :
    rValue = 0
    if (g_options != 0) and (g_index < listlen(g_options)) :
        testOpt = ihpGetOptionPair(g_index, g_options)
        if listlen(testOpt) == 2 :
            testHash = nth(1, testOpt);
            hashValue = nth(1, ihpGetAskewHash(0));

            if testHash == hashValue :
                rValue = 1;



    return rValue;

#**************************************************************************************************************
# ihpGetDrawOptValue
#**************************************************************************************************************
def ihpGetDrawOptValue(g_index, g_drwOptions) :
    rValue = 0

    if g_index < listlen(g_drwOptions) :
        testOpt = ihpGetOptionPair(g_index, g_drwOptions);
        if listlen(testOpt) == 2 :
            rValue = nth(0, testOpt);

    return(rValue);

#**************************************************************************************************************
# ihpGetSideSkewDrawingOptions
#**************************************************************************************************************
def ihpGetSideSkewDrawingOptions(g_value) :
    return pylist(ihpGetAskewHash(g_value),
                  ihpGetRectHash(0), ihpGetRectHash(0),
                  ihpGetAskewHash(g_value));

#**************************************************************************************************************
# ihpGetLeftSkewDrawingOptions
#**************************************************************************************************************
def ihpGetLeftSkewDrawingOptions(g_value) :
    return pylist(ihpGetRectHash(0),
                  ihpGetRectHash(0), ihpGetRectHash(0),
                  ihpGetAskewHash(g_value));

#**************************************************************************************************************
# ihpGetInnerSkewDrawingOptions
#**************************************************************************************************************
def ihpGetInnerSkewDrawingOptions(g_value) :
    return pylist(ihpGetRectHash(0),
                  ihpGetAskewHash(g_value), ihpGetAskewHash(g_value),
                  ihpGetRectHash(0));

#**************************************************************************************************************
# ihpGetNormalizedList
#**************************************************************************************************************
def ihpGetNormalizedList(theList) :
    if type(theList) is PointList :
        return theList

    normalized = list()

    if is_list(theList) :
        for i in range(fix(listlen(theList))) :
            item = nth(i, theList)

            itemList = ihpGetNormalizedList(item)
            for j in range(fix(listlen(itemList))) :
                elem = nth(j, itemList)
                if listlen(normalized) :
                    normalized = cons(normalized, pylist(elem))
                else :
                    normalized = list()
                    normalized.append(elem)


    else :
        if listlen(normalized) :
            normalized = append(normalized, list(theList))
        else :
            normalized = list()
            normalized.append(theList)

    return normalized

#**************************************************************************************************************
# ihpGetShapeBBox
#**************************************************************************************************************
def ihpGetShapeBBox(shapeId) :
    shapeList = ihpGetNormalizedList(shapeId)

    bbox = Box(0, 0, 0, 0)

    if is_list(shapeList) == 0 :
        return bbox

    if listlen(shapeList) == 0 :
        return bbox

    #initialize componetnts first
    currentId = nth(0, shapeList);
    rect = currentId.getBBox()

    x1 = rect.getLeft()
    x2 = rect.getRight()
    y1 = rect.getBottom()
    y2 = rect.getTop()

    # compute min and max Point1(X1, Y1) and Point2(X2, Y2)
    for i in range(fix(listlen(shapeList))) :
        currentId = nth(i, shapeList)

        crect = currentId.getBBox()
        cx1 = crect.getLeft()
        cx2 = crect.getRight()
        cy1 = crect.getBottom()
        cy2 = crect.getTop()

        x1 = min2(x1, cx1)
        y1 = min2(y1, cy1)
        x2 = max2(x2, cx2)
        y2 = max2(y2, cy2)

    return Box(x1, y1, x2, y2)

#***********************************************************************************************************************
# ihpCreatedExtendedShape
#***********************************************************************************************************************
def ihpCreatedExtendedShape(g_cvId, g_layerId, g_shapeId, g_extend = None, g_options = None) :
    options = g_options
    if g_options == None :
        options = list(ihpGetRectHash(0))

    shapeList = ihpGetNormalizedList(g_shapeId)

    theShapes = list();
    for i in range(fix(listlen(shapeList))) :
        shapeId = nth(i, shapeList);
        theShapes = cons(theShapes, pylist(ihpCreateExtendedShapeByPoints(g_cvId, g_layerId, shapeId, g_extend, g_options)));

    return theShapes

#**************************************************************************************************************
# ihpCreateExtendedShapeByPoints
#**************************************************************************************************************
def ihpCreateExtendedShapeByPoints(g_cvId, g_layerId, g_shapeId, g_extend, g_drawOptions) :
    points = PointList()

    bbox = ihpGetShapeBBox(g_shapeId)

    x1 = nth(0, bbox)
    y1 = nth(1, bbox)
    x2 = nth(2, bbox)
    y2 = nth(3, bbox)

    if type(g_extend) is list :
        left = nth(2, g_extend)
        bottom = nth(1, g_extend)
        right = nth(3, g_extend)
        top = nth(0, g_extend)
    if type(g_extend) is Box :
        left = g_extend.getRight()
        bottom = g_extend.getBottom()
        right = g_extend.getTop()
        top = g_extend.getLeft()
    else :
        left = g_extend
        bottom = g_extend
        right = g_extend
        top = g_extend

    # extend the requested shape
    x1 = x1 - left;
    y1 = y1 - bottom;
    x2 = x2 + right;
    y2 = y2 + top;

    optionList = ihpGetNormalizedList(g_drawOptions)

    if ihpIsRectOpt(0, optionList) == 1 and ihpIsRectOpt(1, optionList) == 1 and ihpIsRectOpt(2, optionList) == 1 and ihpIsRectOpt(3, optionList) == 1 :
        points.append(Point(x1, y1))
        points.append(Point(x2, y2))
    else :
        if ihpIsAskewOpt(0, optionList) == 1 :
            points.append(Point(x1 + ihpGetDrawOptValue(0, optionList), y1))
            points.append(Point(x1, y1 + ihpGetDrawOptValue(0, optionList)))
        else :
            points.append(Point(x1, y1))

        if ihpIsAskewOpt(1, optionList) == 1 :
            points.append(Point(x1, y2 - ihpGetDrawOptValue(1, optionList)))
            points.append(Point(x1 + ihpGetDrawOptValue(1, optionList), y2))
        else :
            points.append(Point(x1, y2))

        if ihpIsAskewOpt(2, optionList) == 1 :
            points.append(Point(x2 - ihpGetDrawOptValue(2, optionList), y2))
            points.append(Point(x2, y2 - ihpGetDrawOptValue(2, optionList)))
        else :
            points.append(Point(x2, y2))

        if ihpIsAskewOpt(3, optionList) == 1 :
            points.append(Point(x2, y1 + ihpGetDrawOptValue(3, optionList)))
            points.append(Point(x2 - ihpGetDrawOptValue(3, optionList), y1))
        else :
            points.append(Point(x2, y1));

    return dbCreatePolygon(g_cvId, g_layerId, ihpGetNormalizedList(points))

#**************************************************************************************************************
# ihpSurroundShapeWithRing
#**************************************************************************************************************
def ihpSurroundShapeWithRing(g_cvId, g_layerId, g_shapeId, g_extend, g_ringWidth) :
    left = g_extend
    bottom = g_extend
    right = g_extend
    top = g_extend

    if type(g_extend) is list :
        left = nth(2, g_extend)
        bottom = nth(1, g_extend)
        right = nth(3, g_extend)
        top = nth(0, g_extend)
    if type(g_extend) is Box :
        left = g_extend.getRight()
        bottom = g_extend.getBottom()
        right = g_extend.getTop()
        top = g_extend.getLeft()
    else :
        left = g_extend
        bottom = g_extend
        right = g_extend
        top = g_extend

    shape1 = ihpCreatedExtendedShape(g_cvId, g_layerId, g_shapeId, Box(top, bottom, left, right))
    shape2 = ihpCreatedExtendedShape(g_cvId, g_layerId, g_shapeId, Box(top + g_ringWidth, bottom + g_ringWidth,
                                                                       left + g_ringWidth, right + g_ringWidth))
    hallo = dbLayerXor(g_layerId, car(shape1), car(shape2))

    dbDeleteObject(car(shape1));
    dbDeleteObject(car(shape2));

    return(hallo.getComp(0));

#**************************************************************************************************************
# ihpCreateContactArrayInShape
#**************************************************************************************************************
def ihpCreateContactArrayInShape(g_cvId, g_layer, g_shapeId, g_baseShape, g_size, g_rect, g_drcMinOverlap = None, g_drcMinSpace = None) :

    if g_drcMinOverlap == None :
        g_drcMinOverlap = 0.07

    if g_drcMinSpace == None :
        g_drcMinSpace = 0.18

    if g_baseShape != None :
        bbox = ihpGetShapeBBox(g_baseShape)
        width = abs(nth(0, bbox) - nth(2, bbox))
        height = abs(nth(1, bbox) - nth(3, bbox))

    if type(g_size) is list :
        width = nth(0, g_size)
        height = nth(1, g_size)

    top = g_drcMinOverlap;
    bottom = g_drcMinOverlap;
    left = g_drcMinOverlap;
    right = g_drcMinOverlap;
    xspace = g_drcMinSpace;
    yspace = g_drcMinSpace;

    if type(g_drcMinSpace) is list :
        xspace = car(g_drcMinSpace)
        yspace = cadr(g_drcMinSpace)

    if type(g_drcMinOverlap) is list :
        top = car(g_drcMinOverlap)
        bottom = cadr(g_drcMinOverlap)
        left = caddr(g_drcMinOverlap)
        right = cadddr(g_drcMinOverlap)

    if type(g_shapeId) != list :
        g_shapeId = list(g_shapeId)

    snapGrid = g_cvId.tech.getGridResolution()

    contactList = list()
    for i in range(fix(listlen(g_shapeId))) :
        shape = nth(i, g_shapeId)

        if type(shape) == Polygon :
            continue

        bbox = ihpGetShapeBBox(shape)
        rectWidth = abs(nth(2, bbox) - nth(0, bbox) - left - right)
        rectHeight = abs(nth(3, bbox) - nth(1, bbox) - top - bottom)

        center = pylist((nth(0, bbox) + left + nth(2, bbox) - right)*0.5, (nth(0, bbox) + bottom + nth(3, bbox) - top)*0.5)

        columns = fix((rectWidth+xspace)/(1.0*(width + xspace)))
        rows = fix((rectHeight+yspace)/(1.0*(height + yspace)))

        if columns > 0 and rows > 0 :
            contacts = ihpPerformContactPlacementInShape(g_cvId, g_layer, shape, pylist(columns, rows),
                                                         pylist(width, height, xspace, yspace, left, bottom, center, snapGrid));
            contactList = append(contactList, contacts);

    return contactList

#**************************************************************************************************************
# ihpPerformContactPlacementInShape
#**************************************************************************************************************
def ihpPerformContactPlacementInShape(g_cvId, g_layer, g_shapeId, g_table, g_dimentions) :

    contactList = list()

    if type(g_table) != list or listlen(g_table) != 2 :
        return contactList

    if type(g_dimentions) != list or listlen(g_dimentions) != 7 :
        return contactList

    columns = nth(0, g_table)
    rows = nth(1, g_table)

    width = nth(0, g_dimentions)
    height = nth(1, g_dimentions)
    xspace = nth(2, g_dimentions)
    yspace = nth(3, g_dimentions)
    left = nth(4, g_dimentions)
    bottom = nth(5, g_dimentions)
    center = nth(6, g_dimentions)
    snapGrid = nth(7, g_dimentions)

    bbox = ihpGetShapeBBox(shape);

    xLoc = car(center)-((columns*(width+xspace)-xspace)*0.5);
    xLoc = fix(xLoc/snapGrid)*snapGrid;
    if xLoc < (nth(0, bbox) + left) :
        xLoc = xLoc+snapGrid
        xLoc = fix(xLoc/snapGrid)*snapGrid

    yLoc = cadr(center)-((rows*(height+yspace)-yspace)*0.5)
    yLoc = fix(yLoc/snapGrid)*snapGrid

    if yLoc < (nth(1, bbox) + bottom) :
        yLoc = yLoc+snapGrid
        yLoc = fix(yLoc/snapGrid)*snapGrid

    for i in range(fix(listlen(rows-1))) :
        for j in range(fix(listlen(columns-1))) :
            xOrig = xLoc + (j * (width + xspace))
            xOrig = fix(xOrig / snapGrid)* snapGrid
            yOrig = yLoc + (i * (height + yspace))
            yOrig = fix(yOrig / snapGrid)* snapGrid

            contactId = dbCreateRect(cvid, layer, Box(xOrig, yOrig, (xOrig + width), (yOrig + height)))
            contactList = append(newrects, list(contactId))

    return(contactList)

def ihpSG13Pc_delBipLay(pcCV) :

    layers = pylist("BiWind", "BasPoly", "EmPoly", "ColWind", "DeepCo", "PWell")

    for layerName in layers :
        shapes = pcCV.getShapes()
        for shapeId in shapes :
            if shapeId.layer == Layer(layerName) :
                dbDeleteObject(shapeId)
