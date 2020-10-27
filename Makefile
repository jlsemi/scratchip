install-local:
	if [ -d "dist" ]; then rm -r dist; fi
	python3 setup.py bdist_wheel
	pip3 uninstall scratchip -y
	pip3 install --user `ls dist/*.whl`
