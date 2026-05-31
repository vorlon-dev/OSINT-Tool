import os
import sys
import socket
import datetime
import platform
import subprocess

def install():
    pkgs = ["requests", "colorama"]
    for pkg in pkgs:
        try:
            __import__(pkg)
        except ImportError:
            print("[*] Installing " + pkg + "...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])
            print("[+] " + pkg + " installed!")

install()

import requests
from colorama import Fore, Style, init
init(autoreset=True)

VERSION = "5.0 PRO"
AUTHOR = "PRATAM"
START_TIME = datetime.datetime.now()

STATS = {
    "total_scans": 0,
    "profiles_found": 0,
    "ips_scanned": 0,
    "emails_analyzed": 0,
    "phones_analyzed": 0,
    "domains_scanned": 0,
    "open_ports": 0,
    "api_calls": 0,
    "reports_saved": 0
}

SCAN_HISTORY = []

for folder in ["results", "reports", "cache"]:
    os.makedirs(folder, exist_ok=True)

LOG_FILE = os.path.join("results", "osint.log")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

APIS = {
    "ip_api"       : "http://ip-api.com/json",
    "ipinfo"       : "https://ipinfo.io",
    "hackertarget" : "https://api.hackertarget.com",
    "emailrep"     : "https://emailrep.io",
    "disify"       : "https://www.disify.com/api/email",
    "github"       : "https://api.github.com",
    "reddit"       : "https://www.reddit.com",
    "hn"           : "https://hn.algolia.com/api/v1",
    "alienvault"   : "https://otx.alienvault.com/api/v1",
    "crtsh"        : "https://crt.sh",
}

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def show_banner():
    clear_screen()
    print(Fore.CYAN + "")
    print(Fore.CYAN + "  ================================================================")
    print(Fore.CYAN + "   OSINT TOOL")
    print(Fore.YELLOW + "   Version  : " + VERSION)
    print(Fore.GREEN + "   Author   : " + AUTHOR)
    print(Fore.CYAN + "   Platform : Windows | Linux | Mac | Termux")
    print(Fore.RED + "   Legal    : Educational Use Only")
    print(Fore.CYAN + "  ================================================================")
    print()

def show_section(title):
    print(Fore.CYAN + "")
    print(Fore.CYAN + "  ================================================================")
    print(Fore.YELLOW + "   >> " + title)
    print(Fore.CYAN + "  ================================================================")
    print()

def show_sub(title):
    print()
    print(Fore.CYAN + "  --- " + title + " ---")
    print()

def show_info(key, value, color=Fore.YELLOW):
    pad = " " * (25 - len(str(key)))
    print(Fore.CYAN + "  " + str(key) + pad + " : " + color + str(value))

def show_log(message, log_type="INFO"):
    time_str = datetime.datetime.now().strftime("%H:%M:%S")
    colors = {
        "SUCCESS": Fore.GREEN,
        "ERROR"  : Fore.RED,
        "WARN"   : Fore.YELLOW,
        "SCAN"   : Fore.CYAN,
        "API"    : Fore.MAGENTA,
        "INFO"   : Fore.WHITE
    }
    color = colors.get(log_type, Fore.WHITE)
    print(color + "  [" + time_str + "][" + log_type + "] " + message)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write("[" + time_str + "][" + log_type + "] " + message + "\n")
    except:
        pass

def show_found(name, url):
    print(Fore.GREEN + "  [FOUND] " + name)
    print(Fore.CYAN + "          -> " + url)

def show_progress(current, total, status=""):
    if total == 0:
        return
    percent = round((current / total) * 100)
    filled = round(percent / 2.5)
    if filled > 40:
        filled = 40
    empty = 40 - filled
    bar = "=" * filled + "-" * empty
    print("\r  [" + bar + "] " + str(percent) + "% | " + status + "                    ", end="", flush=True)

def call_api(url, api_name="API", method="GET", data=None):
    STATS["api_calls"] += 1
    try:
        if method == "POST":
            r = requests.post(url, headers=HEADERS, json=data, timeout=15)
        else:
            r = requests.get(url, headers=HEADERS, timeout=15)
        show_log("API success: " + api_name, "API")
        ct = r.headers.get("content-type", "")
        if "json" in ct:
            return r.json()
        return r.text
    except Exception as e:
        show_log("API failed: " + api_name, "WARN")
        return None

def save_report(content, target, report_type):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe = "".join(c if c.isalnum() else "_" for c in target)
    filename = "OSINT_" + report_type + "_" + safe + "_" + timestamp + ".txt"
    filepath = os.path.join("reports", filename)
    header = (
        "================================================================\n"
        "OSINT FRAMEWORK v" + VERSION + " - MADE BY PRATAM\n"
        "================================================================\n"
        "Report : " + report_type + "\n"
        "Target : " + target + "\n"
        "Date   : " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
        "================================================================\n\n"
        + content +
        "\n================================================================\n"
        "MADE BY PRATAM\n"
        "================================================================\n"
    )
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(header)
    STATS["reports_saved"] += 1
    show_log("Report saved: " + filepath, "SUCCESS")
    return filepath

def ask_save(content, target, report_type):
    print()
    save = input(Fore.YELLOW + "  Save report? [Y/N]: " + Fore.WHITE).strip().upper()
    if save == "Y":
        path = save_report(content, target, report_type)
        print(Fore.GREEN + "  [+] Saved: " + path)

def add_history(module, target, result):
    SCAN_HISTORY.append({
        "time"   : datetime.datetime.now().strftime("%H:%M:%S"),
        "module" : module,
        "target" : target,
        "result" : result
    })

def search_username(username):
    show_section("USERNAME SEARCH: " + username)
    show_log("Scanning 100+ platforms...", "SCAN")

    platforms = {
        "GitHub"        : "https://github.com/" + username,
        "Twitter"       : "https://twitter.com/" + username,
        "Instagram"     : "https://instagram.com/" + username,
        "TikTok"        : "https://tiktok.com/@" + username,
        "Reddit"        : "https://reddit.com/user/" + username,
        "YouTube"       : "https://youtube.com/@" + username,
        "LinkedIn"      : "https://linkedin.com/in/" + username,
        "Facebook"      : "https://facebook.com/" + username,
        "Snapchat"      : "https://snapchat.com/add/" + username,
        "Pinterest"     : "https://pinterest.com/" + username,
        "Tumblr"        : "https://" + username + ".tumblr.com",
        "Flickr"        : "https://flickr.com/people/" + username,
        "VK"            : "https://vk.com/" + username,
        "Telegram"      : "https://t.me/" + username,
        "Quora"         : "https://quora.com/profile/" + username,
        "Wattpad"       : "https://wattpad.com/user/" + username,
        "9GAG"          : "https://9gag.com/u/" + username,
        "Imgur"         : "https://imgur.com/user/" + username,
        "Gravatar"      : "https://gravatar.com/" + username,
        "GitLab"        : "https://gitlab.com/" + username,
        "Bitbucket"     : "https://bitbucket.org/" + username,
        "CodePen"       : "https://codepen.io/" + username,
        "Replit"        : "https://replit.com/@" + username,
        "StackOverflow" : "https://stackoverflow.com/users/" + username,
        "HackerRank"    : "https://hackerrank.com/" + username,
        "LeetCode"      : "https://leetcode.com/" + username,
        "HackerNews"    : "https://news.ycombinator.com/user?id=" + username,
        "Dev.to"        : "https://dev.to/" + username,
        "Medium"        : "https://medium.com/@" + username,
        "Hashnode"      : "https://hashnode.com/@" + username,
        "NPM"           : "https://npmjs.com/~" + username,
        "PyPI"          : "https://pypi.org/user/" + username,
        "DockerHub"     : "https://hub.docker.com/u/" + username,
        "Twitch"        : "https://twitch.tv/" + username,
        "Steam"         : "https://steamcommunity.com/id/" + username,
        "PSN"           : "https://psnprofiles.com/" + username,
        "Roblox"        : "https://roblox.com/user.aspx?username=" + username,
        "Minecraft"     : "https://namemc.com/profile/" + username,
        "ChessCom"      : "https://chess.com/member/" + username,
        "Lichess"       : "https://lichess.org/@/" + username,
        "Faceit"        : "https://faceit.com/en/players/" + username,
        "DeviantArt"    : "https://deviantart.com/" + username,
        "ArtStation"    : "https://artstation.com/" + username,
        "Behance"       : "https://behance.net/" + username,
        "Dribbble"      : "https://dribbble.com/" + username,
        "SoundCloud"    : "https://soundcloud.com/" + username,
        "Spotify"       : "https://open.spotify.com/user/" + username,
        "Bandcamp"      : "https://" + username + ".bandcamp.com",
        "Vimeo"         : "https://vimeo.com/" + username,
        "AngelList"     : "https://angel.co/" + username,
        "ProductHunt"   : "https://producthunt.com/@" + username,
        "Fiverr"        : "https://fiverr.com/" + username,
        "Freelancer"    : "https://freelancer.com/u/" + username,
        "TryHackMe"     : "https://tryhackme.com/p/" + username,
        "HackTheBox"    : "https://app.hackthebox.com/profile/" + username,
        "Bugcrowd"      : "https://bugcrowd.com/" + username,
        "HackerOne"     : "https://hackerone.com/" + username,
        "Pastebin"      : "https://pastebin.com/u/" + username,
        "Keybase"       : "https://keybase.io/" + username,
        "AboutMe"       : "https://about.me/" + username,
        "Linktree"      : "https://linktr.ee/" + username,
        "Goodreads"     : "https://goodreads.com/" + username,
        "LastFM"        : "https://last.fm/user/" + username,
        "MyAnimeList"   : "https://myanimelist.net/profile/" + username,
        "Letterboxd"    : "https://letterboxd.com/" + username,
        "Strava"        : "https://strava.com/athletes/" + username,
        "Duolingo"      : "https://duolingo.com/profile/" + username,
        "Ko-fi"         : "https://ko-fi.com/" + username,
        "Patreon"       : "https://patreon.com/" + username,
        "ResearchGate"  : "https://researchgate.net/profile/" + username,
        "Academia"      : "https://independent.academia.edu/" + username,
        "Substack"      : "https://" + username + ".substack.com",
        "Codeforces"    : "https://codeforces.com/profile/" + username,
        "Codecademy"    : "https://codecademy.com/profiles/" + username,
        "Scribd"        : "https://scribd.com/" + username,
        "Etsy"          : "https://etsy.com/people/" + username,
        "Poshmark"      : "https://poshmark.com/closet/" + username,
        "Trakt"         : "https://trakt.tv/users/" + username,
        "Untappd"       : "https://untappd.com/user/" + username,
        "Lichess"       : "https://lichess.org/@/" + username,
        "OpenSea"       : "https://opensea.io/" + username,
    }

    print()
    show_info("Target", username, Fore.WHITE)
    show_info("Platforms", str(len(platforms)), Fore.YELLOW)
    print()

    found_count = 0
    total = len(platforms)
    current = 0
    output = ""
    found_list = []

    for name, url in sorted(platforms.items()):
        current += 1
        show_progress(current, total, name)
        try:
            r = requests.head(url, headers=HEADERS, timeout=8, allow_redirects=True)
            if r.status_code == 200:
                print()
                show_found(name, url)
                found_count += 1
                found_list.append(name)
                output += "[FOUND] " + name + "\n  URL: " + url + "\n\n"
                STATS["profiles_found"] += 1
        except:
            pass

    print("\n")

    show_sub("GITHUB API")
    gh = call_api(APIS["github"] + "/users/" + username, "GitHub")
    if gh and isinstance(gh, dict) and "login" in gh:
        print(Fore.GREEN + "  [+] GitHub user found!")
        show_info("Name",      str(gh.get("name", "N/A")),     Fore.WHITE)
        show_info("Location",  str(gh.get("location", "N/A")), Fore.YELLOW)
        show_info("Email",     str(gh.get("email", "N/A")),    Fore.CYAN)
        show_info("Bio",       str(gh.get("bio", "N/A")),      Fore.WHITE)
        show_info("Company",   str(gh.get("company", "N/A")),  Fore.YELLOW)
        show_info("Followers", str(gh.get("followers", 0)),    Fore.GREEN)
        show_info("Repos",     str(gh.get("public_repos", 0)), Fore.GREEN)
        show_info("Created",   str(gh.get("created_at", "N/A")), Fore.WHITE)
        output += "GitHub: " + str(gh.get("name")) + " | " + str(gh.get("location")) + "\n\n"

    show_sub("REDDIT API")
    rd = call_api(APIS["reddit"] + "/user/" + username + "/about.json", "Reddit")
    if rd and isinstance(rd, dict) and "data" in rd:
        data = rd["data"]
        print(Fore.GREEN + "  [+] Reddit user found!")
        show_info("Name",  str(data.get("name", "N/A")),    Fore.WHITE)
        show_info("Karma", str(data.get("total_karma", 0)), Fore.YELLOW)

    show_sub("HACKERNEWS API")
    hn = call_api(APIS["hn"] + "/users/" + username, "HackerNews")
    if hn and isinstance(hn, dict) and "username" in hn:
        print(Fore.GREEN + "  [+] HackerNews user found!")
        show_info("Username", str(hn.get("username", "N/A")), Fore.WHITE)
        show_info("Karma",    str(hn.get("karma", 0)),        Fore.YELLOW)

    show_sub("SUMMARY")
    show_info("Platforms Scanned", str(total),               Fore.CYAN)
    show_info("Profiles Found",    str(found_count),         Fore.GREEN)
    show_info("Not Found",         str(total - found_count), Fore.RED)

    if found_list:
        print(Fore.GREEN + "\n  Found on:")
        for p in found_list:
            print(Fore.GREEN + "    -> " + p)

    show_sub("GOOGLE DORKS")
    print(Fore.CYAN + "  -> https://google.com/search?q=" + username)
    print(Fore.CYAN + "  -> https://google.com/search?q=" + username + " site:pastebin.com")
    print(Fore.CYAN + "  -> https://google.com/search?q=" + username + " email")
    print(Fore.CYAN + "  -> https://bing.com/search?q=" + username)
    print(Fore.CYAN + "  -> https://duckduckgo.com/?q=" + username)

    add_history("Username", username, str(found_count) + " found")
    show_log("Scan complete: " + str(found_count) + " found", "SUCCESS")
    ask_save(output, username, "Username")

def get_ip_info(ip):
    show_section("IP INTELLIGENCE: " + ip)
    output = ""

    data1 = call_api(APIS["ip_api"] + "/" + ip + "?fields=status,country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,as,mobile,proxy,hosting,query", "ip-api.com")
    if data1 and isinstance(data1, dict) and data1.get("status") == "success":
        show_info("IP",        str(data1.get("query", "")),      Fore.WHITE)
        show_info("Country",   str(data1.get("country", "")) + " [" + str(data1.get("countryCode", "")) + "]", Fore.YELLOW)
        show_info("City",      str(data1.get("city", "")),       Fore.YELLOW)
        show_info("ISP",       str(data1.get("isp", "")),        Fore.GREEN)
        show_info("Org",       str(data1.get("org", "")),        Fore.GREEN)
        show_info("Timezone",  str(data1.get("timezone", "")),   Fore.CYAN)
        show_info("Lat/Lon",   str(data1.get("lat", "")) + ", " + str(data1.get("lon", "")), Fore.CYAN)
        mobile_val = data1.get("mobile", False)
        proxy_val  = data1.get("proxy", False)
        show_info("Mobile",    str(mobile_val), Fore.RED if mobile_val else Fore.GREEN)
        show_info("Proxy/VPN", str(proxy_val),  Fore.RED if proxy_val  else Fore.GREEN)
        output += "IP: " + str(data1.get("query")) + "\nCountry: " + str(data1.get("country")) + "\nISP: " + str(data1.get("isp")) + "\n\n"

    data2 = call_api(APIS["ipinfo"] + "/" + ip + "/json", "ipinfo.io")
    if data2 and isinstance(data2, dict):
        show_info("Hostname", str(data2.get("hostname", "N/A")), Fore.WHITE)

    av = call_api(APIS["alienvault"] + "/indicators/IPv4/" + ip + "/general", "AlienVault")
    if av and isinstance(av, dict):
        pulse_count = av.get("pulse_info", {}).get("count", 0)
        show_info("Threat Pulses", str(pulse_count), Fore.RED if pulse_count > 0 else Fore.GREEN)
        if pulse_count > 0:
            print(Fore.RED + "  [!] WARNING: IP flagged in " + str(pulse_count) + " threat reports!")

    show_sub("PORT SCAN")
    ports = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
        53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
        443: "HTTPS", 445: "SMB", 1433: "MSSQL", 3306: "MySQL",
        3389: "RDP", 5432: "PostgreSQL", 5900: "VNC", 6379: "Redis",
        8080: "HTTP-Alt", 8443: "HTTPS-Alt", 27017: "MongoDB", 9200: "Elasticsearch"
    }
    open_ports = []
    port_num = 0
    for port, service in sorted(ports.items()):
        port_num += 1
        show_progress(port_num, len(ports), "Port " + str(port) + " " + service)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            if sock.connect_ex((ip, port)) == 0:
                print()
                print(Fore.GREEN + "  [OPEN] Port " + str(port) + " - " + service)
                open_ports.append(str(port) + "/" + service)
                STATS["open_ports"] += 1
            sock.close()
        except:
            pass
    print()
    if open_ports:
        show_info("Open Ports", str(len(open_ports)), Fore.RED)
    else:
        print(Fore.LIGHTBLACK_EX + "  No open ports detected")

    show_sub("INVESTIGATION LINKS")
    print(Fore.CYAN + "  -> Shodan     : https://shodan.io/host/" + ip)
    print(Fore.CYAN + "  -> VirusTotal : https://virustotal.com/gui/ip-address/" + ip)
    print(Fore.CYAN + "  -> AbuseIPDB  : https://abuseipdb.com/check/" + ip)
    print(Fore.CYAN + "  -> AlienVault : https://otx.alienvault.com/indicator/ip/" + ip)
    print(Fore.CYAN + "  -> Censys     : https://search.censys.io/hosts/" + ip)
    print(Fore.CYAN + "  -> GreyNoise  : https://viz.greynoise.io/ip/" + ip)

    STATS["ips_scanned"] += 1
    add_history("IP", ip, str(len(open_ports)) + " ports open")
    show_log("IP intelligence complete", "SUCCESS")
    ask_save(output, ip, "IP")

