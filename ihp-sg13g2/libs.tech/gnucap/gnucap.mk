# gnucap.mk — Gnucap compiler and linker flags

GNUCAP_CPPFLAGS = $(shell gnucap-conf --cppflags) ${CPPFLAGS}
GNUCAP_CXXFLAGS = $(shell gnucap-conf --cxxflags) -fPIC -shared ${CXXFLAGS}
GNUCAP_LDFLAGS = $(shell gnucap-conf --ldflags) ${LDFLAGS}
