#!/usr/bin/env python2.7

import sys
import json


class TestResult(object):
    """Class containing iperf3 test results.
    :param text: The raw result from libiperf as text
    :param json: The raw result from libiperf asjson/dict
    :param error: Error captured during test, None if all ok
    :param time: Start time
    :param timesecs: Start time in seconds
    :param system_info: System info
    :param version: Iperf Version
    :param local_host: Local host ip
    :param local_port: Local port number
    :param remote_host: Remote host ip
    :param remote_port: Remote port number
    :param reverse: Test ran in reverse direction
    :param protocol: 'TCP' or 'UDP'
    :param num_streams: Number of test streams
    :param blksize:
    :param omit:
    :param duration: Test duration in seconds
    :param local_cpu_total: The local total CPU load
    :param local_cpu_user: The local user CPU load
    :param local_cpu_system: The local system CPU load
    :param remote_cpu_total: The remote total CPU load
    :param remote_cpu_user: The remote user CPU load
    :param remote_cpu_system: The remote system CPU load
    TCP test specific
    :param tcp_mss_default:
    :param retransmits: amount of retransmits (Only returned from client)
    :param sent_bytes: Sent bytes
    :param sent_bps: Sent bits per second
    :param sent_kbps: sent kilobits per second
    :param sent_Mbps: Sent Megabits per second
    :param sent_kB_s: Sent kiloBytes per second
    :param sent_MB_s: Sent MegaBytes per second
    :param received_bytes:  Received bytes
    :param received_bps: Received bits per second
    :param received_kbps: Received kilobits per second
    :param received_Mbps: Received Megabits per second
    :param received_kB_s: Received kiloBytes per second
    :param received_MB_s: Received MegaBytes per second
    UDP test specific
    :param bytes:
    :param bps:
    :param jitter_ms:
    :param kbps:
    :param Mbps:
    :param kB_s:
    :param MB_s:
    :param packets:
    :param lost_packets:
    :param lost_percent:
    :param seconds:
    """

    def __init__(self, result):
        """Initialise TestResult
        :param result: raw json output from :class:`Client` and :class:`Server`
        """
        # The full result data
        self.text = result
        self.json = json.loads(result)

        if 'error' in self.json:
            self.error = self.json['error']
        else:
            self.error = None

            # start time
            self.time = self.json['start']['timestamp']['time']
            self.timesecs = self.json['start']['timestamp']['timesecs']

            # generic info
            self.system_info = self.json['start']['system_info']
            self.version = self.json['start']['version']

            # connection details
            connection_details = self.json['start']['connected'][0]
            self.local_host = connection_details['local_host']
            self.local_port = connection_details['local_port']
            self.remote_host = connection_details['remote_host']
            self.remote_port = connection_details['remote_port']

            # test setup
            self.tcp_mss_default = self.json['start'].get('tcp_mss_default')
            self.protocol = self.json['start']['test_start']['protocol']
            self.num_streams = self.json['start']['test_start']['num_streams']
            self.blksize = self.json['start']['test_start']['blksize']
            self.omit = self.json['start']['test_start']['omit']
            self.duration = self.json['start']['test_start']['duration']

            # system performance
            cpu_utilization_perc = self.json['end']['cpu_utilization_percent']
            self.local_cpu_total = cpu_utilization_perc['host_total']
            self.local_cpu_user = cpu_utilization_perc['host_user']
            self.local_cpu_system = cpu_utilization_perc['host_system']
            self.remote_cpu_total = cpu_utilization_perc['remote_total']
            self.remote_cpu_user = cpu_utilization_perc['remote_user']
            self.remote_cpu_system = cpu_utilization_perc['remote_system']

            # TCP specific test results
            if self.protocol == 'TCP':
                sent_json = self.json['end']['sum_sent']
                self.sent_bytes = sent_json['bytes']
                self.sent_bps = sent_json['bits_per_second']

                recv_json = self.json['end']['sum_received']
                self.received_bytes = recv_json['bytes']
                self.received_bps = recv_json['bits_per_second']

                # Bits are measured in 10**3 terms
                # Bytes are measured in 2**10 terms
                # kbps = Kilobits per second
                # Mbps = Megabits per second
                # kB_s = kiloBytes per second
                # MB_s = MegaBytes per second

                self.sent_kbps = self.sent_bps / 1000
                self.sent_Mbps = self.sent_kbps / 1000
                self.sent_kB_s = self.sent_bps / (8 * 1024)
                self.sent_MB_s = self.sent_kB_s / 1024

                self.received_kbps = self.received_bps / 1000
                self.received_Mbps = self.received_kbps / 1000
                self.received_kB_s = self.received_bps / (8 * 1024)
                self.received_MB_s = self.received_kB_s / 1024

                # retransmits only returned from client
                self.retransmits = sent_json.get('retransmits')

            # UDP specific test results
            elif self.protocol == 'UDP':
                self.bytes = self.json['end']['sum']['bytes']
                self.bps = self.json['end']['sum']['bits_per_second']
                self.jitter_ms = self.json['end']['sum']['jitter_ms']
                self.kbps = self.bps / 1000
                self.Mbps = self.kbps / 1000
                self.kB_s = self.kbps / (8 * 1024)
                self.MB_s = self.Mbps / 1024
                self.packets = self.json['end']['sum']['packets']
                self.lost_packets = self.json['end']['sum']['lost_packets']
                self.lost_percent = self.json['end']['sum']['lost_percent']
                self.seconds = self.json['end']['sum']['seconds']

    @property
    def reverse(self):
        if self.json['start']['test_start']['reverse']:
            return True
        else:
            return False

    @property
    def type(self):
        if 'connecting_to' in self.json['start']:
            return 'client'
        else:
            return 'server'

    def __repr__(self):
        """Print the result as received from iperf3"""
        return self.text


if __name__ == '__main__':

    def print2(s):
        sys.stdout.write(s)

    raw_s = sys.stdin.read()
    if not raw_s:
        sys.stderr.write("json format error: %s" % raw_s)
        sys.exit(1)

    user_protocol = sys.argv[1].upper()
    result = TestResult(raw_s)
    if result.error:
        sys.stderr.write("error: %s\n" % (result.error,))
        sys.exit(1)
    if user_protocol != result.protocol:
        sys.stderr.write("user_protocol != protocol\n")
        sys.exit(1)

    direction = '->' if result.type == 'client' \
                        and not result.reverse else '<-'
    print2("%s%s%s\t%s\t%s\t%s\t%s\t" % (result.local_host,
                                         direction,
                                         result.remote_host,
                                         user_protocol,
                                         result.time,
                                         result.local_cpu_total,
                                         result.remote_cpu_total))

    if user_protocol == 'TCP':
        print("%.2f\t%.2f" % (result.sent_bytes/(2**20), result.sent_Mbps))
    elif user_protocol == 'UDP':
        print("%.2f\t%.2f\t%.2f%%" % (result.bytes/(2**20),
                              result.Mbps, result.lost_percent))
    else:
        sys.stderr.write("unsupported protocol: %s" % user_protocol)
        sys.exit(1)