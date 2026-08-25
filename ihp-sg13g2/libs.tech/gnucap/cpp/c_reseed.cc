/*                       -*- C++ -*-
 * Copyright (C) 2026 Lukas Deutz
 *
 * This file is a plugin for "Gnucap", the Gnu Circuit Analysis Package
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
 * Increments the global random seed
*/

#include "globals.h"
#include "c_comand.h"
#include "e_cardlist.h"
#include "m_random.h"

/*--------------------------------------------------------------------------*/
namespace {
/*--------------------------------------------------------------------------*/
class CMD_RESEED : public CMD {
public:
  void do_it(CS& cmd, CARD_LIST* scope)override {
    assert(scope);

    ++OPT::rndseed;
    random_seeds.clear();

    scope->precalc_first();
    scope->precalc_last();

    cmd.check(bWARNING, "what's this?");
  }
} p;
/*--------------------------------------------------------------------------*/
DISPATCHER<CMD>::INSTALL d(&command_dispatcher, "reseed|`reseed|.reseed", &p);
/*--------------------------------------------------------------------------*/
}
/*--------------------------------------------------------------------------*/
