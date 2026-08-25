/* $Id: s__init.cc 2016/03/28 al $ -*- C++ -*-
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
 * initialization (allocation, node mapping, etc)
 */
//testing=obsolete
#include "e_cardlist.h"
#include "u_status.h"
#include "u_sim_data.h"
#include "s__.h"
/*--------------------------------------------------------------------------*/
void SIM::command_base(CS& cmd)
{  
  assert(_sim);
  assert(_scope);
  if (_scope == &CARD_LIST::card_list) {
  }else{untested();
  }
  reset_timers();
  _sim->reset_iteration_counter(_sim->_mode);
  _sim->reset_iteration_counter(iPRINTSTEP);

  try {
    setup(cmd);
    _sim->init(_scope);
    _scope->precalc_last();

    _sim->alloc_vectors();
    _sim->_aa.reallocate();
    _sim->_aa.dezero(OPT::gmin);
    _sim->_aa.set_min_pivot(OPT::pivtol);
    assert(_sim->_vdc);
    ::status.set_up.stop();

    switch (ENV::run_mode) {
    case rPRE_MAIN:	unreachable();	break;
    case rBATCH:	sweep(); final(); break;
    case rINTERACTIVE:	itested();sweep(); final(); break;
    case rSCRIPT:	sweep(); final(); break;
    case rPRESET:	/*nothing*/	break;
    }
  }catch (Exception& e) {
    error(bDANGER, e.message() + '\n');
    _sim->count_iterations(iTOTAL);
    _sim->_aa.unallocate();
  }
  finish();
  _sim->unalloc_vectors();
  _sim->_lu.unallocate();
  _sim->_aa.unallocate();

  ::status.total.stop();
}
/*--------------------------------------------------------------------------*/
SIM::~SIM()
{
  //assert(!_scope);
  if (_sim) {
    _sim->uninit();
  }else{
  }
}
/*--------------------------------------------------------------------------*/
void SIM::reset_timers()
{
  ::status.advance.reset();
  ::status.queue.reset();
  ::status.evaluate.reset();
  ::status.load.reset();
  ::status.lud.reset();
  ::status.back.reset();
  ::status.review.reset();
  ::status.accept.reset();
  ::status.output.reset();
  ::status.aux1.reset();
  ::status.aux2.reset();
  ::status.aux3.reset();
  ::status.set_up.reset().start();
  ::status.total.reset().start();
}
/*--------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------*/
// vim:ts=8:sw=2:noet:
