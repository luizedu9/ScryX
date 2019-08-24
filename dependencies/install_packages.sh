
#######################################################################################################
#                                                                                                     #
#                                  INSTALAÇÃO DOS PACOTES NECESSARIOS                                 #
#                                                                                                     #
#######################################################################################################

# MongoDB
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
echo "mongodb-org hold" | sudo dpkg --set-selections
echo "mongodb-org-server hold" | sudo dpkg --set-selections
echo "mongodb-org-shell hold" | sudo dpkg --set-selections
echo "mongodb-org-mongos hold" | sudo dpkg --set-selections
echo "mongodb-org-tools hold" | sudo dpkg --set-selections

sudo apt-get update

sudo apt-get install build-essential libssl-dev

# Mudar vx.xx.x para a mais atual em: https://github.com/nvm-sh/nvm
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash
# Fechar e reabrir terminal

# Ver as versões
nvm ls-remote

# Escolher a ultima versão
nvm install v12.8.1

npm i npm -g

npm install -g @vue/cli

npm install -g @vue/cli-init

sudo apt-get install python3-dev

pip3 install pipenv

pip3 install flask

pipenv install flask marshmallow

pip3 install bson

# Multi-objective optimization utilities
# https://esa.github.io/pagmo2/docs/python/utils/py_mo_utils.html
pip3 install pygmo

pip3 install matplotlib