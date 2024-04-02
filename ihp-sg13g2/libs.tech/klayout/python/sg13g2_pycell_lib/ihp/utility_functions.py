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

import math
from io import StringIO

from cni.dlo import Tech, Numeric
from cni.dlo import Orientation, Location, Layer

nil = 0

tech         = Tech.get('SG13_dev')
techparams   = tech.getTechParams()

SG13_TECHNOLOGY = tech.name()

SG13_EPSILON = techparams['epsilon1']   # for rounding purposes
SG13_GRID    = tech.getGridResolution()
if  SG13_GRID == 0.0 :
    SG13_GRID = techparams['grid']
SG13_IGRID   = 1.0/SG13_GRID            # inverse grid

#***********************************************************************************************************************
# LeQp2
#***********************************************************************************************************************
def LeQp2(a, b, eps):

    if type(a) == str :
        a = eng_string_to_float(a)
    if type(b) == str :
        b = eng_string_to_float(b)

    return a <= b*(1-eps)

#***********************************************************************************************************************
# LeQp3
#***********************************************************************************************************************
def LeQp3(a, b, c, eps):

    if type(a) == str :
        a = eng_string_to_float(a)
    if type(b) == str :
        b = eng_string_to_float(b)
    if type(c) == str :
        c = eng_string_to_float(c)
    
    return a <= b-c*eps

#***********************************************************************************************************************
# fix
#***********************************************************************************************************************
def fix(value):
    if type(value) == float:
        return int(math.floor(value))
    else :
        return value

#***********************************************************************************************************************
# floor
#***********************************************************************************************************************
def floor(value):
    return int(math.floor(value))

#***********************************************************************************************************************
# car
#***********************************************************************************************************************
def car(value):
    return value[0]

#***********************************************************************************************************************
# cdr
#***********************************************************************************************************************
def cdr(value):
    return value[1:]

#***********************************************************************************************************************
# caar
#***********************************************************************************************************************
def caar(value):
    lw = value.lowerLeft()
    x1 = lw.getX();
    return x1

#***********************************************************************************************************************
# cadar
#***********************************************************************************************************************
def cadar(value):
    lw = value.lowerLeft()
    y1 = lw.getY();
    return y1

#***********************************************************************************************************************
# caadr
#***********************************************************************************************************************
def caadr(value):
    ur = value.upperRight()
    x2 = ur.getX()
    return x2

#***********************************************************************************************************************
# cadadr
#***********************************************************************************************************************
def cadadr(value):
    ur = value.upperRight()
    y2 = ur.getY()
    return y2

#***********************************************************************************************************************
# cons
#***********************************************************************************************************************
def cons(mlist, value):
    if type(mlist) != list and type(value) is list :
        value.append(mlist)
        return value

    if type(value) is list :
        mlist = value + mlist
    else :
        mlist.insert(0, value)

    return mlist

#***********************************************************************************************************************
# oddp
#***********************************************************************************************************************
def oddp(value):
    return bool(value & 1)

#***********************************************************************************************************************
# evenp
#***********************************************************************************************************************
def evenp(value):
    return not (bool(value & 1))

#***********************************************************************************************************************
# onep
#***********************************************************************************************************************
def onep(value):
    if value == 1:
        return 1
    else :
        return 0

#***********************************************************************************************************************
# zerop
#***********************************************************************************************************************
def zerop(value):
    if value == 0:
        return 1
    else :
        return 0

#***********************************************************************************************************************
# sprintf
#***********************************************************************************************************************
def sprintf(fmt, *args):
    buf = StringIO.StringIO()
    buf.write(fmt % args)
    return buf.getvalue()

#***********************************************************************************************************************
# strcat
#***********************************************************************************************************************
def strcat(*args):
    lst=[]
    for arg in args:
        lst.append(arg)
    return ' '.join(lst)