def get_email_info(email):
    show_section("EMAIL INTELLIGENCE: " + email)
    if "@" not in email:
        show_log("Invalid email!", "ERROR")
        return
    parts  = email.split("@")
    user   = parts[0]
    domain = parts[1]
    output = ""

    show_info("Full Email", email,  Fore.WHITE)
    show_info("Username",   user,   Fore.YELLOW)
    show_info("Domain",     domain, Fore.YELLOW)
    show_info("Has Numbers",    str(any(c.isdigit() for c in user)), Fore.WHITE)
    show_info("Has Dots",       str("." in user), Fore.WHITE)
    show_info("Has Underscore", str("_" in user), Fore.WHITE)

    er = call_api(APIS["emailrep"] + "/" + email, "EmailRep.io")
    if er and isinstance(er, dict):
        details = er.get("details", {})
        show_info("Reputation",         str(er.get("reputation", "N/A")),             Fore.YELLOW)
        show_info("Credentials Leaked", str(details.get("credentials_leaked", False)), Fore.RED if details.get("credentials_leaked") else Fore.GREEN)
        show_info("Disposable",         str(details.get("disposable", False)),         Fore.RED if details.get("disposable") else Fore.GREEN)
        show_info("Valid MX",           str(details.get("valid_mx", False)),           Fore.GREEN if details.get("valid_mx") else Fore.RED)
        show_info("Suspicious",         str(er.get("suspicious", False)),              Fore.RED if er.get("suspicious") else Fore.GREEN)
        output += "Reputation: " + str(er.get("reputation")) + "\n\n"

    di = call_api(APIS["disify"] + "/" + email, "Disify")
    if di and isinstance(di, dict):
        show_info("Valid Format", str(di.get("format", False)),     Fore.GREEN if di.get("format")     else Fore.RED)
        show_info("Disposable",   str(di.get("disposable", False)), Fore.RED   if di.get("disposable") else Fore.GREEN)
        show_info("DNS Valid",    str(di.get("dns", False)),        Fore.GREEN if di.get("dns")        else Fore.RED)

    providers = {
        "gmail.com"     : ("Google Gmail",   "High"),
        "yahoo.com"     : ("Yahoo Mail",      "Medium"),
        "hotmail.com"   : ("MS Hotmail",      "High"),
        "outlook.com"   : ("MS Outlook",      "High"),
        "protonmail.com": ("ProtonMail E2EE", "Very High"),
        "proton.me"     : ("ProtonMail E2EE", "Very High"),
        "tutanota.com"  : ("Tutanota E2EE",   "Very High"),
        "icloud.com"    : ("Apple iCloud",    "High"),
        "aol.com"       : ("AOL Mail",        "Low"),
        "zoho.com"      : ("Zoho Mail",       "Medium"),
        "yandex.com"    : ("Yandex Mail",     "Low"),
        "yandex.ru"     : ("Yandex Mail",     "Low"),
        "gmx.com"       : ("GMX Mail",        "Medium"),
        "mail.com"      : ("Mail.com",        "Medium"),
        "mailinator.com": ("Mailinator",      "None"),
        "tempmail.com"  : ("Temp Mail",       "None"),
        "guerrillamail.com": ("Guerrilla Mail","None"),
    }
    pinfo = providers.get(domain, ("Custom Domain", "Unknown"))
    sc = Fore.GREEN if pinfo[1] in ["High", "Very High"] else Fore.RED if pinfo[1] in ["Low", "None"] else Fore.YELLOW
    show_info("Provider", pinfo[0], Fore.CYAN)
    show_info("Security", pinfo[1], sc)

    show_sub("BREACH LINKS")
    print(Fore.CYAN + "  -> HaveIBeenPwned : https://haveibeenpwned.com/account/" + email)
    print(Fore.CYAN + "  -> Dehashed       : https://dehashed.com/search?query=" + email)
    print(Fore.CYAN + "  -> IntelX         : https://intelx.io/?s=" + email)
    print(Fore.CYAN + "  -> Epieos         : https://epieos.com/?q=" + email)
    print(Fore.CYAN + "  -> LeakCheck      : https://leakcheck.io/search/" + email)
    print(Fore.CYAN + "  -> SnusBase       : https://snusbase.com")

    STATS["emails_analyzed"] += 1
    add_history("Email", email, "Complete")
    show_log("Email analysis complete", "SUCCESS")
    ask_save(output, email, "Email")

def get_phone_info(phone):
    show_section("PHONE INTELLIGENCE: " + phone)
    clean  = "".join(c for c in phone if c.isdigit() or c == "+")
    digits = "".join(c for c in clean if c.isdigit())

    show_info("Original", phone,            Fore.WHITE)
    show_info("Cleaned",  clean,            Fore.YELLOW)
    show_info("Length",   str(len(digits)), Fore.WHITE)

    fmt = "Unknown"
    if len(digits) == 10: fmt = "National 10 digits"
    if len(digits) == 11: fmt = "International 11 digits"
    if clean.startswith("+"): fmt += " E.164"
    show_info("Format", fmt, Fore.CYAN)

    countries = [
        ("+1",   "USA / Canada",   "North America"),
        ("+44",  "UK",             "Europe"),
        ("+91",  "India",          "Asia"),
        ("+86",  "China",          "Asia"),
        ("+81",  "Japan",          "Asia"),
        ("+49",  "Germany",        "Europe"),
        ("+33",  "France",         "Europe"),
        ("+39",  "Italy",          "Europe"),
        ("+34",  "Spain",          "Europe"),
        ("+7",   "Russia",         "Europe/Asia"),
        ("+55",  "Brazil",         "South America"),
        ("+82",  "South Korea",    "Asia"),
        ("+90",  "Turkey",         "Europe/Asia"),
        ("+92",  "Pakistan",       "Asia"),
        ("+62",  "Indonesia",      "Asia"),
        ("+63",  "Philippines",    "Asia"),
        ("+880", "Bangladesh",     "Asia"),
        ("+234", "Nigeria",        "Africa"),
        ("+27",  "South Africa",   "Africa"),
        ("+20",  "Egypt",          "Africa"),
        ("+971", "UAE",            "Middle East"),
        ("+966", "Saudi Arabia",   "Middle East"),
        ("+965", "Kuwait",         "Middle East"),
        ("+974", "Qatar",          "Middle East"),
        ("+973", "Bahrain",        "Middle East"),
        ("+968", "Oman",           "Middle East"),
        ("+961", "Lebanon",        "Middle East"),
        ("+962", "Jordan",         "Middle East"),
        ("+964", "Iraq",           "Middle East"),
        ("+98",  "Iran",           "Middle East"),
        ("+52",  "Mexico",         "North America"),
        ("+54",  "Argentina",      "South America"),
        ("+56",  "Chile",          "South America"),
        ("+57",  "Colombia",       "South America"),
        ("+61",  "Australia",      "Oceania"),
        ("+64",  "New Zealand",    "Oceania"),
        ("+65",  "Singapore",      "Asia"),
        ("+60",  "Malaysia",       "Asia"),
        ("+66",  "Thailand",       "Asia"),
        ("+84",  "Vietnam",        "Asia"),
        ("+212", "Morocco",        "Africa"),
        ("+213", "Algeria",        "Africa"),
        ("+216", "Tunisia",        "Africa"),
        ("+249", "Sudan",          "Africa"),
        ("+254", "Kenya",          "Africa"),
        ("+31",  "Netherlands",    "Europe"),
        ("+32",  "Belgium",        "Europe"),
        ("+41",  "Switzerland",    "Europe"),
        ("+46",  "Sweden",         "Europe"),
        ("+47",  "Norway",         "Europe"),
        ("+48",  "Poland",         "Europe"),
        ("+40",  "Romania",        "Europe"),
        ("+30",  "Greece",         "Europe"),
    ]

    country_name = "Unknown"
    country_region = "Unknown"
    for code, name, region in countries:
        if clean.startswith(code):
            country_name = name
            country_region = region
            break

    show_info("Country", country_name,   Fore.GREEN)
    show_info("Region",  country_region, Fore.YELLOW)
    print(Fore.CYAN + "  E.164 : +" + digits)

    show_sub("LOOKUP TOOLS")
    print(Fore.CYAN + "  -> Google     : https://google.com/search?q=" + clean)
    print(Fore.CYAN + "  -> Truecaller : https://truecaller.com/search/us/" + digits)
    print(Fore.CYAN + "  -> NumLookup  : https://numlookup.com/?number=" + clean)
    print(Fore.CYAN + "  -> WhitePages : https://whitepages.com/phone/" + digits)
    print(Fore.CYAN + "  -> Sync.me    : https://sync.me/search/?number=" + clean)

    STATS["phones_analyzed"] += 1
    add_history("Phone", phone, country_name)
    show_log("Phone analysis complete", "SUCCESS")

