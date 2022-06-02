# backend

### Before start Django server, PostgreSQL server should be ready!

### Create virtual environment
```shell
python3 -m venv env
```

### Activate virtual environment
```shell
. ./env/bin/activate
```

### Install packages from requirements.txt
```shell
python3 -m pip install -r requirements.txt
```

### Export environment variables
```shell
export \
POSTGRES_USER=YOUR_POSTGRES_USER \
POSTGRES_PASSWORD=YOUR_POSTGRES_PASSWORD \
POSTGRES_HOST=YOUR_POSTGRES_HOST \
POSTGRES_PORT=YOUR_POSTGRES_PORT \
POSTGRES_DATABASE=YOUR_POSTGRES_DATABASE \
DJANGO_PORT=YOUR_DJANGO_PORT \
DJANGO_HOST=YOUR_DJANGO_HOST
```

### Perform Django migrations
```shell
python3 manage.py migrate
```

### Start server Django
```shell
python3 manage.py runserver
```