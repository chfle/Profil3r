import requests
import time


class Domain:

    def __init__(self, config, permutations_list):
        # 100 ms
        self.delay = config['plateform']['domain']['rate_limit'] / 1000
        # {permutation}.{tld}
        self.format = config['plateform']['domain']['format']
        # Top level domains
        self.tld = []

        # can be used with a file with domain names
        with open("domains.txt", 'r') as file:
            self.tld = file.readlines()
        #  domains are not case sensitive
        self.permutations_list = [perm.lower() for perm in permutations_list]
        # domain
        self.type = config['plateform']['domain']['type']

    #  Generate all potential domains names
    def possible_domains(self):
        possible_domains = []

        for domain in self.tld:
            for permutation in self.permutations_list:
                possible_domains.append(self.format.format(
                    permutation=permutation,
                    # must remove \n
                    domain=domain.strip("\n")
                ))

        return possible_domains

    def search(self):
        domains_lists = {
            "type": self.type,
            "accounts": []
        }
        possible_domains_list = self.possible_domains()

        for domain in possible_domains_list:
            try:
                r = requests.head(domain, timeout=5)
            except (requests.ConnectionError, requests.exceptions.ReadTimeout):
                pass
            else:
                # If the domain exists
                if r.status_code < 400:
                    domains_lists["accounts"].append({"value": domain})
            time.sleep(self.delay)

        return domains_lists