def get_domain_info(domain):
    show_section("DOMAIN INTELLIGENCE: " + domain)
    output = ""

    ht = call_api(APIS["hackertarget"] + "/dnslookup/?q=" + domain, "HackerTarget")
    if ht:
        print(Fore.YELLOW + str(ht)[:500])
        output += str(ht) + "\n\n"

    crt = call_api(APIS["crtsh"] + "/?q=" + domain + "&output=json", "crt.sh")
    if crt and isinstance(crt, list):
        print(Fore.GREEN + "  [+] " + str(len(crt)) + " SSL certificates found")
        unique = set()
        for cert in crt[:20]:
            for name in cert.get("name_value", "").split("\n"):
                name = name.strip()
                if name and name not in unique:
                    unique.add(name)
                    print(Fore.GREEN + "  -> " + name)

    av = call_api(APIS["alienvault"] + "/indicators/domain/" + domain + "/general", "AlienVault")
    if av and isinstance(av, dict):
        pulse_count = av.get("pulse_info", {}).get("count", 0)
        show_info("Threat Pulses", str(pulse_count), Fore.RED if pulse_count > 0 else Fore.GREEN)
        if pulse_count > 0:
            print(Fore.RED + "  [!] Domain flagged in threat intelligence!")

    show_sub("SUBDOMAIN SCAN")
    subs = [
        "www", "mail", "ftp", "admin", "api", "dev", "staging",
        "blog", "shop", "m", "app", "portal", "vpn", "smtp",
        "ns1", "ns2", "db", "git", "test", "beta", "demo",
        "cdn", "static", "files", "backup", "secure", "login"
    ]
    found_subs = []
    for i, sub in enumerate(subs):
        show_progress(i + 1, len(subs), sub + "." + domain)
        fqdn = sub + "." + domain
        try:
            socket.gethostbyname(fqdn)
            print()
            print(Fore.GREEN + "  [FOUND] " + fqdn)
            found_subs.append(fqdn)
        except:
            pass
    print()
    show_info("Subdomains Found", str(len(found_subs)), Fore.GREEN)

    show_sub("INVESTIGATION LINKS")
    print(Fore.CYAN + "  -> WHOIS          : https://who.is/whois/" + domain)
    print(Fore.CYAN + "  -> Shodan         : https://shodan.io/search?query=hostname:" + domain)
    print(Fore.CYAN + "  -> VirusTotal     : https://virustotal.com/gui/domain/" + domain)
    print(Fore.CYAN + "  -> Wayback        : https://web.archive.org/web/*/" + domain)
    print(Fore.CYAN + "  -> crt.sh         : https://crt.sh/?q=" + domain)
    print(Fore.CYAN + "  -> Censys         : https://search.censys.io/search?q=" + domain)
    print(Fore.CYAN + "  -> SecurityTrails : https://securitytrails.com/domain/" + domain + "/dns")
    print(Fore.CYAN + "  -> DNSDumpster    : https://dnsdumpster.com")
    print(Fore.CYAN + "  -> AlienVault     : https://otx.alienvault.com/indicator/domain/" + domain)

    STATS["domains_scanned"] += 1
    add_history("Domain", domain, str(len(found_subs)) + " subs")
    show_log("Domain analysis complete", "SUCCESS")
    ask_save(output, domain, "Domain")

