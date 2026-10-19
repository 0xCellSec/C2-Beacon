import os
import socket


from app.core.protocol import Message, MessageType
from app.core.models import BeaconMeta



class BeaconRegistering():
    def get_priv_ip():
        host = socket.gethostname()
        private_ip = socket.gethostbyname(host)
        
        return str(private_ip)
        
    async def get_meta_payload(self) -> BeaconMeta:
        operating = os.uname()
        host_pid = int(os.getpid())
        host_username = str(os.getlogin())
        private_ip = self.get_priv_ip()

        payload = BeaconMeta(os = operating.sysname, 
                             hostname = operating.nodename, 
                             username = host_username, 
                             pid = host_pid, 
                             internal_ip = private_ip)

        return payload

    
        


