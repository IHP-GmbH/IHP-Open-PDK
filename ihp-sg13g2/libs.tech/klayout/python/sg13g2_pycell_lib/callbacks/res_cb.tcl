
#***********************************************************************************************************************
# CbResCalc
#***********************************************************************************************************************
proc CbResCalc {calc r l w b ps cell} {
    
    global SG13_LIBRARY
    global SG13_EPSILON
    global SG13_TECHNOLOGY
    
    set suffix ""
    if {$SG13_TECHNOLOGY == "SG13G2"} {
        set suffix "G2"
    }
    if {$SG13_TECHNOLOGY == "SG13D7"} {
        set suffix "D7"
    }
    
    set rspec  [Stof [techGetParam ${cell}_rspec ]]                       ;# specific body res. per sq. (float)
    set rkspec [Stof [techGetParam ${cell}_rkspec]]                       ;# res. per single contact (float)
    set rzspec [expr {[Stof [techGetParam ${cell}_rzspec]] * 1.0e6}]      ;# transition res. per um width between contact area and body (float)
    set lwd    [expr {[Stof [techGetParam ${cell}_lwd   ]] * 1.0e6}]      ;# line width delta [um] (both edges, positiv value adds to w)
    set kappa  [Stof [techGetParam ${cell}_kappa ]]
    
    set poly_over_cont [Stof [techGetParam "Cnt_d" ]]
    set cont_size      [Stof [techGetParam "Cnt_a"]]
    set cont_space     [Stof [techGetParam "Cnt_b"]]
    set cont_dist      [expr {$cont_space+$cont_size}]
    
    set minW  [Stof [techGetParam ${cell}_minW]]

    set r  [Stof $r ]
    set l  [Stof $l ]
    set w  [Stof $w ]
    set b  [Stof $b ]
    set ps [Stof $ps]

    if {[Less $w $minW 1u} {
         set w $minW ;# avoid divide by zero errors in case of problems
    }
     
    set w  [expr {$w  * 1.0e6}] ;# um (needed for contact calculation)
    set l  [expr {$l  * 1.0e6}]
    set ps [expr {$ps * 1.0e6}]
    
    set result 0
    switch $calc {
        R {
            set weff [expr {$w+$lwd}]
            set result [expr {$l/$weff*($b+1)*$rspec + (2.0/$kappa*$weff+$ps)*$b/$weff*$rspec + 2.0/$w*$rzspec}]
        }
        l {
            set weff [expr {w+lwd}]
            set result [expr {($weff*$r - $b*(2.0/$kappa*$weff+$ps)*$rspec - 2.0*$weff/$w*$rzspec )/($rspec*($b+1))*1e-6}] ;# in [um]
        }
        w {
            set tmp    [expr {$r-2*$b*$rspec/$kappa}]
            set p      [expr {($r*$lwd-$l*($b+1)*$rspec-(2*$lwd/$kappa+$ps)*$b*$rspec-2*$rzspec)/$tmp}]
            set q      [expr {-2*$lwd*$rzspec/$tmp}]
            set w      [expr {-$p/2+sqrt($p*$p/4-$q}]
            set result [expr {[Snap $w] * 1.0e-6}] ;# -> [m]
        }
    }
    
    return $result
}

#******************************************************************************************************
# calculate max. current through resistor

proc CbResCurrent {w cell} { ;# w must be float in [m], i is given as a string

    global SG13_LIBRARY
    global SG13_EPSILON
    
    set ikspec [Stof [techGetParam  ${cell}_ikspec]]
    set ipspec [Stof [techGetParam  ${cell}_ipspec]]

    set poly_over_cont [techGetParam  "Cnt_d"]   
    set cont_size      [techGetParam  "Cnt_a"] 
    set cont_space     [techGetParam  "Cnt_b"] 
    set cont_dist      [expr $cont_space+$cont_size]

    set ncont [expr int( ($w*1.0e6-2.0*$poly_over_cont+$cont_space+$SG13_EPSILON)/$cont_dist )] ;# max. nr. of contacts across resistor width
    if {$ncont < 1} {
        set ncont 1
    }

    set ilim_cont [expr $ikspec*$ncont]
    set ilim_poly [expr $w*$ipspec]

    set ilim $ilim_poly
    
    return [format "%1.2gm" [expr $ilim*1000]]
}

#******************************************************************************************************
# res callback function, used in CDF forms and in automated parameter update
# returns RC value. t = success, nil=failed, CbMsg may hold info text
#******************************************************************************************************

proc CbRes {param} {
    
    global SG13_EPSILON2
    global SG13_GRID
    
    set RC 1
    
    set cellId [iPDK_getCurrentInst]
    set cell   [iPDK_getInstCellName $cellId] 
    
    set minL   [Stof [techGetParam  ${cell}_minL]]
    set minW  0.0
    set minPS 0.0
    set minW  [Stof [techGetParam  ${cell}_minW]]
    set minPS [Stof [techGetParam  ${cell}_minPS]]

    set minB  [expr int([techGetParam  ${cell}_minB])]
    set maxL  [Stof [techGetParam  ${cell}_maxL]]
    set maxW  [Stof [techGetParam  ${cell}_maxW]]
    set maxPS [Stof [techGetParam  ${cell}_maxPS]]
    set maxB  [expr int([techGetParam  ${cell}_maxB])]
    set minR  [CbResCalc R 0.0 $minL $maxW $minB $maxPS $cell]
    set maxR  [CbResCalc R 0.0 $maxL $minW $maxB $maxPS $cell]

    set r  [IsNumberString [iPDK_getParamValue R  $cellId]]
    set w  [IsNumberString [iPDK_getParamValue w  $cellId]]
    set l  [IsNumberString [iPDK_getParamValue l  $cellId]]
    set ps [IsNumberString [iPDK_getParamValue ps $cellId]]
    set b  [expr int([IsNumberString [iPDK_getParamValue b  $cellId]])]
    
    set rold  $r
    set wold  $w
    set lold  $l
    set bold  $b
    set psold $ps
    
    # check the entered parameters
    switch $param {
        R {
            if {$r != 0} {
                if {$r < [expr [CbResCalc "R" $r $minL $maxW $minB $minPS $cell]-$SG13_EPSILON2]} {
                    CbMessage "r too small"
                    set r [CbResCalc "R" $r $minL $w $b $ps $cell]
                }
                if { $r > [expr [CbResCalc "R" $r $maxL $minW $maxB $maxPS $cell] + $SG13_EPSILON2]} {
                    set r [CbResCalc "R" $r $maxL $maxW $b $ps $cell]
                    CbMessage "r too large, changed to r = $r"
               }
               iPDK_setParamValue R [Ftos $r 3] $cellId
            } else {
                CbMessage "INFO: R contains an expression and/or design variable. Parameter check not executed!"
            } 
        }
        l {
            if {$l != 0} {
                set l [CbRoundm $l $SG13_GRID]
                if { [Less $l $minL 1u]} {
                    CbMessage "l too small"
                    set l $minL
                }

                if {[Greater $l $maxL 1u]} {
                    CbMessage "l too large"}
                    set l $maxL
                }
                iPDK_setParamValue l [Ftos $l 3] $cellId
            } else {
                CbMessage "INFO: l contains an expression and/or design variable. Parameter check not executed!\n"
        }
        w {
            if {$w != 0} {
                set w [CbRoundm $w $SG13_GRID]
                if {[Less $w $minW 1u]} {
                    CbMessage "w too small"
                    set $w $minW
               }
               if {[Greater $w $maxW 1u]} {
                   CbMessage "w too large"
                   set w $maxW
               }
               iPDK_setParamValue w [Ftos $w 3] $cellId
            } else {
                CbMessage "INFO: w contains an expression and/or design variable. Parameter check not executed!\n"
            }
        }
        ps {
            if {$ps != 0} {
               set ps [CbRoundm $ps $SG13_GRID]
               if {[Less $ps $minPS 1u]} {
                   CbMessage "ps too small"
                   set $ps $minPS
               }
               if {[Greater $ps $maxPS 1u]} {
                   CbMessage "ps too large"
                   set ps $maxPS
               }
               iPDK_setParamValue ps [Ftos $ps 3] $cellId
           } else {
               CbMessage "INFO: ps contains an expression and/or design variable. Parameter check not executed!\n"
           }
        }
        b {
            if {$b != 0} {
                if {[Less $b $minB 1]} {
                    CbMessage "b too small"
                    set b $minB
                }
                if {[Greater $b $maxB 1]} {
                    CbMessage "b too large"
                    set b $maxB
                }
                iPDK_setParamValue b $b $cellId
            } else {
                CbMessage "INFO: b contains an expression and/or design variable. Parameter check not executed!\n"
            }
        }
    } ; # end switch
    
    set calc [iPDK_getParamValue Calculate $cellId]
    
    #puts $r
    #puts $w
    #puts $l
    #puts $ps
    #puts $b
    
    if {$r!=0 && $w!=0 && $l!=0 && $ps!=0 && $b!=0} {
        # now recalculate other params
        switch $calc {
            R {
                if { $w != 0 && $l != 0 } {
                    set r [CbResCalc R $r $l $w $b $ps $cell]
                    iPDK_setParamValue R [Ftos $r 3] $cellId
                }
            }
            w {
                if { $l!=0 && $r!=0} {
                    set w [CbResCalc w $r $l $w $b $ps $cell]
                    if {[Less $w $minW 1e-6]} {
                        set w $minW
                    }
                    set w [CbRoundm $w $SG13_GRID]
                    iPDK_setParamValue w [Ftos $w 3] $cellId
                }
            }
            l {
                if {$w!=0 && $r!=0} {
                    set l [CbResCalc l $r $l $w $b $ps $cell]
                    set l [CbRoundm $l $SG13_GRID]
                    iPDK_setParamValue l [Ftos $l 3] $cellId
                }
            }
        }
        
        # recalculate r value (may have changed due to grid rounding)
        
        set r [CbResCalc R 0 $l $w $b $ps $cell]
        
        #check for error condition, restore old data in that case
        if {[Less $l $minL 1e-6] || [Greater $l $maxL 1e-6] || [Less $w $minW 1e-6] || [Greater $w $maxW 1e-6] || [Less $ps $minPS 1e-6] || [Greater $ps $maxPS 1e-6] || [Less $b $minB 1] || [Greater $b $maxB 1] || [Less $r $minR 1] || [Greater $r $maxR 1]} {
            if {[Less $l $minL 1e-6] || [Greater $l $maxL 1e-6]} {
                CbMessage [format "%s < l = %s < %s" $minL $l $maxL]
            }
            if {[Less $w $minW 1e-6] || [Greater $w $maxW 1e-6]} {
                CbMessage [format "%s < w = %s < %s" $minW $w $maxW]
            }
            if {[Less $ps $minPS 1e-6] || [Greater $ps $maxPS 1e-6]} {
                CbMessage [format "%s < ps = %s < %s" $minPS $ps $maxPS]
            }
            if {[Less $b $minB 1] || [Greater $b $maxB 1]} {
                CbMessage [format "%s < b = %s < %s" $minB $b $maxB]
            }
            if {[Less $r $minR 1] || [Greater $r $maxR 1]} {
                CbMessage [format "%s < r = %s < %s" $minR $r $maxR]
            }

            set RC 0
            CbMessage "parameter value out of range - restoring last value"

            # Note: bold and b are equal because call comes too late. Need to store backup values in CbResInit
            if {$l > $maxL && $b==$bold} {
                set r $rold
                set l $lold
                set w $wold
                set ps $psold
                set bold 0
            }
            if {$w < 0 && $b==$bold} {
                set r $rold
                set l $lold
                set w $wold
                set ps $psold
                set bold 0
            }
            if {$l < $minL && $param=="b"} {
                CbMessage "uups! I apologize, you found a bug! Can't restore b - will set it to 0"
                set r $rold
                set l $lold
                set w $wold 
                set ps $psold
                set b 0
                if {[Less $r $minR 1]} {
                    set r $minR
                }
                if {[Greater $r $maxR 1]} {
                    set r $maxR
                }
                if {[Less $l $minL 1e-6]} {
                    set l $minL
                }
                if {[Greater $l $maxL 1e-6]} {
                    set l $maxL
                }
                if {[Less $w $minW 1e-6]} {
                    set w $minW
                }
                if {[Greater $w $maxW 1e-6]} {
                    set w $maxW
                }
                if {[Less $ps $minPS 1e-6]} {
                    set ps $minPS
                }
                if {[Greater $ps $maxPS 1e-6]} {
                    set ps $maxPS
                }
                if {[Less $b $minB 1]} {
                    set b $minB
                }
                if {[Greater $b $maxB 1]} {
                    set b $maxB
                }
            } else {
                set r $rold
                set l $lold
                set w $wold 
                set ps $psold
                set b $bold
                if {[Less $r $minR 1]} {
                    set r $minR
                }
                if {[Greater $r $maxR 1]} {
                    set r $maxR
                }
                if {[Less $l $minL 1e-6]} {
                    set l $minL
                }
                if {[Greater $l $maxL 1e-6]} {
                    set l $maxL
                }
                if {[Less $w $minW 1e-6]} {
                    set w $minW
                }
                if {[Greater $w $maxW 1e-6]} {
                    set w $maxW
                }
                if {[Less $ps $minPS 1e-6]} {
                    set ps $minPS
                }
                if {[Greater $ps $maxPS 1e-6]} {
                    set ps $maxPS
                }
                if {[Less $b $minB 1]} {
                    set b $minB
                }
                if {[Greater $b $maxB 1]} {
                    set b $maxB
                }
            }
            
            switch $param {
                R {
                    if { $wold!=0 && $lold!=0} {
                        if {[Less $l $minL 1e-6]} {
                            set l $minL
                        }
                        if {[Greater $l $maxL 1e-6]} {
                            set l $maxL
                        }
                        if {[Less $w $minW 1e-6]} {
                            set w $minW
                        }
                        if {[Greater $w $maxW 1e-6]} {
                            set w $maxW
                        }
                        if {[Less $ps $minPS 1e-6]} {
                            set ps $minPS
                        }
                        if {[Greater $ps $maxPS 1e-6]} {
                            set ps $maxPS
                        }
                        if {[Less $b $minB 1]} {
                            set b $minB
                        }
                        if {[Greater $b $maxB 1]} {
                            set b $maxB
                        }
                        set r [CbResCalc R $r $l $w $b $ps $cell]
                    }
                 }

               w {
                   if { $lold!=0 && $rold!=0} {
                       if {[Less $r $minR 1]} {
                            set r $minR
                        }
                        if {[Greater $r $maxR 1]} {
                            set r $maxR
                        }
                        if {[Less $l $minL 1e-6]} {
                            set l $minL
                        }
                        if {[Greater $l $maxL 1e-6]} {
                            set l $maxL
                        }
                        if {[Less $ps $minPS 1e-6]} {
                            set ps $minPS
                        }
                        if {[Greater $ps $maxPS 1e-6]} {
                            set ps $maxPS
                        }
                        if {[Less $b $minB 1]} {
                            set b $minB
                        }
                        if {[Greater $b $maxB 1]} {
                            set b $maxB
                        }
                        set w [CbResCalc w $r $l $w $b $ps $cell]
                        set w [CbRoundm $w $SG13_GRID]
                    }
                }

               l {
                   if { $wold!=0 && $rold!=0} {
                       if {[Less $r $minR 1]} {
                            set r $minR
                        }
                        if {[Greater $r $maxR 1]} {
                            set r $maxR
                        }
                        if {[Less $l $minL 1e-6]} {
                            set l $minL
                        }
                        if {[Greater $l $maxL 1e-6]} {
                            set l $maxL
                        }
                        if {[Less $w $minW 1e-6]} {
                            set w $minW
                        }
                        if {[Greater $w $maxW 1e-6]} {
                            set w $maxW
                        }
                        if {[Less $ps $minPS 1e-6]} {
                            set ps $minPS
                        }
                        if {[Greater $ps $maxPS 1e-6]} {
                            set ps $maxPS
                        }
                        if {[Less $b $minB 1]} {
                            set b $minB
                        }
                        if {[Greater $b $maxB 1]} {
                            set b $maxB
                        }
                        set l [CbResCalc l $r $l $w $b $ps $cell]
                        set l [CbRoundm $l $SG13_GRID]
                    }
                }
            }
        }
        
        #puts $r
        #puts $w
        #puts $l
        #puts $ps
        #puts $b
        
        #update component CDF:
        iPDK_setParamValue R  [Ftos $r  3] $cellId
        iPDK_setParamValue w  [Ftos $w  3] $cellId
        iPDK_setParamValue l  [Ftos $l  3] $cellId
        iPDK_setParamValue ps [Ftos $ps 3] $cellId
        iPDK_setParamValue b $b $cellId
        iPDK_setParamValue Imax [CbResCurrent $w $cell] $cellId ;# give the user a feedback for the maximum device current 
    } else {
        CbMessage "INFO: Callback function not completely executed due to an expression/variable in the parameters!"
    } 
    
    return $RC
}
