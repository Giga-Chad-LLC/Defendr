import sys
import os
import re
from datetime import datetime
import matplotlib.pyplot as plt



def check_arrays_equal_length(arr1, arr2):
    if len(arr1) != len(arr2):
        raise ValueError(f"Arrays {arr1} and {arr2} are of different length")



def convert_time_format(input_time):
    dt_object = datetime.strptime(input_time, "%d/%b/%Y:%H:%M:%S %z")
    output_time = dt_object.strftime("%d %b %H:%M:%S")
    return output_time



def plot_access_frequency_resource_counts(request_lines, save_filepath):
    n = len(request_lines)
    data_by_method = dict()

    for i in range(n):
        method, url, _ = request_lines[i].split(' ')

        if method not in data_by_method:
            data_by_method[method] = dict()

        if url not in data_by_method[method]:
            data_by_method[method][url] = 0

        data_by_method[method][url] += 1

    unique_methods = list(data_by_method.keys())

    plt.figure(figsize=(10, 6))

    for method in unique_methods:
        plt.scatter(data_by_method[method].values(), data_by_method[method].keys(), label=method)

    plt.xlabel('Visit counts')
    plt.ylabel('URLs')
    plt.title('Timeline Diagram of Visit counts to URLs by HTTP Method')
    plt.legend(title='HTTP Method')

    plt.savefig(save_filepath)



def plot_access_resource_ip(request_lines, remote_hosts, save_filepath):
    check_arrays_equal_length(request_lines, remote_hosts)

    n = len(request_lines)
    data_by_method = dict()

    for i in range(n):
        method, url, _ = request_lines[i].split(' ')

        if method not in data_by_method:
            data_by_method[method] = {
                'urls': [],
                'ips': [],
            }

        data_by_method[method]['urls'].append(url)
        data_by_method[method]['ips'].append(remote_hosts[i])

    unique_methods = list(data_by_method.keys())

    _, ax = plt.subplots(figsize=(10, 6), layout="constrained")
    plt.setp(ax.get_xticklabels(), rotation=35, ha="right")

    for method in unique_methods:
        plt.scatter(data_by_method[method]['ips'], data_by_method[method]['urls'], label=method)

    plt.xlabel('IP Addresses')
    plt.ylabel('URLs')
    plt.title('Timeline Diagram of IPs to URLs by HTTP Method')
    plt.legend(title='HTTP Method')


    plt.savefig(save_filepath)



def plot_access_frequency_resource_time(request_lines, times, save_filepath):
    check_arrays_equal_length(request_lines, times)

    urls = []

    for line in request_lines:
        _, url, _ = line.split(' ')
        urls.append(url)

    _, ax = plt.subplots(figsize=(10, 6), layout="constrained")
    plt.setp(ax.get_xticklabels(), rotation=35, ha="right")

    plt.scatter(times, urls)

    plt.xlabel('Time')
    plt.ylabel('URLs')
    plt.title('Timeline Diagram of Time to URLs')

    plt.savefig(save_filepath)


def plot_access_frequency_user_agent(user_agents, save_filepath):
    browsers = dict()

    for agent in user_agents:
        browser = None

        if 'Chrome' in agent:
            browser = 'Chrome'
        elif 'Safari' in agent:
            browser = 'Safari'
        elif 'OPR' in agent or 'Opera' in agent:
            browser = 'Opera'
        elif 'Firefox' in agent:
            browser = 'Firefox'
        elif 'Edg' in agent or 'Edge' in agent:
            browser = 'Edge'
        elif 'Trident' in agent:
            browser = 'Internet Explorer'
        else:
            browser = 'Other'

        if browser not in browsers:
            browsers[browser] = 0
        browsers[browser] += 1

    plt.figure(figsize=(10, 6))

    plt.scatter(browsers.keys(), browsers.values())

    plt.xlabel('Browser')
    plt.ylabel('Request counts')
    plt.title('Timeline Diagram of Browsers and number of made requests from it')

    plt.savefig(save_filepath)



def plot_error_occurrences_status_code(status_codes, save_filepath):
    occurrences = dict()

    for status_code in status_codes:
        if status_code not in occurrences:
            occurrences[status_code] = 0
        occurrences[status_code] += 1

    plt.figure(figsize=(10, 6))

    plt.scatter(occurrences.keys(), occurrences.values())

    plt.grid(True)
    plt.xlabel('Status code')
    plt.ylabel('Occurrence count')
    plt.title('Timeline Diagram of status codes and their Occurrence counts')

    plt.savefig(save_filepath)



def plot_errors_status_code_time(status_codes, times, save_filepath):
    check_arrays_equal_length(status_codes, times)

    _, ax = plt.subplots(figsize=(10, 6), layout="constrained")
    plt.setp(ax.get_xticklabels(), rotation=35, ha="right")

    plt.scatter(times, status_codes)

    plt.xlabel('Time')
    plt.ylabel('Status code')
    plt.title('Timeline Diagram of status codes and time')

    plt.savefig(save_filepath)



def plot_errors_status_code_ip(status_codes, remote_hosts, save_filepath):
    check_arrays_equal_length(status_codes, remote_hosts)

    _, ax = plt.subplots(figsize=(10, 6), layout="constrained")
    plt.setp(ax.get_xticklabels(), rotation=35, ha="right")

    plt.scatter(remote_hosts, status_codes)

    plt.xlabel('IPs')
    plt.ylabel('Status code')
    plt.title('Timeline Diagram of status codes and its originated IPs')

    plt.savefig(save_filepath)




def main(argc, argv):
    """
    Expects 2 arguments:
        1. path to an Apache2 log file
        2. dirpath by which the resulting plots should be stored
    """

    if (argc < 3):
        raise ValueError(f"Log filepath mot provided.\nUse: {argv[0]} path/to/apache2/log/file path/to/store/directory")

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
            match = log_entry_pattern.match(log_entry)

            if match is None:
                continue

            values = match.groupdict()

            remote_hosts.append(values['remote_host'])
            times.append(convert_time_format(values['timestamp']))
            request_lines.append(values['request_line'])
            status_codes.append(values['status_code'])
            user_agents.append(values['user_agent'])

        save_dirpath = argv[2]

        if not os.path.exists(save_dirpath):
            os.makedirs(save_dirpath)

        now = int(datetime.now().timestamp())
        plot_access_frequency_resource_counts(request_lines, f'{save_dirpath}/plot_access_frequency_resource_counts-{now}.png')
        plot_access_resource_ip(request_lines, remote_hosts, f"{save_dirpath}/plot_access_resource_ip-{now}.png")
        plot_access_frequency_resource_time(request_lines, times, f"{save_dirpath}/plot_access_frequency_resource_time-{now}.png")
        plot_error_occurrences_status_code(status_codes, f"{save_dirpath}/plot_error_occurrences_status_code-{now}.png")
        plot_errors_status_code_time(status_codes, times, f"{save_dirpath}/plot_errors_status_code_time-{now}.png")
        plot_errors_status_code_ip(status_codes, remote_hosts, f"{save_dirpath}/plot_errors_status_code_ip-{now}.png")
        plot_access_frequency_user_agent(user_agents, f"{save_dirpath}/plot_access_frequency_user_agent-{now}.png")

    finally:
        file.close()



if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
