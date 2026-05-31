# OSINT Tool - Professional Intelligence Framework
### Made by PRATAM | v5.0 PRO | Windows | Linux | Mac | Termux Android

---

## TABLE OF CONTENTS

1. What is this tool
2. Legal Warning
3. Free APIs Used
4. Requirements
5. Installation on Windows
6. Installation on Termux Android
7. Installation on Linux and Mac
8. Installation by Downloading ZIP
9. How to Use Every Module
10. Common Errors and Fixes
11. Tips for Best Results
12. FAQ
13. Quick Reference Card

---

## 1. WHAT IS THIS TOOL

OSINT Tool is a free open source intelligence gathering framework.
OSINT means Open Source Intelligence.
It means collecting publicly available information from the internet.

This tool helps you gather information about:
- Usernames across 100 plus social media platforms
- IP addresses and their physical location
- Email addresses and their breach status
- Phone numbers and their country
- Domains and websites
- People by their real name
- Data breaches and password leaks
- Cyber threats and malware

This tool has TWO versions:
- osint.ps1 is the PowerShell version for Windows
- osint.py is the Python version for Termux Android Linux and Mac

---

## 2. LEGAL WARNING

THIS TOOL IS FOR EDUCATIONAL AND LEGAL USE ONLY

YOU CAN ONLY investigate:
- Your own accounts and systems
- Accounts you have written permission to investigate

YOU CANNOT investigate:
- Other people without their permission
- Companies without authorization
- Any system you do not own

The author PRATAM is NOT responsible for any misuse.
Always use this tool ethically and legally.

---

## 3. FREE APIS USED

14 completely free APIs. No payment. No registration. No API keys needed.

| API Name | What it does |
|----------|-------------|
| ip-api.com | Gets location data from IP address |
| ipinfo.io | Gets additional IP information |
| ipapi.co | Gets country details from IP |
| AlienVault OTX | Checks if IP or domain is a known threat |
| HackerTarget | DNS lookup and network scanning |
| crt.sh | Finds SSL certificates and subdomains |
| RDAP | Gets WHOIS domain registration data |
| EmailRep.io | Checks email reputation and breach status |
| Disify | Checks if email is disposable or fake |
| GitHub API | Gets detailed GitHub user profile |
| Reddit API | Gets user karma and post history |
| HackerNews API | Gets user karma and activity |
| ThreatFox | Checks malware threat databases |
| NVD CVE API | Searches vulnerability databases |

---

## 4. REQUIREMENTS

### Windows
- Windows 10 or Windows 11
- PowerShell 5.1 or higher already installed on Windows
- Internet connection
- Nothing else needed

### Termux Android
- Android phone with Termux from F-Droid
- Python 3
- requests library
- colorama library
- Internet connection

### Linux or Mac
- Python 3
- pip package manager
- requests and colorama libraries
- Internet connection

---

## 5. INSTALLATION ON WINDOWS

### Step 1 - Install Git
Go to https://git-scm.com/download/win
Download and install with all default settings.

### Step 2 - Open PowerShell
Press Windows key and R at same time.
Type powershell and press Enter.

### Step 3 - Allow Scripts to Run
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned


Type Y and press Enter. Only needed once.

### Step 4 - Clone the Tool
git clone https://github.com/vorlon-dev/OSINT-Tool.git



### Step 5 - Go Into the Folder
cd OSINT-Tool



### Step 6 - Check Files Exist


You should see osint.ps1 and osint.py in the list.

### Step 7 - Run the Tool
.\osint.ps1



### Step 8 - Agree to Terms
Type exactly:
I AGREE

text

Press Enter.

### Step 9 - Use the Tool
Type a number from 1 to 17 and press Enter.

---

## 6. INSTALLATION ON TERMUX ANDROID

### Step 1 - Install Termux from F-Droid
Do NOT use Google Play version. It is outdated.
Go to https://f-droid.org on your phone.
Download F-Droid app.
Search for Termux and install it.
Open Termux.

### Step 2 - Update Termux
pkg update -y
pkg upgrade -y


Wait for completion. May take 5 minutes.

### Step 3 - Install Python
pkg install python -y


### Step 4 - Install Git
pkg install git -y



### Step 5 - Install Python Libraries
pip install requests colorama


Wait for Successfully installed message.

### Step 6 - Clone the Tool
git clone https://github.com/vorlon-dev/OSINT-Tool.git


### Step 7 - Go Into the Folder
cd OSINT-Tool



### Step 8 - Check Files Exist
is

You should see osint.py in the list.

### Step 9 - Run the Tool
python osint.py




### Step 10 - Agree to Terms
Type exactly:
I AGREE

