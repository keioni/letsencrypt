#!/bin/bash -x

if [ -z $1 ]; then
    echo 'error: hostname required.'
    exit
fi

webroot=/home/keys/www/
hostname=$1
date=`date +%Y%m%d`
certdir=/etc/letsencrypt/ecdsa/$hostname/$date

if [ -e $certdir ]; then
    echo 'warn: cert directory still exists.'
    rm -rf $certdir
fi
mkdir -p $certdir

cat << "__EOF__" > $certdir/openssl.cnf
[req]
distinguished_name = dn
[dn]
[SAN]
__EOF__
echo subjectAltName=DNS:"$hostname" >> $certdir/openssl.cnf

openssl ecparam -out $certdir/privkey.pem -name prime256v1 -genkey
openssl req -new -key $certdir/privkey.pem -sha256 -nodes -outform der -out $certdir/csr.der -subj "/CN=$hostname" -reqexts SAN -config $certdir/openssl.cnf

openssl req -in $certdir/csr.der -inform der -text

cd $certdir
certbot certonly -a webroot -w $webroot/$hostname -d $hostname --csr $certdir/csr.der

mv $certdir/0000_cert.pem $certdir/cert.pem
mv $certdir/0000_chain.pem $certdir/chain.pem
mv $certdir/0001_chain.pem $certdir/fullchain.pem
mv $certdir/privkey.pem $certdir/privkey.pem

mkdir -p /etc/letsencrypt/live/$hostname
ln -sf $certdir/cert.pem /etc/letsencrypt/live/$hostname/cert.pem
ln -sf $certdir/chain.pem /etc/letsencrypt/live/$hostname/chain.pem
ln -sf $certdir/fullchain.pem /etc/letsencrypt/live/$hostname/fullchain.pem
ln -sf $certdir/privkey.pem /etc/letsencrypt/live/$hostname/privkey.pem
