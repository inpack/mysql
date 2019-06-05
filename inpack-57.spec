[project]
name = mysql57
version = 5.7.25
vendor = mysql.com
homepage = https://www.mysql.com
groups = dev/db
description = The world's most popular open source database

%build
PREFIX="/opt/mysql/mysql57"

cd {{.inpack__pack_dir}}/deps

if [ ! -f "mysql-{{.project__version}}.tar.gz" ]; then
    wget https://github.com/mysql/mysql-server/archive/mysql-{{.project__version}}.tar.gz
fi
if [ ! -d "mysql-{{.project__version}}" ]; then
    tar -zxf mysql-{{.project__version}}.tar.gz
fi


if [ ! -f "boost_1_59_0.tar.bz2" ]; then
    wget http://sourceforge.net/projects/boost/files/boost/1.59.0/boost_1_59_0.tar.bz2
fi
if [ ! -d "boost_1_59_0" ]; then
    tar -jxf boost_1_59_0.tar.bz2
fi

mkdir -p {{.buildroot}}/bin
mkdir -p {{.buildroot}}/etc/my.cnf.d
mkdir -p {{.buildroot}}/data
mkdir -p {{.buildroot}}/lib64/mysql/plugin
mkdir -p {{.buildroot}}/lib/plugin
mkdir -p {{.buildroot}}/files
mkdir -p {{.buildroot}}/run
mkdir -p {{.buildroot}}/log

cd mysql-{{.project__version}}
cmake3 . -DWITH_BOOST=../boost_1_59_0 \
  -DCMAKE_INSTALL_PREFIX=$PREFIX \
  -DINSTALL_SBINDIR=bin \
  -DMYSQL_DATADIR=$PREFIX/data \
  -DSYSCONFDIR=$PREFIX/etc \
  -DMYSQL_UNIX_ADDR=$PREFIX/run/mysql.sock \
  -DWITH_INNODB_MEMCACHED=0 \
  -DWITH_EMBEDDED_SERVER=0 \
  -DDEFAULT_CHARSET=utf8 \
  -DWITH_INNOBASE_STORAGE_ENGINE=1 \
  -DWITH_MyISAM_STORAGE_ENGINE=1 \
  -DWITH_MEMORY_STORAGE_ENGINE=1 \
  -DWITH_CSV_STORAGE_ENGINE=1 \
  -DWITH_PERFORMANCE_SCHEMA_STORAGE_ENGINE=1 \
  -DWITHOUT_FEDERATED_STORAGE_ENGINE=1 \
  -DWITHOUT_MRG_MYISAM_STORAGE_ENGINE=1 \
  -DWITHOUT_BLACKHOLE_STORAGE_ENGINE=1 \
  -DWITHOUT_ARCHIVE_STORAGE_ENGINE=1 \
  -DDEFAULT_COLLATION=utf8_general_ci \
  -DMYSQL_USER=action

make mysql -j4
make mysqld -j4
make mysqladmin -j4
make mysqldump -j4
make connection_control -j4
make mysql_ssl_rsa_setup -j4

cd rapid/plugin/group_replication/
make -j4

cd {{.inpack__pack_dir}}/deps/mysql-{{.project__version}}

strip -s sql/mysqld
install sql/mysqld {{.buildroot}}/bin/mysql57d

strip -s client/mysql
install client/mysql {{.buildroot}}/bin/mysql57

strip -s client/mysqladmin
install client/mysqladmin {{.buildroot}}/bin/mysql57admin

strip -s client/mysqldump
install client/mysqldump {{.buildroot}}/bin/mysql57dump

strip -s client/mysql_ssl_rsa_setup
install client/mysql_ssl_rsa_setup {{.buildroot}}/bin/mysql_ssl_rsa_setup

strip -s plugin/connection_control/connection_control.so
install plugin/connection_control/connection_control.so {{.buildroot}}/lib64/mysql/plugin/

strip -s rapid/plugin/group_replication/group_replication.so
install rapid/plugin/group_replication/group_replication.so {{.buildroot}}/lib/plugin/

rsync -av sql/share/* {{.buildroot}}/share/

cd {{.inpack__pack_dir}}
install -m 0644 misc/etc/my.cnf.default {{.buildroot}}/etc/my.cnf.default
install -m 0644 misc/etc/my.server.cnf.default {{.buildroot}}/etc/my.server.cnf.default

cd {{.inpack__pack_dir}}/deps
rm -rf boost_1_59_0
rm -rf mysql-{{.project__version}}


%files
