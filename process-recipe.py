#!/usr/bin/pytho#!/usr/bin/python#!/usr/bin/python#!/usr/bin/python#!/usr/bin/python#!/usr/bin/python#!/usr/bin/pythonn 
''' Process a recipe by downloading and formatting as an ebook, then sending via SMTP '''

import subprocess
import sys
import os
import filecmp
import json
import smtplib

# Deliver to this address
kindle_address = "kindle@address"
personnal_address = "personnal@address"

# SMTP account settings for outgoing mail
smtp_server = 'smtp-mail.outlook.com'
smtp_port = '587'
smtp_username = 'smtp@username'
smtp_password = "smtp@password"

# Path to directories
log_dir = 'logs'
recipe_dir = 'recipes'
ebook_dir = 'ebooks'

# Get command line argument for name of recipe
recipe_name = sys.argv[1]

# Output will be redirected to files when run from cron
#sys.stdout = open( os.path.join( log_dir,'py_out.log'), 'w')
#sys.stderr = open( os.path.join( log_dir,'py_err.log'), 'w')
out_file = open( os.path.join( log_dir, 'out.log'), "w")
err_file = open( os.path.join( log_dir, 'err.log'), "w")
       
# Get name of input and output files
ebook = recipe_name + '.mobi'
recipe = recipe_name + '.recipe'

# If old file exists, delete it
if os.path.exists( os.path.join(ebook_dir, 'old', ebook) ) :
    subprocess.call( ['rm', os.path.join(ebook_dir, 'old', ebook) ],
                     stdout=out_file, stderr=err_file)

# If current file exists, move it to old folder
if os.path.exists( os.path.join(ebook_dir, ebook) ) :
    subprocess.call( ['mv', 
                      os.path.join(ebook_dir, ebook), 
                      os.path.join(ebook_dir, 'old', ebook) ],
                     stdout=out_file, stderr=err_file)

# Build command list
command_list = ['ebook-convert',
os.path.join( recipe_dir, recipe ),
os.path.join( ebook_dir, ebook ),
'--username','lemonde@username',
'--password', "lemonde@password",
'-vv',
'--output-profile', 'kindle']

# Download and format using calibre's command line convert tool
subprocess.call( command_list, stdout=out_file, stderr=err_file )

# If we have downloaded a newer copy :
if True : # not sure how to check this

    print "Sending " + ebook + " over email"

    # Send it over email
    command_list = ['calibre-smtp',
    '-vv',
    '--attachment', os.path.join( ebook_dir, ebook),
    '--subject', 'votre nouvelle edition le monde abonne',
    '--password', smtp_password,
    '--port', smtp_port,
    '--relay', smtp_server,
    '--username', smtp_username,
    smtp_username,
    kindle_address,
    'Automated message sent from Calibre Kindle Server']

    # Send email using calibre's command line SMTP tool
    subprocess.call( command_list, stdout=out_file, stderr=err_file )

    # Send it over email
    command_list = ['calibre-smtp',
    '-vv',
    '--attachment', os.path.join( ebook_dir, ebook),
    '--subject', 'votre nouvelle edition le monde abonne',
    '--password', smtp_password,
    '--port', smtp_port,
    '--relay', smtp_server,
    '--username', smtp_username,
    smtp_username,
    personnal_address,
    'Automated message sent from Calibre Kindle Server']

    # Send email using calibre's command line SMTP tool
    subprocess.call( command_list, stdout=out_file, stderr=err_file )
