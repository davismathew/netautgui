from os import path
import sys
import ansible
sys.path.append(path.abspath('/usr/bin'))
from subprocess import call


call(["ansible-playbook", "-i", "hosts","some.yml"])