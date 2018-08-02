#!/usr/bin/python36
# -*- coding: utf-8 -*-

from tempfile import mkdtemp
from subprocess import Popen
import subprocess

TARGETS = list()
OPENSSL = '/usr/bin/openssl'
CERTBOT = '/usr/bin/certbot'


class CertRenew:

    def __init__(self, domainname: str):
        self.domainname = domainname
        tmpdir_prefix = 'le_{}_'.format(domainname)
        self.tmpdir = mkdtemp(prefix=tmpdir_prefix)
        self.privkey = '{}/privkey.pem'.format(self.tmpdir)
        self.csr = '{}/csr.der'.format(self.tmpdir)
        self.server = 'https://acme-v01.api.letsencrypt.org/directory'

    def make_privkey(self):
        cmd = ' '.join([
            OPENSSL,
            'ecparam',
            '-out {}'.format(self.privkey),
            '-name prime256v1 -genkey',
        ])
        subprocess.call(cmd, shell=True)

    def make_csr(self):
        cmd = ' '.join([
            OPENSSL,
            'req',
            '-new',
            '-key {}'.format(self.privkey),
            '-sha256 -nodes',
            '-outform der',
            '-out {}'.format(self.csr),
            '-subj "/CN={}/C=JP"'.format(self.domainname),
        ])
        subprocess.call(cmd, shell=True)

    def run_certbot(self):
        cmd = ' '.join([
            CERTBOT,
            'certonly -t -a webroot',
            '--webroot-map {}'.format(''),
            '--redirect',
            '--csr {}'.format(self.csr),
            '--server {}'.format(self.server),
        ])
        subprocess.call(cmd, shell=True)


for target in TARGETS:
    CertRenew(target)