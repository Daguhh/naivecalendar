.PHONY: html install install-bin install-manpage install-subcommands  help install-bashcompletion install-conf install-scripts uninstall

PROJECT := naivecalendar

# Get user install configuration
#################################

# List of modules to install
install_list :=

# Install all when creating deb package or get user config
ifeq ($(DEB_BUILD),True)
install_list = install-subcommands install-addons install-events install-themes install-manpage install-bashcompletion
$(info **********  Select all modules for debian package build  **********)
else
CONFIG_FILE := Makefile.config
	ifeq ($(wildcard $(CONFIG_FILE)),)
$(error $(CONFIG_FILE) not found.)
	endif
include $(CONFIG_FILE)
endif

# Apply user config
ifeq ($(INSTALL_SUBCOMMANDS),True)
install_list += install-subcommands
endif

ifeq ($(INSTALL_EVENTS),True)
install_list += install-events
endif

ifeq ($(INSTALL_ADDONS),True)
install_list += install-addons
endif

ifeq ($(INSTALL_MANPAGE),True)
install_list += install-manpage
endif

ifeq ($(INSTALL_BASH_COMPLETION),True)
install_list += install-bashcompletion
endif



# Make recip
#############

# Define PATHs

UID := $(shell id --user)

ifeq ($(UID),0)
    prefix = /usr/local
    bindir = $(prefix)/bin
    datadir = $(prefix)/share
    man1dir = $(prefix)/share/man/man1
else
    ifeq ($(XDG_DATA_HOME),)
        XDG_DATA_HOME := $(HOME)/.local
    endif
    prefix = $(XDG_DATA_HOME)
    bindir = $(prefix)/bin
    datadir = $(prefix)/share
    man1dir = $(prefix)/share/man/man1
endif


_:
	@echo "installation: $(install_list)"

help:
	@echo "Please configure your installation by editing Makefile.config"
	@echo ""
	@echo "Usage:"
	@echo "		install : install following user conf (Makefile.config)" 
	@echo "		uninstall : delete all installed files"
	@echo "		html : Build doc html"
	@echo "		deb : Build debian package"
	@echo ""
	@echo "Installation prefix:"
	@echo "  - /usr/local : run as root"
	@echo "  - ~/.local : run as user"
	@echo "  - custom : override prefix run \"make prefix=my_path install\""

install-exec:
	@echo "set installation path to $(DESTDIR)${prefix}"
	@sed -e "s:\(PREFIX=\).*:\1${prefix}:g" naivecalendar > naivecalendar.tmp
	@printf "%s \e[1;36m%-20s\e[0;32m %s %s\n" "copy" "exec file" "-->"  "$(DESTDIR)$(bindir)"
	@install -D --mode=755 naivecalendar.tmp $(DESTDIR)$(bindir)/naivecalendar
	@rm naivecalendar.tmp

install-scripts:
	@printf "%s \e[1;36m%-20s\e[0;32m %s %s\n" "copy" "script files" "-->"  "$(DESTDIR)$(datadir)/naivecalendar"
	@install -D --mode=755 src/naivecalendar.sh $(DESTDIR)$(datadir)/naivecalendar/naivecalendar.sh
	@install -D --mode=755 src/naivecalendar.py $(DESTDIR)$(datadir)/naivecalendar/naivecalendar.py

install-subcommands:
	@printf "%s \e[1;36m%-20s\e[0;32m %s %s\n" "copy" "subcommands" "-->"  "$(DESTDIR)$(datadir)/naivecalendar"
	@install -D --mode=755 tools/naivecalendar-update-themes $(DESTDIR)$(datadir)/naivecalendar/tools/naivecalendar-update-themes
	@install -D --mode=755 tools/naivecalendar-add-event $(DESTDIR)$(datadir)/naivecalendar/tools/naivecalendar-add-event
	@install -D --mode=755 tools/naivecalendar-configure $(DESTDIR)$(datadir)/naivecalendar/tools/naivecalendar-configure
	@sed -e "s:\(DATA_DIR=\).*:\1${datadir}/naivecalendar:g" tools/naivecalendar-theme-generator > generator.tmp
	@install -D --mode=755 generator.tmp $(DESTDIR)$(datadir)/naivecalendar/tools/naivecalendar-theme-generator
	@rm generator.tmp

install-events: install-scripts
	@printf "%s \e[1;36m%-20s\e[0;32m %s %s\n" "copy" "events config files" "-->"  "$(DESTDIR)$(datadir)/naivecalendar"
	@install -D --mode=644 src/global/events.cfg $(DESTDIR)$(datadir)/naivecalendar/global/events.cfg

install-addons: install-scripts
	@printf "%s \e[1;36m%-20s\e[0;32m %s %s\n" "copy" "addons scripts" "-->"  "$(DESTDIR)$(datadir)/naivecalendar"
	@cp -r src/scripts $(DESTDIR)$(datadir)/naivecalendar
	@install -D --mode=644 src/global/custom_actions.cfg $(DESTDIR)$(datadir)/naivecalendar/global/custom_actions.cfg
	@install -D --mode=755 src/scripts/* $(DESTDIR)$(datadir)/naivecalendar/scripts/

install-themes: install-scripts
	@printf "%s \e[1;36m%-20s\e[0;32m %s %s\n" "copy" "all themes" "-->" "$(DESTDIR)$(datadir)/naivecalendar"
	@cp -r src/themes $(DESTDIR)$(datadir)/naivecalendar

install-manpage:
	@printf "%s \e[1;36m%-20s\e[0;32m %s %s\n" "copy" "mmanpages"  "-->"  "$(DESTDIR)$(man1dir)/"
	@install -D --mode=644 "debian/naivecalendar.1" "$(DESTDIR)$(man1dir)/naivecalendar.1"
	@install -D --mode=644 "debian/naivecalendar-update-themes.1" "$(DESTDIR)$(man1dir)/naivecalendar-update-themes.1"
	@install -D --mode=644 "debian/naivecalendar-add-event.1" "$(DESTDIR)$(man1dir)/naivecalendar-add-event.1"
	@install -D --mode=644 "debian/naivecalendar-configure.1" "$(DESTDIR)$(man1dir)/naivecalendar-configure.1"

install-bashcompletion:
	@printf "%s \e[1;36m%-20s\e[0;32m %s %s\n" "copy" "bash-completion"  "-->"  "$(DESTDIR)$(datadir)/bash-completion/completions/"
	@sed -e "s:/usr:$(DESTDIR)$(prefix):g" debian/naivecalendar.bash-completion > completion.tmp
	@install -D --mode=755 "completion.tmp" "$(DESTDIR)$(datadir)/bash-completion/completions/naivecalendar"
	@rm completion.tmp

install: install-exec install-scripts install-themes $(install_list)

uninstall:
	rm -f $(DESTDIR)$(bindir)/naivecalendar
	rm -rf $(DESTDIR)$(datadir)/naivecalendar/
	rm -rf $(DESTDIR)$(man1dir)/naivecalendar*
	rm -f $(DESTDIR)$(datadir)/bash-completion/completions/naivecalendar

html:
	$(MAKE) -C docs/ html

deb:
	debuild -us -uc

clean-all:
	rm -rf ./docs/_build
	debclean

clean-conf_n_cache:
	rm -rf ${HOME}/.config/naivecalendar
	rm -rf ${HOME}/.cache/naivecalendar


