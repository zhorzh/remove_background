from jupyter/scipy-notebook

# install dev tools
user root
run apt-get update --fix-missing
run apt-get install -y ranger
run apt-get install -y vim
run apt-get remove cmdtest
run apt-get install -y curl
run apt-get install -y tesseract-ocr

# install python dependencies
user root
copy ./requirements.txt /srv/requirements.txt
workdir /srv
run pip install -r requirements.txt

copy ./notebooks /home/jovyan/work/notebooks
run mkdir /home/jovyan/work/notebooks/OUTPUT
copy ./test /home/jovyan/work/test

# run jupyter
user jovyan
workdir /home/jovyan
env JUPYTER_ENABLE_LAB=1
env JUPYTER_TOKEN=123
expose 8888
