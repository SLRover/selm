# Simple Enterprise License Manager (SELM)

![GitHub](https://img.shields.io/github/license/SLRover/selm)

## Description

SELM is WEB-application for software license management. Just manage your licenses painlessly.

## Installation

You can use the Docker or installation from source.

### Docker

For evaluate and testing just run:

```commandline
docker run -d -p 8000:8000 selm:latest
```

If you using SELM in production, you need to run container with volumes:

```commandline
docker run -d -p 8000:8000 -v /opt/selm/data:/app/data -v /opt/selm/config:/app/config selm:latest
```

And visit address `http://youaddress:8000`

### Source

You need to use Python 3.7 or higher.

Clone repository:

```commandline
git clone https://github.com/SLRover/selm.git
```

Create virtual environment:

```commandline
python3 -m venv venv
```

Activate environment:

```commandline
source venv/bin/activate
```

Setup requirements:

```commandline
pip install -r requirements.txt
```

Run application (specify at least two workers):

```commandline
gunicorn -b 0.0.0.0:8000 wsgi:app -w 2 --daemon
```

And visit address `http://youaddress:8000`

### Best practice

For safe use run your application with reverse proxy (for example [NGINX](http://nginx.org)) and SSL.

```
|--------|    SSL    |---------|           |--------|           |------------|
|  User  |<--------->|  NGINX  |<--------->|  SELM  |<--------->|  Database  |
|--------|           |---------|           |--------|           |------------|
```

## Usage

After the first launch you need to specify database. Select SQLite for evaluation and testing or PostgreSQL for production.

Then register a new user and enjoy.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.



## License
[MIT](https://choosealicense.com/licenses/mit/)
