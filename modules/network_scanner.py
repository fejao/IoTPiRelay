#!/usr/bin/env python

import sys
import subprocess

try:
    from iot_fetcher import IotFetcher

except ImportError:
    exit("This script requires to import the IoT shared functions\nThe file iot_fetcher.py was not found")

__author__ = 'https://github.com/fejao'

DEFAULT_NETWORK_ADAPTER_NAME = 'wlan0'

# TODO
# !!! Attention here, you should change it to use as the user using the script
MY_SUDO_PASSWORD = 'devassa'

class NetworkScanner(object):
    '''A'''

    def __init__(self, args, verbose=False):

        self.verbose = verbose

    def scanNetwork(self):
        '''A'''

        command = [
            'arp-scan',
            '--retry=8',
            '--ignoredups',
            '-I',
            DEFAULT_NETWORK_ADAPTER_NAME,
            '--localnet'
        ]

        # sudo_passwd = "devassa"
        command = "arp-scan --retry=8 --ignoredups -I wlan0 --localnet".split()

        # Scan the Network
        command_result = subprocess.Popen(
            ['sudo', '-S'] + command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True)

        # Fetches the output from scanning
        output, err = command_result.communicate()

        if err:
            exit('Error !!!\nScanning the network returned: %s' % err)
        else:
            return output

    def getScanDict(self):
        '''A'''

        if self.verbose:
            print("NetworkScanner.getScanDict")

        # Scan the Network
        output = self.scanNetwork()

        # Init return Dictionary
        founded_dict = {}

        # For every line, that is not '' or ' '
        for line in filter(None, output.split('\n')):
            # Not selecting lines with words: "Interface", "arp-scan", "packets"
            if not any(value in line for value in ("Interface", "arp-scan", "packets")):
                # List of the line values
                line_list = line.split('\t')
                # Add to founded
                founded_dict[line_list[0]] = {
                    'mac' : line_list[1],
                    'vendor' : line_list[2]
                }

        return founded_dict

class IotNetworkScanner(NetworkScanner):
    '''A'''

    def __init__(self, args):

        self.verbose = args.get('verbose')
        self.configFileAddress = args.get('configFileAddress')

        # Sets the fetcher
        fetcher = IotFetcher('Network Scan', self.configFileAddress, self.verbose)

        # Loads the Network Scanning configuration from file
        self.configJson = fetcher.loadConfig()

        # Updates the functionsDict with the Twitter module
        dictValues = {
            'display_name': 'Network Scanning',
            'display_description': 'Scans the Network for unknown connection',
            'function': 'network_scanner'
        }
        fetcher.updatesFunctionsDict(args.get('functionsDict'), dictValues)

        # Sets super
        super(IotNetworkScanner, self).__init__(args, self.verbose)

    def checkConnections(self):
        '''A'''

        if self.verbose:
            print("IotNetworkScanner.checkConnections")

        connections = self.getScanDict()

        err = None
        for key, values in connections.iteritems():
            # Search as known by it's IP
            if key in self.configJson:
                # Gets the known by the IP
                found = self.configJson.get(key)

                # Tests if is the same MAC address
                if not found.get('mac') == values.get('mac'):
                    # Sets the error dictionary
                    # err = {
                    #     'msg': "Computer with unknown MAC address: %s" % found.get('mac'),
                    #     'ip': key,
                    #     'mac': found.get('mac'),
                    #     'vendor': found.get('vendor'),
                    # }
                    err = "Unknown MAC\n%s\nwith IP Address\n%s" % (values.get('mac', key))

                # Tests if is the same vendor name
                elif not found.get('vendor') == values.get('vendor'):
                    # Sets the error dictionary
                    # err = {
                    #     'msg': "Computer with unknown vendor name: %s" % found.get('vendor'),
                    #     'ip': key,
                    #     'mac': found.get('mac'),
                    #     'vendor': found.get('vendor'),
                    # }
                    err = "Unknown vendor\n%s\nwith IP Address\n%s" % (values.get('vendor', key))

            else:
                # Sets the error dictionary for unknown IP
                # err = {
                #     'msg': "IP Address\n%s\nwith mac address\n%s\nis unknown..." % (key, values.get('mac')),
                #     'ip': key,
                #     'mac': values.get('mac'),
                #     'vendor': values.get('vendor'),
                # }
                err = "IP Address\n%s\nwith mac address\n%s\nis unknown..." % (key, values.get('mac'))

        return err
