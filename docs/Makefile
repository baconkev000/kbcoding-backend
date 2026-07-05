# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = ./_build
APP = /app

.PHONY: help livehtml apidocs Makefile

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O) -c .

# Build, watch and serve docs with live reload (docs sources only; do not watch /app)
livehtml:
	sphinx-autobuild -b html --host 0.0.0.0 --port 9000 \
		--ignore "*/media/*" \
		--ignore "*/_build/*" \
		--ignore "*/staticfiles/*" \
		--ignore "*/node_modules/*" \
		--ignore "*/.git/*" \
		--ignore "*/.angular/*" \
		-c . $(SOURCEDIR) $(BUILDDIR)/html

# Outputs rst files from django application code
apidocs:
	sphinx-apidoc -o $(SOURCEDIR)/api $(APP)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O) -c .
