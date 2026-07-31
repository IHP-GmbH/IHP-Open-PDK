global env
global SG13_LIBRARY
set    SG13_LIBRARY SG13_dev
global SG13_TECHNOLOGY
set    SG13_TECHNOLOGY SG13G2
global IHP_iPDK_CbMsg
set    IHP_iPDK_CbMsg ""

global TechParams
dict set TechParams "" ""

puts "Technology $SG13_LIBRARY is loaded."

global SG13_GRID
set    SG13_GRID [techGetParam grid]

if {$SG13_GRID == ""} {
    set SG13_GRID 0.01
}
puts  "GRID : $SG13_GRID"

global SG13_IGRID
set    SG13_IGRID [expr {1.0/$SG13_GRID}] ;# inverse grid
puts  "GRID inverse : $SG13_IGRID"

global SG13_EPSILON
global SG13_EPSILON2

set    SG13_EPSILON  [techGetParam epsilon1]
if {$SG13_EPSILON == ""} {
    set SG13_EPSILON 0.001
}
set    SG13_EPSILON2 [techGetParam epsilon2]
if {$SG13_EPSILON2 == ""} {
    set SG13_EPSILON2 1e-9
}

puts "EPSILON1  : $SG13_EPSILON"
puts "EPSILON2  : $SG13_EPSILON2"

puts "Success."

