#!/bin/bash
echo tecno2020Red | sudo -S docker exec plan-management-db /mysql_config.sh
sleep 10
sudo docker-compose stop plan-management
sudo docker-compose up -d