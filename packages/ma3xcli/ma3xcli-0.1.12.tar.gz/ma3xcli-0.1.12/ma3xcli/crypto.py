# Example text encryption:
# echo "Enter Text:" && read TEXT && \
# echo "Enter Passphrase:" && read -s SECRET && \
# ENC=`echo $TEXT | openssl enc -e -aes-256-cbc -a -salt -k $SECRET` && \
# echo $ENC

# Example text decryption:
# read -s SECRET && echo $ENC | openssl aes-256-cbc -a -d -salt -k $SECRET

import typer
import os,sys
import getpass
import shlex
from pathlib import Path

cmd_enc_txt = "echo %s | openssl enc -e -aes-256-cbc -a -salt -k %s"
cmd_dec_txt = "echo %s | openssl aes-256-cbc -a -d -salt -k %s"
cmd_enc_file = "cat %s | openssl enc -e -aes-256-cbc -a -salt -k %s > %s"
cmd_dec_file = "cat %s | openssl aes-256-cbc -a -d -salt -k %s > %s"

def main(input_object: str, isfile: bool = False, decrypt: bool = False, destroy: bool = False ):

	if destroy:
			typer.echo(os.system("echo 0x90 > %s && rm %s" % (shlex.quote(input_object),shlex.quote(input_object))))
			sys.exit()	
			
	
	passw = getpass.getpass(prompt='Passphrase: ')

	if isfile:
		if decrypt:
			# typer.echo(os.system(cmd_dec_file % (shlex.quote(input_object), passw, shlex.quote(input_object[:-4]))))
			os.system(cmd_dec_file % (shlex.quote(input_object), passw, shlex.quote(input_object[:-4])))
		else:
			# typer.echo(os.system(cmd_enc_file % (shlex.quote(input_object), passw, shlex.quote(input_object+".enc"))))
			os.system(cmd_enc_file % (shlex.quote(input_object), passw, shlex.quote(input_object+".enc")))
	else:
		if decrypt:
			# typer.echo(os.system(cmd_dec_txt % (input_object, passw)))
			os.system(cmd_dec_txt % (input_object, passw))
		else:
			# typer.echo(os.system(cmd_enc_txt % (input_object, passw)))
			os.system(cmd_enc_txt % (input_object, passw))