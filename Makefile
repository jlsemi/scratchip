install-local:
	if [ -d "dist" ]; then rm -r dist; fi
	python3 setup.py bdist_wheel
	python3 -m pip uninstall scratchip -y
	python3 -m pip install --user `ls dist/*.whl`
