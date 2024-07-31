import re
import socket
import urllib.request
from urllib.parse import urlparse
import whois
import datetime
import requests
import numpy as np
from bs4 import BeautifulSoup
from googlesearch import search

class PhishingURLDetector:
    def __init__(self, model):
        self.model = model

    def has_ip_address(self, url):
        try:
            socket.inet_aton(urlparse(url).netloc)
            return 0
        except socket.error:
            return 1

    def url_length(self, url):
        return 1 if len(url) < 54 else -1 if len(url) <= 75 else 0

    def shortening_service(self, url):
        return 0 if re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                    'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                    'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                    'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                    'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                    'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                    'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net', url) else 1

    def has_at_symbol(self, url):
        return 0 if '@' in url else 1

    def double_slash_redirecting(self, url):
        return -1 if url.count('//') > 1 else 1

    def prefix_suffix(self, url):
        return -1 if '-' in urlparse(url).netloc else 1

    def subdomain_count(self, url):
        return -1 if len(urlparse(url).netloc.split('.')) > 3 else 1

    def ssl_final_state(self, url):
        try:
            response = requests.get(url)
            return 1 if response.url.startswith('https') else 0
        except:
            return 0

    def domain_registration_length(self, url):
        try:
            domain_info = whois.whois(urlparse(url).netloc)
            expiration_date = domain_info.expiration_date
            if isinstance(expiration_date, list):
                expiration_date = expiration_date[0]
            return 1 if (expiration_date - datetime.datetime.now()).days > 365 else 0
        except:
            return 0

    def favicon(self, url):
        try:
            response = requests.get(url)
            return 1 if urlparse(response.url).netloc == urlparse(url).netloc else 0
        except:
            return 0

    def port(self, url):
        try:
            port = urlparse(url).port
            return 1 if port is None else -1
        except:
            return 0

    def https_token(self, url):
        return -1 if 'https' in urlparse(url).netloc else 1

    def request_url(self, url):
        try:
            response = requests.get(url)
            return 1 if urlparse(response.url).netloc == urlparse(url).netloc else 0
        except:
            return 0

    def url_of_anchor(self, url):
        try:
            response = requests.get(url)
            return 1 if urlparse(response.url).netloc == urlparse(url).netloc else 0
        except:
            return 0

    def links_in_tags(self, url):
        try:
            response = requests.get(url)
            return 1 if urlparse(response.url).netloc == urlparse(url).netloc else 0
        except:
            return 0

    def sfh(self, url):
        try:
            response = requests.get(url)
            return 1 if urlparse(response.url).netloc == urlparse(url).netloc else 0
        except:
            return 0

    def submitting_to_email(self, url):
        return 0 if 'mailto:' in url else 1

    def abnormal_url(self, url):
        return 1 if urlparse(url).netloc in url else 0

    def redirect(self, url):
        try:
            response = requests.get(url)
            return -1 if response.history else 1
        except:
            return 0

    def on_mouseover(self, url):
        try:
            response = requests.get(url)
            return 0 if re.findall("<script>.+onmouseover.+</script>", response.text) else 1
        except:
            return 1

    def right_click(self, url):
        try:
            response = requests.get(url)
            return 0 if re.findall(r"event.button ?== ?2", response.text) else 1
        except:
            return 1

    def pop_up_window(self, url):
        try:
            response = requests.get(url)
            return 0 if re.findall(r"alert\(", response.text) else 1
        except:
            return 1

    def iframe(self, url):
        try:
            response = requests.get(url)
            return 0 if re.findall(r"[<iframe>|<frameBorder>]", response.text) else 1
        except:
            return 1

    def age_of_domain(self, url):
        try:
            domain_info = whois.whois(urlparse(url).netloc)
            creation_date = domain_info.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            return 1 if (datetime.datetime.now() - creation_date).days > 180 else 0
        except:
            return 0

    def dns_record(self, url):
        try:
            domain_info = whois.whois(urlparse(url).netloc)
            return 1 if domain_info else 0
        except:
            return 0

    def web_traffic(self, url):
        try:
            rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find("REACH")['RANK']
            return 1 if int(rank) < 100000 else -1 if int(rank) >= 100000 else 0
        except:
            return 0

    def page_rank(self, url):
        try:
            rank_checker_response = requests.post("https://www.checkpagerank.net/index.php", {"name": urlparse(url).netloc})
            global_rank = int(re.findall(r"Global Rank: ([0-9]+)", rank_checker_response.text)[0])
            return 1 if 0 < global_rank < 100000 else 0
        except:
            return 0

    def google_index(self, url):
        try:
            site = search(url, 5)
            return 1 if site else 0
        except:
            return 0

    def links_pointing_to_page(self, url):
        try:
            response = requests.get(url)
            number_of_links = len(re.findall(r"<a href=", response.text))
            if number_of_links == 0:
                return 0
            elif 0 < number_of_links <= 2:
                return -1
            else:
                return 1
        except:
            return 0

    def statistical_report(self, url):
        try:
            url_match = re.search(
                'at\.ua|usa\.cc|baltazarpresentes\.com\.br|pe\.hu|esy\.es|hol\.es|sweddy\.com|myjino\.ru|96\.lt|ow\.ly', url)
            ip_address = socket.gethostbyname(urlparse(url).netloc)
            ip_match = re.search(
                '146\.112\.61\.108|213\.174\.157\.151|121\.50\.168\.88|192\.185\.217\.116|78\.46\.211\.158|181\.174\.165\.13|46\.242\.145\.103|121\.50\.168\.40|83\.125\.22\.219|46\.242\.145\.98|'
                '107\.151\.148\.44|107\.151\.148\.107|64\.70\.19\.203|199\.184\.144\.27|107\.151\.148\.108|107\.151\.148\.109|119\.28\.52\.61|54\.83\.43\.69|52\.69\.166\.231|216\.58\.192\.225|'
                '118\.184\.25\.86|67\.208\.74\.71|23\.253\.126\.58|104\.239\.157\.210|175\.126\.123\.219|141\.8\.224\.221|10\.10\.10\.10|43\.229\.108\.32|103\.232\.215\.140|69\.172\.201\.153|'
                '216\.218\.185\.162|54\.225\.104\.146|103\.243\.24\.98|199\.59\.243\.120|31\.170\.160\.61|213\.19\.128\.77|62\.113\.226\.131|208\.100\.26\.234|195\.16\.127\.102|195\.16\.127\.157|'
                '34\.196\.13\.28|103\.224\.212\.222|172\.217\.4\.225|54\.72\.9\.51|192\.64\.147\.141|198\.200\.56\.183|23\.253\.164\.103|52\.48\.191\.26|52\.214\.197\.72|87\.98\.255\.18|209\.99\.17\.27|'
                '216\.38\.62\.18|104\.130\.124\.96|47\.89\.58\.141|78\.46\.211\.158|54\.86\.225\.156|54\.82\.156\.19|37\.157\.192\.102|204\.11\.56\.48|110\.34\.231\.42', ip_address)
            if url_match or ip_match:
                return 0
            return 1
        except:
            return 0
        

    def extract_features(self, url):
        return np.array([self.has_ip_address(url),
                         self.url_length(url),
                         self.shortening_service(url),
                         self.has_at_symbol(url),
                         self.double_slash_redirecting(url),
                         self.prefix_suffix(url),
                         self.subdomain_count(url),
                         self.ssl_final_state(url),
                         self.domain_registration_length(url),
                         self.favicon(url),
                         self.port(url),
                         self.https_token(url),
                         self.request_url(url),
                         self.url_of_anchor(url),
                         self.links_in_tags(url),
                         self.sfh(url),
                         self.submitting_to_email(url),
                         self.abnormal_url(url),
                         self.redirect(url),
                         self.on_mouseover(url),
                         self.right_click(url),
                         self.pop_up_window(url),
                         self.iframe(url),
                         self.age_of_domain(url),
                         self.dns_record(url),
                         self.web_traffic(url),
                         self.page_rank(url),
                         self.google_index(url),
                         self.links_pointing_to_page(url),
                         self.statistical_report(url)]).reshape(1, -1)
