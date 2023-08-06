# Installation
pip install twine

# To update
rm -rf ./dist
python setup.py sdist bdist_wheel
twine check dist/*
twine upload dist/*
