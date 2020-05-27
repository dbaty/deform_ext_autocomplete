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

.PHONY:	quality
quality:
	check-manifest
	isort --check-only --diff
	python setup.py check --strict --metadata --restructuredtext
	pylint --reports=no setup.py src/deform_ext_autocomplete tests

.PHONY: clean
clean:
	rm -rf .coverage
	rm -rf ./dist/
	find . -name "*.pyc" | xargs rm -f
