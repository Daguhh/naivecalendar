.PHONY: install uninstall 


ifeq ($(PREFIX),)
prefix:=/usr
else
prefix:=$(PREFIX)
endif

#prefix = /usr
bindir := $(prefix)/bin
datadir := $(prefix)/share/naivecalendar
man1dir := $(prefix)/share/man/man1
completiondir := $(prefix)/share/bash-completion/completions


install-bin:
	sed -e "s:\(PREFIX=\).*:\1${prefix}:g" naivecalendar > naivecalendar.tmp
	install --mode=755 naivecalendar.tmp $(DESTDIR)$(bindir)/naivecalendar
	rm naivecalendar.tmp

install-scripts:
	install -D --mode=755 src/naivecalendar.sh $(DESTDIR)$(datadir)/naivecalendar.sh
	install -D --mode=755 src/naivecalendar.py $(DESTDIR)$(datadir)/naivecalendar.py

install-subcommands:
	install -D --mode=644 tools/naivecalendar-update $(DESTDIR)$(datadir)/tools/naivecalendar-update
	install -D --mode=644 tools/naivecalendar-add-event $(DESTDIR)$(datadir)/tools/event

install-conf:
	cp -r src/themes $(DESTDIR)$(datadir)/themes
	cp -r src/global $(DESTDIR)$(datadir)/global
	cp -r src/scripts $(DESTDIR)$(datadir)/scripts

install-manpage:
	install -D --mode=644 "debian/naivecalendar.1" "$(DESTDIR)$(man1dir))/naivecalendar.1"
	install -D --mode=644 "debian/naivecalendar-update.1" "$(DESTDIR)$(man1dir))/naivecalendar-update.1"
	install -D --mode=644 "debian/naivecalendar-add-event.1" "$(DESTDIR)$(man1dir))/naivecalendar-add-event.1"

install-bashcompletion:
	install -D --mode=644 "debian/naivecalendar.bash-completion" "$(DESTDIR)$(completiondir)/naivecalendar"

install: install-bin install-scripts install-subcommands install-manpage install-conf install-bashcompletion

uninstall:
	rm $(DESTDIR)$(bindir)/naivecalendar
	rm -r $(DESTDIR)$(datadir)/
	rm -r $(DESTDIR)$(man1dir)/naivecalendar*
	rm -r $(DESTDIR)$(completiondir))/naivecalendar
