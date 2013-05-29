#========================#
# - Dawawin Makefile 0.1 #
# - Under Waqf license   #
# - Date 1434/07/14      #
#========================#
	
SHELL=/bin/bash
PYTHON=`which python`
DESTDIR=/
.PHONY: all install uninstall

all:
	@echo "You can use install uninstall args , if you want to install in system use root permissions .";

install:
	$(PYTHON) setup.py install --root $(DESTDIR) --record=installed-files.txt

uninstall:		
	@bash uninstall
