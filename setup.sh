export PIPENV_VENV_IN_PROJECT=true

pipenv --three
echo $PYTHONPATH
echo $PATH
pipenv install ray
#pipenv install git+http://github.com/ray-project/ray#egg=ray
pipenv lock --clear
pipenv shell
pip install psutil
