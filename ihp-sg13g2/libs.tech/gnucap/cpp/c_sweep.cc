/*                       -*- C++ -*-
 * Copyright (C) 2001 Albert Davis
 *               2026 Felix Salfelder
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
 * Step a parameter and repeat a group of commands
 */
#include "globals.h"
#include "u_parameter.h"
#include "u_lang.h"
#include "c_comand.h"
#include "e_cardlist.h"
#include "d_dot.h"
/*--------------------------------------------------------------------------*/
const int swp_nest_max = 10;
extern int swp_count[], swp_steps[];
extern int swp_type[];
extern int swp_nest;
/*--------------------------------------------------------------------------*/
namespace {
  static std::string tempfile = STEPFILE;
  std::string para_name[swp_nest_max];
  double start[swp_nest_max];
  double last[swp_nest_max];
/*--------------------------------------------------------------------------*/
/* sweep_fix: fix the value for sweep command.
 * (find value by interpolation)
 * if not sweeping, return "start" (the first arg).
 */
  // copy from c_modify
double sweep_fix(double Start, double Last)
{
  double value = Start;
  if (swp_steps[swp_nest] != 0) {
    double offset = static_cast<double>(swp_count[swp_nest]) 
      / static_cast<double>(swp_steps[swp_nest]);
    if (swp_type[swp_nest]=='L') { untested();
      untested();
      if (Start == 0.) { untested();
	untested();
	throw Exception("log sweep can't pass zero");
	value = 0;
      }else{ untested();
	untested();
	value = Start * pow( (Last/Start), offset );
      }
    }else{
      value = Start + (Last-Start) * offset;
    }
  }
  return value;
}
/*--------------------------------------------------------------------------*/
static void setup(CS& cmd, CARD_LIST* Scope)
{
  assert(Scope);
  PARAM_LIST const* params = Scope->params();
  for (;;) {
    if (cmd.umatch("li{near} ")) { untested();
      swp_type[swp_nest] = 0;
    }else if (cmd.umatch("lo{g} ")) { untested();
      swp_type[swp_nest] = 'L';
    }else{
      break;
    }
  }
  PARAMETER<double> s, l;
  PARAMETER<int> c;
  cmd >> c;
  c.e_val(2., params);

  while(cmd.more()){
    cmd >> para_name[swp_nest];
    cmd >> s;
    cmd >> l;

    s.e_val(0., params);
    l.e_val(1., params);

    start[swp_nest] = s;
    last[swp_nest] = l;
    assert (c>0);
    swp_steps[swp_nest] = int(c)-1;

    trace4("got", swp_nest, para_name[swp_nest], start[swp_nest], last[swp_nest] );
    ++swp_nest;
  }
//  swp_nest = swp_nest_bak;
}
/*--------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------*/
class CMD_SWEEP : public CMD {
  CARD_LIST _body;
public:
  void do_it(CS& cmd, CARD_LIST* Scope)override {
    if(swp_nest>=swp_nest_max) { untested();
      error(bDANGER, "nesting too deep\n");
    } else if (cmd.more()) {
      setup(cmd, Scope);
      buildfile(cmd, _body);
      doit(Scope);
    }else{ incomplete();
    }
  }
private:
  void doit(CARD_LIST* scope) {
    trace2("sweep doit", head, swp_nest);
    double para_value;

    int j = 0; // fixme.

    for (swp_count[j]=0; swp_count[j]<=swp_steps[j];
        ++swp_count[j]) {

      for(int i = 0; i<swp_nest; ++i){
	std::swap(swp_nest, j);
	para_value = sweep_fix(start[i], last[i] );
	trace3("setting", i, para_name[i], para_value);
	scope->params()->set( para_name[i], para_value );
	std::swap(swp_nest, j);
      }

      if(1) {
	for(auto c : _body){
	  assert(c);
	  if(auto dot = dynamic_cast<DEV_DOT const*>(c)) {
	    trace1("exec", dot->s());
	    CS cmd(CS::_STRING, dot->s());
	    cmdproc(cmd, scope);
	    trace1("done exec", dot->s());
	  }else{
	  }
	}
      }else{
      }
    }
    swp_count[swp_nest] = 0;
  }
/*--------------------------------------------------------------------------*/
  void buildfile(CS& cmd, CARD_LIST& stash) {
    unsigned nest = 0;

    DEV_DOT* d = new DEV_DOT;
    d->set(std::string("// ") + cmd.fullstring().c_str());
    stash.push_back(d);

    for (;;) {
      cmd.getline("sweep>");

      if (cmd.umatch(".sweep |`sweep ")) { untested();
	nest++;
      } else if (cmd.umatch("go ")) {
	if (nest) { untested();
	  nest--;
	}else {
	  break;
	}
      }else{
      }

      {
	d = new DEV_DOT;
	d->set(cmd.fullstring().c_str());
	trace1("build", d->s());
	stash.push_back(d);
      }
    }
#if 0
      switch (ENV::run_mode) {
        case rSCRIPT:
          trace0("in script mode");
          sbuffer = cmd.get_line("").fullstring();
          break;
         case rBATCH:
           trace0("in batch mode");
	   sbuffer = cmd.get_line("").fullstring();
           trace1("in batch mode", sbuffer);
	   break;
	 case rPRE_MAIN:
	 case rINTERACTIVE:
	 case rPRESET:
           trace1("not in script mode", ENV::run_mode);
           getcmd(">>>", buffer, BUFLEN);
           sbuffer=buffer;
      }
#endif
  }
} p;
DISPATCHER<CMD>::INSTALL d(&command_dispatcher, "`sweep|.sweep", &p);
/*--------------------------------------------------------------------------*/
}
/*--------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------*/
// vim:ts=8:sw=2:noet
