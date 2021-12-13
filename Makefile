.PHONY: doc-html install install-bin install-manpage install-subcommands  help install-bashcompletion install-conf install-scripts uninstall

PROJECT := naivecalendar

help:
	@echo "Please configure your installation by editing Makefile.config"
	@echo ""
	@echo "Usage:"
	@echo "		install : perfom install following user conf (Makefile.config)" 
	@echo "		uninstall : delete all installed files"
	@echo "		doc-html : Build doc html"

# Get user install configuration
#################################

CONFIG_FILE := Makefile.config

ifeq ($(wildcard $(CONFIG_FILE)),)
$(error $(CONFIG_FILE) not found.)
endif
include $(CONFIG_FILE)

install_list := 
ifeq ($(INSTALL_SUBCOMMANDS),True)
install_list += install-subcommands
endif

ifeq ($(INSTALL_ADDONS),True)
install_list += install-addons
endif

ifeq ($(INSTALL_ALL_THEMES),True)
install_list += install-themes
else
install_list += install-theme-default
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

ifeq ($(PREFIX),)
prefix:=/usr/local
else
prefix:=$(PREFIX)
endif

bindir := $(prefix)/bin
datadir := $(prefix)/share/naivecalendar
man1dir := $(prefix)/share/man/man1

ifeq ($(COMPLETION_PATH),)
completiondir := $(prefix)/share/bash-completion/completions
else
completiondir := $(COMPLETION)
endif

#
test:
	echo "installation: $(install_list)"

install-exec:
	@echo "set installation path to $(DESTDIR)${prefix}"
	@sed -e "s:\(PREFIX=\).*:\1$(DESTDIR)${prefix}:g" naivecalendar > naivecalendar.tmp
	@echo "copy \e[1;36mbin script\e[0;32m  -->  $(DESTDIR)$(bindir)/naivecalendar"
	@install -D --mode=755 naivecalendar.tmp $(DESTDIR)$(bindir)/naivecalendar
	@rm naivecalendar.tmp

install-scripts:
	@echo "copy \e[1;36mscript files\e[0;32m  -->  $(DESTDIR)$(datadir)/naivecalendar.sh" 
	@install -D --mode=755 src/naivecalendar.sh $(DESTDIR)$(datadir)/naivecalendar.sh
	@install -D --mode=755 src/naivecalendar.py $(DESTDIR)$(datadir)/naivecalendar.py

install-subcommands:
	@echo "copy \e[1;36msubcommands\e[0;32m  -->  $(DESTDIR)$(datadir)/"
	@install -D --mode=755 tools/naivecalendar-update $(DESTDIR)$(datadir)/tools/naivecalendar-update
	@install -D --mode=755 tools/naivecalendar-add-event $(DESTDIR)$(datadir)/tools/naivecalendar-add-event

install-events:
	@echo "copy \e[1;36mevents config files\e[0;32m  -->  $(DESTDIR)$(datadir)/themes/"
	@cp -r src/global $(DESTDIR)$(datadir)

install-addons:
	@echo "copy \e[1;36maddons scripts\e[0;32m  -->  $(DESTDIR)$(datadir)/themes/"
	@cp -r src/scripts $(DESTDIR)$(datadir)

install-themes:
	@echo "copy \e[1;36mall themes files\e[0;32m  -->  $(DESTDIR)$(datadir)/themes/"
	@cp -r src/themes $(DESTDIR)$(datadir)

install-theme-default:
	@echo "copy \e[1;36mdefault theme\e[0;32m  -->  $(DESTDIR)$(datadir)/themes/"
	@install -D --mode=644 src/themes/classic_dark_extended.rasi $(DESTDIR)$(datadir)/themes/classic_dark_extended.rasi
	@install -D --mode=644 src/themes/classic_dark_extended.cfg $(DESTDIR)$(datadir)/themes/classic_dark_extended.cfg
	@install -D --mode=644 src/themes/common/theme_dark.rasi $(DESTDIR)$(datadir)/themes/common/theme_dark.rasi
	@install -D --mode=644 src/themes/common/position.rasi $(DESTDIR)$(datadir)/themes/common/position.rasi
	@install -D --mode=644 src/themes/common/shape_extended.rasi $(DESTDIR)$(datadir)/themes/common/shape_extended.rasi
	@install -D --mode=644 src/themes/common/shape_base.rasi $(DESTDIR)$(datadir)/themes/common/shape_base.rasi
	@install -D --mode=644 src/themes/common/theme_base.rasi $(DESTDIR)$(datadir)/themes/common/theme_base.rasi

install-manpage:
	@echo "copy \e[1;36mmanpages\e[0;32m  -->  $(DESTDIR)$(man1dir))/"
	@install -D --mode=644 "debian/naivecalendar.1" "$(DESTDIR)$(man1dir)/naivecalendar.1"
	@install -D --mode=644 "debian/naivecalendar-update.1" "$(DESTDIR)$(man1dir)/naivecalendar-update.1"
	@install -D --mode=644 "debian/naivecalendar-add-event.1" "$(DESTDIR)$(man1dir)/naivecalendar-add-event.1"

install-bashcompletion:
	@echo "copy \e[1;36mbash-completion\e[0;32m  -->  $(DESTDIR)$(completiondir)/"
	@sed -e "s:/usr:$(DESTDIR)$(prefix):g" debian/naivecalendar.bash-completion > completion.tmp
	@install -D --mode=755 "completion.tmp" "$(DESTDIR)$(completiondir)/naivecalendar"
	@rm completion.tmp

install: install-exec install-scripts install-events $(install_list)
#install-full: install-exec install-scripts install-subcommands install-events install-addons install-themes install-manpage install-bashcompletion
#install-minimal: install-exec install-scripts install-theme-default install-events

uninstall:
	rm -f $(DESTDIR)$(bindir)/naivecalendar
	rm -rf $(DESTDIR)$(datadir)/
	rm -rf $(DESTDIR)$(man1dir)/naivecalendar*
	rm -rf $(DESTDIR)$(completiondir)/naivecalendar

doc-html:
	$(MAKE) -C docs/ html

