import os
from typing import Dict
from abc import ABC,abstractmethod
import tempfile

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.appconfiguration import AzureAppConfigurationClient
from azure.core.exceptions import ResourceNotFoundError
import psycopg2

class ConfigurationError(Exception):
    pass

class AzureRemote(ABC):
    def __init__(self,prefix=""):
        self.prefix = prefix

    def __getitem__(self,key):
        try:
            return self.get_from_client(self.prefix+key)
        except ResourceNotFoundError as rnf:
            raise KeyError(key) from rnf

    @abstractmethod
    def get_from_client(self,key):
        pass

class AppConfig(AzureRemote):
    """
    A dict-like representation of a Appconfig for getting config settings. 
    """
    def __init__(self,connection_string,prefix=""):
        super().__init__(prefix)
        self.client = AzureAppConfigurationClient.from_connection_string(connection_string)
    def get_from_client(self,key):
        return self.client.get_configuration_setting(key).value

class KeyvaultSecrets(AzureRemote):
    """
    A dict-like representation of a KeyVault for getting secrets.
    """
    def __init__(self,url,credentials=None,prefix=""):
        super().__init__(prefix)
        if credentials is None:
            credentials = DefaultAzureCredential()
        self.client = SecretClient(url,credentials)
    def get_from_client(self,key):
        return self.client.get_secret(key).value

def sec_con(secrets:Dict[str,str],config:Dict[str,str],auth="ssl",**kwargs):
    """
    Connect to a remote database using a settings dict and certs stored in
    a secrets dictionary as strings. 
    """
    required_files = ["sslrootcert"]
        
    if auth=="ssl":
        required_files += ["sslcert","sslkey"]

    try:
        cert_dir = tempfile.TemporaryDirectory()
        filenames = {k:os.path.join(cert_dir.name,k) for k in required_files}

        for k,filename in filenames.items():
            with open(filename,"w") as f:
                f.write(secrets[k])
            os.chmod(filename,0o0600)

        if auth == "password" and "password" not in kwargs.keys():
            kwargs["password"] = secrets["password"]

        return psycopg2.connect(
                    host = config["host"],
                    user = config["user"],
                    sslmode = "require",
                    **kwargs,
                    **filenames
                )
    except KeyError as ke:
        raise ConfigurationError(f"Tried getting config {ke.args[0]}") from ke
    finally:
        cert_dir.cleanup()
