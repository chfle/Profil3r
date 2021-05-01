import time
import pwnedpasswords


class Email:

    def __init__(self, config, permutations_list):
        # Have I been pwned API rate limit ( 1500 ms)
        self.delay = DELAY = config['plateform']['email']['rate_limit'] / 1000
        # Getting domains from a extern email_domains.txt file with more than 100 Email. To use a different list
        # simply replace this text file with another
        self.domains = []

        with open('email_domains.txt', 'r') as file:
            self.domains = file.readlines()
        #  {username}@{domain}
        self.format = config['plateform']['email']['format']
        #  email addresses are not case sensitive
        self.permutations_list = [perm.lower() for perm in permutations_list]
        # email
        self.type = config['plateform']['email']['type']

    #  Generate all potential addresses
    def possible_emails(self):
        possible_emails = []

        for domain in self.domains:
            for permutation in self.permutations_list:
                possible_emails.append(self.format.format(
                    permutation=permutation,
                    domain=domain
                ))
        return possible_emails

    #  We use the Have I Been Pwned API to search for breached emails
    def search(self):
        emails_usernames = {
            "type": self.type,
            "accounts": []
        }
        possible_emails_list = self.possible_emails()

        for possible_email in possible_emails_list:
            pwned = pwnedpasswords.check(possible_email)

            # Not breached email
            if not pwned:
                emails_usernames["accounts"].append({"value": possible_email, "breached": False})
            # Breached emails
            else:
                emails_usernames["accounts"].append({"value": possible_email, "breached": True})

            time.sleep(self.delay)

        return emails_usernames
