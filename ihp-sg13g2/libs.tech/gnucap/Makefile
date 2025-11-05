GCMG_FLAGS = -I $(shell gnucap-conf --includedir) -I models
GNUCAP_CPPFLAGS = $(shell gnucap-conf --cppflags) ${CPPFLAGS}
GNUCAP_CXXFLAGS = $(shell gnucap-conf --cxxflags) -fPIC -shared ${CXXFLAGS}
SPAKCONVERT = `which spak-convert`
SPAKFLAGS = --va-include ../verilog-a/psp103/psp103_nqs.va \
			--va-include ../verilog-a/r3_cmc/r3_cmc.va \
			--va-include ../verilog-a/mosvar/mosvar.va \
			--va-include models/capacitor.va \
			--va-include models/bjt.va \
			--va-include models/vbic_4T_et_cf.va

# Default target
all: plugins/psp103_nqs.so \
	 plugins/r3_cmc.so \
	 plugins/mosvar.so \
	 plugins/vbic_4T_et_cf.so \
	 plugins/cornerMOSlv_tt.so \
	 plugins/cornerMOSlv_ss.so \
	 plugins/cornerMOSlv_ff.so \
	 plugins/cornerMOSlv_sf.so \
	 plugins/cornerMOSlv_fs.so \
	 plugins/cornerMOShv_tt.so \
	 plugins/cornerMOShv_ss.so \
	 plugins/cornerMOShv_ff.so \
	 plugins/cornerMOShv_sf.so \
	 plugins/cornerMOShv_fs.so \
	 plugins/cornerCAP_typ.so \
	 plugins/cornerCAP_bcs.so \
	 plugins/cornerCAP_wcs.so \
	 plugins/cornerHBT_typ.so \
	 plugins/cornerHBT_bcs.so \
	 plugins/cornerHBT_wcs.so \
	 plugins/cornerRES_typ.so \
	 plugins/cornerRES_bcs.so \
	 plugins/cornerRES_wcs.so \
	 plugins/capacitor.so \
	 plugins/resistor.so

stat: plugins/cornerMOSlv_tt_stat.so \
	  plugins/cornerMOShv_tt_stat.so \
	  plugins/cornerCAP_typ_stat.so \
	  plugins/cornerHBT_typ_stat.so \
	  plugins/cornerRES_typ_stat.so

# Shared library targets
plugins/%.so: plugins/%.cc
	$(CXX) $(GNUCAP_CPPFLAGS) $(GNUCAP_CXXFLAGS) $< -o $@

# C++ file generation
plugins/psp103_nqs.cc: ../verilog-a/psp103/psp103_nqs.va
	gnucap-mg-vams $(GCMG_FLAGS) -o $@ --cc $<

plugins/r3_cmc.cc: ../verilog-a/r3_cmc/r3_cmc.va
	gnucap-mg-vams $(GCMG_FLAGS) -o $@ --cc $<

plugins/mosvar.cc: ../verilog-a/mosvar/mosvar.va
	gnucap-mg-vams $(GCMG_FLAGS) -o $@ --cc $<

plugins/cornerMOSlv_%.cc: models/cornerMOSlv.va
	gnucap-mg-vams $(GCMG_FLAGS) -D mos_$* -D "mc_ok 1" -o $@ --cc $<

plugins/cornerMOShv_%.cc: models/cornerMOShv.va
	gnucap-mg-vams $(GCMG_FLAGS) -D mos_$* -D "mc_ok 1" -o $@ --cc $<

plugins/cornerCAP_%.cc: models/cornerCAP.va
	gnucap-mg-vams $(GCMG_FLAGS) -D cap_$* -D "mc_ok 1" -o $@ --cc $<

plugins/cornerHBT_%.cc: models/cornerHBT.va
	gnucap-mg-vams $(GCMG_FLAGS) -D hbt_$* -D "mc_ok 1" -o $@ --cc $<

plugins/cornerRES_%.cc: models/cornerRES.va
	gnucap-mg-vams $(GCMG_FLAGS) -D res_$* -D "mc_ok 1" -o $@ --cc $<

plugins/%.cc: models/%.va
	gnucap-mg-vams $(GCMG_FLAGS) -o $@ --cc $<

# va generation (only when REGENERATE_VA=1 is set)
ifdef REGENERATE_VA
models/%.va: ../xyce/models/%.lib
	$(SPAKCONVERT) $< $@ --input-simulator xyce --output-simulator gnucap $(SPAKFLAGS)
endif

.PHONY: clean distclean stat

# Remove build artifacts only
clean:
	rm -f plugins/*.cc plugins/*.so

# Remove build artifacts and generated .va files that can be regenerated from .lib files
distclean: clean
	rm -f models/corner*.va \
	      models/capacitors_*.va \
	      models/resistors_*.va \
	      models/sg13g2_hbt_*.va \
	      models/sg13g2_moshv_*.va \
	      models/sg13g2_moslv_*.va
