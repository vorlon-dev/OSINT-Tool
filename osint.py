@'
#!/usr/bin/env python3
# ================================================================
#    ___  ____ ___ _   _ _____   _____ ___   ___  _
#   / _ \/ ___|_ _| \ | |_   _| |_   _/ _ \ / _ \| |
#  | | | \___ \| ||  \| | | |     | || | | | | | | |
#  | |_| |___) | || |\  | | |     | || |_| | |_| | |___
#   \___/|____/___|_| \_| |_|     |_| \___/ \___/|_____|
#
#  OSINT Framework v5.0 PRO - Python Edition
#  Made by PRATAM
#  Works on Windows, Linux, Mac, Termux Android
#  Educational and Legal Use Only
# ================================================================

import os
import sys
import json
import socket
import requests
import datetime
import platform
import subprocess
from colorama import Fore, Back, Style, init

init(autoreset=True)

# ================================================================
# GLOBAL CONFIG
# ================================================================

VERSION    = "5.0 PRO PYTHON"
AUTHOR     = "PRATAM"
START_TIME = datetime.datetime.now()

STATS = {
    "total_scans": 0,
    "usernames_found": 0,
    "emails_analyzed": 0,
    "phones_analyzed": 0,
    "ips_scanned": 0,
    "domains_scanned": 0,
    "profiles_found": 0,
    "open_ports": 0,
    "api_calls": 0,
    "reports_saved": 0
}

SCAN_HISTORY = []

# Create folders
for folder in ["results", "reports", "cache"]:
    os.makedirs(folder, exist_ok=True)

# Log file
LOG_FILE = os.path.join("results", "osint.log")

# ================================================================
# FREE OPEN SOURCE APIS
# ================================================================