Press Enter.

### Step 11 - Use the Tool
Type a number from 1 to 15 and press Enter.

### To See The Collected Data 
cd /data/data/com.termux

### 2 
ls 

###3
cd files/home 

###4
ls 

###5
cd results

###6
ls 

###7
cat osint.log or file name which is  visible in that folder 

---

## 7. INSTALLATION ON LINUX AND MAC

### Ubuntu or Debian Linux
sudo apt update
sudo apt install python3 python3-pip git -y
pip3 install requests colorama
git clone https://github.com/vorlon-dev/OSINT-Tool.git
cd OSINT-Tool
python3 osint.py



### Mac
brew install python git
pip3 install requests colorama
git clone https://github.com/vorlon-dev/OSINT-Tool.git
cd OSINT-Tool
python3 osint.py


---

## 8. INSTALLATION BY DOWNLOADING ZIP

### Step 1
Go to https://github.com/vorlon-dev/OSINT-Tool

### Step 2
Click the green CODE button.
Click Download ZIP.
Wait for download.

### Step 3
Extract the ZIP to your Desktop.

### Step 4 Windows
Open PowerShell and run:
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
cd C:\Users\YourUsername\Desktop\OSINT-Tool
.\osint.ps1



### Step 4 Termux or Linux
Navigate to the extracted folder and run:
python osint.py



---

## 9. HOW TO USE EVERY MODULE

### MAIN MENU
================================================================
MAIN MENU - OSINT FRAMEWORK
[1] Username Search - 100+ platforms plus APIs
[2] IP Intelligence - Geo plus Ports plus Threats
[3] Email OSINT - Deep analysis
[4] Phone Intelligence - Country plus Carrier
[5] Domain Intelligence - DNS plus Subdomains
[6] Person Search - People Finder
[7] Google Dork Generator - Auto Dorks
[8] Local Network Info - System Scan
[9] Breach Hunter - Leak Search
[10] Threat Intelligence - AlienVault plus ThreatFox
[11] FULL OSINT SCAN - All Modules
[12] Statistics
[13] Scan History
[14] Open Reports Folder
[15] Exit
Made by PRATAM



---

### MODULE 1 - USERNAME SEARCH

What it does:
Searches username across 100 plus platforms.
Uses GitHub API Reddit API HackerNews API for deep data.

How to use:
Step 1 - Type 1 and press Enter
Step 2 - Type the username when asked
Step 3 - Press Enter
Step 4 - Wait 2 to 5 minutes for scan
Step 5 - Read results
Step 6 - Choose Y to save report or N to skip



Example:
Choice: 1
Username: john_doe


Results you will see:
- Green FOUND with URL for each active profile
- Progress bar showing scan progress
- GitHub name bio location email followers repos
- Reddit karma and posts
- HackerNews karma
- Google search links
- OSINT tool links

Platforms checked include:
GitHub Twitter Instagram TikTok Reddit YouTube LinkedIn Facebook Snapchat Pinterest Tumblr Flickr VK Telegram Quora Wattpad GitLab Bitbucket CodePen Replit StackOverflow HackerRank LeetCode Dev.to Medium Hashnode NPM PyPI DockerHub Twitch Steam PSN Roblox Minecraft ChessCom Lichess Faceit DeviantArt ArtStation Behance Dribbble SoundCloud Spotify Bandcamp Vimeo 500px Unsplash AngelList ProductHunt Fiverr Freelancer Upwork TryHackMe HackTheBox Bugcrowd HackerOne Pastebin Keybase AboutMe Linktree Goodreads LastFM MyAnimeList Letterboxd Strava Duolingo and many more.

---

### MODULE 2 - IP INTELLIGENCE

What it does:
Gets location ISP and threat data from any IP.
Scans 20 common ports.
Uses 3 free APIs for maximum information.

How to use:
Step 1 - Type 2 and press Enter
Step 2 - Type the IP address when asked
Step 3 - Press Enter
Step 4 - Wait 1 to 2 minutes
Step 5 - Read results
Step 6 - Choose to save or not


Example:
Choice: 2
IP Address: 8.8.8.8



Results you will see:
- Country region city ZIP coordinates timezone
- ISP organization AS number
- Whether mobile proxy or hosting datacenter
- Open ports with service names
- AlienVault threat pulse count
- Warning if IP is flagged malicious
- Investigation links to Shodan VirusTotal AbuseIPDB Censys GreyNoise

