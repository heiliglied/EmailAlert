# -*- coding: utf-8 -*-
'''
Created on 2017. 5. 6.

@author: Lilie
'''
import configparser
import sys
import socket
import smtplib
import urllib.request
import inspect
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def set_load(self_dir):
    config = configparser.ConfigParser()
    config.read(self_dir + '/setup.ini')
    return config;

def send():
    #print(socket.gethostbyname(socket.getfqdn()))

    if len(sys.argv) == 1 or len(sys.argv) > 4:
        print('Run with options [sendtype] [attach file] [contents file]')
        sys.exit(0)

    if(sys.argv[1] == '-help'):
        print('attach file : add file path')
        print('if not add file with filepath option, please add option none')
        print('contents file : send contents file name')
        sys.exit(0)

    self_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

    config = set_load(self_dir)    
    ip_get = urllib.request.urlopen('http://bot.whatismyipaddress.com')
    ip_address = ip_get.read().decode('utf-8')
    now_ip = config.get('default', 'nowip')

    if now_ip != ip_address:
        config.set('default', 'nowip', ip_address)
        with open(self_dir + '/setup.ini', 'w') as config_set:
            config.write(config_set)

        host = config.get('smtp', 'host')
        port = config.get('smtp', 'port')
        id = config.get('smtp', 'id')
        password = config.get('smtp', 'pass')
    
        if host is None:
            print('host is null')
            sys.exit(0)
        if port is None:
            print('port is null')
            sys.exit(0)
        if id is None:
            print('id is null')
            sys.exit(0)
        if password is None:
            print('password is null')
            sys.exit(0)

        f = open(self_dir + '/' + config.get('default', 'mailreceiver'), 'r')
        receive_list = ''
        while True:
            list = f.readline()
            receive_list = receive_list + list
            if not list: break

        if receive_list is None:
            print('receiver is null')
            sys.exit(0)

        if port == '465':
            smtp = smtplib.SMTP_SSL(host, port)
        else:
            smtp = smtplib.SMTP(host, port)
            smtp.starttls()

        smtp.login(id, password)

        msg = MIMEMultipart()
        msg['Subject'] = config.get('default', 'mailsubject')
        msg['To'] = receive_list
		
        send_text = config.get('default', 'mailtext')
        send_text = send_text.replace("your_ip_address", ip_address)
		
        text = MIMEText(send_text)
        msg.attach(text)

        if len(sys.argv) > 2:
            files = MIMEApplication(open(str(sys.argv[2]), 'rb').read())
            files.add_header('Content-Disposition', 'attachment', filename=str(sys.argv[1]))
            msg.attach(files)
		
            if len(sys.argv) == 4:
                send_text = open(str(sys.argv[3]), 'r').read()
                send_text = send_text.replace("your_ip_address", ip_address)
                text = MIMEText(send_text, 'html')            
                msg.attach(text)
		
        msg['From'] = config.get('smtp', 'id')
        smtp.sendmail(config.get('smtp', 'id'), receive_list, msg.as_string())
        smtp.quit()

if __name__ == '__main__':
    send()
