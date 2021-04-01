#!/bin/bash
mysql -uroot -p'tecno2020Red' tecnoredDB<<EOFMYSQL
SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));
EOFMYSQL
