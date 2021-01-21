## Services

- plan management : http://localhost:8000/login/
- tecnored charts : 
    - fostac: http://localhost:5000/charts/g_fostac/6
    - motor: http://localhost:5000/charts/g_motor/6
    - merma: http://localhost:5000/charts/g_merma/6
    - inca: http://localhost:5000/charts/g_inca/6
- php admin: http://localhost:8080/

## Requirements

Require the next list of ports:

- 8000
- 5000


## Use

### Initialize DB

```
docker-compose up -d plan-management-db
```

### Start/stop services

To start services: 

```
docker-compose up -d plan-management-db
```

To stop services:

```
docker-compose stop
```

