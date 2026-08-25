/*$Id: s__solve.cc,v 26.138 2013/04/24 02:44:30 al Exp $ -*- C++ -*-
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
 * solve one step of a transient or dc analysis
 */
//testing=script 2006.07.14
#include "e_cardlist.h"
#include "u_status.h"
#include "u_sim_data.h"
#include "s__.h"
/*--------------------------------------------------------------------------*/
//	bool	SIM::solve(int,int);
//	void	SIM::finish_building_evalq();
//	void	SIM::advance_time();
//	void	SIM::set_flags();
//	void	SIM::clear_arrays();
//	void	SIM::evaluate_models();
//	void	SIM::set_damp();
//	void	SIM::load_matrix();
//	void	SIM::solve_equations();
/*--------------------------------------------------------------------------*/
static bool converged = false;
/*--------------------------------------------------------------------------*/
bool SIM::solve(OPT::ITL itl, TRACE trace)
{
  assert(_sim->_loadq.empty());
  converged = false;
  int convergedcount = 0;
  
  _sim->reset_iteration_counter(iSTEP);
  advance_time();

  _sim->_damp = OPT::dampmax;
 
  do{
    if (trace >= tITERATION) {
      print_results(static_cast<double>(-_sim->iteration_number()));
    }
    set_flags();
    clear_arrays();
    finish_building_evalq();
    
    _sim->count_iterations(iPRINTSTEP);
    _sim->count_iterations(iSTEP);
    _sim->count_iterations(_sim->_mode);
    _sim->count_iterations(iTOTAL);
    
    evaluate_models();

    if (converged) {
      if (_sim->_limiting) {
	error(bDEBUG, "converged beyond limit, resetting limit\n");
	_sim->set_limit();
	convergedcount = 0;
      }else{
	++convergedcount;
      }
    }else{
      convergedcount = 0;
    }
    if (convergedcount <= OPT::itermin) {
      converged = false;
    }else{
    }
      
    if (!converged || !OPT::fbbypass || _sim->_damp < .99) {
      set_damp();
      load_matrix();
      solve_equations();
    }else{
      _sim->_loadq.clear();
    }
  }while (!converged && !_sim->exceeds_iteration_limit(itl));

  return converged;
}
/*--------------------------------------------------------------------------*/
bool SIM::solve_with_homotopy(OPT::ITL itl, TRACE trace)
{
  solve(itl, trace);
  trace2("plain", _sim->_iter[iSTEP], OPT::gmin);
  if (!converged && OPT::itl[OPT::SSTEP] > 0) {
    int save_itermin = OPT::itermin;
    OPT::itermin = 0;
    double save_gmin = OPT::gmin;
    OPT::gmin = 1;
    while (_sim->_iter[iPRINTSTEP] < OPT::itl[OPT::SSTEP] && OPT::gmin > save_gmin) {
      //_scope->precalc();
      _sim->set_inc_mode_no();
      solve(itl, trace);
      if (!converged) {
	trace2("fail", _sim->_iter[iSTEP], OPT::gmin);
	OPT::gmin *= 3.5;
      }else{
	trace2("success", _sim->_iter[iSTEP], OPT::gmin);
	OPT::gmin /= 4;
      }
    }
    OPT::itermin = save_itermin;
    OPT::gmin = save_gmin;
    //_scope->precalc();
    solve(itl, trace);
    if (!converged) {
      trace2("final fail", _sim->_iter[iSTEP], OPT::gmin);
    }else{itested();
      trace2("final success", _sim->_iter[iSTEP], OPT::gmin);
    }
  }else{
  }
  return converged;
}
/*--------------------------------------------------------------------------*/
/* finish_building_evalq
 * This function scans the circuit to queue for evaluation anything 
 * that is relevant that the devices missed themselves.
 * For now, it scans the whole circuit, but this will change.
 * This is slow, but the result is still faster than not having a queue.
 * The plan is .. every node knows whether it needs eval or not, and
 * only those nodes needing eval will be scanned.
 * Its purpose is to catch nodes that wake up after being dormant
 */
