/*                       -*- C++ -*-
 * Copyright (C) 2008 Albert Davis
 *               2026 Lukas Deutz
 *
 * Based on measure_average.cc and modified to compute the standard deviation.
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
 * Measures sample standard deviation.
 */
#include "globals.h"
#include "u_parameter.h"
#include "m_wave.h"
#include "u_function.h"
/*--------------------------------------------------------------------------*/
namespace {
/*--------------------------------------------------------------------------*/
class MEASURE : public FUNCTION {
public:
  std::string eval(CS& Cmd, const PARAM_LIST* Scope)const override{
    std::string probe_name;
    PARAMETER<double> before(BIGBIG);
    PARAMETER<double> after(-BIGBIG);
    
    size_t here = Cmd.cursor();
    Cmd >> probe_name;
    WAVE* w = find_wave(probe_name);

    if (!w) { untested();
      Cmd.reset(here);
    }else{
    }

    here = Cmd.cursor();
    do {
      ONE_OF
	|| Get(Cmd, "probe",  &probe_name)
	|| Get(Cmd, "before", &before)
	|| Get(Cmd, "after",  &after)
	|| Get(Cmd, "end",    &before)
	|| Get(Cmd, "begin",  &after)
	;
    }while (Cmd.more() && !Cmd.stuck(&here));

    if (!w) { untested();
      w = find_wave(probe_name);
    }else{
    }

    if (w) {
      before.e_val(BIGBIG, Scope);
      after.e_val(-BIGBIG, Scope);

      WAVE::const_iterator begin = lower_bound(w->begin(), w->end(), DPAIR(after, -BIGBIG));
      WAVE::const_iterator end   = upper_bound(w->begin(), w->end(), DPAIR(before, BIGBIG));

      // Welford's algorithm
      double count = 0;
      double mean = 0;
      double M2 = 0;
      WAVE::const_iterator i = begin;
      while (i < end) {
        count++;
        double delta = i->second - mean;
        mean += delta / count;
        double delta2 = i->second - mean;
        M2 += delta * delta2;
        ++i;
      }
      double std_dev = sqrt(M2 / (count - 1));
      return to_string(std_dev);
    }else{ untested();
      throw Exception_No_Match(probe_name);
    }
  }
} p4;
DISPATCHER<FUNCTION>::INSTALL d4(&measure_dispatcher, "sample_std|sstd", &p4);
/*--------------------------------------------------------------------------*/
}
/*--------------------------------------------------------------------------*/
/*--------------------------------------------------------------------------*/
// vim:ts=8:sw=2:noet:
