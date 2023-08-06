import os
import fs
from fs import open_fs
import gnupg


class PgpEncryption:

    def __init__(self, input_file, output_folder, key_location, key_password, recipients):
        """
        With PGP encryption, you can easily encrypt and decrypt all kind of files
        :param input_file: The file you want to encrypt or decrypt. The full filepath is needed
        :param output_folder: The folder where you want to store the file
        :param key_location: Location of the public / private key
        :param key_password: The password of the private key. Not
        :param recipients: The mail-address the key is coupled to
        """
        # Set variables
        self.input_file = input_file
        self.datadir_output = output_folder
        self.gpg = gnupg.GPG(gnupghome=key_location)
        self.key_password = key_password
        self.recipients = recipients
        os.makedirs(self.datadir_output, exist_ok=True)

    def sign_detached(self):
        # Generate detached signatures for files
        with open(self.input_file, 'rb') as f:
            filename = os.path.basename(self.input_file)
            stream = self.gpg.sign_file(f, passphrase=self.key_password, detach=True, output='{}{}.sig'.format(self.datadir_output, filename))
            print('{} - {}'.format(self.input_file, stream.status))


    def verify_detached(self):
        with open(self.input_file, 'rb') as f:
            filename = os.path.basename(self.input_file)
            verify = self.gpg.verify_file('{}{}'.format(f, self.datadir_input, filename))
            print('{} - {}'.format(self.input_file, verify.status))


    def encrypt_files(self):
        with open(self.input_file, 'rb') as f:
            filename = os.path.basename(self.input_file)
            status = self.gpg.encrypt_file(f, recipients=[self.recipients], output='{}{}.gpg'.format(self.datadir_output, filename))
            # print('ok: {}'.format(status.ok))
            # print('status: {}'.format(status.status))
            print('stderr: {}'.format(status.stderr))
            if status.ok is not True:
                raise Exception(status.status)
            return status.status


    def decrypt_files(self):
        with open(self.input_file, 'rb') as f:
            # Remove the .gpg extension from the filename
            filename = os.path.basename(self.input_file)[0:-4]
            status = self.gpg.decrypt_file(f, passphrase=self.key_password, output='{}{}'.format(self.datadir_output, filename))
            # print('ok: {}'.format(status.ok))
            # print('status: {}'.format(status.status))
            print('stderr: {}'.format(status.stderr))
            if status.ok is not True:
                raise Exception(status.status)
            return status.status

