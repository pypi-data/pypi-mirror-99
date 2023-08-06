# sharefile-webui

Simple web app for sharing files via URL link. Application is 
based on Python Flask, Flask-Restful and JavaScript for simple file 
administration.

## Usage
```bash
sharefile-webui --help
usage: sharefile-webui [-h] [-o HOST] [-p PORT] [-d SHARE_DIRETORY] [-u ADD_USER] [-r REMOVE_USER] [-l]

Share Files WEB UI v1.0.1

optional arguments:
  -h, --help            show this help message and exit
  -o HOST, --host HOST  APP server host
  -p PORT, --port PORT  APP server port
  -d SHARE_DIRETORY, --share-directory SHARE_DIRETORY
                        Directory where shares are stored.
  -u ADD_USER, --add-user ADD_USER
                        Add admin user in user@password format.
  -r REMOVE_USER, --remove-user REMOVE_USER
                        Remove admin user from users list.
  -l, --list-users      List existing admin users
```
Example:
```bash
sharefile-webui -u username@password
sharefile-webui -p 5555 -d /tmp
```
This example will share `/tmp` directory on http://localhost:5555
By requesting this URL you will be prompted to fill user and password 
to access admin UI for file sharing. For each file of directory you can 
generate secure token. When secure token is generated file could be shared
via URL link.

## Instalation
```bash
pip3 install sharefile-webui
```

### systemd configuration
```bash
PORT=5555
SHARE_DIR=/tmp
echo "[Unit]
Description=ShareFileWebUI

[Service]
ExecStart=/bin/bash -c \"/usr/local/bin/sharefile-webui -p ${PORT} -d ${SHARE_DIR}  >> /var/log/sharefile-webui.log 2>&1 &\"
ExecStop=killall sharefile-webui
ExecRestart=/bin/bash -c \"killall sharefile-webui && /usr/local/bin/sharefile-webui  -p ${PORT} -d ${SHARE_DIR} >> /var/log/sharefile-webui.log 2>&1 &\"
ExecStatus=ps -ax | grep sharefile-webui
Type=forking

[Install]
WantedBy=multi-user.target
" > /lib/systemd/system/sharefile-webui.service
systemctl enable sharefile-webui.service
```
after that is possible to use
```bash
systemctl start sharefile-webui.service
```

## Screenshot
![sharefile-webui screenshot](https://gitlab.com/alda78/sharefile-webui/-/raw/master/sharefile-webui.png)