Ports scanned:
21 FTP, 22 SSH, 23 Telnet, 25 SMTP, 53 DNS, 80 HTTP, 110 POP3, 143 IMAP, 443 HTTPS, 445 SMB, 1433 MSSQL, 3306 MySQL, 3389 RDP, 5432 PostgreSQL, 5900 VNC, 6379 Redis, 8080 HTTP-Alt, 8443 HTTPS-Alt, 27017 MongoDB, 9200 Elasticsearch

---

### MODULE 3 - EMAIL OSINT

What it does:
Checks email breach status using EmailRep.io API.
Checks if disposable using Disify API.
Detects provider and security level.
Gets DNS records of email domain.

How to use:
Step 1 - Type 3 and press Enter
Step 2 - Type the email address when asked
Step 3 - Press Enter
Step 4 - Read results
Step 5 - Choose to save or not


Example:
Choice: 3
Email: someone@gmail.com



Results you will see:
- Username and domain breakdown
- EmailRep reputation score
- Whether credentials were leaked in breaches
- Whether email is on spam blacklists
- Whether email is disposable
- Whether MX records are valid
- Provider name and security rating
- MX A SPF DMARC NS DNS records
- Username variations for further searching
- Breach database links

Provider security ratings:
ProtonMail = Very High End to End Encrypted
Tutanota = Very High End to End Encrypted
Google Gmail = High
Microsoft Outlook = High
Apple iCloud = High
Yahoo Mail = Medium
AOL Mail = Low
Yandex Mail = Low
Mailinator = None Disposable
Guerrilla Mail = None Disposable

---

### MODULE 4 - PHONE INTELLIGENCE

What it does:
Detects country from phone number.
Covers 50 plus countries.
Shows formatted versions.
Provides lookup tool links.

How to use:
Step 1 - Type 4 and press Enter
Step 2 - Type phone number WITH country code
Step 3 - Always start with + sign
Step 4 - Press Enter
Step 5 - Read results
Step 6 - Choose to save or not



Example:
Choice: 4
Phone: +12025551234



Country codes:
+1 USA Canada, +44 UK, +91 India, +86 China, +81 Japan, +49 Germany, +33 France, +39 Italy, +34 Spain, +7 Russia, +55 Brazil, +82 South Korea, +90 Turkey, +92 Pakistan, +62 Indonesia, +63 Philippines, +880 Bangladesh, +234 Nigeria, +27 South Africa, +20 Egypt, +971 UAE, +966 Saudi Arabia, +965 Kuwait, +974 Qatar, +973 Bahrain, +968 Oman, +961 Lebanon, +962 Jordan, +964 Iraq, +212 Morocco, +213 Algeria, +98 Iran, +52 Mexico, +61 Australia, +64 New Zealand, +65 Singapore, +60 Malaysia, +66 Thailand, +84 Vietnam, +31 Netherlands, +32 Belgium, +41 Switzerland, +46 Sweden, +47 Norway, +48 Poland, +40 Romania, +30 Greece, +249 Sudan, +251 Ethiopia, +254 Kenya

Results you will see:
- Cleaned number format
- Digit count
- Format type
- Country name and region
- E.164 international format
- Formatted with brackets
- Lookup tool links

---

### MODULE 5 - DOMAIN INTELLIGENCE

What it does:
Complete domain reconnaissance.
Uses HackerTarget crt.sh AlienVault APIs.
Scans for subdomains.
Gets all DNS record types.

How to use:
Step 1 - Type 5 and press Enter
Step 2 - Type domain name without http or www
Step 3 - Press Enter
Step 4 - Wait 1 to 3 minutes for subdomain scan
Step 5 - Read results
Step 6 - Choose to save or not



Example:
Choice: 5
Domain: example.com



Results you will see:
- HackerTarget DNS data
- crt.sh SSL certificates and subdomains
- AlienVault threat pulse count
- A AAAA MX NS TXT CNAME SOA DNS records
- Found subdomains with IP addresses
- HTTP HTTPS status codes
- Investigation links

Subdomains checked:
www mail ftp admin api dev staging blog shop mobile app portal vpn remote smtp pop ns1 ns2 db git jenkins test beta demo cdn static files backup and more.

---

### MODULE 6 - PERSON SEARCH

What it does:
Searches for a real person by name.
Generates people search engine links.
Generates social media search links.
Generates Google dork searches.

How to use:
Step 1 - Type 6 and press Enter
Step 2 - Type first name when asked
Step 3 - Press Enter
Step 4 - Type last name when asked
Step 5 - Press Enter
Step 6 - Type location or press Enter to skip
Step 7 - Type age or press Enter to skip
Step 8 - Read all generated links
Step 9 - Click links in browser to investigate



Example:
Choice: 6
First Name: John
Last Name: Smith
Location: New York
Age: 30



