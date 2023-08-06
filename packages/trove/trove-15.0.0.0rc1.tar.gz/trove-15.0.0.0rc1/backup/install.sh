#!/usr/bin/env bash
set -e

export APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1
APTOPTS="-y -qq --no-install-recommends --allow-unauthenticated"

case "$1" in
"mysql5.7")
    curl -sSL https://repo.percona.com/apt/percona-release_latest.$(lsb_release -sc)_all.deb -o percona-release.deb
    dpkg -i percona-release.deb
    percona-release enable-only tools release
    apt-get update
    apt-get install $APTOPTS percona-xtrabackup-24
    rm -f percona-release.deb
    ;;
"mysql8.0")
    curl -sSL https://repo.percona.com/apt/percona-release_latest.$(lsb_release -sc)_all.deb -o percona-release.deb
    dpkg -i percona-release.deb
    percona-release enable-only tools release
    apt-get update
    apt-get install $APTOPTS percona-xtrabackup-80
    rm -f percona-release.deb
    ;;
"mariadb")
    apt-key adv --fetch-keys 'https://mariadb.org/mariadb_release_signing_key.asc'
    add-apt-repository "deb [arch=amd64] http://mirror2.hs-esslingen.de/mariadb/repo/10.4/ubuntu $(lsb_release -cs) main"
    apt-get install $APTOPTS mariadb-backup
    ;;
"postgresql")
    apt-key adv --fetch-keys 'https://www.postgresql.org/media/keys/ACCC4CF8.asc'
    add-apt-repository "deb [arch=amd64] http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main"
    apt-get install $APTOPTS postgresql-client-12
    ;;
*)
    echo "datastore $1 not supported"
    exit 1
    ;;
esac

apt-get clean
rm -rf /var/lib/apt/lists/*
