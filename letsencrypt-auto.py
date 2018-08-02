#!/usr/bin/python36
# -*- coding: utf-8 -*-

from subprocess import Popen
from random import choice
import subprocess
import string

TARGETS = list()
OPENSSL = '/usr/bin/openssl'


class LetsEncrypt:

    def __init__(self):
        pass

    def build_path(self):
        rand_len = 8
        rand_src = string.ascii_letters + string.digits
        self.rand_path = ''.join(choice(rand_src) for i in range(rand_len))
        self.privkey = '/tmp/{}/privkey.pem'.format(self.rand_path)
        self.csr = '/tmp/{}/csr.der'.format(self.rand_path)

    def __check_file_exist(self, target: str):
        pass

    def make_privkey(self):
        # XXX check file existency
        cmd = ' '.join([
            OPENSSL,
            'ecparam',
            '-out {}'.format(self.privkey),
            '-name prime256v1 -genkey',
        ])
        subprocess.call(cmd, shell=True)

    def make_csr(self, target_path: str):
        infile = ''
        cmd = ' '.join([
            OPENSSL,
            'req',
            '-new',
            '-key {}',format(self.privkey),
            '-sha256 -nodes -outform der',
            '-out {}'.format(self.csr),
            '-in {}'.format(infile),
            '-subj "/CN={}'.format(''),
            '-reqexts SAN -config',
        ])
        subprocess.call(cmd, shell=True)

# for target in TARGETS
#     target_path = '{}_{}'.format(target, get_temp_file())
#     make_privkey(target_path)

#     csr_file = '/etc/letsencrypt/der_keys/$HOSTNAME/csr.der'
#     arg = 

#     Popen()
