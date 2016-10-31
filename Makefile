SHELL := /bin/zsh
Make     = $(MAKE) --no-print-directory
Makefile = $(PWD)/Makefile
Act      = action

# find all directories that are not . files
Dirs     = $(shell find . -type d  -not -path '*/\.*')

actions:
	@$(foreach Dir,$(Dirs),\
	      	(cd $(Dir); \
                 $(MAKE) -f $(Makefile) Dir=$(Dir) $(Act););)

# write this code, assuming you have landed in a $(Dir)
action:
	@echo $(Dir)
	@ls | wc -l


sync:  ready 
	@- git status
	@- git add --all . 
	@- git commit -am "auto commit"
	@- git push origin master

commit:  ready
	@- git add --all . 
	@- git status
	@- git commit -a 
	@- git push origin master

update:; @- git pull origin master
status:; @- git status

ready: gitting 

gitting:
	@git config --global credential.helper cache
	@git config credential.helper 'cache --timeout=3600'

you:
	@git config --global user.name "Your name"
	@git config --global user.email your@email.address

rahlk:
	@git config --global user.name "Rahul Krishna"
	@git config --global user.email i.m.ralk@gmail.com


