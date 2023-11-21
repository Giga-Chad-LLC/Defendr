import sys
import re
from datetime import datetime
import matplotlib.pyplot as plt



def check_arrays_equal_length(arr1, arr2):
    if len(arr1) != len(arr2):
        raise ValueError(f"Arrays {arr1} and {arr2} are of different length")



def plot_access_frequency_resource_ip(request_lines, remote_hosts, save_filepath):
    check_arrays_equal_length(request_lines, remote_hosts)

    n = len(request_lines)
    data_by_method = dict()

    for i in range(n):
        method, url, _ = request_lines[i].split(' ')

        if method not in data_by_method:
            data_by_method[method] = dict()

        if url not in data_by_method[method]:
            data_by_method[method][url] = 0

        data_by_method[method][url] += 1

        # if method not in data_by_method:
        #     data_by_method[method] = {
        #         'urls': [],
        #         'ips': [],
        #     }

        # data_by_method[method]['urls'].append(url)
        # data_by_method[method]['ips'].append(remote_hosts[i])

        # unique_methods = list(data_by_method.keys())

        # plt.figure(figsize=(17, 10))

        # for method in unique_methods:
        #     plt.scatter(data_by_method[method]['ips'], data_by_method[method]['urls'], label=method)

        # plt.xlabel('IP Addresses')
        # plt.ylabel('URLs')
        # plt.title('Timeline Diagram of IPs to URLs by HTTP Method')
        # plt.legend(title='HTTP Method')

        # plt.savefig(save_filepath)



def plot_access_frequency_resource_time(request_lines, times):
    check_arrays_equal_length(request_lines, times)




def plot_error_occurance_status_code_ip(status_codes, remote_hosts):
    check_arrays_equal_length(status_codes, remote_hosts)



def plot_error_occurance_status_code_time(status_codes, times):
    check_arrays_equal_length(status_codes, times)



def main(argc, argv):
    if (argc < 2):
        raise ValueError(f"Log filepath mot provided.\nUse: {argv[0]} path/to/apache2/log/file")

    log_entry_pattern = re.compile(
        r'(?P<remote_host>[\d\.]+) (?P<user_identifier>[\w-]+) (?P<user_id>[\w-]+) \[(?P<timestamp>.*?)\] "(?P<request_line>.*?)" (?P<status_code>\d+) (?P<response_size>[\d-]+) "(?P<referrer>.*?)" "(?P<user_agent>.*?)"'
    )

    filepath = argv[1]
    file = open(filepath, "r")
    try:
        remote_hosts = []
        times = []
        request_lines = []
        status_codes = []
        user_agents = []

        for log_entry in file.readlines():
            values = log_entry_pattern.match(log_entry).groupdict()

            remote_hosts.append(values['remote_host'])
            times.append(values['timestamp'])
            request_lines.append(values['request_line'])
            status_codes.append(values['status_code'])
            user_agents.append(values['user_agent'])

        plot_access_frequency_resource_ip(request_lines, remote_hosts, f'access_frequency_resource_ip-{datetime.now().timestamp()}.png')


    finally:
        file.close()



if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
