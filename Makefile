##
## Makefile (for developers)
##

package_name = deform_ext_autocomplete

.PHONY: coverage
coverage:
	coverage run setup.py test -q
	coverage html -d "$(tmp_cov_dir)"
	open "$(tmp_cov_dir)/index.html"
	@echo "Coverage information is available at '$(tmp_cov_dir)'."

cov: coverage

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

.PHONY: test
test:
	PYTHONWARNINGS=all python setup.py test

.PHONY: upload
upload:
	python setup.py sdist upload

.PHONY: clean
clean:
	rm -rf .coverage
	rm -rf ./dist/
	find . -name "*.pyc" | xargs rm -f
