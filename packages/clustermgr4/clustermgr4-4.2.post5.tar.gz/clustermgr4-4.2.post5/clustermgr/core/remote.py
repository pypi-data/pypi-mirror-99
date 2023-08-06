import StringIO
import socket
import os
import base64
import logging

from logging.handlers import RotatingFileHandler
from paramiko import SSHException
from paramiko.client import SSHClient, AutoAddPolicy
from paramiko.ssh_exception import PasswordRequiredException 
from flask import current_app

from clustermgr.extensions import wlogger
from clustermgr.config import Config
from clustermgr.core.clustermgr_logging import remote_logger as logger

from paramiko.util import log_to_file
log_to_file(os.path.join(os.path.expanduser("~"), ".clustermgr4", "logs", "paramiko.log"), level = "DEBUG")

def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc)
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)


def get_os_type(self):

    cin, cout, cerr = self.run("ls /etc/*release")
    files = cout.split()
    
    if files[0] == '/etc/alpine-release':
        os_type = 'Alpine'

    cin, cout, cerr = self.run("cat "+files[0])

    if "Ubuntu" in cout and "18.04" in cout:
        os_type = "Ubuntu 18"
    if "Ubuntu" in cout and "20.04" in cout:
        os_type = "Ubuntu 20"
    if "CentOS" in cout and "release 7." in cout:
        os_type = "CentOS 7"
    if "CentOS" in cout and "release 8." in cout:
        os_type = "CentOS 8"
    if 'Red Hat Enterprise Linux' in cout and '7.' in cout:
        os_type = 'RHEL 7'
    if 'Red Hat Enterprise Linux' in cout and '8.' in cout:
        os_type = 'RHEL 8'
    if 'Debian' in cout and "(stretch)" in cout:
        os_type = 'Debian 9'
    if 'Debian' in cout and "(buster)" in cout:
        os_type = 'Debian 10'

    self.server_os = os_type
    
    return self.server_os


class ClientNotSetupException(Exception):
    """Exception raised when the client is not initialized because
    of connection failures."""
    pass

class mySSHClient(SSHClient):
    def __init__(self):
        super(mySSHClient, self).__init__()

    def __del__(self):
        self.close()

