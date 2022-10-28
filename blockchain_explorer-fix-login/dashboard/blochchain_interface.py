import os
import subprocess
import json
from dotenv import load_dotenv
from unittest import result
import mcrpc

load_dotenv()
class Multichain ():
    def __init__(self, mode = 'dev'):
        self.mode = mode
        self.rpc_host = ''
        self.rpc_port = ''
        self.rpc_user = ''
        self.rpc_pass = ''
        self.connect()

    def connect(self):
        if self.mode =='dev':
            self.rpc_host = os.getenv('RPC_HOST_DEV')
            self.rpc_port = os.getenv('RPC_PORT_DEV')
            self.rpc_user = os.getenv('RPC_USER_DEV')
            self.rpc_pass = os.getenv('RPC_PASS_DEV')  
        if self.mode =='prod':
            pass
        if self.mode =='local':
            self.rpc_host = os.getenv('RPC_HOST')
            self.rpc_port = os.getenv('RPC_PORT')
            self.rpc_user = os.getenv('RPC_USER')
            self.rpc_pass = os.getenv('RPC_PASS')
        try:
            self.client = mcrpc.RpcClient(self.rpc_host,port=self.rpc_port, user=self.rpc_user, pwd=self.rpc_pass)
        except:
            self.client = None


