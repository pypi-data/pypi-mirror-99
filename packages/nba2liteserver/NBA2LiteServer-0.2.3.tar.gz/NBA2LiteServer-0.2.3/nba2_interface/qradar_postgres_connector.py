import os

from subprocess import PIPE, run
from paramiko.client import SSHClient
from paramiko import AutoAddPolicy

from nba2_interface import definition

SET_PERMISSIONS_SCRIPT_NAME = "set-atlanta.sh"
SCP_PORT = 22
DOWNLOAD_TOKEN = "download"


class QRadarPostgresConnector(object):
    def __init__(self, permission_script_path: os.path = None):
        if permission_script_path:
            self._execute_permissions_script(permission_script_path=permission_script_path)

    def _execute_permissions_script(self, permission_script_path: os.path):
        try:
            program = f"{permission_script_path}/{SET_PERMISSIONS_SCRIPT_NAME}".replace("\\", "/")  # it must be Linux path
            cmd = 'C:/Program Files/Git/bin/bash.exe' if definition.IS_WINDOWS_OS else "/bin/bash"
            result = run([cmd, '-c', program], stdout=PIPE, stderr=PIPE)
            print(
                f"Set access to QRadar: return code: {result.returncode}, stdout = {result.stdout}, stderr = {result.stderr}")
            if result.returncode != 0:
                raise AssertionError("Can't connect to Atlanta access for QRadar")
        except Exception as e:
            print(f"error: {e}")
            raise e

    def _copy_file_from_to_remote(self, direction, src_file_name, dest_file_name, qradar_ip: str, user: str, password: str):
        sftp = None
        client = None
        path, file = os.path.split(dest_file_name)
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        try:
            client = SSHClient()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(hostname=qradar_ip,
                           port=SCP_PORT,
                           username=user,
                           password=password)
            sftp = client.open_sftp()
            if direction is DOWNLOAD_TOKEN:
                sftp.get(src_file_name, dest_file_name)
            else:
                sftp.put(src_file_name, dest_file_name)
        except Exception as e:
            print(f"error: {e}")
        finally:
            if sftp:
                sftp.close()
            if client:
                client.close()

    def _exec_remote_command(self, ip: str, user: str, password: str, cmd: str):
        session = client = status = None
        stdout_data = []
        stderr_data = []
        ret = []
        nbytes = 4096
        try:
            client = SSHClient()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(hostname=ip,
                           port=SCP_PORT,
                           username=user,
                           password=password)
            transport = client.get_transport()
            session = transport.open_session()
            session.exec_command(cmd)

            while True:
                if session.recv_ready():
                    stdout_data.append(session.recv(nbytes))
                if session.recv_stderr_ready():
                    stderr_data.append(session.recv_stderr(nbytes))
                if session.exit_status_ready():
                    break
            status = session.recv_exit_status()
            for item in stdout_data:
                d = item.decode('ascii').replace("\n", "")
                ret.append(d)
        except Exception as e:
            print(f"error: {e}")
        finally:
            if session:
                session.close()
            if client:
                client.close()
            return status, ret, stderr_data

    def get_models_from_qradar(self, ip: str, user: str, password: str, db_tree_file_name: str, db_models_file_name: str,
                               db_dest_path: str):
        try:
            db_src_path = "/tmp/"
            cmds = [
                f"psql -U qradar -d qradar -c \"Copy (select * from network_threat_analytics_hca_models) To '{db_src_path}{db_models_file_name}' With CSV DELIMITER ',' HEADER; \"",
                f"psql -U qradar -d qradar -c \"Copy (select * from network_threat_analytics_hca_algorithms) To '{db_src_path}{db_tree_file_name}' With CSV DELIMITER ',' HEADER; \""
            ]

            for cmd in cmds:
                status, ret, stderr_data = self._exec_remote_command(ip, user=user, password=password, cmd=cmd)
                print(f"{cmd}: \nstatus: {status}, ret: {ret}, err: {stderr_data}")

            models_dir, _ = os.path.split(db_dest_path) #  remove the last /
            if not os.path.exists(models_dir):
                os.makedirs(db_dest_path, exist_ok=True)
            for file in [db_models_file_name, db_tree_file_name]:
                self._copy_file_from_to_remote(DOWNLOAD_TOKEN, f"{db_src_path}{file}", f"{db_dest_path}{file}",
                                               qradar_ip=ip, user=user, password=password)
                print(f"Download {file}")
        except Exception as e:
            print(f"error: {e}")
            raise e
