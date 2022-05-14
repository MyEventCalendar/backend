# EventCalendar

### build docker image
```shell
docker build . -t event-calendar 
```

### start docker container
```shell
docker run -d -p 8000:8000 -v /path/to/your/data:/app/src/db event-calendar
```
