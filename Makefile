##
## Makefile (for developers)
##

package_name = deform_ext_autocomplete

.PHONY: coverage
coverage:
	pytest --cov deform_ext_autocomplete

.PHONY: test
test:
	pytest

.PHONY: docs
docs:
	SPHINXOPTS="-W -n" $(MAKE) -C docs html

.PHONY: dist
dist:
	python setup.py sdist

.PHONY:	qa
qa:
	pep8 -r setup.py || true
	pep8 -r $(package_name) || true
	pep8 -r demo || true
	pyflakes setup.py
	pyflakes $(package_name)
	pyflakes demo

.PHONY: upload
upload:
	python setup.py sdist upload

.PHONY: clean
clean:
	rm -rf .coverage
	rm -rf ./dist/
	find . -name "*.pyc" | xargs rm -f