Results you will see:
- People search engine links Spokeo BeenVerified Whitepages TruePeopleSearch FastPeopleSearch 411.com PeekYou Pipl Radaris Intelius
- Social media links LinkedIn Facebook Twitter Instagram TikTok
- Professional links AngelList Crunchbase GitHub ResearchGate
- Google dork searches exact name with location on LinkedIn in PDFs with email with phone
- Image search links Google Bing Yandex
- News search links Google News Bing News

---

### MODULE 7 - GOOGLE DORK GENERATOR

What it does:
Generates advanced Google search queries.
Finds information that normal searches miss.

How to use:
Step 1 - Type 7 and press Enter
Step 2 - Type any target when asked
Step 3 - Press Enter
Step 4 - Get list of search URLs
Step 5 - Copy URL and paste in browser



Example:
Choice: 7
Target: john_doe



Results you will see:
- Basic searches exact phrase title URL text
- File type searches PDF Word Excel text CSV JSON SQL log
- Social media searches LinkedIn Facebook Twitter Instagram GitHub
- Code site searches GitHub GitLab Pastebin Gist
- Sensitive searches password email phone credentials API key leaked
- Other engines Bing DuckDuckGo Yandex Startpage

---

### MODULE 8 - LOCAL NETWORK INFO

What it does:
Shows your public IP and location.
Shows system information.
Provides privacy testing links.

How to use:
Step 1 - Type 8 and press Enter
Step 2 - Results appear automatically
Step 3 - No input needed


Results you will see:
- Your public IP address
- Your location from IP
- Your ISP
- Whether VPN detected
- Computer hostname
- Operating system
- Machine type
- Python version
- Local IP address
- Privacy tool links

---

### MODULE 9 - BREACH HUNTER

What it does:
Provides links to breach databases for checking.
Generates Google breach dork searches.

How to use:
Step 1 - Type 9 and press Enter
Step 2 - Type email or username when asked
Step 3 - Press Enter
Step 4 - Get links to check manually in browser



Example:
Choice: 9
Target: someone@gmail.com



Results you will see:
- HaveIBeenPwned link
- Dehashed link
- LeakCheck link
- IntelX link
- BreachDirectory link
- SnusBase link
- WeLeakInfo link
- PSBDMP link
- Pastebin Hastebin paste site links
- Google dork searches for breach data

---

### MODULE 10 - THREAT INTELLIGENCE

What it does:
Checks if IP or domain is malicious.
Uses AlienVault OTX free API.
Provides 8 plus threat platform links.

How to use:
Step 1 - Type 10 and press Enter
Step 2 - Type IP or domain when asked
Step 3 - Press Enter
Step 4 - Read threat analysis
Step 5 - Choose to save or not



Example:
Choice: 10
Target IP/Domain: 1.2.3.4



Results you will see:
- AlienVault pulse count zero is clean higher is suspicious
- Reputation score
- Red warning if flagged malicious
- Links to AlienVault Shodan VirusTotal AbuseIPDB ThreatCrowd GreyNoise IBM X-Force ThreatFox

---

### MODULE 11 - FULL OSINT SCAN

What it does:
Runs ALL modules together in one scan.
Most powerful option in the tool.

How to use:
Step 1 - Type 11 and press Enter
Step 2 - Type username or press Enter to skip
Step 3 - Type IP address or press Enter to skip
Step 4 - Type email or press Enter to skip
Step 5 - Type phone with country code or press Enter to skip
Step 6 - Type domain or press Enter to skip
Step 7 - Type first name or press Enter to skip
Step 8 - Type last name or press Enter to skip
Step 9 - Wait for all scans to complete
Step 10 - This takes 5 to 20 minutes
Step 11 - Read all results



Tip: Only fill fields you have data for.
Leave blank by pressing Enter to skip.

---

### MODULE 12 - STATISTICS

Type 12 and press Enter.
Shows session summary including runtime total scans profiles found IPs scanned ports discovered emails phones domains API calls and reports saved.

---

### MODULE 13 - SCAN HISTORY

Type 13 and press Enter.
Shows table of all scans with time module target and result.

---

### MODULE 14 - OPEN REPORTS FOLDER

Type 14 and press Enter.
Opens folder with all saved reports.

Reports saved at:
Windows: C:\Users\YourName\Desktop\OSINT-Tool\reports\
Termux: /data/data/com.termux/files/home/OSINT-Tool/reports/
Linux: /home/YourUsername/OSINT-Tool/reports/

File names look like:
OSINT_Username_john_doe_20240101_143025.txt
OSINT_IP_8_8_8_8_20240101_143510.txt

