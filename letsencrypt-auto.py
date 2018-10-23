#!/usr/bin/python36
# -*- coding: utf-8 -*-

import logging
import os
import sys
import re
from tempfile import mkdtemp
from subprocess import Popen
import subprocess


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


class CertRenew:
    OPENSSL = '/usr/bin/openssl'
    CERTBOT = '/usr/bin/certbot'
    WEBROOT = '/home/keys/$DOMAINNAME'
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


def get_targets() -> list:
    TARGETS = '/etc/httpd/conf.d/vhost_*.conf'
    logger.debug('arguments(%s): %s', len(sys.argv), ', '.join(sys.argv))
    if len(sys.argv) < 3:
        logger.debug('get from target lists: %s', TARGETS)
        domains = list() # XXX
    else:
        logger.debug('get from command line argument(s).')
        domains = sys.argv[2:]
    logger.debug('targets: %s', ', '.join(domains))
    return domains

def main():
    logger.debug('staring program')
    targets = get_targets()
    for domain in targets:
        logger.info('run for: %s', domain)
        le = CertRenew(domain)
        logger.info('privkey: %s', le.privkey)
        le.make_privkey()
        logger.info('csr: %s', le.csr)
        le.make_csr()


if __name__ == "__main__":
    main()
