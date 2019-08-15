
#######################################################################################################
#                                                                                                     #
#                                  INSTALAÇÃO DOS PACOTES NECESSARIOS                                 #
#                                                                                                     #
#######################################################################################################

# Multi-objective optimization utilities
# https://esa.github.io/pagmo2/docs/python/utils/py_mo_utils.html
echo 'Installing pygmo'
pip3 install pygmo

echo ''

echo 'Installing python3-dev'
sudo apt-get install python3-dev

echo ''

echo 'Installing matplotlib'
pip3 install matplotlib