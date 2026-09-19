# PACT kit — maintainer commands.
# Adopters never need this file. `make check` is exactly what CI runs.
# Windows without make: check.ps1.

# python3 on Unix CI; `python` on Windows if python3 is not on PATH.
ifeq ($(OS),Windows_NT)
  PY ?= python
else
  PY ?= python3
endif
SCRIPTS := automation/scripts

.PHONY: check leaks links entry canon schemas mapping instance test matrix fix-canon adapters help

help:
	@echo "make check     run every verification level (what CI runs)"
	@echo "make leaks     L0  origin traces in any file"
	@echo "make links     L1  internal links and anchors resolve; no orphan files"
	@echo "make entry     L1  every runtime pointer file exists and matches the generator"
	@echo "make schemas   L2  every YAML validates against schemas/"
	@echo "make mapping   L2  every track covers 100% of neutral symbols"
	@echo "make test      L3  pytest for validate_pr and friends"
	@echo "make canon     L5  fenced fragments match their source; no duplicated canon"
	@echo "make adapters  L5  every adapter's out/ matches a fresh generation"
	@echo "make instance  L6  example and profile instances are complete and coherent"
	@echo "make matrix    regenerate docs/compatibility-matrix.md"
	@echo "make fix-canon rewrite fenced copies from templates/_fragments/"

check: leaks links entry schemas mapping test canon adapters instance
	@echo
	@echo "All checks passed."

leaks:
	@$(PY) $(SCRIPTS)/check_leaks.py

links:
	@$(PY) $(SCRIPTS)/check_links.py

entry:
	@$(PY) $(SCRIPTS)/entry_points.py --check

schemas:
	@$(PY) $(SCRIPTS)/check_schemas.py

mapping:
	@$(PY) $(SCRIPTS)/check_mapping.py

test:
	@$(PY) -m pytest automation/tests -q

canon:
	@$(PY) $(SCRIPTS)/check_canon.py

instance:
	@$(PY) $(SCRIPTS)/check_instance.py

adapters:
	@$(PY) $(SCRIPTS)/check_adapters.py

matrix:
	@$(PY) $(SCRIPTS)/check_mapping.py --write-matrix

fix-canon:
	@$(PY) $(SCRIPTS)/check_canon.py --fix
