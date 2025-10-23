# © 2025 Mouvement Français pour un Revenu de Base http://www.revenudebase.info
#
# SPDX-License-Identifier: Apache-2.0+
# SPDX-FileContributor:    Henri  GEIST

TARGET                  := ton-revenu-universel-specs
LOGO                    := mfrb-logo.svg
PDF_THEME               := mfrb-theme.yml
IMAGES_DIR              := images

SHELL                   := /bin/sh
ASCIIDOCTOR             := asciidoctor
ASCIIDOCTOR_PDF         := asciidoctor-pdf

GIT_DATE                := git log -n 1
GIT_DATE                += --date=format:"%-d/%-m/%-Y"
GIT_DATE                += --pretty=format:"%cd"
COMMIT_DATE             := $(shell $(GIT_DATE))

GIT_DESCRIBE            := git describe --dirty --broken
DIRTY_BROKEN            := \(dirty\|broken\)
COMMIT_COUNT            := \([1-9][0-9]*\)
COMMIT_HASH             := \(g[0-9a-f]\+\)
OPTIONAL_DIRTY_BROKEN   := \(-$(DIRTY_BROKEN)\|\)
PLUS_POST_TAG_ID        := -e 's/-$(COMMIT_COUNT)-$(COMMIT_HASH)$(OPTIONAL_DIRTY_BROKEN)$$/+\1.\2\3/1'
PLUS_DIRTY_BROKEN       := -e 's/-$(DIRTY_BROKEN)$$/+\1/1'
COMMIT_DESCRIPTION      := $(shell $(GIT_DESCRIBE) | sed $(PLUS_POST_TAG_ID) $(PLUS_DIRTY_BROKEN))

ASCIIDOCTOR_OPTIONS     := -a revdate='$(COMMIT_DATE)'
ASCIIDOCTOR_OPTIONS     += -a docdate='$(COMMIT_DATE)'
ASCIIDOCTOR_OPTIONS     += -a revnumber='$(COMMIT_DESCRIPTION)'
ASCIIDOCTOR_OPTIONS     += -a source-highlighter=coderay
ASCIIDOCTOR_OPTIONS     += -a imagesdir=$(IMAGES_DIR)
ASCIIDOCTOR_OPTIONS     += -a experimental
ASCIIDOCTOR_OPTIONS     += -r asciidoctor-diagram

ASCIIDOCTOR_PDF_OPTIONS := $(ASCIIDOCTOR_OPTIONS)
ASCIIDOCTOR_PDF_OPTIONS += -a pdf-theme=$(PDF_THEME)
ASCIIDOCTOR_PDF_OPTIONS += -a autofit-option


.POSIX:
.SUFFIXES:
.SECONDARY:
.DELETE_ON_ERROR:


all: build

build: pdf html

pdf:  $(TARGET).pdf

html: $(TARGET).html

clean:
	@echo Cleaning...
	$(RM) $(TARGET).pdf
	$(RM) $(TARGET).html
	$(RM) -r $(IMAGES_DIR)
	$(RM) -r .asciidoctor

.PHONY: clean all build pdf html

%.pdf: %.adoc $(PDF_THEME) $(LOGO) $(MAKEFILE_LIST)
	@echo $(ASCIIDOCTOR_PDF) $@
	$(ASCIIDOCTOR_PDF) $(ASCIIDOCTOR_PDF_OPTIONS) $<

%.html: %.adoc $(MAKEFILE_LIST)
	@echo $(ASCIIDOCTOR) $@
	$(ASCIIDOCTOR)     $(ASCIIDOCTOR_OPTIONS)     $<
