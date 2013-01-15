build-deb:
	debuild -sa

build-rpm:
	python ./setup.py bdist_rpm --fix-python

check:
	cd test && python test.py

clean:
	rm -rf BalanceLogic.egg-info build dist debian/files debian/python-balance-logic*
