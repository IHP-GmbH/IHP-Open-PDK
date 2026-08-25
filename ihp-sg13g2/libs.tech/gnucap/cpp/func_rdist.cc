/*                           -*- C++ -*-
 * Copyright (C) 2025 Felix Salfelder
 * Author: Felix Salfelder <felix@salfelder.org>
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
 * You should have received a copy of the GNU General Public License along with
 * Foobar. If not, see <https://www.gnu.org/licenses/>.
 *------------------------------------------------------------------
 */
#include "u_function.h"
#include "m_random.h"
#include "m_expression.h"
#include "globals.h"
#include "io_.h"
/*--------------------------------------------------------------------------*/
int get_args(Expression* E, Base const** a, int min_args, int max_args=0)
{
  max_args = max_args?:min_args;
  assert(E);
  auto it = E->end();
  --it;

  Token* pl = E->back();
  if(dynamic_cast<Token_PARLIST*>(pl)) {
    assert(it!=E->begin());
    --it;
  }else{ untested();
    throw Exception("need args");
  }

  int i = 0;
  for(; i < max_args; ++i) {
    if(auto cc=dynamic_cast<Token_CONSTANT const*>(*it)) {
      a[i] = cc->data();
      assert(it!=E->begin()); // inside PARLIST. expecting STOP
      --it;
    }else if(!dynamic_cast<Token_STOP const*>(*it)) {
    }else if(i<min_args){
      throw Exception("need more args");
    }
  }

  if(dynamic_cast<Token_STOP const*>(*it)) {
  }else{
    throw Exception("too many args");
  }

  return i;
}
/*--------------------------------------------------------------------------*/
void delete_args(Expression* E, int howmany)
{
  Token* pl = E->back();
  E->pop_back();
  assert(dynamic_cast<Token_PARLIST*>(pl));
  delete pl;
  for(int i=0; i<howmany; ++i){
    delete E->back();
    E->pop_back();
  }
  assert(dynamic_cast<Token_STOP const*>(E->back()));
  delete E->back();
  E->pop_back();
}
/*--------------------------------------------------------------------------*/
double get_double(Base const* b)
{
  bool ok = false;
  double p;
  if(auto f = dynamic_cast<Float const*>(b)){
    p = f->value();
    ok = true;
  }else if(auto i = dynamic_cast<Integer const*>(b)){
    p = i->value();
    ok = true;
  }else{
  }

  if(ok){
    return p;
  }else{
    throw Exception("not double\n");
  }
}
/*--------------------------------------------------------------------------*/
int32_t get_int(Base const* b)
{
  bool ok = false;
  int32_t p;
  if(auto f = dynamic_cast<Float const*>(b)){
    p = int32_t(f->value());
    ok = true;
  }else if(auto i = dynamic_cast<Integer const*>(b)){
    p = i->value();
    ok = true;
  }else{
  }

  if(ok){
    return p;
  }else{
    throw Exception("not int\n");
  }
}
/*--------------------------------------------------------------------------*/
std::string get_string(Base const* b)
{
  std::string p;
  if(auto f = dynamic_cast<String const*>(b)){
    return f->val_string();
  }else{
    throw Exception("not string\n");
  }
}
/*--------------------------------------------------------------------------*/
namespace {
/*--------------------------------------------------------------------------*/
class RDIST_UNIFORM : public FUNCTION {
public:
  explicit RDIST_UNIFORM() : FUNCTION() {}
public:
  void stack_op(Expression* E)const override {
    Base const* args[4];
    int argc = get_args(E, args, 3, 4);

    // E >> init >> a1 >> a0 [ >> slot ];
    bool global = false;
    if(argc == 4){ untested();
      std::string slot = get_string(args[0]);
      if(slot == "\"instance\""){
      }else if(slot == "\"global\""){
	global = true;
      }else{
      }
    }else{ untested();
      assert(argc==3);
    }
    double a0 = get_double(args[argc-3]);
    double a1 = get_double(args[argc-2]);
    int32_t init = get_int(args[argc-1]);

    double u;
    if(global){
      int32_t seed = init + OPT::rndseed;
      u = rdist::uniform(seed, a1, a0);
    }else{
      u = rdist::uniform(random_seed(init), a1, a0);
    }

    delete_args(E, argc);
    Float* f = new Float(u);
    E->push_back(new Token_CONSTANT(f));
  }
}p0;
DISPATCHER<FUNCTION>::INSTALL d0(&function_dispatcher, "$rdist_uniform", &p0);
/*--------------------------------------------------------------------------*/
class RDIST_NORMAL : public FUNCTION {
public:
  explicit RDIST_NORMAL() : FUNCTION() {}
public:
  void stack_op(Expression* E)const override {
    Base const* args[4];
    int argc = get_args(E, args, 3, 4);

    // E >> init >> a1 >> a0 [ >> slot ];
    bool global = false;
    if(argc == 4){ untested();
      std::string slot = get_string(args[0]);
      if(slot == "\"instance\""){
      }else if(slot == "\"global\""){
	global = true;
      }else{
      }
    }else{ untested();
      assert(argc==3);
    }
    double a0 = get_double(args[argc-3]);
    double a1 = get_double(args[argc-2]);
    int32_t init = get_int(args[argc-1]);

    double u;
    if(global){
      int32_t seed = init + OPT::rndseed;
      u = rdist::normal(seed, a1, a0);
    }else{
      u = rdist::normal(random_seed(init), a1, a0);
    }
    delete_args(E, argc);
    Float* f = new Float(u);
    E->push_back(new Token_CONSTANT(f));
  }
}p1;
DISPATCHER<FUNCTION>::INSTALL d1(&function_dispatcher, "$rdist_normal", &p1);
/*--------------------------------------------------------------------------*/
class RDIST_EXPONENTIAL : public FUNCTION {
public:
  explicit RDIST_EXPONENTIAL() : FUNCTION() {}
public:
  void stack_op(Expression* E)const override {
    Base const* args[2];
    get_args(E, args, 2);

    double a0 = get_double(args[0]);
    int32_t init = get_int(args[1]);

    double u = rdist::exponential(random_seed(init), a0);

    delete_args(E, 2);
    Float* f = new Float(u);
    E->push_back(new Token_CONSTANT(f));
  }
}p2;
DISPATCHER<FUNCTION>::INSTALL d2(&function_dispatcher, "$rdist_exponential", &p2);
/*--------------------------------------------------------------------------*/
class RDIST_POISSON : public FUNCTION {
public:
  explicit RDIST_POISSON() : FUNCTION() {}
public:
  void stack_op(Expression* E)const override {
    Base const* args[2];
    get_args(E, args, 2);

    double a0 = get_double(args[0]);
    int32_t init = get_int(args[1]);

    double u = rdist::poisson(random_seed(init), a0);

    delete_args(E, 2);
    Float* f = new Float(u);
    E->push_back(new Token_CONSTANT(f));
  }
}p3;
DISPATCHER<FUNCTION>::INSTALL d3(&function_dispatcher, "$rdist_poisson", &p3);
/*--------------------------------------------------------------------------*/
class RDIST_CHI_SQUARE : public FUNCTION {
public:
  explicit RDIST_CHI_SQUARE() : FUNCTION() {}
public:
  void stack_op(Expression* E)const override {
    Base const* args[2];
    get_args(E, args, 2);

    int a0 = get_int(args[0]);
    int32_t init = get_int(args[1]);

    double u = rdist::chi_square(random_seed(init), a0);

    delete_args(E, 2);
    Float* f = new Float(u);
    E->push_back(new Token_CONSTANT(f));
  }
}p4;
DISPATCHER<FUNCTION>::INSTALL d4(&function_dispatcher, "$rdist_chi_square", &p4);
/*--------------------------------------------------------------------------*/
class RDIST_T : public FUNCTION {
public:
  explicit RDIST_T() : FUNCTION() {}
public:
  void stack_op(Expression* E)const override {
    Base const* args[2];
    get_args(E, args, 2);

    int a0 = get_int(args[0]);
    int32_t init = get_int(args[1]);

    double u = rdist::t(random_seed(init), a0);

    delete_args(E, 2);
    Float* f = new Float(u);
    E->push_back(new Token_CONSTANT(f));
  }
}p5;
DISPATCHER<FUNCTION>::INSTALL d5(&function_dispatcher, "$rdist_t", &p5);
/*--------------------------------------------------------------------------*/
class RDIST_ERLANGIAN : public FUNCTION {
public:
  explicit RDIST_ERLANGIAN() : FUNCTION() {}
public:
  void stack_op(Expression* E)const override {
    Base const* args[3];
    get_args(E, args, 3);

    double a0 = get_double(args[0]);
    double a1 = get_double(args[1]);
    int32_t init = get_int(args[2]);

    double u = rdist::erlangian(random_seed(init), a1, a0);

    delete_args(E, 3);
    Float* f = new Float(u);
    E->push_back(new Token_CONSTANT(f));
  }
}p6;
DISPATCHER<FUNCTION>::INSTALL d6(&function_dispatcher, "$rdist_erlangian", &p6);
/*--------------------------------------------------------------------------*/
}
/*--------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------*/
// vim:ts=8:sw=2:noet:
