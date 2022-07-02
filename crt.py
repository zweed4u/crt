#!/usr/bin/python3
import json
import requests


class CertificateTransparancy:
    # Let's discover some subdomains!
    # - envs like mail.dev.google.com
    # - permutation like mail-dev.google.com
    # Dork via site:<domain> -<excludes> inurl:<substr> ext:<extension>
    # Manually check certs - SANs DNS
    def __init__(self):
        self.base_url = "https://crt.sh"

    def search(self, domain, use_subdomain_wildcard=True, json_output=True):
        if use_subdomain_wildcard:
            print(f"Checking subdomains :: %.{domain}")
        query_string = {
            "q": f"%.{domain}" if use_subdomain_wildcard else domain,
            "output": "json" if json_output else None,
        }
        response = requests.get(self.base_url, params=query_string)
        response.raise_for_status()
        # qa, admin, dev, beta, api
        return response.json()


domain = input("Domain: ")
c = CertificateTransparancy()
results = c.search(domain)
for identity in results:
    for i in identity.get("name_value", "").splitlines():
        # ready to send these to httpx
        print(i)
