# © 2025 Mouvement Français pour un Revenu de Base http://www.revenudebase.info
#
# SPDX-License-Identifier: Apache-2.0+
# SPDX-FileContributor:    Henri  GEIST


TARGETS       := $(patsubst %.bats, %.tap, $(wildcard *.bats))
SPECS_DIR     := ../specs
RESULTS_DIR   := results
SHELL_SCRIPTS := $(wildcard *.bash *.sh)

SHELL         := /bin/sh
REQFLOW       := reqflow stat -s
TAP_CONSUMER  := tappy --verbose
SHELLCHECK    := shellcheck

BATS_FLAGS    := -F tap13

define REQFLOW_CONF =
document $(@:.req=-specs)
   -path        "$(SPECS_DIR)/$(@:.req=-specs.adoc)"
   -type        "txt"
   -sort        "alphanum"
   -start-after "^\\s*== Exigences"
   -req         "^\\|\\s*<<(F[pc]_[1-9]([0-9_]*[0-9])?)>>"
   -end-req     "^\\|==="
   -stop-after  "^\\s*== Raisons d'êtres"

document $(@:.req=-tests)
   -path       "$(RESULTS_DIR)/$(@:.req=.tap)"
   -type       "txt"
   -sort       "alphanum"
   -stop-after "^Bail out!"
   -req        "^((not )?ok\\s+\\d+)\\s"
   -end-req    "^1[.][.]"
   -ref        "^[no][ok].*\\s+\\d+\\stest_(F[pc]_[1-9]([0-9_]*[0-9])?)"
   -nocov
endef

.POSIX:
.SUFFIXES:
.SECONDARY:
.DELETE_ON_ERROR:

all: check

build: $(addprefix $(RESULTS_DIR)/, $(TARGETS))

check: $(patsubst %.tap, check_%, $(TARGETS))
	$(SHELLCHECK)   $(wildcard *.bats) $(SHELL_SCRIPTS)
	$(TAP_CONSUMER) $(RESULTS_DIR)

clean:
	$(RM) $(addprefix $(RESULTS_DIR)/, $(TARGETS))
	$(RM) $(TARGETS:.tap=.req)

.PHONY: all build check clean phony

$(foreach ITEM, $(TARGETS),$(eval check_$(ITEM:.tap=): $(RESULTS_DIR)/$(ITEM)))

check_%: %.req phony
	RESULT=$$($(REQFLOW) -c $< 2>&1) || (printf "%s\n" "$$RESULT" >&2 && false)

$(RESULTS_DIR)/%.tap: %.bats $(SHELL_SCRIPTS) $(MAKEFILE_LIST) | $(RESULTS_DIR)
	./$< $(BATS_FLAGS) > $@ || true

%.req: $(MAKEFILE_LIST)
	$(file >$@, $(REQFLOW_CONF))
	sed -i 's/\(^.\+$$\)/\1 \\/1' $@

$(RESULTS_DIR):
	mkdir $@
