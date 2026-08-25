/*$Id: s__out.cc 2016/09/22 $ -*- C++ -*-
 * Copyright (C) 2001 Albert Davis
 * Author: Albert Davis <aldavis@gnu.org>
 *
 * This file is part of "Gnucap", the Gnu Circuit Analysis Package
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
 * 02110-1301, USA.
 *------------------------------------------------------------------
 * tr,dc analysis output functions (and some ac)
 */
//testing=obsolete,script 2005.09.17
#include "u_sim_data.h"
#include "u_status.h"
#include "m_wave.h"
#include "u_prblst.h"
#include "declare.h"	/* plottr, plopen */
#include "s__.h"
/*--------------------------------------------------------------------------*/
/* SIM::____list: access probe lists
 */
const PROBELIST& SIM::alarmlist()const
{
  return _probe_lists->alarm[_sim->_mode];
}
const PROBELIST& SIM::plotlist()const
{
  return _probe_lists->plot[_sim->_mode];
}
const PROBELIST& SIM::printlist()const
{
  return _probe_lists->print[_sim->_mode];
}
const PROBELIST& SIM::storelist()const
{
  return _probe_lists->store[_sim->_mode];
}
/*--------------------------------------------------------------------------*/
/* SIM::out: output the data, "keep" for ac reference
 * x = the x coordinate
 * print = selected points, "print" to screen, files, etc.
 * store = all points, for internal postprocessing, measure
 * keep = after the command is done, dcop for ac
 */
void SIM::outdata(double x, int outflags)
{
  ::status.output.start();
  if (outflags & ofKEEP) {
    _sim->keep_voltages();
  }else{
  }
  if (outflags & ofPRINT) {
    plottr(x, plotlist());
    print_results(x);
    _sim->reset_iteration_counter(iPRINTSTEP);
    ::status.hidden_steps = 0;
  }else{
    ++::status.hidden_steps;
  }
  if (outflags & ofSTORE) {
    alarm();
    store_results(x);
  }else{
  }
  ::status.output.stop();
}
/*--------------------------------------------------------------------------*/
/* SIM::head: print column headings and draw plot borders
 */
void SIM::head(double start, double stop, const std::string& col1)
{
  if (_sim->_waves) {
    delete [] _sim->_waves;
  }else{
  }

  _sim->_waves = new WAVE [storelist().size()];


  if (!plopen(start, stop, plotlist())) {
    // ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    int width = std::min(OPT::numdgt+5, BIGBUFLEN-10);
    char format[20];
    //sprintf(format, "%%c%%-%u.%us", width, width);
    sprintf(format, "%%c%%-%us", width);

    _out.form(format, '#', col1.c_str());

    for (PROBELIST::const_iterator
	   p=printlist().begin();  p!=printlist().end();  ++p) {
      _out.form(format, ' ', p->label().c_str());
    }
    _out << '\n';
  }else{
  }
}
/*--------------------------------------------------------------------------*/
/* SIM::print_results: print the list of results (text form) to _out
 * The argument is the first column (independent variable, aka "x")
 */
void SIM::print_results(double x)
{
  if (!IO::plotout.any()) {
    _out.setfloatwidth(OPT::numdgt, OPT::numdgt+6);
    assert(x != NOT_VALID);
    _out << x;
    for (PROBELIST::const_iterator
	   p=printlist().begin();  p!=printlist().end();  ++p) {
      _out << p->value();
    }
    _out << '\n';
  }else{
  }
}
/*--------------------------------------------------------------------------*/
/* SIM::alarm: print a message when a probe is out of range
 */
void SIM::alarm(void)
{
  _out.setfloatwidth(OPT::numdgt, OPT::numdgt+6);
  for (PROBELIST::const_iterator
	 p=alarmlist().begin();  p!=alarmlist().end();  ++p) {
    if (!p->in_range()) {
      _out << p->label() << '=' << p->value() << '\n';
    }else{
    }
  }
}
/*--------------------------------------------------------------------------*/
/* SIM::store: store data in preparation for post processing
 */
void SIM::store_results(double x)
{
  int ii = 0;
  for (PROBELIST::const_iterator
	 p=storelist().begin();  p!=storelist().end();  ++p) {
    _sim->_waves[ii++].push(x, p->value());
  }
}
/*--------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------*/
// vim:ts=8:sw=2:noet:
