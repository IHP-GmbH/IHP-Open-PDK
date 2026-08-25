/*                       -*- C++ -*-
 * Copyright (C) 2001 Albert Davis
 *               2026 Felix Salfelder
 *
 * Based on s_dc.cc and modified to support seed sweeps for Monte Carlo
 * simulations.
 *
 * This file implements a plugin for "Gnucap", the GNU Circuit Analysis Package.
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
 * dc analysis top with seed sweep support
 */
#include "globals.h"
#include "u_status.h"
#include "u_prblst.h"
#include "u_cardst.h"
#include "e_elemnt.h"
#include "e_cardlist.h"
#include "s__.h"
#include "constant.h"
#include "m_random.h"
#include "s__init.cc"
#include "s__out.cc"
#include "s__solve.cc"
/*--------------------------------------------------------------------------*/
namespace {
/*--------------------------------------------------------------------------*/
class SWEEPVAL : public COMMON_COMPONENT {
  double _value;
public:
  explicit	SWEEPVAL(int c=0)
    :COMMON_COMPONENT(c) {}
  explicit	SWEEPVAL(const SWEEPVAL& p)
    :COMMON_COMPONENT(p), _value(p._value) {}
		~SWEEPVAL() { trace1("~SWEEPVAL", this);}
  COMMON_COMPONENT* clone()const override{
    return new SWEEPVAL(*this);
  }

public:
  void set_value(double v) { _value = v; }
  bool has_value()const override{ return true; }
  double value()const override { return _value; }


private:
  std::string name()const override{untested(); return "sweepval";}

private: // override virtual
  bool operator==(const COMMON_COMPONENT& p) const override {
    return dynamic_cast<SWEEPVAL const*>(&p);
  }
  bool has_tr_eval()const override {return true;}
  bool has_ac_eval()const override {untested(); return true;}
  bool use_obsolete_callback_parse()const override {untested(); return false;}
  bool use_obsolete_callback_print()const override {untested(); return false;}
  bool has_parse_params_obsolete_callback()const override {untested(); return false;}

private:
  void tr_eval(ELEMENT* d)const override {
    d->_y[0] = FPOLY1(CPOLY1(d->_y[0].x, 0., _value));
  }
  void ac_eval(ELEMENT* d)const override { untested();
    tr_eval(d);
    d->_ev = d->_y[0].f1;
  }
};
/*--------------------------------------------------------------------------*/
static SWEEPVAL p1(CC_STATIC);
static DISPATCHER<COMMON_COMPONENT>::INSTALL d1(&bm_dispatcher,
       "sweepval", &p1);
/*--------------------------------------------------------------------------*/
}
namespace {
/*--------------------------------------------------------------------------*/
class DCOP : public SIM {
protected: // tmp hack
  double _temp_c;
protected:
  void	fix_args(int);
  void	options(CS&, int);
private:
  void	sweep()override;
  void	precalc();
  void	sweep_recursive(int);
  void	first(int);
  bool	next(int);
  void	final()override		{_scope->dc_final();}
  void	finish()override;

  explicit DCOP(const DCOP&): SIM() { untested();unreachable(); incomplete();}
protected:
  void set_sweepval(int i, double d){
    ::status.set_up.start();
    assert(_sweepval[i]);
    std::string n = _param_name[i];
    if(n=="$seed"){
      OPT::rndseed = d;
    }else if(n!=""){
      PARAM_LIST* pl = _scope->params();
      assert(pl);
      pl->set(n, d);
    }else if(_zap[i]){
      assert(_ctrl[i]);
      auto c=prechecked_cast<SWEEPVAL*>(_ctrl[i]);
      assert(c);
      c->set_value(d);
    }else{
    }
    *_sweepval[i] = d;
    if(_sweepval[i] == &_temp_c){
      assert(_scope->params());
      assert(_temp_c != NOT_INPUT);
      _scope->params()->set_temperature(_temp_c + P_CELSIUS0);
    }else{
    }
    ::status.set_up.stop();
  }
  double get_sweepval(int i) const{
    assert(_sweepval[i]);
    return *_sweepval[i];
  }
protected:
  explicit DCOP();
  ~DCOP() {}
  
protected:
  enum {DCNEST = 4};
  int _n_sweeps;
  PARAMETER<double> _start[DCNEST];
  PARAMETER<double> _stop[DCNEST];
  PARAMETER<double> _step_in[DCNEST];
  double _step[DCNEST];
  bool _linswp[DCNEST];
  double* _sweepval[DCNEST];	/* pointer to thing to sweep, dc command */
  ELEMENT* _zap[DCNEST];	/* to branch to zap, for re-expand */
  COMMON_COMPONENT* _ctrl[DCNEST]; /* take control */
  std::string _param_name[DCNEST];
  double _param[DCNEST];        // sweep this value:
  PARAM_INSTANCE _param_zap[DCNEST]; // keep a backup
  CARDSTASH _stash[DCNEST];	/* store std values of elements being swept */
  bool _loop[DCNEST];		/* flag: do it again backwards */
  bool _reverse_in[DCNEST];	/* flag: sweep backwards, input */
  bool _reverse[DCNEST];	/* flag: sweep backwards, working */
  bool _cont;			/* flag: continue from previous run */
  TRACE _trace;			/* enum: show extended diagnostics */
  enum {ONE_PT, LIN_STEP, LIN_PTS, TIMES, OCTAVE, DECADE} _stepmode[DCNEST];
  bool _have_param;             /* sweep a param */
};
/*--------------------------------------------------------------------------*/
class DC : public DCOP {
public:
  explicit DC(): DCOP() {}
  ~DC() {}
  void	do_it(CS&, CARD_LIST*)override;
private:
  void	setup(CS&)override;
  explicit DC(const DC&): DCOP() { untested();unreachable(); incomplete();}
};
/*--------------------------------------------------------------------------*/
class OP : public DCOP {
public:
  explicit OP(): DCOP() {}
  ~OP() {}
  void	do_it(CS&, CARD_LIST*)override;
private:
  void	setup(CS&)override;
  explicit OP(const OP&): DCOP() { untested();unreachable(); incomplete();}
};
/*--------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------*/
void DC::do_it(CS& Cmd, CARD_LIST* Scope)
{
  assert(Scope);
  if (Scope == &CARD_LIST::card_list) {
  }else{untested();
  }
  _scope = Scope;
  _sim->_time0 = 0.;
  _sim->set_command_dc();
  _sim->_phase = p_INIT_DC;
  ::status.dc.reset().start();
  command_base(Cmd);
  _scope = nullptr;
  ::status.dc.stop();
}
/*--------------------------------------------------------------------------*/
void OP::do_it(CS& Cmd, CARD_LIST* Scope)
{
  assert(Scope);
  if (Scope == &CARD_LIST::card_list) {
  }else{untested();
  }
  _scope = Scope;
  _sim->_time0 = 0.;
  _sim->set_command_op();
  _sim->_phase = p_INIT_DC;
  ::status.op.reset().start();
  command_base(Cmd);
  _scope = nullptr;
  ::status.op.stop();
}
/*--------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------*/
DCOP::DCOP()
  :SIM(),
   _n_sweeps(1),
   _cont(false),
   _trace(tNONE)
{
  for (int ii = 0; ii < DCNEST; ++ii) {
    _loop[ii] = false;
    _reverse_in[ii] = false;
    _reverse[ii] = false;
    _step[ii]=0.;
    _linswp[ii]=true;
    _sweepval[ii]=&_sim->_genout;
    _zap[ii] = nullptr;
    _ctrl[ii] = nullptr;
    _stepmode[ii] = ONE_PT;
    _param[ii] = NOT_VALID;
  }
  
  //BUG// in SIM.  should be initialized there.
  //_sim->_genout=0.;
  _out=IO::mstdout;
  //_sim->_uic=false;
}
/*--------------------------------------------------------------------------*/
void DCOP::finish(void)
{
  for (int ii = 0;  ii < _n_sweeps;  ++ii) {
    std::string n = _param_name[ii];
    if (_zap[ii]) {
      _stash[ii].restore();
      _zap[ii]->precalc_first();
      _zap[ii]->precalc_last();
      _zap[ii] = nullptr;
      _ctrl[ii] = nullptr;
    }else if (n != "") {
      PARAM_LIST* pl = _scope->params();
      assert(pl);
      std::string previous_value = _param_zap[ii].string();
      CS cmd(CS::_STRING, n + "=" + previous_value);
      pl->set(n, previous_value);
    }else{
    }
    assert(!_ctrl[ii]);
  }
}
/*--------------------------------------------------------------------------*/
void OP::setup(CS& Cmd)
{
  _temp_c = OPT::temp_k - P_CELSIUS0;
  _cont = false;
  _trace = tNONE;
  _out = IO::mstdout;
  _out.reset(); //BUG// don't know why this is needed */
  bool ploton = IO::plotset  &&  plotlist().size() > 0;

  _zap[0] = nullptr;
  _sweepval[0] = &_temp_c;
  _have_param = true; // temp requires precalc

  if (Cmd.match1("'\"({") || Cmd.is_float()) {
    Cmd >> _start[0];
    if (Cmd.match1("'\"({") || Cmd.is_float()) {
      Cmd >> _stop[0];
    }else{
      _stop[0] = _start[0];
    }
  }else{
  }
  
  _step[0] = 0.;
  _sim->_genout = 0.;

  options(Cmd,0);

  _n_sweeps = 1;
  Cmd.check(bWARNING, "what's this?");
  _sim->_freq = 0;

  IO::plotout = (ploton) ? IO::mstdout : OMSTREAM();
  initio(_out);

  _start[0].e_val(OPT::temp_k - P_CELSIUS0, _scope->params());
  fix_args(0);
}
/*--------------------------------------------------------------------------*/
void DC::setup(CS& Cmd)
{
  assert(_scope);
  assert(_scope->params());
  _temp_c = OPT::temp_k - P_CELSIUS0;
  _cont = false;
  _trace = tNONE;
  _out = IO::mstdout;
  _out.reset(); //BUG// don't know why this is needed */
  bool ploton = IO::plotset  &&  plotlist().size() > 0;
  _have_param = false;

  if (Cmd.more()) {
    for (_n_sweeps = 0; Cmd.more() && _n_sweeps < DCNEST; ++_n_sweeps) {
      CARD_LIST::fat_iterator ci = findbranch(Cmd, _scope);
      if (!ci.is_end()) {			// sweep a component
	if (ELEMENT* c = dynamic_cast<ELEMENT*>(*ci)) {
	  _zap[_n_sweeps] = c;
	  _param_name[_n_sweeps] = ""; // not used.
	 // trace2("_zap", c->value(), c->value().string());
	}else{untested();
	  throw Exception("dc/op: can't sweep " + (**ci).long_label() + '\n');
	}
      }else if (Cmd.is_float()) {		// sweep the generator
	_zap[_n_sweeps] = nullptr;
      }else if(Cmd >> "$seed"){
	  _param_name[_n_sweeps] = "$seed";
	  _have_param = true;
      }else if (Cmd.is_alpha()) {
	std::string pname;

	size_t here = Cmd.cursor();
        Cmd >> pname;
	PARAM_INSTANCE zap = _scope->params()->deep_lookup(pname);
	if(zap.has_hard_value()){
	  _param_zap[_n_sweeps] = zap;
	  _param_name[_n_sweeps] = pname;
	  _have_param = true;
	}else{
	  // possibly not a parameter. go on
	  Cmd.reset(here);
	}
      }else{ untested();
	// leave as it was .. repeat Cmd with no args
      }
      
      if (Cmd.match1("'\"({") || Cmd.is_float()) {	// set up parameters
	_start[_n_sweeps] = "NA";
	_stop[_n_sweeps] = "NA";
	Cmd >> _start[_n_sweeps] >> _stop[_n_sweeps];
	_step[_n_sweeps] = 0.;
      }else{
	// leave it as it was .. repeat Cmd with no args
      }
      
      _sim->_genout = 0.;
      options(Cmd,_n_sweeps);
    }
  }else{
  }
  Cmd.check(bWARNING, "what's this?");

  IO::plotout = (ploton) ? IO::mstdout : OMSTREAM();
  initio(_out);

  assert(_n_sweeps > 0);
  for (int ii = 0;  ii < _n_sweeps;  ++ii) {
    _start[ii].e_val(0., _scope->params());
    fix_args(ii);

    if (_zap[ii]) { // component
      _stash[ii] = _zap[ii];			// stash the std value
      assert(!_ctrl[ii]);
      _ctrl[ii] = bm_dispatcher.clone("sweepval");
      assert(_ctrl[ii]);
      _zap[ii]->attach_common(_ctrl[ii]);	// take control
      _sweepval[ii] = &_param[ii];
    }else if (_param_name[ii] == "$seed") {
      _sweepval[ii] = &_param[ii];
    }else if (_param_name[ii] != "") {
      _sweepval[ii] = &_param[ii];
    }else{ // generator
      _sweepval[ii] = &_sim->_genout;			// point to value to patch
    }
  }
  _sim->_freq = 0;

  if(_temp_c == NOT_INPUT) {
    _scope->params()->set_temperature(OPT::temp_k);
  }else{
  }

  trace1("dcopt", _temp_c);
}
/*--------------------------------------------------------------------------*/
void DCOP::fix_args(int Nest)
{
  _stop[Nest].e_val(_start[Nest], _scope->params());
  _step_in[Nest].e_val(0., _scope->params());
  _step[Nest] = _step_in[Nest];
  
  switch (_stepmode[Nest]) {
  case ONE_PT:
  case LIN_STEP:
    _linswp[Nest] = true;
    break;
  case LIN_PTS:untested();
    if (_step[Nest] <= 2.) {untested();
      _step[Nest] = 2.;
    }else{untested();
    }
    _linswp[Nest] = true;
    break;
  case TIMES:itested();
    if (_step[Nest] == 0.  &&  _start[Nest] != 0.) {untested();
      _step[Nest] = _stop[Nest] / _start[Nest];
    }else{itested();
    }
    _linswp[Nest] = false;
    break;
  case OCTAVE:untested();
    if (_step[Nest] == 0.) {untested();
      _step[Nest] = 1.;
    }else{untested();
    }
    _step[Nest] = pow(2.00000001, 1./_step[Nest]);
    _linswp[Nest] = false;
    break;
  case DECADE:
    if (_step[Nest] == 0.) {untested();
      _step[Nest] = 1.;
    }else{
    }
    _step[Nest] = pow(10., 1./_step[Nest]);
    _linswp[Nest] = false;
    break;
  };
  
  if (_step[Nest] == 0.) {	// prohibit log sweep from 0
    _step[Nest] = _stop[Nest] - _start[Nest];
    _linswp[Nest] = true;
  }else{
  }
}
/*--------------------------------------------------------------------------*/
void DCOP::options(CS& Cmd, int Nest)
{
  _sim->_uic = _loop[Nest] = _reverse_in[Nest] = false;
  size_t here = Cmd.cursor();

  double temp_k = OPT::temp_k;
  bool temp_given = false;

  do{
    ONE_OF
      || (Cmd.match1("'\"({")	&& ((Cmd >> _step_in[Nest]), (_stepmode[Nest] = LIN_STEP)))
      || (Cmd.is_float()	&& ((Cmd >> _step_in[Nest]), (_stepmode[Nest] = LIN_STEP)))
      || (Get(Cmd, "*",		  &_step_in[Nest]) && (_stepmode[Nest] = TIMES))
      || (Get(Cmd, "+",		  &_step_in[Nest]) && (_stepmode[Nest] = LIN_STEP))
      || (Get(Cmd, "by",	  &_step_in[Nest]) && (_stepmode[Nest] = LIN_STEP))
      || (Get(Cmd, "step",	  &_step_in[Nest]) && (_stepmode[Nest] = LIN_STEP))
      || (Get(Cmd, "d{ecade}",	  &_step_in[Nest]) && (_stepmode[Nest] = DECADE))
      || (Get(Cmd, "ti{mes}",	  &_step_in[Nest]) && (_stepmode[Nest] = TIMES))
      || (Get(Cmd, "lin",	  &_step_in[Nest]) && (_stepmode[Nest] = LIN_PTS))
      || (Get(Cmd, "o{ctave}",	  &_step_in[Nest]) && (_stepmode[Nest] = OCTAVE))
      || Get(Cmd, "c{ontinue}",   &_cont)
      || (Get(Cmd, "dt{emp}",	  &temp_k, mOFFSET, OPT::temp_k) && (temp_given=true))
      || Get(Cmd, "lo{op}", 	  &_loop[Nest])
      || Get(Cmd, "re{verse}",	  &_reverse_in[Nest])
      || (Get(Cmd, "te{mperature}",&temp_k, mOFFSET, P_CELSIUS0) && (temp_given=true))
      || (Get(Cmd, "$temperature", &temp_k) && (temp_given=true))
      || (Cmd.umatch("tr{ace} {=}") &&
	  (ONE_OF
	   || Set(Cmd, "n{one}",      &_trace, tNONE)
	   || Set(Cmd, "o{ff}",       &_trace, tNONE)
	   || Set(Cmd, "w{arnings}",  &_trace, tUNDER)
	   || Set(Cmd, "i{terations}",&_trace, tITERATION)
	   || Set(Cmd, "v{erbose}",   &_trace, tVERBOSE)
	   || Cmd.warn(bWARNING, 
		       "need none, off, warnings, iterations, verbose")
	   )
	  )
      || outset(Cmd,&_out)
      ;
  }while (Cmd.more() && !Cmd.stuck(&here));

  if(temp_given) {
    _temp_c = temp_k - P_CELSIUS0;
  }else{
    _temp_c = NOT_INPUT;
  }
  trace2("options", temp_given, _temp_c);
}
/*--------------------------------------------------------------------------*/
void DCOP::sweep()
{
  head(_start[0], _stop[0], " ");
  _sim->_bypass_ok = false;
  _sim->set_inc_mode_bad();
  if (_cont) {untested();
    _sim->restore_voltages();
    _scope->tr_restore();
  }else{
    _sim->clear_limit();
    _scope->tr_begin();
  }
  try {
    sweep_recursive(_n_sweeps);
  }catch (Exception& e) {
    error(bDANGER, e.message() + '\n');
  }
}
/*--------------------------------------------------------------------------*/
void DCOP::precalc()
{
  ::status.set_up.start();
  trace1("precalc", _temp_c);
  if(_temp_c != NOT_INPUT) {
    _scope->params()->set_temperature(_temp_c + P_CELSIUS0);
  }else{
  }

  if(_have_param || _temp_c != NOT_INPUT){
    // do them all.
    assert(_scope->params());
    random_seeds.clear();
    _scope->precalc_last();
  }else{
    for (int ii = 0;  ii < _n_sweeps;  ++ii) {
      if (_zap[ii]) {
	// only sweep elements
	_zap[ii]->precalc_last();
      }else{
      }
    }
  }
  ::status.set_up.stop();
}
/*--------------------------------------------------------------------------*/
void DCOP::sweep_recursive(int Nest)
{
  --Nest;
  assert(Nest >= 0);
  assert(Nest < DCNEST);

  OPT::ITL itl = OPT::DCBIAS;
  
  first(Nest);
  do {
    if (Nest == 0) {
      precalc();
      int converged = solve_with_homotopy(itl,_trace);
      if (!converged) {
	error(bWARNING, "did not converge\n");
      }else{
      }
      ::status.accept.start();
      _sim->set_limit();
      _scope->tr_accept();
      ::status.accept.stop();
      _sim->_has_op = _sim->_mode;
      outdata(*_sweepval[Nest], ofPRINT | ofSTORE | ofKEEP);
      itl = OPT::DCXFER;
    }else{
      sweep_recursive(Nest);
    }
  } while (next(Nest));
}
/*--------------------------------------------------------------------------*/
void DCOP::first(int Nest)
{
  assert(Nest >= 0);
  assert(Nest < DCNEST);
  assert(_start);
  assert(_sweepval);
  assert(_sweepval[Nest]);

  set_sweepval(Nest, _start[Nest]);
  _reverse[Nest] = false;
  if (_reverse_in[Nest]) {untested();
    while (next(Nest)) {untested();
      /* nothing */;
    }
    _reverse[Nest] = true;
    next(Nest);
  }else{
  }
  _sim->_phase = p_INIT_DC;
  if(_sweepval[Nest] == &_temp_c){
    assert(_temp_c != NOT_INPUT);
    _scope->params()->set_temperature(_temp_c + P_CELSIUS0);
    // precalc?
  }else{
  }
}
/*--------------------------------------------------------------------------*/
bool DCOP::next(int Nest)
{
  double sweepval = NOT_VALID;
  bool ok = false;

  if (_linswp[Nest]) {
    double fudge = _step[Nest] / 10.;
    if (_step[Nest] == 0.) {
      // not stepping
      assert(!ok);
      assert(sweepval == NOT_VALID);
    }else{
      // stepping
      if (!_reverse[Nest]) {
	sweepval = *(_sweepval[Nest]) + _step[Nest];
	fixzero(&sweepval, _step[Nest]);
	ok = in_order(_start[Nest]-fudge, sweepval, _stop[Nest]+fudge);
	if (!ok  &&  _loop[Nest]) {
	  // turn around
	  _reverse[Nest] = true;
	}else{
	  // forward
	}
      }else{
	assert(_reverse[Nest]);
	assert(!ok);
	assert(sweepval == NOT_VALID);
      }
      if (_reverse[Nest]) {
	assert(!ok);
	//assert(sweepval == NOT_VALID);
	sweepval = *(_sweepval[Nest]) - _step[Nest];
	fixzero(&sweepval, _step[Nest]);
	ok = in_order(_start[Nest]-fudge, sweepval, _stop[Nest]+fudge);
      }else{
	// not sure of status
      }
    }
  }else{
    // not linswp
    double fudge = pow(_step[Nest], .1);
    if (_step[Nest] == 1.) {untested();
      // not stepping
      assert(!ok);
      assert(sweepval == NOT_VALID);
    }else{
      if (!_reverse[Nest]) {
	sweepval = get_sweepval(Nest) * _step[Nest];
	ok = in_order(_start[Nest]/fudge, sweepval, _stop[Nest]*fudge);
	if (!ok  &&  _loop[Nest]) {untested();
	  // turn around
	  _reverse[Nest] = true;
	}else{
	  // forward
	}
      }else{untested();
	assert(_reverse[Nest]);
	assert(!ok);
	assert(sweepval == NOT_VALID);
      }
      if (_reverse[Nest]) {untested();
	assert(!ok);
	assert(sweepval == NOT_VALID);
	sweepval = get_sweepval(Nest) / _step[Nest];
	ok = in_order(_start[Nest]/fudge, sweepval, _stop[Nest]*fudge);
      }else{
	// not sure of status
      }
    }
  }
  _sim->_phase = p_DC_SWEEP;
  if (ok) {
    assert(sweepval != NOT_VALID);
    set_sweepval(Nest, sweepval);
    return true;
  }else{
    //assert(sweepval == NOT_VALID);
    return false;
  }
}
/*--------------------------------------------------------------------------*/
static DC p2;
static OP p4;
static DISPATCHER<CMD>::INSTALL d2(&command_dispatcher, "dc|`dc", &p2);
static DISPATCHER<CMD>::INSTALL d4(&command_dispatcher, "op|`op", &p4);
}
/*--------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------*/
// vim:ts=8:sw=2:noet:
