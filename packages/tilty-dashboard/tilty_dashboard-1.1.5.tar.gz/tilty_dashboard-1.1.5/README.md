Tilty Dashboard
===============

[![Coverage Status](https://coveralls.io/repos/github/myoung34/tilty-dashboard/badge.svg)](https://coveralls.io/github/myoung34/tilty-dashboard)
[![PyPI version](https://img.shields.io/pypi/v/tilty-dashboard.svg)](https://pypi.python.org/pypi/tilty-dashboard/)

This is a minimalistic websocket based dashboard for the Tilt hydrometer.

It's fed by sqlite via [tilty](https://github.com/myoung34/tilty)

![](images/dash.gif)

## Installation And Running ##

### Docker ###

```
# assume $(pwd)/data contains tilt.sqlite that is being written to with tilty
$ docker run -it data:/etc/tilty -p 5000:5000 myoung34/tilty-dashboard:latest
# now hit http://localhost:5000
```

### Pip ###

```
$ pip install tilty-dashboard

$ cat <<EOF >/etc/tilty/prod.config
[webapp]
  host=0.0.0.0
  port=5000
  database_uri="sqlite:////etc/tilty/tilt.sqlite"
EOF

$ cat <<EOF >/etc/tilty/prod.configspec
[webapp]
  host=string(default=127.0.0.1)
  port=string(default=5000)
  database_uri=string(default="sqlite:////etc/tilty/tilt.sqlite")
EOF

$ curl -sL https://raw.githubusercontent.com/myoung34/tilty-dashboard/master/config/prod_gunicorn.py >/etc/tilty/gunicorn.py

$ cd /usr/local/lib/python3.7/dist-packages

$ gunicorn --worker-class eventlet -w 1 -c /etc/tilty/gunicorn.py tilty_dashboard:app
```

## Local Development ##

Seed the database:

```
$ make seed
```

Run it in docker:

```
$ docker-compose up
```

Then just hit http://localhost:5000