def search_person(first, last, location="", age=""):
    full = first + " " + last
    show_section("PERSON SEARCH: " + full)
    show_info("Full Name", full, Fore.WHITE)
    if location: show_info("Location", location, Fore.CYAN)
    if age:      show_info("Age",      age,      Fore.WHITE)

    encoded = requests.utils.quote(full)

    show_sub("PEOPLE SEARCH ENGINES")
    print(Fore.CYAN + "  -> Spokeo           : https://spokeo.com/search?q=" + encoded)
    print(Fore.CYAN + "  -> Whitepages       : https://whitepages.com/name/" + first + "-" + last)
    print(Fore.CYAN + "  -> BeenVerified     : https://beenverified.com/people/" + first + "-" + last)
    print(Fore.CYAN + "  -> TruePeopleSearch : https://truepeoplesearch.com/results?name=" + encoded)
    print(Fore.CYAN + "  -> FastPeopleSearch : https://fastpeoplesearch.com/name/" + first + "-" + last)
    print(Fore.CYAN + "  -> PeekYou          : https://peekyou.com/" + first + "+" + last)
    print(Fore.CYAN + "  -> Pipl             : https://pipl.com/search/?q=" + encoded)
    print(Fore.CYAN + "  -> Radaris          : https://radaris.com/p/" + first + "/" + last)
    print(Fore.CYAN + "  -> Intelius         : https://intelius.com/people/" + first + "-" + last)

    show_sub("SOCIAL MEDIA")
    print(Fore.CYAN + "  -> LinkedIn  : https://linkedin.com/search/results/people/?keywords=" + encoded)
    print(Fore.CYAN + "  -> Facebook  : https://facebook.com/search/people/?q=" + encoded)
    print(Fore.CYAN + "  -> Twitter   : https://twitter.com/search?q=" + encoded + "&f=user")
    print(Fore.CYAN + "  -> TikTok    : https://tiktok.com/search/user?q=" + encoded)
    print(Fore.CYAN + "  -> Instagram : https://instagram.com/explore/tags/" + first + last)

    show_sub("GOOGLE DORKS")
    print(Fore.CYAN + "  -> https://google.com/search?q=" + full)
    print(Fore.CYAN + "  -> https://google.com/search?q=" + full + " site:linkedin.com")
    print(Fore.CYAN + "  -> https://google.com/search?q=" + full + " site:facebook.com")
    print(Fore.CYAN + "  -> https://google.com/search?q=" + full + " filetype:pdf")
    print(Fore.CYAN + "  -> https://google.com/search?q=" + full + " email")
    print(Fore.CYAN + "  -> https://google.com/search?q=" + full + " phone")

    show_sub("IMAGE SEARCH")
    print(Fore.CYAN + "  -> Google Images : https://google.com/search?q=" + full + "&tbm=isch")
    print(Fore.CYAN + "  -> Bing Images   : https://bing.com/images/search?q=" + full)
    print(Fore.CYAN + "  -> Yandex        : https://yandex.com/images/search?text=" + encoded)

    add_history("Person", full, "Complete")
    show_log("Person search complete", "SUCCESS")

