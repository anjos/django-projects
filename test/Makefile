# Created by Andre Anjos <andre.dos.anjos@cern.ch> 
# Thu  4 Mar 23:14:52 2010 

# a little make function to ease the administration task
admin=PYTHONPATH=$(2) ../sw/bin/django-admin.py $(1) --settings=settings
python=../sw/bin/python
project=$(shell basename $(shell dirname `pwd`))
python_version=$(shell ../sw/bin/python -c 'import sys; print "%d.%d" % sys.version_info[0:2]')
media_link=if [ ! -L $(1) ]; then ln -s ../sw/lib/python$(python_version)/site-packages/$(1)/media $(1); fi

all:
	@echo "Project:" $(project)
	@echo "Python:" python$(python_version)
	@if [ ! -e db.sql3 ]; then $(MAKE) admin; fi
	@if [ ! -L $(project) ]; then ln -s ../$(project)/media $(project); fi
	@$(call media_link,djit)
	$(call admin,runserver,..:.) 8080

admin:
	$(call admin,syncdb,.) --noinput
	$(python) ./initial_data.py

clean:
	@find . -name '*.pyc' -print0 | xargs -0 rm -f
	@find . -name '*~' -print0 | xargs -0 rm -f

mrproper: clean
	@rm -f $(project)
	@rm -f djit
	@rm -f *.sql3
