PYTHON ?= python3
ENTRY ?= main

.PHONY: all build check submission test doctor package clean

all: check build

build:
	$(PYTHON) scripts/build.py $(ENTRY)

check:
	$(PYTHON) scripts/check.py

submission:
	$(PYTHON) scripts/check.py --submission

test:
	$(PYTHON) -m unittest discover -s tests -v

doctor:
	$(PYTHON) scripts/doctor.py

package:
	$(PYTHON) scripts/package.py

clean:
	$(PYTHON) -c "from pathlib import Path; import shutil; p=Path('build'); p.is_symlink() and (_ for _ in ()).throw(SystemExit('Refusing symlinked build directory')); p.is_dir() and shutil.rmtree(p)"