def search_breaches(target):
    show_section("BREACH HUNTER: " + target)

    show_sub("BREACH DATABASES")
    print(Fore.CYAN + "  -> HaveIBeenPwned  : https://haveibeenpwned.com/account/" + target)
    print(Fore.CYAN + "  -> Dehashed        : https://dehashed.com/search?query=" + target)
    print(Fore.CYAN + "  -> LeakCheck       : https://leakcheck.io/search/" + target)
    print(Fore.CYAN + "  -> IntelX          : https://intelx.io/?s=" + target)
    print(Fore.CYAN + "  -> BreachDirectory : https://breachdirectory.org")
    print(Fore.CYAN + "  -> SnusBase        : https://snusbase.com")
    print(Fore.CYAN + "  -> WeLeakInfo      : https://weleakinfo.to/search/" + target)

    show_sub("PASTE SITES")
    print(Fore.CYAN + "  -> Pastebin : https://pastebin.com/search?q=" + target)
    print(Fore.CYAN + "  -> Hastebin : https://hastebin.com/search/" + target)

    show_sub("GOOGLE DORKS")
    print(Fore.RED + "  -> https://google.com/search?q=" + target + " site:pastebin.com")
    print(Fore.RED + "  -> https://google.com/search?q=" + target + " password")
    print(Fore.RED + "  -> https://google.com/search?q=" + target + " leaked")
    print(Fore.RED + "  -> https://google.com/search?q=" + target + " breach")
    print(Fore.RED + "  -> https://google.com/search?q=" + target + " credentials")

    add_history("Breach", target, "Complete")
    show_log("Breach search complete", "SUCCESS")

