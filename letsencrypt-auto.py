#!/usr/bin/python36
# -*- coding: utf-8 -*-

from tempfile import mkdtemp
from subprocess import Popen
import subprocess

TARGETS = list()


class CertRenew:
    OPENSSL = '/usr/bin/openssl'
    CERTBOT = '/usr/bin/certbot'
    # ACME_SERVER = 'https://acme-v01.api.letsencrypt.org/directory'

    def __init__(self, domainname: str):
        self.domainname = domainname
        tmpdir_prefix = 'le_{}_'.format(domainname)
        self.tmpdir = mkdtemp(prefix=tmpdir_prefix)
        self.privkey = '{}/privkey.pem'.format(self.tmpdir)
        self.csr = '{}/csr.der'.format(self.tmpdir)
        self.openssl_cnf = '{}/openssl.cnf'.format(self.tmpdir)

    def make_openssl_cnf(self):
        with open(self.openssl_cnf, 'w') as f:
            f.write('''
[req]
distinguished_name = dn
[dn]
[SAN]
subjectAltName=DNS:{}
            ''').format(self.domainname)

    def make_privkey(self):
        cmd = ' '.join([
            self.OPENSSL,
            'ecparam',
            '-out {}'.format(self.privkey),
            '-name prime256v1 -genkey',
        ])
        subprocess.call(cmd, shell=True)

    def make_csr(self):
        cmd = ' '.join([
            self.OPENSSL,
            'req',
            '-new',
            '-key {}'.format(self.privkey),
            '-sha256 -nodes',
            '-outform der',
            '-out {}'.format(self.csr),
            '-subj "/CN={}/C=JP"'.format(self.domainname),
            '-config {}'.format(self.openssl_cnf),
        ])
        subprocess.call(cmd, shell=True)

    def run_certbot(self):
        cmd = ' '.join([
            self.CERTBOT,
            'certonly -t -a webroot',
            '--webroot-map {}'.format(''),
            '--redirect',
            '--csr {}'.format(self.csr),
            # '--server {}'.format(self.server),
        ])
        
        subprocess.call(cmd, shell=True)

    def install_certs(self):
        pass
        

# for target in TARGETS:
#     CertRenew(target)

le = CertRenew('keys.jp')
print('privkey: {}').format(le.privkey)
le.make_privkey()
print('csr: {}').format(le.csr)
le.make_csr()
