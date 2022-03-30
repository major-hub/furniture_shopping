# furniture_shopping

Online Furniture e-Commerce by iFraganus
___

# pip

```
python3 -m venv venv
source ./venv/bin/activate

python -m pip install -U pip
pip install -r requirements.txt
```

___

# postgres

```
CREATE DATABASE furniture_shopping WITH OWNER solijonov;
GRANT ALL ON DATABASE furniture_shopping TO solijonov;
```

___

# Systemd service [furniture_shopping.service]

```
[Unit]
Description=Systemd service daemon for furniture_shopping
Before=nginx.service
After=network.target

[Service]
User=major
Group=major
WorkingDirectory=/home/major/furniture_shopping
ExecStart=/home/major/furniture_shopping/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/major/furniture_shopping/gunicorn.sock project.wsgi:application
Restart=always
SyslogIdentifier=gunicorn

[Install]
WantedBy=multi-user.target
```

___

# Nginx [furniture_shopping_backend]

```
server {
    listen 80;
    server_name ? www.?;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static {
        alias /home/major/furniture_shopping/static;
    }
    
    location /media  {
        alias /home/major/furniture_shopping/media;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/major/furniture_shopping/gunicorn.sock;
    }
}
```

___

# Nginx [furniture_shopping_frontend]

```
server {
    listen 80;
    server_name ? www.?;

    root /home/major/frontend/?/build;

    index index.html index.htm index.nginx-debian.html;

    location / {
        try_files $uri $uri/ /index.html;
        # try_files $uri $uri/ =404;
    }
}
```
