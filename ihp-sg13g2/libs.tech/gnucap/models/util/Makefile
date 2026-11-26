include ../../gnucap.mk

MODELGEN_VERILOG = gnucap-mg-vams
MGFLAGS = -I $(shell gnucap-conf --includedir) -I .
TARGET_DIR = ../../plugins/util
TARGETS = idc vpulse
PLUGINS = $(TARGETS:%=$(TARGET_DIR)/%.so)

all: $(PLUGINS)

$(TARGET_DIR):
	mkdir -p $@

$(TARGETS): %: $(TARGET_DIR)/%.so

$(TARGET_DIR)/%.cc: %.va | $(TARGET_DIR)
	$(MODELGEN_VERILOG) $(MGFLAGS) -o $@ --cc $<

$(TARGET_DIR)/%.o: $(TARGET_DIR)/%.cc
	$(CXX) $(GNUCAP_CPPFLAGS) $(CPPFLAGS) -c -fPIC $(GNUCAP_CXXFLAGS) $(CXXFLAGS) $< -o $@

$(TARGET_DIR)/%.so: $(TARGET_DIR)/%.o
	$(CXX) -shared $(GNUCAP_LDFLAGS) $(LDFLAGS) $< -o $@

clean:
	rm -f $(PLUGINS) $(TARGETS:%=$(TARGET_DIR)/%.cc) $(TARGETS:%=$(TARGET_DIR)/%.o)

.PHONY: all clean $(TARGETS)