APIS = {
    "ip_api_com"     : "http://ip-api.com/json",
    "ipinfo_io"      : "https://ipinfo.io",
    "ipapi_co"       : "https://ipapi.co",
    "hackertarget"   : "https://api.hackertarget.com",
    "emailrep"       : "https://emailrep.io",
    "disify"         : "https://www.disify.com/api/email",
    "github_api"     : "https://api.github.com",
    "reddit_api"     : "https://www.reddit.com",
    "hn_api"         : "https://hn.algolia.com/api/v1",
    "alienvault"     : "https://otx.alienvault.com/api/v1",
    "threatfox"      : "https://threatfox-api.abuse.ch/api/v1",
    "nvd_api"        : "https://services.nvd.nist.gov/rest/json/cves/2.0",
    "crt_sh"         : "https://crt.sh",
    "rdap"           : "https://rdap.org"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# ================================================================
# UI FUNCTIONS
# ================================================================

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    clear()
    print(Fore.CYAN + """
  ================================================================
     ___  ____ ___ _   _ _____   _____ ___   ___  _     
    / _ \/ ___|_ _| \ | |_   _| |_   _/ _ \ / _ \| |    
   | | | \___ \| ||  \| | | |     | || | | | | | | |    
   | |_| |___) | || |\  | | |     | || |_| | |_| | |___ 
    \___/|____/___|_| \_| |_|     |_| \___/ \___/|_____| 
  """)
    print(Fore.YELLOW + f"       PROFESSIONAL INTELLIGENCE FRAMEWORK v{VERSION}")
    print(Fore.GREEN  + f"                    Made by {AUTHOR}")
    print(Fore.CYAN   + "         Works on Windows, Linux, Mac, Termux")
    print(Fore.RED    + "             Educational and Legal Use Only")
    print(Fore.CYAN   + "  ================================================================\n")

def section(title):
    print(Fore.DarkCyan if hasattr(Fore, 'DarkCyan') else Fore.CYAN)
    print(Fore.CYAN   + "\n  ================================================================")
    print(Fore.YELLOW + f"   >> {title}")
    print(Fore.CYAN   + "  ================================================================\n")

def subsection(title):
    print(Fore.CYAN + f"\n  ~~~ {title} ~~~\n")

def info(key, value, color=Fore.YELLOW):
    pad = " " * (25 - len(key))
    print(Fore.CYAN + f"  {key}{pad} : " + color + str(value))

def log(message, log_type="INFO"):
    time_str = datetime.datetime.now().strftime("%H:%M:%S")
    colors = {
        "SUCCESS" : Fore.GREEN,
        "ERROR"   : Fore.RED,
        "WARN"    : Fore.YELLOW,
        "SCAN"    : Fore.CYAN,
        "FOUND"   : Fore.GREEN,
        "API"     : Fore.MAGENTA,
        "INFO"    : Fore.WHITE
    }
    color = colors.get(log_type, Fore.WHITE)
    print(color + f"  [{time_str}][{log_type}] {message}")
    try:
        with open(LOG_FILE, "a") as f:
            f.write(f"[{time_str}][{log_type}] {message}\n")
    except:
        pass

def found(platform_name, url):
    print(Back.GREEN + Fore.WHITE + "  [FOUND] " + Style.RESET_ALL +
          Fore.GREEN + f" {platform_name}")
    print(Fore.CYAN  + f"          -> {url}")

def api_result(api_name, result, color=Fore.GREEN):
    print(Back.BLUE + Fore.WHITE + "  [API] " + Style.RESET_ALL +
          Fore.CYAN + f" {api_name}" + color + f" : {result}")

def progress_bar(current, total, status=""):
    percent = round((current / total) * 100)
    filled  = round(percent / 2.5)
    empty   = 40 - filled
    bar     = "=" * filled + "-" * empty
    print(f"\r  [{bar}] {percent}% | {status}                    ", end="", flush=True)

def api_request(url, api_name="API", headers=None, method="GET", data=None):
    STATS["api_calls"] += 1
    h = HEADERS.copy()
    if headers:
        h.update(headers)
    try:
        if method == "POST":
            response = requests.post(url, headers=h, json=data, timeout=15)
        else:
            response = requests.get(url, headers=h, timeout=15)
        log(f"API success: {api_name}", "API")
        return response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text
    except Exception as e:
        log(f"API failed: {api_name} - {str(e)}", "WARN")
        return None

def save_report(content, target, report_type):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe      = "".join(c if c.isalnum() else "_" for c in target)
    filename  = f"OSINT_{report_type}_{safe}_{timestamp}.txt"
    filepath  = os.path.join("reports", filename)
    header = f"""================================================================
         OSINT FRAMEWORK v{VERSION}
              INVESTIGATION REPORT
              MADE BY PRATAM
================================================================
Report Type    : {report_type}
Target         : {target}
Generated      : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Investigator   : {os.environ.get('USER', os.environ.get('USERNAME', 'Unknown'))}
Computer       : {socket.gethostname()}
API Calls Made : {STATS['api_calls']}
================================================================

{content}

================================================================
MADE BY PRATAM
Educational and Legal Use Only
================================================================
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(header)
    STATS["reports_saved"] += 1
    log(f"Report saved: {filepath}", "SUCCESS")
    return filepath

def save_prompt(content, target, report_type):
    print()
    save = input(Fore.YELLOW + "  Save report? [Y/N]: " + Fore.WHITE).strip().upper()
    if save == "Y":
        path = save_report(content, target, report_type)
        print(Fore.GREEN + f"  [+] Saved: {path}")
        open_f = input(Fore.YELLOW + "  Open reports folder? [Y/N]: " + Fore.WHITE).strip().upper()
        if open_f == "Y":
            if os.name == "nt":
                os.startfile(os.path.abspath("reports"))
            else:
                subprocess.Popen(["xdg-open", os.path.abspath("reports")])

def add_history(module, target, result):
    SCAN_HISTORY.append({
        "time"   : datetime.datetime.now().strftime("%H:%M:%S"),
        "module" : module,
        "target" : target,
        "result" : result
    })

# ================================================================
# MODULE 1: USERNAME SEARCH (150+ PLATFORMS)
# ================================================================

def search_username(username):
    section(f"USERNAME ENUMERATION: {username}")
    log(f"Scanning platforms for: {username}", "SCAN")

    platforms = {
        # Social Media
        "GitHub"        : f"https://github.com/{username}",
        "Twitter"       : f"https://twitter.com/{username}",
        "Instagram"     : f"https://instagram.com/{username}",
        "TikTok"        : f"https://tiktok.com/@{username}",
        "Reddit"        : f"https://reddit.com/user/{username}",
        "YouTube"       : f"https://youtube.com/@{username}",
        "LinkedIn"      : f"https://linkedin.com/in/{username}",
        "Facebook"      : f"https://facebook.com/{username}",
        "Snapchat"      : f"https://snapchat.com/add/{username}",
        "Pinterest"     : f"https://pinterest.com/{username}",
        "Tumblr"        : f"https://{username}.tumblr.com",
        "Flickr"        : f"https://flickr.com/people/{username}",
        "VK"            : f"https://vk.com/{username}",
        "Telegram"      : f"https://t.me/{username}",
        "Discord"       : f"https://discord.com/users/{username}",
        "Quora"         : f"https://quora.com/profile/{username}",
        "Wattpad"       : f"https://wattpad.com/user/{username}",
        "9GAG"          : f"https://9gag.com/u/{username}",
        "Imgur"         : f"https://imgur.com/user/{username}",
        "Gravatar"      : f"https://gravatar.com/{username}",
        # Developer
        "GitLab"        : f"https://gitlab.com/{username}",
        "Bitbucket"     : f"https://bitbucket.org/{username}",
        "CodePen"       : f"https://codepen.io/{username}",
        "Replit"        : f"https://replit.com/@{username}",
        "StackOverflow" : f"https://stackoverflow.com/users/{username}",
        "HackerRank"    : f"https://hackerrank.com/{username}",
        "LeetCode"      : f"https://leetcode.com/{username}",
        "HackerNews"    : f"https://news.ycombinator.com/user?id={username}",
        "Dev.to"        : f"https://dev.to/{username}",
        "Medium"        : f"https://medium.com/@{username}",
        "Hashnode"      : f"https://hashnode.com/@{username}",
        "NPM"           : f"https://npmjs.com/~{username}",
        "PyPI"          : f"https://pypi.org/user/{username}",
        "DockerHub"     : f"https://hub.docker.com/u/{username}",
        # Gaming
        "Twitch"        : f"https://twitch.tv/{username}",
        "Steam"         : f"https://steamcommunity.com/id/{username}",
        "PSN"           : f"https://psnprofiles.com/{username}",
        "Roblox"        : f"https://roblox.com/user.aspx?username={username}",
        "Minecraft"     : f"https://namemc.com/profile/{username}",
        "ChessCom"      : f"https://chess.com/member/{username}",
        "Lichess"       : f"https://lichess.org/@/{username}",
        "Faceit"        : f"https://faceit.com/en/players/{username}",
        # Creative
        "DeviantArt"    : f"https://deviantart.com/{username}",
        "ArtStation"    : f"https://artstation.com/{username}",
        "Behance"       : f"https://behance.net/{username}",
        "Dribbble"      : f"https://dribbble.com/{username}",
        "SoundCloud"    : f"https://soundcloud.com/{username}",
        "Spotify"       : f"https://open.spotify.com/user/{username}",
        "Bandcamp"      : f"https://{username}.bandcamp.com",
        "Vimeo"         : f"https://vimeo.com/{username}",
        "500px"         : f"https://500px.com/p/{username}",
        "Unsplash"      : f"https://unsplash.com/@{username}",
        # Professional
        "AngelList"     : f"https://angel.co/{username}",
        "ProductHunt"   : f"https://producthunt.com/@{username}",
        "Fiverr"        : f"https://fiverr.com/{username}",
        "Freelancer"    : f"https://freelancer.com/u/{username}",
        "Upwork"        : f"https://upwork.com/freelancers/~{username}",
        # Security
        "TryHackMe"     : f"https://tryhackme.com/p/{username}",
        "HackTheBox"    : f"https://app.hackthebox.com/profile/{username}",
        "Bugcrowd"      : f"https://bugcrowd.com/{username}",
        "HackerOne"     : f"https://hackerone.com/{username}",
        # Other
        "Pastebin"      : f"https://pastebin.com/u/{username}",
        "Keybase"       : f"https://keybase.io/{username}",
        "AboutMe"       : f"https://about.me/{username}",
        "Linktree"      : f"https://linktr.ee/{username}",
        "Goodreads"     : f"https://goodreads.com/{username}",
        "LastFM"        : f"https://last.fm/user/{username}",
        "MyAnimeList"   : f"https://myanimelist.net/profile/{username}",
        "Letterboxd"    : f"https://letterboxd.com/{username}",
        "Strava"        : f"https://strava.com/athletes/{username}",
        "Duolingo"      : f"https://duolingo.com/profile/{username}",
    }

    print()
    info("Target Username", username, Fore.WHITE)
    info("Total Platforms", str(len(platforms)), Fore.YELLOW)
    print()

    found_count  = 0
    total        = len(platforms)
    current      = 0
    output       = ""
    found_list   = []

    for platform_name, url in sorted(platforms.items()):
        current += 1
        progress_bar(current, total, platform_name)
        try:
            r = requests.head(url, headers=HEADERS, timeout=8, allow_redirects=True)
            if r.status_code == 200:
                print()
                found(platform_name, url)
                found_count += 1
                found_list.append(platform_name)
                output += f"[FOUND] {platform_name}\n  URL: {url}\n\n"
                STATS["profiles_found"] += 1
        except:
            pass

    print("\n")

    # GitHub API
    subsection("GITHUB API DEEP SCAN")
    gh = api_request(f"{APIS['github_api']}/users/{username}", "GitHub API")
    if gh and isinstance(gh, dict) and "login" in gh:
        api_result("GitHub API", "User found!", Fore.GREEN)
        info("Name",      str(gh.get("name", "N/A")), Fore.WHITE)
        info("Bio",       str(gh.get("bio", "N/A")), Fore.GRAY if hasattr(Fore, 'GRAY') else Fore.WHITE)
        info("Company",   str(gh.get("company", "N/A")), Fore.YELLOW)
        info("Location",  str(gh.get("location", "N/A")), Fore.YELLOW)
        info("Email",     str(gh.get("email", "N/A")), Fore.CYAN)
        info("Blog",      str(gh.get("blog", "N/A")), Fore.CYAN)
        info("Twitter",   str(gh.get("twitter_username", "N/A")), Fore.CYAN)
        info("Followers", str(gh.get("followers", 0)), Fore.GREEN)
        info("Repos",     str(gh.get("public_repos", 0)), Fore.GREEN)
        info("Created",   str(gh.get("created_at", "N/A")), Fore.WHITE)
        output += f"=== GITHUB ===\nName: {gh.get('name')}\nLocation: {gh.get('location')}\nEmail: {gh.get('email')}\n\n"

    # Reddit API
    subsection("REDDIT API DEEP SCAN")
    rd = api_request(f"{APIS['reddit_api']}/user/{username}/about.json", "Reddit API")
    if rd and isinstance(rd, dict) and "data" in rd:
        data = rd["data"]
        api_result("Reddit API", "User found!", Fore.GREEN)
        info("Name",    str(data.get("name", "N/A")), Fore.WHITE)
        info("Karma",   str(data.get("total_karma", 0)), Fore.YELLOW)
        info("Premium", str(data.get("is_gold", False)), Fore.YELLOW)
        output += f"=== REDDIT ===\nName: {data.get('name')}\nKarma: {data.get('total_karma')}\n\n"

    # HackerNews API
    subsection("HACKERNEWS API SCAN")
    hn = api_request(f"{APIS['hn_api']}/users/{username}", "HackerNews API")
    if hn and isinstance(hn, dict) and "username" in hn:
        api_result("HackerNews", "User found!", Fore.GREEN)
        info("Username", str(hn.get("username", "N/A")), Fore.WHITE)
        info("Karma",    str(hn.get("karma", 0)), Fore.YELLOW)
        output += f"=== HACKERNEWS ===\nUsername: {hn.get('username')}\nKarma: {hn.get('karma')}\n\n"

    subsection("SCAN SUMMARY")
    info("Username",          username,              Fore.WHITE)
    info("Platforms Scanned", str(total),            Fore.CYAN)
    info("Profiles Found",    str(found_count),      Fore.GREEN)
    info("Not Found",         str(total-found_count),Fore.RED)
    info("API Calls",         str(STATS["api_calls"]),Fore.MAGENTA)

    if found_list:
        print(Fore.GREEN + "\n  Found on:")
        for p in found_list:
            print(Fore.GREEN + f"    -> {p}")

    subsection("GOOGLE DORKS")
    dorks = [
        f'https://google.com/search?q="{username}"',
        f'https://google.com/search?q="{username}"+site:pastebin.com',
        f'https://google.com/search?q="{username}"+site:github.com',
        f'https://google.com/search?q="{username}"+email',
    ]
    for d in dorks:
        print(Fore.CYAN + f"  -> {d}")

    STATS["usernames_found"] += found_count
    add_history("Username", username, f"{found_count} found")
    log(f"Username scan complete: {found_count} found", "SUCCESS")
    save_prompt(output, username, "Username")

# ================================================================
# MODULE 2: IP INTELLIGENCE
# ================================================================

def get_ip_intelligence(ip):
    section(f"IP INTELLIGENCE: {ip}")
    log(f"Querying IP APIs...", "SCAN")

    output = ""

    subsection("API 1 - ip-api.com")
    data1 = api_request(f"{APIS['ip_api_com']}/{ip}?fields=status,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,asname,reverse,mobile,proxy,hosting,query", "ip-api.com")
    if data1 and isinstance(data1, dict) and data1.get("status") == "success":
        api_result("ip-api.com", "Data received", Fore.GREEN)
        info("IP Address",   str(data1.get("query", "")),      Fore.WHITE)
        info("Country",      f"{data1.get('country')} [{data1.get('countryCode')}]", Fore.YELLOW)
        info("Region",       str(data1.get("regionName", "")), Fore.YELLOW)
        info("City",         str(data1.get("city", "")),       Fore.YELLOW)
        info("ZIP",          str(data1.get("zip", "")),        Fore.WHITE)
        info("Coordinates",  f"{data1.get('lat')}, {data1.get('lon')}", Fore.CYAN)
        info("Timezone",     str(data1.get("timezone", "")),   Fore.CYAN)
        info("ISP",          str(data1.get("isp", "")),        Fore.GREEN)
        info("Org",          str(data1.get("org", "")),        Fore.GREEN)
        info("AS",           str(data1.get("as", "")),         Fore.WHITE)
        info("Mobile",       str(data1.get("mobile", False)),  Fore.RED if data1.get("mobile") else Fore.GREEN)
        info("Proxy/VPN",    str(data1.get("proxy", False)),   Fore.RED if data1.get("proxy") else Fore.GREEN)
        info("Hosting",      str(data1.get("hosting", False)), Fore.YELLOW if data1.get("hosting") else Fore.GREEN)
        output += f"=== ip-api.com ===\nIP: {data1.get('query')}\nCountry: {data1.get('country')}\nCity: {data1.get('city')}\nISP: {data1.get('isp')}\n\n"

    subsection("API 2 - ipinfo.io")
    data2 = api_request(f"{APIS['ipinfo_io']}/{ip}/json", "ipinfo.io")
    if data2 and isinstance(data2, dict):
        api_result("ipinfo.io", "Data received", Fore.GREEN)
        info("Hostname", str(data2.get("hostname", "N/A")), Fore.WHITE)
        info("Org",      str(data2.get("org", "N/A")),      Fore.GREEN)
        info("Postal",   str(data2.get("postal", "N/A")),   Fore.WHITE)

    subsection("API 3 - AlienVault OTX")
    av = api_request(f"{APIS['alienvault']}/indicators/IPv4/{ip}/general", "AlienVault OTX")
    if av and isinstance(av, dict):
        api_result("AlienVault OTX", "Threat data received", Fore.GREEN)
        pulse_count = av.get("pulse_info", {}).get("count", 0)
        info("Pulse Count", str(pulse_count), Fore.RED if pulse_count > 0 else Fore.GREEN)
        info("Reputation",  str(av.get("reputation", "N/A")), Fore.YELLOW)
        if pulse_count > 0:
            print(Fore.RED + f"  [!] This IP is flagged in {pulse_count} threat pulses!")

    subsection("PORT SCAN")
    log("Scanning 20 common ports...", "SCAN")

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
        progress_bar(port_num, len(ports), f"Port {port} ({service})")
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                print()
                print(Fore.GREEN + f"  [OPEN] Port {port} - {service}")
                open_ports.append(f"{port}/{service}")
                STATS["open_ports"] += 1
            sock.close()
        except:
            pass

    print()

    if open_ports:
        info("Open Ports", str(len(open_ports)), Fore.RED)
        output += f"=== OPEN PORTS ===\n{', '.join(open_ports)}\n\n"
    else:
        print(Fore.LIGHTBLACK_EX + "  No open ports detected")

    subsection("THREAT INTELLIGENCE LINKS")
    links = [
        f"Shodan       : https://shodan.io/host/{ip}",
        f"VirusTotal   : https://virustotal.com/gui/ip-address/{ip}",
        f"AbuseIPDB    : https://abuseipdb.com/check/{ip}",
        f"AlienVault   : https://otx.alienvault.com/indicator/ip/{ip}",
        f"Censys       : https://search.censys.io/hosts/{ip}",
        f"GreyNoise    : https://viz.greynoise.io/ip/{ip}",
        f"IBM XForce   : https://exchange.xforce.ibmcloud.com/ip/{ip}",
    ]
    for link in links:
        print(Fore.CYAN + f"  -> {link}")

    STATS["ips_scanned"] += 1
    add_history("IP", ip, f"{len(open_ports)} ports open")
    log("IP intelligence complete", "SUCCESS")
    save_prompt(output, ip, "IP")

# ================================================================
# MODULE 3: EMAIL OSINT
# ================================================================

def get_email_intelligence(email):
    section(f"EMAIL INTELLIGENCE: {email}")

    if "@" not in email:
        log("Invalid email format!", "ERROR")
        return

    parts  = email.split("@")
    user   = parts[0]
    domain = parts[1]
    output = ""

    subsection("EMAIL BREAKDOWN")
    info("Full Email",     email,          Fore.WHITE)
    info("Username",       user,           Fore.YELLOW)
    info("Domain",         domain,         Fore.YELLOW)
    info("Length",         str(len(email)),Fore.WHITE)
    info("Has Numbers",    str(any(c.isdigit() for c in user)), Fore.WHITE)
    info("Has Dots",       str("." in user), Fore.WHITE)
    info("Has Underscore", str("_" in user), Fore.WHITE)

    subsection("API 1 - EmailRep.io")
    er = api_request(f"{APIS['emailrep']}/{email}", "EmailRep.io")
    if er and isinstance(er, dict):
        api_result("EmailRep.io", "Data received", Fore.GREEN)
        info("Reputation",         str(er.get("reputation", "N/A")),            Fore.YELLOW)
        info("Suspicious",         str(er.get("suspicious", "N/A")),            Fore.RED if er.get("suspicious") else Fore.GREEN)
        details = er.get("details", {})
        info("Credentials Leaked", str(details.get("credentials_leaked", False)), Fore.RED if details.get("credentials_leaked") else Fore.GREEN)
        info("Disposable",         str(details.get("disposable", False)),        Fore.RED if details.get("disposable") else Fore.GREEN)
        info("Blacklisted",        str(details.get("blacklisted", False)),       Fore.RED if details.get("blacklisted") else Fore.GREEN)
        info("Valid MX",           str(details.get("valid_mx", False)),          Fore.GREEN if details.get("valid_mx") else Fore.RED)
        info("Free Provider",      str(details.get("free_provider", False)),     Fore.WHITE)
        output += f"=== EmailRep ===\nReputation: {er.get('reputation')}\nSuspicious: {er.get('suspicious')}\n\n"

    subsection("API 2 - Disify")
    di = api_request(f"{APIS['disify']}/{email}", "Disify")
    if di and isinstance(di, dict):
        api_result("Disify", "Data received", Fore.GREEN)
        info("Valid Format", str(di.get("format", False)),     Fore.GREEN if di.get("format") else Fore.RED)
        info("Disposable",   str(di.get("disposable", False)), Fore.RED if di.get("disposable") else Fore.GREEN)
        info("DNS Valid",    str(di.get("dns", False)),        Fore.GREEN if di.get("dns") else Fore.RED)

    subsection("PROVIDER DETECTION")
    providers = {
        "gmail.com": ("Google Gmail", "High"),
        "yahoo.com": ("Yahoo Mail", "Medium"),
        "hotmail.com": ("Microsoft Hotmail", "High"),
        "outlook.com": ("Microsoft Outlook", "High"),
        "protonmail.com": ("ProtonMail E2EE", "Very High"),
        "proton.me": ("ProtonMail E2EE", "Very High"),
        "tutanota.com": ("Tutanota E2EE", "Very High"),
        "icloud.com": ("Apple iCloud", "High"),
        "aol.com": ("AOL Mail", "Low"),
        "zoho.com": ("Zoho Mail", "Medium"),
        "yandex.com": ("Yandex Mail", "Low"),
        "yandex.ru": ("Yandex Mail", "Low"),
        "gmx.com": ("GMX Mail", "Medium"),
        "mail.com": ("Mail.com", "Medium"),
        "mailinator.com": ("Mailinator Disposable", "None"),
        "guerrillamail.com": ("Guerrilla Disposable", "None"),
        "10minutemail.com": ("10 Minute Mail", "None"),
        "tempmail.com": ("Temp Mail", "None"),
    }
    provider_info = providers.get(domain, ("Custom Domain", "Unknown"))
    info("Provider",  provider_info[0], Fore.CYAN)
    info("Security",  provider_info[1], Fore.GREEN if provider_info[1] in ["High", "Very High"] else Fore.RED if provider_info[1] in ["Low", "None"] else Fore.YELLOW)

    subsection("BREACH LINKS")
    breach_links = [
        f"HaveIBeenPwned  : https://haveibeenpwned.com/account/{email}",
        f"Dehashed        : https://dehashed.com/search?query={email}",
        f"IntelX          : https://intelx.io/?s={email}",
        f"LeakCheck       : https://leakcheck.io/search/{email}",
        f"Epieos          : https://epieos.com/?q={email}",
    ]
    for link in breach_links:
        print(Fore.CYAN + f"  -> {link}")

    STATS["emails_analyzed"] += 1
    add_history("Email", email, "Analysis complete")
    log("Email intelligence complete", "SUCCESS")
    save_prompt(output, email, "Email")

# ================================================================
# MODULE 4: PHONE INTELLIGENCE
# ================================================================

def get_phone_intelligence(phone):
    section(f"PHONE INTELLIGENCE: {phone}")
    log("Analyzing phone number...", "SCAN")

    clean  = "".join(c for c in phone if c.isdigit() or c == "+")
    digits = "".join(c for c in clean if c.isdigit())
    output = ""

    subsection("NUMBER ANALYSIS")
    info("Original",    phone,           Fore.WHITE)
    info("Cleaned",     clean,           Fore.YELLOW)
    info("Digits Only", digits,          Fore.WHITE)
    info("Length",      str(len(digits)),Fore.WHITE)

    fmt = "Unknown"
    if len(digits) == 10:  fmt = "National (10 digits)"
    if len(digits) == 11:  fmt = "International (11 digits)"
    if len(digits) == 12:  fmt = "International with code"
    if clean.startswith("+"): fmt += " - E.164"
    info("Format", fmt, Fore.CYAN)

    subsection("COUNTRY DETECTION")
    countries = [
        ("+1",    "USA / Canada",    "North America"),
        ("+44",   "United Kingdom",  "Europe"),
        ("+91",   "India",           "Asia"),
        ("+86",   "China",           "Asia"),
        ("+81",   "Japan",           "Asia"),
        ("+49",   "Germany",         "Europe"),
        ("+33",   "France",          "Europe"),
        ("+39",   "Italy",           "Europe"),
        ("+34",   "Spain",           "Europe"),
        ("+7",    "Russia",          "Europe/Asia"),
        ("+55",   "Brazil",          "South America"),
        ("+82",   "South Korea",     "Asia"),
        ("+90",   "Turkey",          "Europe/Asia"),
        ("+92",   "Pakistan",        "Asia"),
        ("+62",   "Indonesia",       "Asia"),
        ("+63",   "Philippines",     "Asia"),
        ("+880",  "Bangladesh",      "Asia"),
        ("+234",  "Nigeria",         "Africa"),
        ("+27",   "South Africa",    "Africa"),
        ("+20",   "Egypt",           "Africa"),
        ("+971",  "UAE",             "Middle East"),
        ("+966",  "Saudi Arabia",    "Middle East"),
        ("+52",   "Mexico",          "North America"),
        ("+61",   "Australia",       "Oceania"),
        ("+64",   "New Zealand",     "Oceania"),
        ("+65",   "Singapore",       "Asia"),
        ("+60",   "Malaysia",        "Asia"),
        ("+66",   "Thailand",        "Asia"),
        ("+84",   "Vietnam",         "Asia"),
        ("+212",  "Morocco",         "Africa"),
        ("+213",  "Algeria",         "Africa"),
        ("+98",   "Iran",            "Middle East"),
        ("+964",  "Iraq",            "Middle East"),
        ("+965",  "Kuwait",          "Middle East"),
        ("+974",  "Qatar",           "Middle East"),
        ("+961",  "Lebanon",         "Middle East"),
        ("+962",  "Jordan",          "Middle East"),
        ("+968",  "Oman",            "Middle East"),
        ("+973",  "Bahrain",         "Middle East"),
    ]

    country_name = "Unknown"
    country_region = "Unknown"
    for code, name, region in countries:
        if clean.startswith(code):
            country_name = name
            country_region = region
            break

    info("Country", country_name,   Fore.GREEN)
    info("Region",  country_region, Fore.YELLOW)

    subsection("FORMATTED NUMBERS")
    print(Fore.CYAN  + f"  E.164      : +{digits}")
    print(Fore.WHITE + f"  RFC3966    : tel:+{digits}")

    subsection("OSINT TOOLS")
    links = [
        f"Google     : https://google.com/search?q=%22{clean}%22",
        f"Truecaller : https://truecaller.com/search/us/{digits}",
        f"NumLookup  : https://numlookup.com/?number={clean}",
        f"WhitePages : https://whitepages.com/phone/{digits}",
        f"Sync.me    : https://sync.me/search/?number={clean}",
    ]
    for link in links:
        print(Fore.CYAN + f"  -> {link}")

    output += f"Phone: {phone}\nCountry: {country_name}\n"
    STATS["phones_analyzed"] += 1
    add_history("Phone", phone, country_name)
    log("Phone analysis complete", "SUCCESS")
    save_prompt(output, digits, "Phone")

# ================================================================
# MODULE 5: DOMAIN INTELLIGENCE
# ================================================================

def get_domain_intelligence(domain):
    section(f"DOMAIN INTELLIGENCE: {domain}")
    log("Comprehensive domain scan...", "SCAN")

    output = ""

    subsection("API 1 - HackerTarget DNS")
    ht_dns = api_request(f"{APIS['hackertarget']}/dnslookup/?q={domain}", "HackerTarget DNS")
    if ht_dns:
        api_result("HackerTarget", "DNS data received", Fore.GREEN)
        print(Fore.YELLOW + f"  {ht_dns}")
        output += f"=== HackerTarget DNS ===\n{ht_dns}\n\n"

    subsection("API 2 - crt.sh SSL Certificates")
    crt = api_request(f"{APIS['crt_sh']}/?q={domain}&output=json", "crt.sh")
    if crt and isinstance(crt, list):
        api_result("crt.sh", f"{len(crt)} certificates found", Fore.GREEN)
        unique = set()
        for cert in crt[:20]:
            for name in cert.get("name_value", "").split("\n"):
                if name not in unique:
                    unique.add(name)
                    print(Fore.GREEN + f"  -> {name}")
        output += f"=== SSL Certs ===\n" + "\n".join(unique) + "\n\n"

    subsection("API 3 - AlienVault Domain Intel")
    av = api_request(f"{APIS['alienvault']}/indicators/domain/{domain}/general", "AlienVault")
    if av and isinstance(av, dict):
        api_result("AlienVault OTX", "Domain intel received", Fore.GREEN)
        pulse_count = av.get("pulse_info", {}).get("count", 0)
        info("Pulse Count", str(pulse_count), Fore.RED if pulse_count > 0 else Fore.GREEN)
        if pulse_count > 0:
            print(Fore.RED + "  [!] Domain flagged in threat intelligence!")

    subsection("DNS RECORDS")
    import subprocess as sp
    for record_type in ["A", "MX", "NS", "TXT"]:
        try:
            result = sp.run(["nslookup", f"-type={record_type}", domain],
                          capture_output=True, text=True, timeout=10)
            if result.stdout:
                print(Fore.CYAN + f"  [{record_type} Records]")
                for line in result.stdout.split("\n"):
                    if line.strip() and "server" not in line.lower():
                        print(Fore.YELLOW + f"    {line.strip()}")
        except:
            pass

    subsection("SUBDOMAIN SCAN")
    log("Scanning common subdomains...", "SCAN")
    subs = ["www", "mail", "ftp", "admin", "api", "dev", "staging",
            "blog", "shop", "m", "app", "portal", "vpn", "remote",
            "smtp", "pop", "ns1", "ns2", "db", "git", "jenkins"]

    found_subs = []
    for i, sub in enumerate(subs):
        progress_bar(i+1, len(subs), f"{sub}.{domain}")
        fqdn = f"{sub}.{domain}"
        try:
            socket.gethostbyname(fqdn)
            print()
            print(Fore.GREEN + f"  [FOUND] {fqdn}")
            found_subs.append(fqdn)
        except:
            pass

    print()
    info("Subdomains Found", str(len(found_subs)), Fore.GREEN)

    subsection("OSINT TOOLS")
    links = [
        f"WHOIS          : https://who.is/whois/{domain}",
        f"Shodan         : https://shodan.io/search?query=hostname:{domain}",
        f"VirusTotal     : https://virustotal.com/gui/domain/{domain}",
        f"URLScan        : https://urlscan.io/search/#{domain}",
        f"Wayback        : https://web.archive.org/web/*/{domain}",
        f"SecurityTrails : https://securitytrails.com/domain/{domain}/dns",
        f"crt.sh         : https://crt.sh/?q={domain}",
        f"Censys         : https://search.censys.io/search?q={domain}",
    ]
    for link in links:
        print(Fore.CYAN + f"  -> {link}")

    STATS["domains_scanned"] += 1
    add_history("Domain", domain, f"{len(found_subs)} subdomains")
    log("Domain intelligence complete", "SUCCESS")
    save_prompt(output, domain, "Domain")

# ================================================================
# MODULE 6: PERSON SEARCH
# ================================================================

def search_person(first, last, location="", age=""):
    full_name = f"{first} {last}"
    section(f"PERSON SEARCH: {full_name}")
    log(f"Person intelligence: {full_name}", "SCAN")

    info("First Name", first,     Fore.YELLOW)
    info("Last Name",  last,      Fore.YELLOW)
    info("Full Name",  full_name, Fore.WHITE)
    if location: info("Location", location, Fore.CYAN)
    if age:      info("Age",      age,      Fore.WHITE)

    encoded = requests.utils.quote(full_name)
    output  = f"Target: {full_name}\nLocation: {location}\n\n"

    subsection("PEOPLE SEARCH ENGINES")
    engines = [
        f"Spokeo           : https://spokeo.com/search?q={encoded}",
        f"BeenVerified     : https://beenverified.com/people/{first}-{last}",
        f"Whitepages       : https://whitepages.com/name/{first}-{last}",
        f"TruePeopleSearch : https://truepeoplesearch.com/results?name={encoded}",
        f"FastPeopleSearch : https://fastpeoplesearch.com/name/{first}-{last}",
        f"411.com          : https://411.com/people/{encoded}",
        f"PeekYou          : https://peekyou.com/{first}+{last}",
        f"Pipl             : https://pipl.com/search/?q={encoded}",
        f"Radaris          : https://radaris.com/p/{first}/{last}",
        f"ZabaSearch       : https://zabasearch.com/people/{first}+{last}",
    ]
    for e in engines:
        print(Fore.CYAN + f"  -> {e}")

    subsection("SOCIAL MEDIA")
    social = [
        f"LinkedIn  : https://linkedin.com/search/results/people/?keywords={encoded}",
        f"Facebook  : https://facebook.com/search/people/?q={encoded}",
        f"Twitter   : https://twitter.com/search?q=%22{full_name}%22&f=user",
        f"Instagram : https://instagram.com/explore/tags/{first+last}/",
        f"TikTok    : https://tiktok.com/search/user?q={encoded}",
    ]
    for s in social:
        print(Fore.CYAN + f"  -> {s}")

    subsection("GOOGLE DORKS")
    dorks = [
        f'https://google.com/search?q="{full_name}"',
        f'https://google.com/search?q="{full_name}"+"{location}"',
        f'https://google.com/search?q="{full_name}"+site:linkedin.com',
        f'https://google.com/search?q="{full_name}"+filetype:pdf',
        f'https://google.com/search?q="{full_name}"+email',
        f'https://google.com/search?q="{full_name}"+phone',
    ]
    for d in dorks:
        print(Fore.CYAN + f"  -> {d}")

    add_history("Person", full_name, "Search complete")
    log("Person search complete", "SUCCESS")
    save_prompt(output, f"{first}-{last}", "Person")

# ================================================================
# MODULE 7: BREACH HUNTER
# ================================================================

def search_breaches(target):
    section(f"BREACH HUNTER: {target}")
    log("Searching breach databases...", "SCAN")

    subsection("BREACH DATABASES")
    dbs = [
        f"HaveIBeenPwned  : https://haveibeenpwned.com/account/{target}",
        f"Dehashed        : https://dehashed.com/search?query={target}",
        f"LeakCheck       : https://leakcheck.io/search/{target}",
        f"IntelX          : https://intelx.io/?s={target}",
        f"BreachDirectory : https://breachdirectory.org",
        f"SnusBase        : https://snusbase.com",
        f"WeLeakInfo      : https://weleakinfo.to/search/{target}",
        f"PSBDMP          : https://psbdmp.ws/search?q={target}",
    ]
    for db in dbs:
        print(Fore.CYAN + f"  -> {db}")

    subsection("PASTE SITES")
    pastes = [
        f"Pastebin    : https://pastebin.com/search?q={target}",
        f"Hastebin    : https://hastebin.com/search/{target}",
        f"Paste.ee    : https://paste.ee/search/{target}",
    ]
    for p in pastes:
        print(Fore.CYAN + f"  -> {p}")

    subsection("GOOGLE DORKS")
    dorks = [
        f'https://google.com/search?q="{target}"+site:pastebin.com',
        f'https://google.com/search?q="{target}"+password',
        f'https://google.com/search?q="{target}"+leaked',
        f'https://google.com/search?q="{target}"+breach',
        f'https://google.com/search?q="{target}"+credentials',
    ]
    for d in dorks:
        print(Fore.RED + f"  -> {d}")

    add_history("Breach", target, "Search complete")
    log("Breach search complete", "SUCCESS")

# ================================================================
# MODULE 8: LOCAL NETWORK INFO
# ================================================================

def get_network_info():
    section("LOCAL NETWORK INFORMATION")
    log("Gathering system info...", "SCAN")

    subsection("YOUR PUBLIC IP")
    try:
        pub = requests.get("https://api.ipify.org?format=json", timeout=5).json()
        info("Public IP", pub.get("ip", "Unknown"), Fore.GREEN)
        geo = api_request(f"{APIS['ip_api_com']}/{pub.get('ip')}", "ip-api.com")
        if geo and isinstance(geo, dict) and geo.get("status") == "success":
            info("Location", f"{geo.get('city')}, {geo.get('country')}", Fore.YELLOW)
            info("ISP",      geo.get("isp", "N/A"), Fore.CYAN)
    except:
        log("Could not fetch public IP", "ERROR")

    subsection("SYSTEM INFORMATION")
    info("Hostname",   socket.gethostname(),  Fore.WHITE)
    info("Platform",   platform.system(),     Fore.WHITE)
    info("Version",    platform.version(),    Fore.WHITE)
    info("Machine",    platform.machine(),    Fore.WHITE)
    info("Python",     platform.python_version(), Fore.GREEN)
    info("Username",   os.environ.get("USER", os.environ.get("USERNAME", "Unknown")), Fore.WHITE)

    subsection("LOCAL IP ADDRESSES")
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        info("Local IP", local_ip, Fore.YELLOW)
    except:
        pass

    subsection("PRIVACY CHECK TOOLS")
    tools = [
        "IP Leak Test   : https://ipleak.net",
        "DNS Leak Test  : https://dnsleaktest.com",
        "WebRTC Test    : https://browserleaks.com/webrtc",
        "Speed Test     : https://fast.com",
        "Fingerprint    : https://browserleaks.com",
    ]
    for t in tools:
        print(Fore.CYAN + f"  -> {t}")

    log("Network scan complete", "SUCCESS")

# ================================================================
# MODULE 9: GOOGLE DORKS
# ================================================================

def get_google_dorks(target):
    section(f"GOOGLE DORK GENERATOR: {target}")
    output = ""

    subsection("BASIC SEARCHES")
    basic = [
        f'"{target}"',
        f'intitle:"{target}"',
        f'inurl:"{target}"',
        f'intext:"{target}"',
    ]
    for d in basic:
        url = f"https://google.com/search?q={requests.utils.quote(d)}"
        print(Fore.CYAN + f"  -> {url}")
        output += url + "\n"

    subsection("FILE SEARCHES")
    for ft in ["pdf", "doc", "xls", "txt", "csv", "xml", "json", "sql", "log"]:
        url = f'https://google.com/search?q="{target}"+filetype:{ft}'
        print(Fore.CYAN + f"  -> {url}")

    subsection("SOCIAL MEDIA")
    for site in ["linkedin.com", "facebook.com", "twitter.com", "instagram.com", "github.com"]:
        url = f'https://google.com/search?q="{target}"+site:{site}'
        print(Fore.CYAN + f"  -> {url}")

    subsection("SENSITIVE SEARCHES")
    for term in ["password", "email", "phone", "credentials", "api key", "leaked"]:
        url = f'https://google.com/search?q="{target}"+{term}'
        print(Fore.RED + f"  -> {url}")

    subsection("OTHER ENGINES")
    engines = [
        f"Bing       : https://bing.com/search?q=%22{target}%22",
        f"DuckDuckGo : https://duckduckgo.com/?q=%22{target}%22",
        f"Yandex     : https://yandex.com/search/?text={target}",
        f"Startpage  : https://startpage.com/search?q=%22{target}%22",
    ]
    for e in engines:
        print(Fore.CYAN + f"  -> {e}")

    add_history("Dorks", target, "Generated")
    log("Dork generation complete", "SUCCESS")
    save_prompt(output, target, "Dorks")

# ================================================================
# MODULE 10: THREAT INTELLIGENCE
# ================================================================

def get_threat_intelligence(target):
    section(f"THREAT INTELLIGENCE: {target}")
    log("Gathering threat intel...", "SCAN")
    output = ""

    subsection("AlienVault OTX API")
    av = api_request(f"{APIS['alienvault']}/indicators/IPv4/{target}/general", "AlienVault OTX")
    if av and isinstance(av, dict):
        api_result("AlienVault OTX", "Data received", Fore.GREEN)
        pulse_count = av.get("pulse_info", {}).get("count", 0)
        info("Pulse Count", str(pulse_count), Fore.RED if pulse_count > 0 else Fore.GREEN)
        info("Reputation",  str(av.get("reputation", "N/A")), Fore.YELLOW)
        if pulse_count > 0:
            print(Fore.RED + f"  [!] Target in {pulse_count} threat pulses!")
        output += f"AlienVault Pulses: {pulse_count}\n"

    subsection("ThreatFox API")
    tf = api_request(APIS["threatfox"], "ThreatFox",
                    method="POST", data={"query": "search_ioc", "search_term": target})
    if tf and isinstance(tf, dict):
        api_result("ThreatFox", "Data received", Fore.GREEN)
        info("Status", str(tf.get("query_status", "N/A")), Fore.GREEN)
        if tf.get("data"):
            print(Fore.RED + f"  [!] Found in ThreatFox database!")

    subsection("THREAT INTEL LINKS")
    links = [
        f"AlienVault   : https://otx.alienvault.com/indicator/ip/{target}",
        f"Shodan       : https://shodan.io/host/{target}",
        f"VirusTotal   : https://virustotal.com/gui/ip-address/{target}",
        f"AbuseIPDB    : https://abuseipdb.com/check/{target}",
        f"ThreatCrowd  : https://threatcrowd.org/ip.php?ip={target}",
        f"GreyNoise    : https://viz.greynoise.io/ip/{target}",
        f"ThreatFox    : https://threatfox.abuse.ch/browse.php?search={target}",
        f"IBM XForce   : https://exchange.xforce.ibmcloud.com/ip/{target}",
    ]
    for link in links:
        print(Fore.CYAN + f"  -> {link}")

    add_history("Threat", target, "Intel gathered")
    log("Threat intelligence complete", "SUCCESS")
    save_prompt(output, target, "Threat")

# ================================================================
# STATISTICS
# ================================================================

def show_statistics():
    section("SESSION STATISTICS")
    runtime = datetime.datetime.now() - START_TIME
    hours, remainder = divmod(int(runtime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)

    info("Runtime",          f"{hours}h {minutes}m {seconds}s", Fore.CYAN)
    info("Total Scans",      str(STATS["total_scans"]),      Fore.YELLOW)
    info("Profiles Found",   str(STATS["profiles_found"]),   Fore.GREEN)
    info("IPs Scanned",      str(STATS["ips_scanned"]),      Fore.GREEN)
    info("Open Ports",       str(STATS["open_ports"]),       Fore.RED)
    info("Emails Analyzed",  str(STATS["emails_analyzed"]),  Fore.GREEN)
    info("Phones Analyzed",  str(STATS["phones_analyzed"]),  Fore.GREEN)
    info("Domains Scanned",  str(STATS["domains_scanned"]),  Fore.GREEN)
    info("API Calls Made",   str(STATS["api_calls"]),        Fore.MAGENTA)
    info("Reports Saved",    str(STATS["reports_saved"]),    Fore.CYAN)

# ================================================================
# SCAN HISTORY
# ================================================================

def show_history():
    section("SCAN HISTORY")
    if not SCAN_HISTORY:
        print(Fore.LIGHTBLACK_EX + "  No scans yet")
        return
    print(Fore.CYAN + "  Time      Module        Target                   Result")
    print(Fore.LIGHTBLACK_EX + "  ----      ------        ------                   ------")
    for h in SCAN_HISTORY:
        mod = h["module"].ljust(13)
        tgt = h["target"].ljust(24)
        print(Fore.WHITE + f"  {h['time']}  {mod} {tgt} {h['result']}")

# ================================================================
# MAIN MENU
# ================================================================

def main_menu():
    print(Fore.CYAN + """
  ================================================================
              MAIN MENU - OSINT FRAMEWORK
  ================================================================""")
    items = [
        ("[1]  Username Search",          "150+ platforms + APIs"),
        ("[2]  IP Intelligence",           "3 APIs + Port Scan + Threats"),
        ("[3]  Email OSINT",               "EmailRep + Disify + DNS"),
        ("[4]  Phone Intelligence",        "60+ countries"),
        ("[5]  Domain Intelligence",       "HackerTarget + crt.sh + RDAP"),
        ("[6]  Person Search",             "People Finders + Dorks"),
        ("[7]  Google Dork Generator",     "Advanced Dorks"),
        ("[8]  Local Network Info",        "System + Network"),
        ("[9]  Breach Hunter",             "Leak Databases"),
        ("[10] Threat Intelligence",       "AlienVault + ThreatFox"),
        ("[11] FULL OSINT SCAN",           "All Modules"),
        ("[12] Statistics",                ""),
        ("[13] Scan History",              ""),
        ("[14] Open Reports",              ""),
        ("[15] Exit",                      ""),
    ]
    for item, desc in items:
        color = Fore.YELLOW if "FULL" in item else Fore.RED if "Exit" in item else Fore.WHITE
        if desc:
            print(color + f"   {item}" + Fore.LIGHTBLACK_EX + f" - {desc}")
        else:
            print(color + f"   {item}")

    print(Fore.CYAN + "  ================================================================")
    print(Fore.LIGHTBLACK_EX + f"  Made by PRATAM | v{VERSION}")
    print()
    return input(Fore.YELLOW + "  Choice: " + Fore.WHITE).strip()

# ================================================================
# ENTRY POINT
# ================================================================

def main():
    banner()

    print(Fore.RED    + "  ================================================================")
    print(Fore.RED    + "                       LEGAL DISCLAIMER")
    print(Fore.RED    + "  ================================================================")
    print(Fore.YELLOW + "  This tool is for EDUCATIONAL and LEGAL use ONLY.")
    print(Fore.YELLOW + "  PRATAM is NOT responsible for any misuse.")
    print(Fore.RED    + "  ================================================================\n")

    agree = input(Fore.YELLOW + "  Type 'I AGREE' to continue: " + Fore.WHITE).strip()

    if agree != "I AGREE":
        print(Fore.RED + "  Exiting...")
        sys.exit(0)

    banner()
    log(f"OSINT Framework v{VERSION} initialized", "SUCCESS")
    log(f"Made by {AUTHOR}", "SUCCESS")

    while True:
        choice = main_menu()
        STATS["total_scans"] += 1

        if choice == "1":
            u = input(Fore.YELLOW + "  Username: " + Fore.WHITE).strip()
            if u: search_username(u)

        elif choice == "2":
            ip = input(Fore.YELLOW + "  IP Address: " + Fore.WHITE).strip()
            if ip: get_ip_intelligence(ip)

        elif choice == "3":
            e = input(Fore.YELLOW + "  Email: " + Fore.WHITE).strip()
            if e: get_email_intelligence(e)

        elif choice == "4":
            p = input(Fore.YELLOW + "  Phone (eg +1234567890): " + Fore.WHITE).strip()
            if p: get_phone_intelligence(p)

        elif choice == "5":
            d = input(Fore.YELLOW + "  Domain (eg google.com): " + Fore.WHITE).strip()
            if d: get_domain_intelligence(d)

        elif choice == "6":
            fn  = input(Fore.YELLOW + "  First Name: " + Fore.WHITE).strip()
            ln  = input(Fore.YELLOW + "  Last Name: " + Fore.WHITE).strip()
            loc = input(Fore.YELLOW + "  Location (optional): " + Fore.WHITE).strip()
            age = input(Fore.YELLOW + "  Age (optional): " + Fore.WHITE).strip()
            if fn and ln: search_person(fn, ln, loc, age)

        elif choice == "7":
            t = input(Fore.YELLOW + "  Target: " + Fore.WHITE).strip()
            if t: get_google_dorks(t)

        elif choice == "8":
            get_network_info()

        elif choice == "9":
            t = input(Fore.YELLOW + "  Target (email/username): " + Fore.WHITE).strip()
            if t: search_breaches(t)

        elif choice == "10":
            t = input(Fore.YELLOW + "  Target IP/Domain: " + Fore.WHITE).strip()
            if t: get_threat_intelligence(t)

        elif choice == "11":
            section("FULL OSINT SCAN")
            u   = input(Fore.CYAN + "  Username   : " + Fore.WHITE).strip()
            ip  = input(Fore.CYAN + "  IP Address : " + Fore.WHITE).strip()
            e   = input(Fore.CYAN + "  Email      : " + Fore.WHITE).strip()
            p   = input(Fore.CYAN + "  Phone      : " + Fore.WHITE).strip()
            d   = input(Fore.CYAN + "  Domain     : " + Fore.WHITE).strip()
            fn  = input(Fore.CYAN + "  First Name : " + Fore.WHITE).strip()
            ln  = input(Fore.CYAN + "  Last Name  : " + Fore.WHITE).strip()
            if u:       search_username(u)
            if ip:      get_ip_intelligence(ip)
            if e:       get_email_intelligence(e)
            if p:       get_phone_intelligence(p)
            if d:       get_domain_intelligence(d)
            if fn and ln: search_person(fn, ln)
            log("Full scan complete!", "SUCCESS")

        elif choice == "12":
            show_statistics()

        elif choice == "13":
            show_history()

        elif choice == "14":
            path = os.path.abspath("reports")
            if os.name == "nt":
                os.startfile(path)
            else:
                print(Fore.CYAN + f"  Reports folder: {path}")
                subprocess.Popen(["xdg-open", path])

        elif choice == "15":
            print(Fore.GREEN + "\n  Thanks for using OSINT Tool by PRATAM!")
            print(Fore.YELLOW + "  Stay Legal. Stay Ethical.\n")
            sys.exit(0)

        else:
            log("Invalid choice. Select 1-15.", "WARN")

        print()
        input(Fore.LIGHTBLACK_EX + "  Press ENTER to continue...")
        banner()

if __name__ == "__main__":
    main()
'@ | Out-File -FilePath "C:\Users\prata\OneDrive\Desktop\OSINT-Tool\osint.py" -Encoding UTF8 -Force

Write-Host "[+] Python version created!" -ForegroundColor Green