#***********************************************************************************************************************
# eng_string
#***********************************************************************************************************************
def eng_string( x, sig_figs=3, si=True):
    """
    Returns float/int value <x> formatted in a simplified engineering format -
    using an exponent that is a multiple of 3.

    sig_figs: number of significant figures

    si: if true, use SI suffix for exponent, e.g. k instead of e3, n instead of
    e-9 etc.
    """
    x = float(x)
    sign = ''
    if x < 0:
        x = -x
        sign = '-'
    if x == 0:
        exp = 0
        exp3 = 0
        x3 = 0
    else:
        exp = int(math.floor(math.log10( x )))
        exp3 = exp - ( exp % 3)
        x3 = x / ( 10 ** exp3)
        x3 = round( x3, -int( math.floor(math.log10( x3 )) - (sig_figs-1)) )
        if x3 == int(x3): # prevent from displaying .0
            x3 = int(x3)

    if si and exp3 >= -24 and exp3 <= 24 and exp3 != 0:
        exp3_text = 'yzafpnum kMGTPEZY'[ exp3 // 3 + 8]
    elif exp3 == 0:
        exp3_text = ''
    else:
        exp3_text = 'e%s' % exp3

    return ( '%s%s%s') % ( sign, x3, exp3_text)

#***********************************************************************************************************************
# eng_string_to_float
#***********************************************************************************************************************
def eng_string_to_float(x):
    """
    Returns float/int value from formatted simplified engineering format
    <x>

    si: if true, use SI suffix for exponent, e.g. k instead of e3, n instead of
    e-9 etc.
    """

    eng = x[-1:]
    exp = -1

    for i in 'yzafpnum kMGTPEZY':
        exp += 1
        if i is eng:
            break

    exp = (exp - 8) * 3

    try:
        int(eng)
        return eval(x)
    except:
        pass

    number_string = x[:-1]
    number = 0

    try:
        number = float(number_string)
    except:
        raise ValueError

    return number * (10**exp)

#***********************************************************************************************************************
# GridFix
#***********************************************************************************************************************
def GridFix(x):
    return fix(x*SG13_IGRID+SG13_EPSILON)*SG13_GRID         # always use "nice" numbers, as 1/grid may be irrational

#***********************************************************************************************************************
# LayerGridFix
#***********************************************************************************************************************
def LayerGridFix(layerId, value):
    if type(layerId) == str :
        layerId = Layer(layerId)

    # take grid for used layer from tf
    grid = layerId.getGridResolution()
    # to avoid error if grid for used layer was not found
    if  grid == 0 :
        grid = SG13_GRID

    igrid = 1.0/grid    # inverse grid
    fix(value*igrid+SG13_EPSILON)*grid # always use "nice" numbers, as 1/grid may be irrational

    return value

def tog(x):
    return GridFix(x);

def Snap(x):
    return GridFix(x);

def nonzero (x):
    return (abs(x)>=1e-10)

def iszero (x):
    return (abs(x)<1e-10)

#***********************************************************************************************************************
# hiGetAttention - rings the bell in the keyboard or terminal
#***********************************************************************************************************************
def hiGetAttention():
    print('\a')

#***********************************************************************************************************************
# strToOrient
#***********************************************************************************************************************
def strToOrient(value):
    if value == 'R0' :
        return Orientation.R0

    if value == 'R90' :
        return Orientation.R90

    if value == 'R180' :
        return Orientation.R180

    if value == 'R270' :
        return Orientation.R270

    if value == 'MY' :
        return Orientation.MY

    if value == 'MYR90' :
        return Orientation.MYR90

    if value == 'MX' :
        return Orientation.MX

    if value == 'MXR90' :
        return Orientation.MXR90

#***********************************************************************************************************************
# strToAlignt
#***********************************************************************************************************************
def strToAlignt(value):
    if value == 'lowerLeft' :
        return Location.LOWER_LEFT

    if value == 'centerLeft' :
        return Location.CENTER_LEFT

    if value == 'uperLeft' :
        return Location.UPPER_LEFT

    if value == 'lowerCenter' :
        return Location.LOWER_CENTER

    if value == 'centerCenter' :
        return Location.CENTER_CENTER

    if value == 'upperCenter' :
        return Location.UPPER_CENTER

    if value == 'lowerCenter' :
        return Location.LOWER_CENTER

    if value == 'centerRight' :
        return Location.CENTER_RIGHT

    if value == 'upperRight' :
        return Location.UPPER_RIGHT

#***********************************************************************************************************************
# strToBool
#***********************************************************************************************************************
def strToBool(val):
    if val == 'nil' :
        return False
    elif val.upper() == 'FALSE' :
        return False
    elif val.upper() == 'NO' :
        return False
    elif val == '0' :
        return False
    elif val == '' :
        return False

    return True

#***********************************************************************************************************************
# checkForYes
#***********************************************************************************************************************
def checkForYes(value):
    if type(value) == str :
        val = value.lower()
        if val == 't' or val == '1' or val == 'yes' or val == 'y' :
            return True
        else :
            return False
    else :
        if type(value) == bool :
            return value
        else :
            return value != 0

#****************************************************************************************************
# inductor_minD
#****************************************************************************************************
def inductor_minD(w, s, nr, grid):
    sqrt2 = math.sqrt(2)
    dmin = 0

    if nr == 1 :
         dmin = GridFix((s+w+w)*(1+sqrt2)/2+grid*2)*2
    elif nr == 2 :
         dmin = GridFix((GridFix(w/sqrt2+s/2)+GridFix(s*0.4143)+0.02+w)*2*(1+sqrt2)+0.01)
    elif  nr > 2 :
        dmin = GridFix(((GridFix(w/sqrt2+s/2)+GridFix(s*0.4143))*2+2*s+4*w)*(1+sqrt2))

    return dmin

#***********************************************************************************************************************
# resCalc - used for rsil, rhigh, rpnd, rppd
#***********************************************************************************************************************
def resCalc(self, cell):

    global techparams

    lwd    = Numeric(techparams[cell+'_lwd'])
    rspec  = Numeric(techparams[cell+'_rspec'])
    rzspec = Numeric(techparams[cell+'_rzspec'])
    kappa  = Numeric(techparams[cell+'_kappa'])

    weff = self.w+lwd
    r = self.l/weff*(self.b+1)*rspec + (2.0/kappa*weff+self.ps)*self.b/weff*rspec + 2.0/self.w*rzspec

    return round(r*1e03)/1e03

#****************************************************************************************************
# CbResCalc
#****************************************************************************************************
def CbResCalc(calc, r, l, w, b, ps, cell):

    global techparams
    global SG13_TECHNOLOGY

    suffix = 'G2'
    
    rspec  = Numeric(techparams[cell+suffix+'_rspec']) # specific body res. per sq. (float)
    rkspec = Numeric(techparams[cell+'_rkspec']) # res. per single contact (float)
    rzspec = Numeric(techparams[cell+'_rzspec']) * 1e6 # transition res. per um width between contact area and body (float)
    lwd    = Numeric(techparams[cell+suffix+'_lwd']) * 1e6  # line width delta [um] (both edges, positiv value adds to w)
    kappa  = Numeric(techparams[cell+'_kappa'])
    poly_over_cont = techparams['Cnt_d'] # strcat(cell '_poly_over_cont'))
    cont_size = techparams['Cnt_a'] # techGetSpacingRule(tfId 'minWidth' 'Cont')     # size of contact array [um]
    cont_space = techparams['Cnt_b'] # techGetSpacingRule(tfId 'minSpacing' 'Cont')
    cont_dist = cont_space+cont_size
    minW = Numeric(techparams[cell+'_minW'])

    # must check for string arguments and convert to float
    if type(r) == str :
        r=Numeric(r)
    if type(l) == str :
        l=Numeric(l)
    if type(w) == str :
        w=Numeric(w)
    if type(b) == str :
        b=Numeric(b)
    if type(ps) == str :
        ps=Numeric(ps)

    if LeQp3(w, minW, '1u', techparams['epsilon1']) :  # 6.8.03 GG: wmin -> minW,HS: Function'LeQp' 28.9.2004
        w = minW    # avoid divide by zero errors in case of problems ; 21.7.03 GG: eps -> minW
    
    w = w * 1e6 # um (needed for contact calculation);HS 4.10.2004
    l = l * 1e6
    ps = ps * 1e6

    # here: all dimensions given in [um]!
    result = 0

    if calc == 'R' :
        weff = w+lwd
        #result = l/weff*(b+1)*rspec+(2.0/kappa*weff+ps)*b/weff*rspec+2.0/weff*rzspec+2.0*(rkspec/ncont)
        result = l/weff*(b+1)*rspec+(2.0/kappa*weff+ps)*b/weff*rspec+2.0/w*rzspec
    elif calc == 'l' :
        weff = w+lwd
        #result = (weff*(r-2.0*rkspec/ncont)-b*(2.0/kappa*weff+ps)*rspec-2.0*rzspec)/(rspec*(b+1))*1.0e-6 ; in [m]
        result = (weff*r-b*(2.0/kappa*weff+ps)*rspec-2.0*weff/w*rzspec)/(rspec*(b+1))*1.0e-6 # in [m]
    elif calc == 'w' :
        tmp = r-2*b*rspec/kappa
        p = (r*lwd-l*(b+1)*rspec-(2*lwd/kappa+ps)*b*rspec-2*rzspec)/tmp
        q = -2*lwd*rzspec/tmp
        w = -p/2+sqrt(p*p/4-q)
        result = Snap(w)*1e-6 #  -> [m]

    return result

#***********************************************************************************************************************
# CbResCurrent
#***********************************************************************************************************************
def CbResCurrent(w, eps, cell) : # w must be float in [m], i is given as a string

    global techparams

    ikspec = Numeric(techparams[cell+'_ikspec'])
    ipspec = Numeric(techparams[cell+'_ipspec'])
    poly_over_cont = techparams['Cnt_d']
    cont_size  = techparams['Cnt_a']
    cont_space = techparams['Cnt_b']
    cont_dist = cont_space+cont_size

    ncont = fix( (w*1.0e6-2.0*poly_over_cont+cont_space+eps)/cont_dist ) # max. nr. of contacts across resistor width
    if ncont < 1 :
        ncont = 1

    ilim_cont = ikspec*ncont
    ilim_poly = w*ipspec

    ilim = ilim_poly
    return str(ilim*1000)+'m'

#***********************************************************************************************************************
# CbCapCalc
#***********************************************************************************************************************
def CbCapCalc(calc, c, l, w, cell) :

    global techparams

    caspec = Numeric(techparams[cell+'_caspec'])*1e-12 # specific cap per sq. [um] (float)
    cpspec = Numeric(techparams[cell+'_cpspec'])*1e-6  # specific cap. per [um] perimeter (float)
    lwd    = Numeric(techparams[cell+'_lwd'])          # line width delta [m] ; 30.7.05 GG: fixed

    if type(c) == str :
        c = Numeric(c)
    if type(l) == str :
        l = Numeric(l)
    if type(w) == str :
        w = Numeric(w)

    w = w * 1e6 # um (needed for contact calculation)
    l = l * 1e6
    lwd = lwd * 1e6

    result = 0
    if calc == 'C' :
        leff = l+lwd
        weff = w+lwd
        result = leff*weff*caspec + 2.0*(leff+weff)*cpspec
    elif calc == 'l' :
        weff = w+lwd
        result = ((c-2.0*weff*cpspec)/(caspec*weff+2.0*cpspec) - lwd) * 1.0e-6
    elif calc == 'w' :
        leff = l+lwd
        result = ((c-2.0*leff*cpspec)/(caspec*leff+2.0*cpspec) - lwd) * 1.0e-6
    elif calc == 'lw' :
        result = ( -2.0*cpspec/caspec + sqrt(4.0*cpspec*cpspec/(caspec*caspec) + c/caspec) - lwd) * 1.0e-6

    return result

#***********************************************************************************************************************
# CbTapCalc
#***********************************************************************************************************************
def CbTapCalc(calc, r, l, w, cell) :

    global techparams

    raspec = Numeric(techparams[cell+'_raspec'])*1.0e12 ;# specific res per sq. [um] (float)
    rpspec = Numeric(techparams[cell+'_rpspec'])*1.0e6  ;# specific res. per [um] perimeter (float)

    w = w*1.0e6 ;# um (needed for contact calculation)
    l = l*1.0e6
    a = l*w
    p = 2.0*(l+w)

    result = 0
    if calc == 'R' :
        result = 1.0/(1.0/(raspec/a) + 1.0/(rpspec/p))
    elif calc == 'l' :
        result = (raspec*rpspec- r*raspec*2.0*w)/(r*raspec*2.0+r*rpspec*w)*1.0e-6
    elif calc == 'w' :
        result = (raspec*rpspec- r*raspec*2.0*l)/(r*raspec*2.0+r*rpspec*l)*1.0e-6
    elif calc == 'wl' :
        result = ((-4.0*r*raspec + sqrt(16.0*r*r*raspec*raspec + 4.0*r*rpspec*rpspec*raspec))/(2.0*r*rpspec))*1.0e-6

    return result

#***********************************************************************************************************************
# CbDiodeCalc
#***********************************************************************************************************************
def CbDiodeCalc(calc, a, l, w, cell) :

    global techparams

    minL = Numeric(techparams[cell+'_minL'])
    minW = Numeric(techparams[cell+'_minW'])

    if calc != 'w' and calc != 'wl' :
        if w < minW :
            print("w {0} too small\n".format(w))
    if calc != 'l' and calc != 'wl' :
        if l < minL :
            print("l {0} too small\n".format(l))

    if type(a) == str :
        a = Numeric(a)
    if type(l) == str :
        l = Numeric(l)
    if type(w) == str :
        w = Numeric(w)

    w = w*1.0e6 # um (needed for contact calculation)
    l = l*1.0e6

    result = 0
    if calc == 'a' :
        result = w*l*1.0e-12
    elif calc == 'p' :
        result = (w+l)*2.0e-6
    elif calc == 'l' :
        result = (a/w)*1.0e6
    elif calc == 'w' :
        result = (a/l)*1.0e6
    elif calc == 'wl' :
        result = sqrt(a)

    return result

def listlen(mlist) :
    return len(mlist)

def isOdd(x) :
    if x == 0 :
        return 0

    if (x % 2) != 0 :
        return 1

    return 0

def isEven(x) :
    if x == 0 :
        return 1

    if (x % 2) == 0 :
        return 1

    return 0

def is_list(x) :
    if type (x) is list :
        return 1

    return 0

def min2(a, b) :
    return min(a, b)

def max2(a, b) :
    return max(a, b)

def pylist(*args) :
    mlist = list()

    for key in args :
        mlist.append(key)

    return mlist