void SIM::finish_building_evalq(void)
{
  ::status.queue.start();
  assert(_scope);
  if (_scope == &CARD_LIST::card_list) {
  }else{untested();
  }
  _scope->tr_queue_eval();
  ::status.queue.stop();
}
/*--------------------------------------------------------------------------*/
void SIM::advance_time(void)
{
  assert(_scope);
  if (_scope == &CARD_LIST::card_list) {
  }else{untested();
  }
  ::status.advance.start();
  static double time1, time2;
  if (_sim->_time0 > 0) {//44061 // not initial DC
    if (_sim->_time0 > time1) {//43294 // moving forward
      std::swap(_sim->_v0,_sim->_vt1);
      if (OPT::predictor!=0. && time1 > time2) {//42447 // 
	double dtdt = (_sim->_time0 - time1) / (time1 - time2);
	trace4("", _sim->_time0, time1, time2, dtdt);
	if (dtdt <= OPT::predictor) {//42094 // normal prediction
	  for (int ii=1; ii <= _sim->_total_nodes; ++ii) {
	    double vt2 = _sim->_v0[ii];
	    double vt1 = _sim->_vt1[ii];
	    double vt0 = vt1 + (vt1 - vt2) * dtdt;
	    _sim->_v0[ii] = vt0;
	  }
	}else{//353 // long shot, large step follows small step
	  std::copy_n(_sim->_vt1, _sim->_total_nodes+1, _sim->_v0);
	}
      }else{//847 // first step, no history
	std::copy_n(_sim->_vt1, _sim->_total_nodes+1, _sim->_v0);
      }
      _scope->tr_advance();
    }else{//767 // moving backward
      /* don't save voltages.  They're wrong! */
      /* instead, restore a clean start for iteration */
      std::copy_n(_sim->_vt1, _sim->_total_nodes+1, _sim->_v0);
      _scope->tr_regress();
    }
  }else{//6771 // initial DCOP
    time1 = time2 = 0;
    _scope->dc_advance();
  }
  time2 = time1;
  time1 = _sim->_time0;
  ::status.advance.stop();
}
/* last_iter_time is initially 0 by C definition.
 * On subsequent runs it will start with an arbitrary positive value.
 * _sim->_time0 starts at either 0 or the ending time of the last run.
 * In either case, (time0 > last_iter_time) is false on the first step.
 * This correctly results in "don't save voltages..."
 */
/*--------------------------------------------------------------------------*/
void SIM::set_flags()
{
  _sim->_limiting = false;
  _sim->_fulldamp = false;
  
  if (OPT::incmode == false) {
    _sim->set_inc_mode_no();
  }else if (_sim->inc_mode_is_bad()) {
    _sim->set_inc_mode_no();
  }else if (_sim->is_iteration_number(OPT::itl[OPT::TRLOW])) {
    _sim->set_inc_mode_no();
  }else if (_sim->is_iteration_number(0)) {
    // leave it as is
  }else{
    _sim->set_inc_mode_yes();
  }

  _sim->_bypass_ok = 
    (is_step_rejected()  ||  _sim->_damp < OPT::dampmax*OPT::dampmax)
    ? false : bool(OPT::bypass);
}
/*--------------------------------------------------------------------------*/
void SIM::clear_arrays(void)
{
  if (!_sim->is_inc_mode()) {			/* Clear working array */
    _sim->_aa.zero();
    _sim->_aa.dezero(OPT::gmin);		/* gmin fudge */
    std::fill_n(_sim->_i, _sim->_aa.size()+1, 0);
  }else{
  }
  // assert(_sim->_loadq.empty()); // queued load in *_advance.
}
/*--------------------------------------------------------------------------*/
void SIM::evaluate_models()
{
  assert(_scope);
  if (_scope == &CARD_LIST::card_list) {
  }else{untested();
  }
  ::status.evaluate.start();
  if (OPT::bypass) {
    converged = true;
    swap(_sim->_evalq, _sim->_evalq_uc);
    while (!_sim->_evalq->empty()) {
      converged &= _sim->_evalq->front()->do_tr();
      _sim->_evalq->pop_front();
    }
  }else{
    _sim->_evalq_uc->clear();
    converged = _scope->do_tr();
  }
  while (!_sim->_late_evalq.empty()) { //BUG// encapsulation violation
    converged &= _sim->_late_evalq.front()->do_tr_last();
    _sim->_late_evalq.pop_front();
  }
  ::status.evaluate.stop();
}
/*--------------------------------------------------------------------------*/
void SIM::set_damp()
{
  if (_sim->is_second_iteration() && !converged && OPT::dampstrategy&dsINIT) {
    _sim->_damp = OPT::dampmin;
  }else if (_sim->is_first_iteration()  ||  converged) {
    _sim->_damp = OPT::dampmax;
  }else if (_sim->_fulldamp) {
    _sim->_damp = OPT::dampmin;
  }else{
    _sim->_damp = OPT::dampmax;
  }
  trace1("", _sim->_damp);
}
/*--------------------------------------------------------------------------*/
void SIM::load_matrix()
{
  ::status.load.start();
  if (OPT::traceload && _sim->is_inc_mode()) {
    while (!_sim->_loadq.empty()) {
      _sim->_loadq.back()->tr_load();
      _sim->_loadq.pop_back();
    }
  }else{
    _sim->_loadq.clear();
    assert(_scope);
    if (_scope == &CARD_LIST::card_list) {
    }else{untested();
    }
    _scope->tr_load();
  }
  assert(_sim->_loadq.empty());
  ::status.load.stop();
}
/*--------------------------------------------------------------------------*/
void SIM::solve_equations()
{
  ::status.lud.start();
  _sim->_aa.lu_decomp(bool(OPT::lubypass && _sim->is_inc_mode()));
  ::status.lud.stop();

  ::status.back.start();
  _sim->_aa.fbsub(_sim->_v0, _sim->_i, _sim->_v0);
  ::status.back.stop();
}
/*--------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------*/
// vim:ts=8:sw=2:noet:
