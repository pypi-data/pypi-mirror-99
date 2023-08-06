#!/usr/bin/env python
# -*- coding: utf8 -*-
#
# $Id$
#
# Copyright (c) 2012-2014 "dark[-at-]gotohack.org"
#
# This file is part of pymobiledevice
#
# pymobiledevice is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
import os
from pymobiledevice.lockdown import LockdownClient
from pprint import pprint
from pymobiledevice.afc import AFCClient, AFCShell
from optparse import OptionParser


class HouseArrestClient(AFCClient):

    def __init__(self, udid=None):
        lockdownClient = LockdownClient(udid)
        serviceName = "com.apple.mobile.house_arrest"
        super(HouseArrestClient, self).__init__(lockdownClient, serviceName)


    def stop_session(self):
        print("Disconecting...")
        self.service.close()

    def send_command(self, applicationId, cmd="VendContainer"):
        self.service.sendPlist({"Command": cmd, "Identifier": applicationId})
        res = self.service.recvPlist()

        if res.get("Error"):
            print(res["Error"])
            return False
        else:
            return True

    def shell(self, applicationId, cmd="VendContainer"):
        res = self.send_command(applicationId, cmd)
        if res:
            AFCShell(client=self).cmdloop()


if __name__ == "__main__":
    parser = OptionParser(usage="%prog -a  applicationId")
    parser.add_option("-a", "--application", dest="applicationId", default=False,
                  help="Application ID <com.apple.iBooks>", type="string")
    parser.add_option("-c", "--command", dest="cmd", default=False,
                  help="House_Arrest commands: ", type="string")

    (options, args) = parser.parse_args()
    h = HouseArrestClient()
    if options.cmd:
        h.shell(options.applicationId, cmd=options.cmd)
    else:
        h.shell(options.applicationId)