def get_network_info():
    show_section("LOCAL NETWORK INFO")

    show_sub("YOUR PUBLIC IP")
    try:
        pub = requests.get("https://api.ipify.org?format=json", timeout=5).json()
        pub_ip = pub.get("ip", "Unknown")
        show_info("Public IP", pub_ip, Fore.GREEN)
        geo = call_api(APIS["ip_api"] + "/" + pub_ip, "ip-api.com")
        if geo and isinstance(geo, dict) and geo.get("status") == "success":
            show_info("Location",  str(geo.get("city")) + ", " + str(geo.get("country")), Fore.YELLOW)
            show_info("ISP",       str(geo.get("isp", "N/A")), Fore.CYAN)
            proxy = geo.get("proxy", False)
            show_info("Proxy/VPN", str(proxy), Fore.RED if proxy else Fore.GREEN)
    except:
        show_log("Could not get public IP", "ERROR")

    show_sub("SYSTEM INFO")
    show_info("Hostname", socket.gethostname(),      Fore.WHITE)
    show_info("Platform", platform.system(),         Fore.WHITE)
    show_info("Machine",  platform.machine(),        Fore.WHITE)
    show_info("Python",   platform.python_version(), Fore.GREEN)
    show_info("Username", os.environ.get("USER", os.environ.get("USERNAME", "Unknown")), Fore.WHITE)

    show_sub("LOCAL IP")
    try:
        show_info("Local IP", socket.gethostbyname(socket.gethostname()), Fore.YELLOW)
    except:
        pass

    show_sub("PRIVACY TOOLS")
    print(Fore.CYAN + "  -> IP Leak  : https://ipleak.net")
    print(Fore.CYAN + "  -> DNS Leak : https://dnsleaktest.com")
    print(Fore.CYAN + "  -> Speed    : https://fast.com")
    print(Fore.CYAN + "  -> WebRTC   : https://browserleaks.com/webrtc")

    show_log("Network scan complete", "SUCCESS")

def get_dorks(target):
    show_section("GOOGLE DORK GENERATOR: " + target)

    show_sub("BASIC SEARCHES")
    print(Fore.CYAN + "  -> https://google.com/search?q=" + target)
    print(Fore.CYAN + "  -> https://google.com/search?q=intitle:" + target)
    print(Fore.CYAN + "  -> https://google.com/search?q=inurl:" + target)
    print(Fore.CYAN + "  -> https://google.com/search?q=intext:" + target)

    show_sub("FILE SEARCHES")
    for ft in ["pdf", "doc", "xls", "txt", "csv", "sql", "log", "xml", "json"]:
        print(Fore.CYAN + "  -> https://google.com/search?q=" + target + " filetype:" + ft)

    show_sub("SOCIAL MEDIA")
    for site in ["linkedin.com", "facebook.com", "twitter.com", "instagram.com", "github.com", "reddit.com"]:
        print(Fore.CYAN + "  -> https://google.com/search?q=" + target + " site:" + site)

    show_sub("SENSITIVE DATA")
    for term in ["password", "email", "phone", "leaked", "credentials", "api key"]:
        print(Fore.RED + "  -> https://google.com/search?q=" + target + " " + term)

    show_sub("OTHER ENGINES")
    print(Fore.CYAN + "  -> Bing       : https://bing.com/search?q=" + target)
    print(Fore.CYAN + "  -> DuckDuckGo : https://duckduckgo.com/?q=" + target)
    print(Fore.CYAN + "  -> Yandex     : https://yandex.com/search/?text=" + target)
    print(Fore.CYAN + "  -> Startpage  : https://startpage.com/search?q=" + target)

    show_log("Dorks generated", "SUCCESS")

def get_threat_intel(target):
    show_section("THREAT INTELLIGENCE: " + target)

    av = call_api(APIS["alienvault"] + "/indicators/IPv4/" + target + "/general", "AlienVault")
    if av and isinstance(av, dict):
        pulse_count = av.get("pulse_info", {}).get("count", 0)
        show_info("Threat Pulses", str(pulse_count), Fore.RED if pulse_count > 0 else Fore.GREEN)
        show_info("Reputation",    str(av.get("reputation", "N/A")), Fore.YELLOW)
        if pulse_count > 0:
            print(Fore.RED + "  [!] FLAGGED in " + str(pulse_count) + " threat reports!")

    show_sub("INVESTIGATION LINKS")
    print(Fore.CYAN + "  -> AlienVault  : https://otx.alienvault.com/indicator/ip/" + target)
    print(Fore.CYAN + "  -> Shodan      : https://shodan.io/host/" + target)
    print(Fore.CYAN + "  -> VirusTotal  : https://virustotal.com/gui/ip-address/" + target)
    print(Fore.CYAN + "  -> AbuseIPDB   : https://abuseipdb.com/check/" + target)
    print(Fore.CYAN + "  -> ThreatCrowd : https://threatcrowd.org/ip.php?ip=" + target)
    print(Fore.CYAN + "  -> GreyNoise   : https://viz.greynoise.io/ip/" + target)
    print(Fore.CYAN + "  -> IBM XForce  : https://exchange.xforce.ibmcloud.com/ip/" + target)
    print(Fore.CYAN + "  -> ThreatFox   : https://threatfox.abuse.ch/browse.php?search=" + target)

    show_log("Threat intel complete", "SUCCESS")

def show_stats():
    show_section("SESSION STATISTICS")
    runtime = datetime.datetime.now() - START_TIME
    total_secs = int(runtime.total_seconds())
    h = total_secs // 3600
    m = (total_secs % 3600) // 60
    s = total_secs % 60
    show_info("Runtime",         str(h) + "h " + str(m) + "m " + str(s) + "s", Fore.CYAN)
    show_info("Total Scans",     str(STATS["total_scans"]),     Fore.YELLOW)
    show_info("Profiles Found",  str(STATS["profiles_found"]),  Fore.GREEN)
    show_info("IPs Scanned",     str(STATS["ips_scanned"]),     Fore.GREEN)
    show_info("Open Ports",      str(STATS["open_ports"]),      Fore.RED)
    show_info("Emails Analyzed", str(STATS["emails_analyzed"]), Fore.GREEN)
    show_info("Phones Analyzed", str(STATS["phones_analyzed"]), Fore.GREEN)
    show_info("Domains Scanned", str(STATS["domains_scanned"]), Fore.GREEN)
    show_info("API Calls",       str(STATS["api_calls"]),       Fore.MAGENTA)
    show_info("Reports Saved",   str(STATS["reports_saved"]),   Fore.CYAN)

def show_history():
    show_section("SCAN HISTORY")
    if not SCAN_HISTORY:
        print(Fore.LIGHTBLACK_EX + "  No scans yet")
        return
    for h in SCAN_HISTORY:
        print(Fore.WHITE + "  [" + h["time"] + "] " + h["module"].ljust(10) + " | " + h["target"].ljust(20) + " | " + h["result"])

