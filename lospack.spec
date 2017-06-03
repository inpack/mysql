project.name = mysql57
project.version = 5.7.18
project.vendor = mysql.com
project.homepage = https://www.mysql.com
project.groups = dev/db
project.description = The world's most popular open source database

%build
PREFIX="{{.project__prefix}}"

cd {{.lospack__pack_dir}}/deps

if [ ! -f "mysql-5.7.18.tar.gz" ]; then
    wget https://github.com/mysql/mysql-server/archive/mysql-5.7.18.tar.gz
fi
if [ ! -d "mysql-server-mysql-5.7.18" ]; then
    tar -zxf mysql-5.7.18.tar.gz
fi


if [ ! -f "boost_1_59_0.tar.bz2" ]; then
    wget http://sourceforge.net/projects/boost/files/boost/1.59.0/boost_1_59_0.tar.bz2
fi
if [ ! -d "boost_1_59_0" ]; then
    tar -jxf boost_1_59_0.tar.bz2
fi

mkdir -p {{.buildroot}}/{bin,etc/my.cnf.d,data,lib64/mysql/plugin,files,run,log}

install ../misc/etc/my.cnf.default {{.buildroot}}/etc/my.cnf.default
install ../misc/etc/my.server.cnf.default {{.buildroot}}/etc/my.server.cnf.default

cd mysql-server-mysql-5.7.18
cmake . -DWITH_BOOST=../boost_1_59_0 \
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

make mysql -j2
make mysqld -j2
make mysqladmin -j2
make connection_control -j2


strip -s sql/mysqld
install sql/mysqld {{.buildroot}}/bin/mysql57d

strip -s client/mysql
install client/mysql {{.buildroot}}/bin/mysql57

strip -s client/mysqladmin
install client/mysqladmin {{.buildroot}}/bin/mysql57admin

strip -s plugin/connection_control/connection_control.so
install plugin/connection_control/connection_control.so {{.buildroot}}/lib64/mysql/plugin/

rsync -av sql/share/* {{.buildroot}}/share/

%files
