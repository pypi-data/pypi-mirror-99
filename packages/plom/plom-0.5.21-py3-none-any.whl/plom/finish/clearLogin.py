# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2019-2020 Andrew Rechnitzer
# Copyright (C) 2019-2021 Colin B. Macdonald

from getpass import getpass

from plom.messenger import Messenger


def clear_manager_login(server=None, password=None):
    """Force clear the "manager" authorisation, e.g., after a crash.

    Args:
        server (str): in the form "example.com" or "example.com:41984".
        password (str): if not specified, prompt on the command line.
    """
    if server and ":" in server:
        s, p = server.split(":")
        msgr = Messenger(s, port=p)
    else:
        msgr = Messenger(server)
    msgr.start()

    if not password:
        password = getpass('Please enter the "manager" password: ')

    msgr.clearAuthorisation("manager", password)
    print("Manager login cleared.")
    msgr.stop()