class RemoteClient(object):
    """Remote Client is a wrapper over SSHClient with utility functions.

    Args:
        host (string): The hostname of the server to connect. It can be an IP
            address of the server also.
        user (string, optional): The user to connect to the remote server. It
            defaults to root

    Attributes:
        host (string): The hostname passed in as a the argument
        user (string): The user to connect as to the remote server
        client (:class:`paramiko.client.SSHClient`): The SSHClient object used
            for all the communications with the remote server.
        sftpclient (:class:`paramiko.sftp_client.SFTPClient`): The SFTP object
            for all the file transfer operations over the SSH.
    """

    def __init__(self, host, ip=None, user='root', passphrase=None, ssh_port=22):
        self.host = host
        self.ip = ip
        self.user = user
        self.ssh_port = ssh_port
                
        if not passphrase:
            pw_file = os.path.join(current_app.config['DATA_DIR'], '.pw')
            if os.path.exists(pw_file):
                encoded_passphrase = open(pw_file).read()
            
                passphrase = decode(
                                os.getenv('NEW_UUID'), 
                                encoded_passphrase
                                )
        self.passphrase = passphrase
        self.client = mySSHClient()
        self.sftpclient = None
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.client.load_system_host_keys()
        logger.debug("RemoteClient created for host: %s", host)

    def startup(self):
        """Function that starts SSH connection and makes client available for
        carrying out the functions. It tries with the hostname, if it fails
        it tries with the IP address if supplied
        """
        try:
            logger.debug("Trying to connect to remote server %s:%s", self.host, self.ssh_port)
            self.client.connect(self.host, port=self.ssh_port, username=self.user, 
                                    passphrase=self.passphrase)
            self.sftpclient = self.client.open_sftp()
        except PasswordRequiredException:
            raise ClientNotSetupException('Pubkey is encrypted.')
        
        except SSHException as e:
            raise ClientNotSetupException(e)
        
        except:
            if self.ip:
                logger.warning("Connection with hostname failed. Retrying "
                                "with IP")
                self._try_with_ip()
            else:
                logger.error("Connection to %s failed.", self.host)
                raise ClientNotSetupException('Could not connect to the host.')


    def _try_with_ip(self):
        try:
            logger.debug("Connecting to IP:%s User:%s" % (self.ip, self.user))
            self.client.connect(self.ip, port=22, username=self.user,
                                passphrase=self.passphrase)
            self.sftpclient = self.client.open_sftp()
        except PasswordRequiredException:
            raise ClientNotSetupException('Pubkey is encrypted.')

        except SSHException as e:
            raise ClientNotSetupException(e)

        except socket.error:
            logger.error("Connection with IP (%s) failed.", self.ip)
            raise ClientNotSetupException('Could not connect to the host.')

    def rename(self, oldpath, newpath):
        """Rename a file or folder from oldpath to newpath.
        Args:
            oldpath (string): old file/folder name
            newpath (string): new file/folder name

        Returns:
            True if rename successful else False
        """
        
        logger.debug("[%s] Renaming file %s to %s", self.host, oldpath, newpath)
        
        try:
            r = self.sftpclient.rename(oldpath, newpath)
            return True
        except Exception as err:
            return False

    def download(self, remote, local):
        """Downloads a file from remote server to the local system.

        Args:
            remote (string): location of the file in remote server
            local (string): path where the file should be saved
        """
        if not self.sftpclient:
            raise ClientNotSetupException(
                'Cannot download file. Client not initialized')

        logger.debug("[%s] Downloading file %s", self.host, remote)

        try:
            self.sftpclient.get(remote, local)
            return True, local
        except OSError:
            logger.debug("[%s] ERROR %s", self.host, OSError)
            return False, "Error: Local file %s doesn't exist." % local
        except IOError:
            logger.debug("[%s] ERROR %s", self.host, IOError)
            return False, "Error: Remote location %s doesn't exist." % remote

    def upload(self, local, remote):
        """Uploads the file from local location to remote server.

        Args:
            local (string): path of the local file to upload
            remote (string): location on remote server to put the file
        """
        if not self.sftpclient:
            raise ClientNotSetupException(
                'Cannot upload file. Client not initialized')
        logger.debug("[%s] Uploading file %s", self.host, remote)
        try:
            self.sftpclient.put(local, remote)
            return True, remote
        except OSError:
            logger.debug("[%s] ERROR %s", self.host, OSError)
            return False, "Error: Local file %s doesn't exist." % local
        except IOError:
            logger.debug("[%s] ERROR %s", self.host, IOError)
            return False, "Error: Remote location %s doesn't exist." % remote

    def exists(self, filepath):
        """Returns whether a file exists or not in the remote server.

        Args:
            filepath (string): path to the file to check for existance

        Returns:
            True if it exists, False if it doesn't
        """
        if not self.client:
            raise ClientNotSetupException(
                'Cannot run procedure. Client not initialized')
                
        logger.debug("[%s] Echecking existence of  file %s", self.host, filepath)
        try:
            self.sftpclient.stat(filepath)
            return True
        except:
            return False

    def run(self, command):
        """Run a command in the remote server.

        Args:
            command (string): the command to be run on the remote server

        Returns:
            tuple of three strings containing text from stdin, stdout an stderr
        """
        if not self.client:
            raise ClientNotSetupException(
                'Cannot run procedure. Client not initialized')


        logger.debug("[%s] Running command %s", self.host, command)

        #buffers = self.client.exec_command(command, timeout=30)
        buffers = self.client.exec_command(command)
        output = []
        for buf in buffers:
            try:
                output.append(buf.read())
            except IOError:
                output.append('')

        return tuple(output)

    def get_file(self, filename):
        """Reads content of filename on remote server

        Args:
            filename (string): name of file to be read from remote server

        Returns:
            tuple: True/False, file like object / error
        """
        
        logger.debug("[%s] Getting file %s", self.host, filename)
        
        file_obj = StringIO.StringIO()
        try:
            result = self.sftpclient.getfo(filename, file_obj)
            file_obj.seek(0)
            return result, file_obj
        except Exception as err:
            print err
            return False, err
    
    def put_file(self,  filename, filecontent):
        """Puts content to a file on remote server

        Args:
            filename (string): name of file to be written on remote server
            filecontent (string): content of file

        Returns:
            tuple: True/False, file size / error
        """

        logger.debug("[%s] Putting file %s", self.host, filename)

        file_obj = StringIO.StringIO()
        file_obj.write(filecontent)
        file_obj.seek(0)

        try:
            result = self.sftpclient.putfo(file_obj, filename)
            return True, result.st_size
        except Exception as err:
            return False, err

    def mkdir(self,  dirname):
        """Creates a new directory.

        Args:
            dirname (string): the full path of the directory that needs to be
                created

        Returns:
            a tuple containing the success or failure of operation and dirname
                on success and error on failure
        """
        
        logger.debug("[%s] Creating directory %s", self.host, dirname)
        
        try:
            self.sftpclient.mkdir(dirname)
            return True, dirname
        except Exception as err:
            return False, err

    def listdir(self, dirname):
        """Lists all the files and folders in a directory.

        Args:
            dirname (string): the full path of the directory that needs to be
                listed

        Returns:
            a list of the files and folders in the directory
        """
        
        logger.debug("[%s] Getting directory listing of %s", self.host, dirname)
        
        try:
            result = self.sftpclient.listdir(dirname)
            return True, result
        except Exception as err:
            return False, err

    def get_os_type(self):
        return get_os_type(self)


    def close(self):
        """Close the SSH Connection
        """
        self.client.close()

    def __repr__(self):
        return "RemoteClient({0}, ip={1}, user={2}, port={3})".format(self.host, self.ip,
                                                            self.user, self.ssh_port)


def get_connection(server, task_id):

    wlogger.log(task_id, "Making SSH connection to {} ...".format(server.hostname),
                        'action', server.id)
    
    conn = RemoteClient(server.hostname, ip=server.ip, ssh_port=server.ssh_port)

    try:
        conn.startup()
    except:
        wlogger.log(tid, "Can't establish SSH connection to  {}".format(server.hostname), 'error', server.id)
        wlogger.log(tid, "Ending current process.", "error", server.id)
        return

    return conn


#Fake RemoteClient
class FakeRemote:
    
    """Provides fake remote class with the same run() function.
    """

    def run(self, cmd):
        
        """This method executes cmd as a sub-process.

        Args:
            cmd (string): commands to run locally
        
        Returns:
            Standard input, output and error of command
        
        """
        print cmd
        cin, cout, cerr = os.popen3(cmd)

        return '', cout.read(), cerr.read()


    def put_file(self, filename, filecontent):
        with open(filename, 'w') as file_obj:
            file_obj.write(filecontent)

    def rename(self, oldname, newname):
        os.rename(oldname, newname)

    def get_file(self, filename):
        return True, open(filename)

    def get_os_type(self):
        return get_os_type(self)
