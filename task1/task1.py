import subprocess
import re

import pandas as pd


def ping(host):
    result = subprocess.run(['ping', '-c', '1', host], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    return output


def create_csv(hosts):

    data = []
    for host in hosts:

        result = ping(host)
        ip = re.search("((/d+).(/d+).(/d+).(/d+))", result)
        ttl = re.search("ttl=(/d+)", result)
        rtt = re.search("time=(/d+).(/d+)", result)

        if ttl:
            data.append({
                "host": host,
                "ip": ip.group(1) if ip else "Nan",
                "rtt": rtt.group(1) if rtt else "Nan",
                "ttl": ttl.group(1),
                "packet_loss": "0"
            })
        else:
            data.append({
                "host": host,
                "ip": ip.group(1) if ip else "Nan",
                "rtt": "Nan",
                "ttl": "Nan",
                "packet_loss": "100"
            })

    df = pd.DataFrame(data)
    df.to_csv("task1/ping_results.csv", index=False)
    return df


def main():
    hosts = {"ya.ru", "vk.com", "github.com", "habr.com",
             "google.com", "wildberries.ru", "2gis.ru",
             "ozon.ru", "pinterest.com", "nsu.ru"}

    results = create_csv(hosts)


if __name__ == "__main__":
    main()
