#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys, os
import random, string
import subprocess, shlex 
from ConfigParser import ConfigParser
from HTMLParser import HTMLParser
import shutil
import urllib

# for gnome/gtk clipboard support 
# source http://www.answermysearches.com/python-how-to-copy-and-paste-to-the-clipboard-in-linux/286/
import pygtk
pygtk.require('2.0')
import gtk

anonymized = True
random_length = 8

# parse parameters
if len(sys.argv) < 3:
    print 'More parameters please!'
    sys.exit(1)
if len(sys.argv) > 3 and sys.argv[3] == 'pub':
    anonymized = False
filename = sys.argv[2]
profile_name = sys.argv[1]
profile_path = 'profiles/%s' % profile_name
if not os.path.exists(profile_path):
    print 'Profile %s not found.' % profile_name

# load profile settings
print 'Using profile: %s located at %s' % (profile_name, profile_path)
config = ConfigParser()
config.readfp(open(profile_path))
server_path = config.get('server', 'name')
ssh_server = config.get('ssh', 'server')
print 'will connect to %s via ssh' % ssh_server

# generate random part
random_string = ''.join(random.choice(string.hexdigits) for x in range(random_length)).lower() + '/' if anonymized else ''
path = config.get('server', 'path')

# folder or file?
created_htaccess = False
is_dir = os.path.isdir(filename)
if is_dir:
    print '%s is a folder' % filename
    if os.path.exists(filename + '/.htaccess'):
        print '.htaccess file already exists'
    else:
        shutil.copyfile('.htaccess', filename + '/.htaccess')
        created_htaccess = True
    print filename.split('/')
    output_file = filename.split('/')[-2] if filename.split('/')[-1] == '' else filename.split('/')[-1]
else:
    output_file = os.path.basename(filename)

link = 'http://%s/%s%s' % (server_path, random_string, urllib.pathname2url(output_file))
print 'will make %s' % link 


# rsync call
# create folder via ssh
remote_path = '%s/%s%s' % (path, random_string, output_file if is_dir else '')
command_line = ['ssh', '%s@%s' % (config.get('ssh', 'user'), ssh_server), 'mkdir', '-p', "'%s'" % remote_path]
print command_line
subprocess.call(command_line, shell=False)

#command_line = ['rsync', '-avz', '--delete-during', filename, "-e ssh %s@%s:'%s'" % (config.get('ssh', 'user'), ssh_server, remote_path)]
command_line = 'rsync -avz --delete-during "%s" -e ssh %s@%s:"\'%s\'"' % (filename, config.get('ssh', 'user'), ssh_server, remote_path)

print command_line
# print shlex.split(command_line)
# sys.exit(0)
subprocess.call(command_line, shell=True)

# delete again
if created_htaccess:
    os.remove(filename + '/.htaccess')

# print link
clipboard = gtk.clipboard_get()
print 'your link %s has been copied to clipboard' % link
clipboard.set_text(link)
clipboard.store()