def show_menu():
    print(Fore.CYAN + "\n  ================================================================")
    print(Fore.CYAN + "              MAIN MENU - OSINT FRAMEWORK")
    print(Fore.CYAN + "              Made by PRATAM")
    print(Fore.CYAN + "  ================================================================")
    print(Fore.WHITE + "   [1]  Username Search       - 100+ platforms + APIs")
    print(Fore.WHITE + "   [2]  IP Intelligence       - 3 APIs + Port Scan")
    print(Fore.WHITE + "   [3]  Email OSINT           - EmailRep + Disify")
    print(Fore.WHITE + "   [4]  Phone Intelligence    - 50+ countries")
    print(Fore.WHITE + "   [5]  Domain Intelligence   - HackerTarget + crt.sh")
    print(Fore.WHITE + "   [6]  Person Search         - People Finders + Dorks")
    print(Fore.WHITE + "   [7]  Google Dork Generator - Advanced Dorks")
    print(Fore.WHITE + "   [8]  Local Network Info    - System + Network")
    print(Fore.WHITE + "   [9]  Breach Hunter         - Leak Databases")
    print(Fore.WHITE + "   [10] Threat Intelligence   - AlienVault OTX")
    print(Fore.YELLOW + "   [11] FULL OSINT SCAN       - All Modules")
    print(Fore.WHITE + "   [12] Statistics")
    print(Fore.WHITE + "   [13] Scan History")
    print(Fore.WHITE + "   [14] Reports Folder Path")
    print(Fore.RED   + "   [15] Exit")
    print(Fore.CYAN + "  ================================================================")
    print(Fore.LIGHTBLACK_EX + "  v" + VERSION + " | Made by PRATAM")
    print()
    return input(Fore.YELLOW + "  Choice: " + Fore.WHITE).strip()

def main():
    show_banner()
    print(Fore.RED    + "  ================================================================")
    print(Fore.RED    + "  LEGAL DISCLAIMER")
    print(Fore.YELLOW + "  This tool is for EDUCATIONAL and LEGAL use ONLY.")
    print(Fore.YELLOW + "  PRATAM is NOT responsible for any misuse.")
    print(Fore.RED    + "  ================================================================")
    print()
    agree = input(Fore.YELLOW + "  Type I AGREE to continue: " + Fore.WHITE).strip()
    if agree != "I AGREE":
        print(Fore.RED + "  Exiting...")
        sys.exit(0)
    show_banner()
    show_log("OSINT Framework v" + VERSION + " ready", "SUCCESS")
    show_log("Made by " + AUTHOR, "SUCCESS")

    while True:
        choice = show_menu()
        STATS["total_scans"] += 1

        if choice == "1":
            u = input(Fore.YELLOW + "  Username: " + Fore.WHITE).strip()
            if u: search_username(u)
        elif choice == "2":
            ip = input(Fore.YELLOW + "  IP Address: " + Fore.WHITE).strip()
            if ip: get_ip_info(ip)
        elif choice == "3":
            e = input(Fore.YELLOW + "  Email: " + Fore.WHITE).strip()
            if e: get_email_info(e)
        elif choice == "4":
            p = input(Fore.YELLOW + "  Phone (eg +1234567890): " + Fore.WHITE).strip()
            if p: get_phone_info(p)
        elif choice == "5":
            d = input(Fore.YELLOW + "  Domain (eg google.com): " + Fore.WHITE).strip()
            if d: get_domain_info(d)
        elif choice == "6":
            fn  = input(Fore.YELLOW + "  First Name: " + Fore.WHITE).strip()
            ln  = input(Fore.YELLOW + "  Last Name: " + Fore.WHITE).strip()
            loc = input(Fore.YELLOW + "  Location (optional): " + Fore.WHITE).strip()
            age = input(Fore.YELLOW + "  Age (optional): " + Fore.WHITE).strip()
            if fn and ln: search_person(fn, ln, loc, age)
        elif choice == "7":
            t = input(Fore.YELLOW + "  Target: " + Fore.WHITE).strip()
            if t: get_dorks(t)
        elif choice == "8":
            get_network_info()
        elif choice == "9":
            t = input(Fore.YELLOW + "  Target: " + Fore.WHITE).strip()
            if t: search_breaches(t)
        elif choice == "10":
            t = input(Fore.YELLOW + "  Target IP/Domain: " + Fore.WHITE).strip()
            if t: get_threat_intel(t)
        elif choice == "11":
            show_section("FULL OSINT SCAN")
            u  = input(Fore.CYAN + "  Username   : " + Fore.WHITE).strip()
            ip = input(Fore.CYAN + "  IP Address : " + Fore.WHITE).strip()
            e  = input(Fore.CYAN + "  Email      : " + Fore.WHITE).strip()
            p  = input(Fore.CYAN + "  Phone      : " + Fore.WHITE).strip()
            d  = input(Fore.CYAN + "  Domain     : " + Fore.WHITE).strip()
            fn = input(Fore.CYAN + "  First Name : " + Fore.WHITE).strip()
            ln = input(Fore.CYAN + "  Last Name  : " + Fore.WHITE).strip()
            if u:         search_username(u)
            if ip:        get_ip_info(ip)
            if e:         get_email_info(e)
            if p:         get_phone_info(p)
            if d:         get_domain_info(d)
            if fn and ln: search_person(fn, ln)
            show_log("Full scan complete!", "SUCCESS")
        elif choice == "12":
            show_stats()
        elif choice == "13":
            show_history()
        elif choice == "14":
            print(Fore.CYAN + "  Reports: " + os.path.abspath("reports"))
        elif choice == "15":
            print(Fore.GREEN + "\n  Thanks for using OSINT Tool by PRATAM!")
            print(Fore.YELLOW + "  Stay Legal. Stay Ethical.\n")
            sys.exit(0)
        else:
            show_log("Invalid choice", "WARN")

        print()
        input(Fore.LIGHTBLACK_EX + "  Press ENTER to continue...")
        show_banner()

if __name__ == "__main__":
    main()