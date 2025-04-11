# Minimal Makefile for building Sphinx documentation locally

# You can run this from the `docs/` directory:
#   make html        → builds HTML docs in _build/html
#   make clean       → removes build artifacts
#   make latexpdf    → builds a PDF (requires LaTeX installed)

SPHINXBUILD   = sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

.PHONY: help clean html latexpdf

help:
	@echo "Makefile for building the documentation:"
	@echo "  make html      → Build HTML documentation"
	@echo "  make latexpdf  → Build PDF documentation (requires LaTeX)"
	@echo "  make clean     → Remove build directory"

html:
	$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" -a

latexpdf:
	$(SPHINXBUILD) -M latexpdf "$(SOURCEDIR)" "$(BUILDDIR)"

clean:
	rm -rf "$(BUILDDIR)"