rm dist/* -rf
python setup.py bdist_wheel
twine upload dist/*

