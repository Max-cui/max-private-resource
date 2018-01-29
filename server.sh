#!/bin/sh

cat <<EOF > /etc/supervisord.conf
[unix_http_server]
file=/tmp/supervisor.sock

[supervisord]
logfile=/tmp/supervisord.log
logfile_maxbytes=50MB
logfile_backups=10
loglevel=info
pidfile=/tmp/supervisord.pid
nodaemon=false
minfds=1024
minprocs=200

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix:///tmp/supervisor.sock ; use a unix:// URL  for a unix socket

[program:data-server]
command=/usr/bin/python /data_server/data-exchange/gunicorn_app.py
autostart=true
autorestart=true
startsecs=3
stderr_logfile=/var/log/data_server_err.log
stdout_logfile=/var/log/data_server.log
EOF

supervisord -c /etc/supervisord.conf