---

### MODULE 15 - EXIT

Type 15 and press Enter to close the tool.

---

## 10. COMMON ERRORS AND FIXES

### Error 1 - Scripts disabled on Windows
Message: cannot be loaded because running scripts is disabled
Fix: Run this command:
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
Type Y and press Enter.

### Error 2 - File not found on Windows
Message: The term osint.ps1 is not recognized
Fix: Run cd OSINT-Tool first then run .\osint.ps1

### Error 3 - No module named requests
Fix: Run pip install requests colorama

### Error 4 - pkg not found in Termux
Fix: Install Termux from F-Droid not Google Play

### Error 5 - python not found on Linux
Fix: Use python3 osint.py instead of python osint.py

### Error 6 - git not found
Fix: Run pkg install git -y on Termux or sudo apt install git on Linux

### Error 7 - Connection error
Fix: Check internet connection and try again

### Error 8 - git push rejected
Fix: Run git push --force

### Error 9 - Scan is slow
This is normal. Wait for it to complete. Do not close terminal.

---

## 11. TIPS FOR BEST RESULTS

Username Search: Use exact username. Try lowercase variations.
IP Address: Use format 192.168.1.1 without http or www.
Email: Include full email with at symbol. Use lowercase.
Phone: Always include country code starting with plus sign. No spaces or dashes.
Domain: Type only domain like example.com without http or www.
Full Scan: Fill as many fields as possible for best results.
Reports: Always save reports for important investigations.
Internet: Use stable WiFi for best API response times.

---

## 12. FAQ

Q: Is this tool free?
A: Yes completely free. No payment. No API keys needed.

Q: Does it need internet?
A: Yes. Internet is required for all API calls.

Q: How long does username scan take?
A: Usually 2 to 5 minutes.

Q: Can I scan multiple targets at once?
A: Use module 11 Full Scan for multiple inputs at once.

Q: Is activity logged online?
A: No. Only saved locally in results folder.

Q: Does it work on Mac?
A: Yes. Install Python 3 and run python3 osint.py.

Q: How to update the tool?
A: Go into folder and run git pull.

Q: Can I add more platforms?
A: Yes. Edit the platforms section in osint.py or osint.ps1.

Q: Why do some APIs fail?
A: Free APIs sometimes have downtime. Tool continues with other APIs.

Q: Is VPN recommended?
A: Yes. VPN is good privacy practice for any internet activity.

---

## 13. QUICK REFERENCE CARD

Windows Commands:
Open PowerShell : Win + R then type powershell
Allow scripts : Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
Clone tool : git clone https://github.com/vorlon-dev/OSINT-Tool.git
Enter folder : cd OSINT-Tool
Run tool : .\osint.ps1
Update tool : git pull


Termux Commands:
Update Termux : pkg update -y && pkg upgrade -y
Install Python Git : pkg install python git -y
Install libraries : pip install requests colorama
Clone tool : git clone https://github.com/vorlon-dev/OSINT-Tool.git
Enter folder : cd OSINT-Tool
Run tool : python osint.py
Update tool : git pull



Linux Commands:
Install all : sudo apt install python3 python3-pip git -y
Install libraries : pip3 install requests colorama
Clone tool : git clone https://github.com/vorlon-dev/OSINT-Tool.git
Enter folder : cd OSINT-Tool
Run tool : python3 osint.py
Update tool : git pull



Module Numbers:
1 = Username Search
2 = IP Intelligence
3 = Email OSINT
4 = Phone Intelligence
5 = Domain Intelligence
6 = Person Search
7 = Google Dork Generator
8 = Local Network Info
9 = Breach Hunter
10 = Threat Intelligence
11 = Full OSINT Scan ALL modules
12 = Statistics
13 = Scan History
14 = Open Reports Folder
15 = Exit



---

## FOLDER STRUCTURE
OSINT-Tool/
├── osint.ps1 - Windows PowerShell version
├── osint.py - Python version for Termux Linux Mac
├── README.md - This complete guide
├── LICENSE - MIT open source license
├── results/ - Auto created contains log file
├── reports/ - Auto created contains saved reports
└── cache/ - Auto created for temporary data



---

## ABOUT

Tool Name  : OSINT Tool
Version    : 5.0 PRO
Author     : PRATAM
Language   : PowerShell and Python
APIs Used  : 14 Free Open Source APIs
Platforms  : Windows Linux Mac Termux Android
License    : MIT Free and Open Source
GitHub     : https://github.com/vorlon-dev/OSINT-Tool

---

Made by PRATAM
Star this repository if this tool helped you
Stay Legal Stay Ethical Stay Safe
