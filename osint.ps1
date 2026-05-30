<#
================================================================================
   ___  ____ ___ _   _ _____   _____ ___   ___  _     
  / _ \/ ___|_ _| \ | |_   _| |_   _/ _ \ / _ \| |    
 | | | \___ \| ||  \| | | |     | || | | | | | | |    
 | |_| |___) | || |\  | | |     | || |_| | |_| | |___ 
  \___/|____/___|_| \_| |_|     |_| \___/ \___/|_____|

  Ultimate OSINT Framework v4.0 PRO - 2000+ Lines
  Made by PRATAM
  Educational and Legal Use Only
================================================================================
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = "SilentlyContinue"
$ProgressPreference = "SilentlyContinue"

# ================================================================================
# GLOBAL CONFIG
# ================================================================================

$Global:Config = @{
    Version    = "4.0 PRO"
    Author     = "PRATAM"
    ScriptRoot = $PSScriptRoot
    ResultsDir = ""
    ReportsDir = ""
    LogFile    = ""
    CacheDir   = ""
}

$Global:Config.ResultsDir = Join-Path $Global:Config.ScriptRoot "results"
$Global:Config.ReportsDir = Join-Path $Global:Config.ScriptRoot "reports"
$Global:Config.CacheDir   = Join-Path $Global:Config.ScriptRoot "cache"
$Global:Config.LogFile    = Join-Path $Global:Config.ResultsDir "osint.log"

foreach ($dir in @($Global:Config.ResultsDir, $Global:Config.ReportsDir, $Global:Config.CacheDir)) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}

$Global:Network = @{
    UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    Timeout   = 10
    Delay     = 150
}

$Global:Stats = @{
    SessionStart   = Get-Date
    TotalScans     = 0
    UsernamesFound = 0
    EmailsAnalyzed = 0
    PhonesAnalyzed = 0
    IPsScanned     = 0
    DomainsScanned = 0
    ProfilesFound  = 0
    OpenPorts      = 0
    ReportsSaved   = 0
}

$Global:ScanHistory = @()

# ================================================================================
# UI FUNCTIONS
# ================================================================================

function Write-Banner {
    Clear-Host
    Write-Host ""
    Write-Host "  ================================================================" -ForegroundColor Cyan
    Write-Host "     ___  ____ ___ _   _ _____   _____ ___   ___  _     " -ForegroundColor Cyan
    Write-Host "    / _ \/ ___|_ _| \ | |_   _| |_   _/ _ \ / _ \| |    " -ForegroundColor Cyan
    Write-Host "   | | | \___ \| ||  \| | | |     | || | | | | | | |    " -ForegroundColor Cyan
    Write-Host "   | |_| |___) | || |\  | | |     | || |_| | |_| | |___ " -ForegroundColor Cyan
    Write-Host "    \___/|____/___|_| \_| |_|     |_| \___/ \___/|_____| " -ForegroundColor Cyan
    Write-Host ""
    Write-Host "          PROFESSIONAL INTELLIGENCE FRAMEWORK v$($Global:Config.Version)" -ForegroundColor Yellow
    Write-Host "                      Made by PRATAM" -ForegroundColor Green
    Write-Host "               Educational and Legal Use Only" -ForegroundColor Red
    Write-Host "  ================================================================" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Section {
    param([string]$Title)
    Write-Host ""
    Write-Host "  ================================================================" -ForegroundColor DarkCyan
    Write-Host "   >> $Title" -ForegroundColor Yellow
    Write-Host "  ================================================================" -ForegroundColor DarkCyan
    Write-Host ""
}

function Write-SubSection {
    param([string]$Title)
    Write-Host ""
    Write-Host "  ~~~ $Title ~~~" -ForegroundColor DarkCyan
    Write-Host ""
}

function Write-Info {
    param([string]$Key, [string]$Value, [string]$Color = "Yellow")
    $pad = " " * (25 - $Key.Length)
    Write-Host "  $Key$pad : " -NoNewline -ForegroundColor Cyan
    Write-Host "$Value" -ForegroundColor $Color
}

function Write-Log {
    param([string]$Message, [string]$Type = "INFO")
    $time = Get-Date -Format "HH:mm:ss"
    $color = switch ($Type) {
        "SUCCESS" { "Green" }
        "ERROR"   { "Red" }
        "WARN"    { "Yellow" }
        "SCAN"    { "Cyan" }
        "FOUND"   { "Green" }
        default   { "White" }
    }
    Write-Host "  [$time][$Type] $Message" -ForegroundColor $color
    try { "[$time][$Type] $Message" | Out-File -FilePath $Global:Config.LogFile -Append -Encoding UTF8 } catch {}
}

function Write-Found {
    param([string]$Platform, [string]$URL)
    Write-Host "  [FOUND] " -NoNewline -BackgroundColor DarkGreen -ForegroundColor White
    Write-Host " $Platform" -ForegroundColor Green
    Write-Host "          -> $URL" -ForegroundColor Cyan
}

function Write-ProgressBar {
    param([int]$Current, [int]$Total, [string]$Status = "")
    $percent = [math]::Round(($Current / $Total) * 100)
    $filled  = [math]::Round($percent / 2.5)
    $empty   = 40 - $filled
    $bar     = "=" * $filled + "-" * $empty
    Write-Host "`r  [$bar] $percent% | $Status                    " -NoNewline -ForegroundColor Cyan
}

function Write-ResultLine {
    param([string]$Label, [string]$Value)
    Write-Host "  [+] $Label" -NoNewline -ForegroundColor DarkGray
    Write-Host " : $Value" -ForegroundColor White
}

function Export-Report {
    param([string]$Content, [string]$Target, [string]$Type)
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $safe = $Target -replace "[^a-zA-Z0-9]", "_"
    $filename = "OSINT_${Type}_${safe}_$timestamp.txt"
    $filepath = Join-Path $Global:Config.ReportsDir $filename
    $header = @"
================================================================
         OSINT FRAMEWORK v$($Global:Config.Version)
              INVESTIGATION REPORT
              MADE BY PRATAM
================================================================
Report Type    : $Type
Target         : $Target
Generated      : $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
Investigator   : $env:USERNAME
Computer       : $env:COMPUTERNAME
Framework      : $($Global:Config.Version)
================================================================

$Content

================================================================
Made by PRATAM | Educational Use Only
================================================================
"@
    $header | Out-File -FilePath $filepath -Encoding UTF8
    $Global:Stats.ReportsSaved++
    Write-Log "Report saved: $filepath" "SUCCESS"
    return $filepath
}

function Show-SavePrompt {
    param([string]$Content, [string]$Target, [string]$Type)
    Write-Host ""
    Write-Host "  Save report? [Y/N]: " -NoNewline -ForegroundColor Yellow
    $save = Read-Host
    if ($save -match "^[Yy]$") {
        $path = Export-Report -Content $Content -Target $Target -Type $Type
        Write-Host "  Open folder? [Y/N]: " -NoNewline -ForegroundColor Yellow
        $open = Read-Host
        if ($open -match "^[Yy]$") { Start-Process explorer.exe $Global:Config.ReportsDir }
    }
}

function Add-ScanHistory {
    param([string]$Module, [string]$Target, [string]$Result)
    $Global:ScanHistory += [PSCustomObject]@{
        Time   = Get-Date -Format "HH:mm:ss"
        Module = $Module
        Target = $Target
        Result = $Result
    }
}

# ================================================================================
# MODULE 1: USERNAME SEARCH (100+ PLATFORMS)
# ================================================================================

function Search-Username {
    param([string]$Username)

    Write-Section "USERNAME ENUMERATION: $Username"
    Write-Log "Starting username scan on 100+ platforms" "SCAN"

    $platforms = @{
        # Social Media
        "GitHub"          = "https://github.com/$Username"
        "Twitter"         = "https://twitter.com/$Username"
        "Instagram"       = "https://instagram.com/$Username"
        "TikTok"          = "https://tiktok.com/@$Username"
        "Reddit"          = "https://reddit.com/user/$Username"
        "YouTube"         = "https://youtube.com/@$Username"
        "LinkedIn"        = "https://linkedin.com/in/$Username"
        "Facebook"        = "https://facebook.com/$Username"
        "Snapchat"        = "https://snapchat.com/add/$Username"
        "Pinterest"       = "https://pinterest.com/$Username"
        "Tumblr"          = "https://$Username.tumblr.com"
        "Flickr"          = "https://flickr.com/people/$Username"
        "VK"              = "https://vk.com/$Username"
        "Telegram"        = "https://t.me/$Username"
        "Discord"         = "https://discord.com/users/$Username"
        "Quora"           = "https://quora.com/profile/$Username"
        "Wattpad"         = "https://wattpad.com/user/$Username"
        "9GAG"            = "https://9gag.com/u/$Username"
        "Imgur"           = "https://imgur.com/user/$Username"
        "Gravatar"        = "https://gravatar.com/$Username"
        "MeWe"            = "https://mewe.com/i/$Username"
        "Gab"             = "https://gab.com/$Username"
        "Parler"          = "https://parler.com/profile/$Username"
        "Minds"           = "https://minds.com/$Username"

        # Developer
        "GitLab"          = "https://gitlab.com/$Username"
        "Bitbucket"       = "https://bitbucket.org/$Username"
        "CodePen"         = "https://codepen.io/$Username"
        "Replit"          = "https://replit.com/@$Username"
        "Glitch"          = "https://glitch.com/@$Username"
        "StackOverflow"   = "https://stackoverflow.com/users/$Username"
        "HackerRank"      = "https://hackerrank.com/$Username"
        "LeetCode"        = "https://leetcode.com/$Username"
        "Codeforces"      = "https://codeforces.com/profile/$Username"
        "HackerNews"      = "https://news.ycombinator.com/user?id=$Username"
        "Dev.to"          = "https://dev.to/$Username"
        "Hashnode"        = "https://hashnode.com/@$Username"
        "Medium"          = "https://medium.com/@$Username"
        "Substack"        = "https://$Username.substack.com"
        "SourceForge"     = "https://sourceforge.net/u/$Username"
        "NPM"             = "https://npmjs.com/~$Username"
        "PyPI"            = "https://pypi.org/user/$Username"
        "DockerHub"       = "https://hub.docker.com/u/$Username"

        # Gaming
        "Twitch"          = "https://twitch.tv/$Username"
        "Steam"           = "https://steamcommunity.com/id/$Username"
        "Xbox"            = "https://xboxgamertag.com/search/$Username"
        "PSN"             = "https://psnprofiles.com/$Username"
        "Roblox"          = "https://roblox.com/user.aspx?username=$Username"
        "Minecraft"       = "https://namemc.com/profile/$Username"
        "ChessCom"        = "https://chess.com/member/$Username"
        "Lichess"         = "https://lichess.org/@/$Username"
        "Faceit"          = "https://faceit.com/en/players/$Username"
        "Kongregate"      = "https://kongregate.com/accounts/$Username"
        "Newgrounds"      = "https://$Username.newgrounds.com"
        "GameFAQs"        = "https://gamefaqs.gamespot.com/community/$Username"

        # Creative
        "DeviantArt"      = "https://deviantart.com/$Username"
        "ArtStation"      = "https://artstation.com/$Username"
        "Behance"         = "https://behance.net/$Username"
        "Dribbble"        = "https://dribbble.com/$Username"
        "SoundCloud"      = "https://soundcloud.com/$Username"
        "Spotify"         = "https://open.spotify.com/user/$Username"
        "Bandcamp"        = "https://$Username.bandcamp.com"
        "Mixcloud"        = "https://mixcloud.com/$Username"
        "Vimeo"           = "https://vimeo.com/$Username"
        "Dailymotion"     = "https://dailymotion.com/$Username"
        "500px"           = "https://500px.com/p/$Username"
        "Unsplash"        = "https://unsplash.com/@$Username"
        "Giphy"           = "https://giphy.com/$Username"
        "Pixiv"           = "https://pixiv.net/users/$Username"

        # Professional
        "AngelList"       = "https://angel.co/$Username"
        "ProductHunt"     = "https://producthunt.com/@$Username"
        "Upwork"          = "https://upwork.com/freelancers/~$Username"
        "Fiverr"          = "https://fiverr.com/$Username"
        "Freelancer"      = "https://freelancer.com/u/$Username"
        "Guru"            = "https://guru.com/freelancers/$Username"
        "Crunchbase"      = "https://crunchbase.com/person/$Username"

        # Content
        "Pastebin"        = "https://pastebin.com/u/$Username"
        "Gist"            = "https://gist.github.com/$Username"
        "Keybase"         = "https://keybase.io/$Username"
        "AboutMe"         = "https://about.me/$Username"
        "Linktree"        = "https://linktr.ee/$Username"
        "Carrd"           = "https://$Username.carrd.co"
        "Scribd"          = "https://scribd.com/$Username"
        "SlideShare"      = "https://slideshare.net/$Username"
        "Archive.org"     = "https://archive.org/details/@$Username"

        # Security
        "TryHackMe"       = "https://tryhackme.com/p/$Username"
        "HackTheBox"      = "https://app.hackthebox.com/profile/$Username"
        "Bugcrowd"        = "https://bugcrowd.com/$Username"
        "HackerOne"       = "https://hackerone.com/$Username"
        "Intigriti"       = "https://intigriti.com/profile/$Username"

        # Other
        "Yelp"            = "https://yelp.com/user_details?userid=$Username"
        "Goodreads"       = "https://goodreads.com/$Username"
        "LastFM"          = "https://last.fm/user/$Username"
        "MyAnimeList"     = "https://myanimelist.net/profile/$Username"
        "Letterboxd"      = "https://letterboxd.com/$Username"
        "Untappd"         = "https://untappd.com/user/$Username"
    }

    Write-Host ""
    Write-Info "Target Username" $Username "White"
    Write-Info "Total Platforms" "$($platforms.Count)" "Yellow"
    Write-Host ""

    $found    = 0
    $total    = $platforms.Count
    $current  = 0
    $output   = ""
    $foundList = @()

    foreach ($platform in $platforms.Keys | Sort-Object) {
        $current++
        $url = $platforms[$platform]
        Write-ProgressBar -Current $current -Total $total -Status $platform

        try {
            $response = Invoke-WebRequest -Uri $url -Method Head `
                -TimeoutSec $Global:Network.Timeout `
                -UserAgent $Global:Network.UserAgent `
                -ErrorAction Stop

            if ($response.StatusCode -eq 200) {
                Write-Host ""
                Write-Found -Platform $platform -URL $url
                $found++
                $foundList += $platform
                $output += "[FOUND] $platform`n"
                $output += "  URL     : $url`n"
                $output += "  Status  : Active`n`n"
                $Global:Stats.ProfilesFound++
            }
        }
        catch {}

        Start-Sleep -Milliseconds $Global:Network.Delay
    }

    Write-Host ""
    Write-Host ""

    Write-SubSection "SCAN RESULTS"
    Write-Info "Username" $Username "White"
    Write-Info "Platforms Scanned" "$total" "Cyan"
    Write-Info "Profiles Found" "$found" "Green"
    Write-Info "Not Found" "$($total - $found)" "Red"
    Write-Info "Hit Rate" "$([math]::Round(($found/$total)*100, 1))%" "Yellow"

    if ($foundList.Count -gt 0) {
        Write-Host ""
        Write-Host "  Found on:" -ForegroundColor Green
        foreach ($p in $foundList) {
            Write-Host "    -> $p" -ForegroundColor Green
        }
    }

    Write-SubSection "SEARCH ENGINE LINKS"
    Write-Host "  Google     : https://google.com/search?q=%22$Username%22" -ForegroundColor Cyan
    Write-Host "  Bing       : https://bing.com/search?q=%22$Username%22" -ForegroundColor Cyan
    Write-Host "  DuckDuckGo : https://duckduckgo.com/?q=%22$Username%22" -ForegroundColor Cyan
    Write-Host "  Yandex     : https://yandex.com/search/?text=$Username" -ForegroundColor Cyan

    Write-SubSection "OSINT LOOKUP TOOLS"
    Write-Host "  Sherlock    : https://github.com/sherlock-project/sherlock" -ForegroundColor Cyan
    Write-Host "  WhatsMyName : https://whatsmyname.app" -ForegroundColor Cyan
    Write-Host "  Namechk     : https://namechk.com/s/$Username" -ForegroundColor Cyan
    Write-Host "  Knowem      : https://knowem.com/checkusernames.php?u=$Username" -ForegroundColor Cyan
    Write-Host "  CheckUsernames: https://checkusernames.com" -ForegroundColor Cyan

    Write-SubSection "GOOGLE DORKS"
    Write-Host "  -> https://google.com/search?q=%22$Username%22+site:pastebin.com" -ForegroundColor Cyan
    Write-Host "  -> https://google.com/search?q=%22$Username%22+site:github.com" -ForegroundColor Cyan
    Write-Host "  -> https://google.com/search?q=%22$Username%22+site:twitter.com" -ForegroundColor Cyan
    Write-Host "  -> https://google.com/search?q=%22$Username%22+filetype:pdf" -ForegroundColor Cyan
    Write-Host "  -> https://google.com/search?q=intitle:%22$Username%22" -ForegroundColor Cyan
    Write-Host "  -> https://google.com/search?q=%22$Username%22+email" -ForegroundColor Cyan
    Write-Host "  -> https://google.com/search?q=%22$Username%22+phone" -ForegroundColor Cyan

    $Global:Stats.UsernamesFound += $found
    Add-ScanHistory -Module "Username" -Target $Username -Result "$found profiles found"
    Write-Log "Username scan complete: $found profiles found" "SUCCESS"
    Show-SavePrompt -Content $output -Target $Username -Type "Username"
}

# ================================================================================
# MODULE 2: IP INTELLIGENCE (GEO + PORTS + THREAT)
# ================================================================================

function Get-IPIntelligence {
    param([string]$IPAddress)

    Write-Section "IP ADDRESS INTELLIGENCE: $IPAddress"
    Write-Log "Gathering IP intelligence..." "SCAN"

    $output = ""

    Write-SubSection "GEOLOCATION"
    try {
        $fields = "status,message,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query"
        $data = Invoke-RestMethod -Uri "http://ip-api.com/json/$IPAddress`?fields=$fields" -TimeoutSec 10

        if ($data.status -eq "success") {
            Write-Info "IP Address"    $data.query "White"
            Write-Info "Hostname"      $data.reverse "Gray"
            Write-Info "Country"       "$($data.country) [$($data.countryCode)]" "Yellow"
            Write-Info "Region"        $data.regionName "Yellow"
            Write-Info "City"          $data.city "Yellow"
            Write-Info "District"      $data.district "Yellow"
            Write-Info "ZIP Code"      $data.zip "Gray"
            Write-Info "Latitude"      $data.lat "Cyan"
            Write-Info "Longitude"     $data.lon "Cyan"
            Write-Info "Timezone"      "$($data.timezone) (UTC$($data.offset))" "Cyan"
            Write-Info "Currency"      $data.currency "Green"
            Write-Info "ISP"           $data.isp "Green"
            Write-Info "Organization"  $data.org "Green"
            Write-Info "AS Number"     $data.as "Gray"
            Write-Info "AS Name"       $data.asname "Gray"

            $output += "=== IP INFORMATION ===`n"
            $output += "IP         : $($data.query)`n"
            $output += "Country    : $($data.country)`n"
            $output += "City       : $($data.city)`n"
            $output += "ISP        : $($data.isp)`n"
            $output += "AS         : $($data.as)`n`n"

            Write-SubSection "SECURITY FLAGS"
            if ($data.mobile)  { Write-Info "Mobile"    "YES - Cellular/Mobile Network" "Red" }
            else               { Write-Info "Mobile"    "No" "Green" }
            if ($data.proxy)   { Write-Info "Proxy/VPN" "YES - Anonymizer Detected" "Red" }
            else               { Write-Info "Proxy/VPN" "No" "Green" }
            if ($data.hosting) { Write-Info "Hosting"   "YES - Datacenter/Hosting IP" "Yellow" }
            else               { Write-Info "Hosting"   "No" "Green" }

            $output += "=== FLAGS ===`n"
            $output += "Mobile  : $($data.mobile)`n"
            $output += "Proxy   : $($data.proxy)`n"
            $output += "Hosting : $($data.hosting)`n`n"
        }
    }
    catch {
        Write-Log "Primary IP API failed" "WARN"
        try {
            $backup = Invoke-RestMethod -Uri "https://ipinfo.io/$IPAddress/json" -TimeoutSec 10
            Write-Info "IP"       $backup.ip "White"
            Write-Info "City"     $backup.city "Yellow"
            Write-Info "Country"  $backup.country "Yellow"
            Write-Info "Org"      $backup.org "Green"
        }
        catch {
            Write-Log "All IP APIs failed" "ERROR"
        }
    }

    Write-SubSection "PORT SCAN"
    Write-Log "Scanning 30 common ports..." "SCAN"

    $ports = @{
        21    = "FTP"
        22    = "SSH"
        23    = "Telnet"
        25    = "SMTP"
        53    = "DNS"
        80    = "HTTP"
        110   = "POP3"
        135   = "RPC"
        139   = "NetBIOS"
        143   = "IMAP"
        443   = "HTTPS"
        445   = "SMB"
        1433  = "MSSQL"
        1723  = "PPTP"
        3306  = "MySQL"
        3389  = "RDP"
        5432  = "PostgreSQL"
        5900  = "VNC"
        6379  = "Redis"
        8080  = "HTTP-Alt"
        8443  = "HTTPS-Alt"
        8888  = "HTTP-Alt2"
        9200  = "Elasticsearch"
        9300  = "Elasticsearch-T"
        11211 = "Memcached"
        27017 = "MongoDB"
        27018 = "MongoDB-Alt"
        50000 = "SAP"
        5000  = "Flask/UPnP"
        6667  = "IRC"
    }

    $openPorts = @()
    $portNum = 0

    foreach ($port in $ports.Keys | Sort-Object) {
        $portNum++
        Write-ProgressBar -Current $portNum -Total $ports.Count -Status "Port $port ($($ports[$port]))"
        try {
            $tcp = New-Object System.Net.Sockets.TcpClient
            $con = $tcp.BeginConnect($IPAddress, $port, $null, $null)
            $wait = $con.AsyncWaitHandle.WaitOne(800, $false)
            if ($wait -and $tcp.Connected) {
                Write-Host ""
                Write-Host "  [OPEN] Port $port - $($ports[$port])" -ForegroundColor Green
                $openPorts += "$port/$($ports[$port])"
                $Global:Stats.OpenPorts++
                $tcp.Close()
            }
        }
        catch {}
    }

    Write-Host ""

    if ($openPorts.Count -gt 0) {
        $output += "=== OPEN PORTS ===`n"
        $output += ($openPorts -join ", ") + "`n`n"
        Write-Info "Open Ports" "$($openPorts.Count) found" "Red"
        foreach ($p in $openPorts) {
            Write-Host "    $p" -ForegroundColor Green
        }
    }
    else {
        Write-Host "  No open ports detected (firewall may block)" -ForegroundColor DarkGray
    }

    Write-SubSection "THREAT INTELLIGENCE LINKS"
    Write-Host "  Shodan       : https://shodan.io/host/$IPAddress" -ForegroundColor Cyan
    Write-Host "  VirusTotal   : https://virustotal.com/gui/ip-address/$IPAddress" -ForegroundColor Cyan
    Write-Host "  AbuseIPDB    : https://abuseipdb.com/check/$IPAddress" -ForegroundColor Cyan
    Write-Host "  ThreatCrowd  : https://threatcrowd.org/ip.php?ip=$IPAddress" -ForegroundColor Cyan
    Write-Host "  Censys       : https://search.censys.io/hosts/$IPAddress" -ForegroundColor Cyan
    Write-Host "  IPVoid       : https://ipvoid.com/ip-blacklist-check/" -ForegroundColor Cyan
    Write-Host "  GreyNoise    : https://viz.greynoise.io/ip/$IPAddress" -ForegroundColor Cyan
    Write-Host "  AlienVault   : https://otx.alienvault.com/indicator/ip/$IPAddress" -ForegroundColor Cyan
    Write-Host "  IBM XForce   : https://exchange.xforce.ibmcloud.com/ip/$IPAddress" -ForegroundColor Cyan
    Write-Host "  Google Maps  : https://maps.google.com/?q=$($data.lat),$($data.lon)" -ForegroundColor Cyan

    $Global:Stats.IPsScanned++
    Add-ScanHistory -Module "IP" -Target $IPAddress -Result "$($openPorts.Count) ports open"
    Write-Log "IP intelligence complete" "SUCCESS"
    Show-SavePrompt -Content $output -Target $IPAddress -Type "IP"
}

# ================================================================================
# MODULE 3: EMAIL OSINT
# ================================================================================

function Get-EmailIntelligence {
    param([string]$EmailAddress)

    Write-Section "EMAIL INTELLIGENCE: $EmailAddress"

    if ($EmailAddress -notmatch "^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$") {
        Write-Log "Invalid email format!" "ERROR"
        return
    }

    $parts   = $EmailAddress.Split("@")
    $user    = $parts[0]
    $domain  = $parts[1]
    $output  = ""

    Write-SubSection "EMAIL BREAKDOWN"
    Write-Info "Full Email"    $EmailAddress "White"
    Write-Info "Username Part" $user         "Yellow"
    Write-Info "Domain Part"   $domain       "Yellow"
    Write-Info "Email Length"  "$($EmailAddress.Length) chars" "Gray"

    $output += "=== EMAIL INFO ===`n"
    $output += "Email    : $EmailAddress`n"
    $output += "Username : $user`n"
    $output += "Domain   : $domain`n`n"

    Write-SubSection "USERNAME PATTERNS"
    $hasNums  = $user -match "\d"
    $hasDots  = $user -match "\."
    $hasUnder = $user -match "_"
    $hasHyph  = $user -match "-"
    $isLower  = $user -ceq $user.ToLower()
    $isUpper  = $user -ceq $user.ToUpper()

    Write-Info "Contains Numbers"     $(if ($hasNums)  { "Yes" } else { "No" }) "Gray"
    Write-Info "Contains Dots"        $(if ($hasDots)  { "Yes" } else { "No" }) "Gray"
    Write-Info "Contains Underscore"  $(if ($hasUnder) { "Yes" } else { "No" }) "Gray"
    Write-Info "Contains Hyphens"     $(if ($hasHyph)  { "Yes" } else { "No" }) "Gray"
    Write-Info "All Lowercase"        $(if ($isLower)  { "Yes" } else { "No" }) "Gray"

    Write-SubSection "PROVIDER IDENTIFICATION"
    $provider = @{ Name="Unknown"; Security="Unknown"; Type="Unknown"; Country="Unknown" }

    switch -Wildcard ($domain) {
        "gmail.com"       { $provider = @{ Name="Google Gmail";        Security="High";          Type="Webmail";    Country="USA" } }
        "googlemail.com"  { $provider = @{ Name="Google Gmail";        Security="High";          Type="Webmail";    Country="USA" } }
        "yahoo.com"       { $provider = @{ Name="Yahoo Mail";          Security="Medium";        Type="Webmail";    Country="USA" } }
        "yahoo.*"         { $provider = @{ Name="Yahoo Mail";          Security="Medium";        Type="Webmail";    Country="USA" } }
        "hotmail.com"     { $provider = @{ Name="Microsoft Hotmail";   Security="High";          Type="Webmail";    Country="USA" } }
        "hotmail.*"       { $provider = @{ Name="Microsoft Hotmail";   Security="High";          Type="Webmail";    Country="USA" } }
        "outlook.com"     { $provider = @{ Name="Microsoft Outlook";   Security="High";          Type="Webmail";    Country="USA" } }
        "outlook.*"       { $provider = @{ Name="Microsoft Outlook";   Security="High";          Type="Webmail";    Country="USA" } }
        "live.com"        { $provider = @{ Name="Microsoft Live";      Security="High";          Type="Webmail";    Country="USA" } }
        "protonmail.com"  { $provider = @{ Name="ProtonMail";          Security="Very High E2EE";Type="Secure";     Country="Switzerland" } }
        "protonmail.ch"   { $provider = @{ Name="ProtonMail";          Security="Very High E2EE";Type="Secure";     Country="Switzerland" } }
        "proton.me"       { $provider = @{ Name="ProtonMail";          Security="Very High E2EE";Type="Secure";     Country="Switzerland" } }
        "tutanota.com"    { $provider = @{ Name="Tutanota";            Security="Very High E2EE";Type="Secure";     Country="Germany" } }
        "tutanota.de"     { $provider = @{ Name="Tutanota";            Security="Very High E2EE";Type="Secure";     Country="Germany" } }
        "icloud.com"      { $provider = @{ Name="Apple iCloud";        Security="High";          Type="Webmail";    Country="USA" } }
        "me.com"          { $provider = @{ Name="Apple iCloud";        Security="High";          Type="Webmail";    Country="USA" } }
        "mac.com"         { $provider = @{ Name="Apple iCloud";        Security="High";          Type="Webmail";    Country="USA" } }
        "aol.com"         { $provider = @{ Name="AOL Mail";            Security="Low";           Type="Webmail";    Country="USA" } }
        "zoho.com"        { $provider = @{ Name="Zoho Mail";           Security="Medium";        Type="Business";   Country="India" } }
        "yandex.com"      { $provider = @{ Name="Yandex Mail";         Security="Low";           Type="Webmail";    Country="Russia" } }
        "yandex.ru"       { $provider = @{ Name="Yandex Mail";         Security="Low";           Type="Webmail";    Country="Russia" } }
        "mail.com"        { $provider = @{ Name="Mail.com";            Security="Medium";        Type="Webmail";    Country="USA" } }
        "gmx.com"         { $provider = @{ Name="GMX Mail";            Security="Medium";        Type="Webmail";    Country="Germany" } }
        "gmx.net"         { $provider = @{ Name="GMX Mail";            Security="Medium";        Type="Webmail";    Country="Germany" } }
        "gmx.*"           { $provider = @{ Name="GMX Mail";            Security="Medium";        Type="Webmail";    Country="Germany" } }
        "guerrillamail.*" { $provider = @{ Name="Guerrilla Mail";      Security="None";          Type="Disposable"; Country="Unknown" } }
        "mailinator.com"  { $provider = @{ Name="Mailinator";          Security="None";          Type="Disposable"; Country="Unknown" } }
        "10minutemail.*"  { $provider = @{ Name="10 Minute Mail";      Security="None";          Type="Disposable"; Country="Unknown" } }
        "tempmail.com"    { $provider = @{ Name="Temp Mail";           Security="None";          Type="Disposable"; Country="Unknown" } }
        "throwaway.email" { $provider = @{ Name="Throwaway Email";     Security="None";          Type="Disposable"; Country="Unknown" } }
        "sharklasers.com" { $provider = @{ Name="Guerrilla Mail";      Security="None";          Type="Disposable"; Country="Unknown" } }
        default           { $provider = @{ Name="Custom Domain";       Security="Unknown";       Type="Custom";     Country="Unknown" } }
    }

    $secColor = switch ($provider.Security) {
        "Very High E2EE" { "Green" }
        "High"           { "Green" }
        "Medium"         { "Yellow" }
        "Low"            { "Red" }
        "None"           { "Red" }
        default          { "Gray" }
    }

    Write-Info "Provider Name"   $provider.Name     "Cyan"
    Write-Info "Security Level"  $provider.Security  $secColor
    Write-Info "Account Type"    $provider.Type      "Gray"
    Write-Info "Provider Country" $provider.Country  "Yellow"

    $output += "=== PROVIDER ===`n"
    $output += "Provider : $($provider.Name)`n"
    $output += "Security : $($provider.Security)`n`n"

    Write-SubSection "DNS RECORDS"
    Write-Log "Querying DNS records for $domain..." "SCAN"

    try {
        $mx = Resolve-DnsName -Name $domain -Type MX -ErrorAction Stop | Sort-Object Preference
        Write-Host "  MX Records (Mail Servers):" -ForegroundColor Cyan
        foreach ($r in $mx) {
            Write-Host "    Priority $($r.Preference) -> $($r.NameExchange)" -ForegroundColor Yellow
            $output += "MX: $($r.NameExchange)`n"
        }
    }
    catch { Write-Host "  MX Records: Not found" -ForegroundColor DarkGray }

    try {
        $a = Resolve-DnsName -Name $domain -Type A -ErrorAction Stop
        Write-Host "  A Records (IP Addresses):" -ForegroundColor Cyan
        foreach ($r in $a) {
            Write-Host "    -> $($r.IPAddress)" -ForegroundColor Yellow
        }
    }
    catch {}

    try {
        $txt = Resolve-DnsName -Name $domain -Type TXT -ErrorAction Stop
        Write-Host "  TXT Records:" -ForegroundColor Cyan
        $hasSPF = $false
        $hasDMARC = $false
        foreach ($r in $txt) {
            $str = $r.Strings -join " "
            if ($str -like "*v=spf*")   { Write-Host "    [SPF]   $str" -ForegroundColor Green;  $hasSPF = $true }
            if ($str -like "*v=DMARC*") { Write-Host "    [DMARC] $str" -ForegroundColor Green;  $hasDMARC = $true }
        }
        if (-not $hasSPF)   { Write-Host "    [SPF]   NOT configured" -ForegroundColor Red }
        if (-not $hasDMARC) { Write-Host "    [DMARC] NOT configured" -ForegroundColor Red }
    }
    catch {}

    try {
        $ns = Resolve-DnsName -Name $domain -Type NS -ErrorAction Stop
        Write-Host "  NS Records (Name Servers):" -ForegroundColor Cyan
        foreach ($r in $ns) {
            Write-Host "    -> $($r.NameHost)" -ForegroundColor Gray
        }
    }
    catch {}

    Write-SubSection "USERNAME VARIATIONS"
    $variations = @(
        $user,
        $user.ToLower(),
        $user.ToUpper(),
        ($user -replace "[0-9]", ""),
        ($user -replace "[._-]", ""),
        ($user -replace "[._-]", "_"),
        ($user -replace "[._-]", "."),
        ($user -replace "[._-]", "-"),
        ($user.Split(".") | Select-Object -First 1),
        ($user.Split("_") | Select-Object -First 1),
        ($user.Split("-") | Select-Object -First 1)
    ) | Select-Object -Unique | Where-Object { $_ -ne "" -and $_.Length -gt 0 }

    Write-Host "  Possible usernames from this email:" -ForegroundColor Cyan
    foreach ($var in $variations | Select-Object -First 10) {
        Write-Host "    -> $var" -ForegroundColor Gray
    }

    Write-SubSection "BREACH & LEAK INVESTIGATION"
    Write-Host "  HaveIBeenPwned  : https://haveibeenpwned.com/account/$EmailAddress" -ForegroundColor Cyan
    Write-Host "  Dehashed        : https://dehashed.com/search?query=$EmailAddress" -ForegroundColor Cyan
    Write-Host "  LeakCheck       : https://leakcheck.io/search/$EmailAddress" -ForegroundColor Cyan
    Write-Host "  IntelX          : https://intelx.io/?s=$EmailAddress" -ForegroundColor Cyan
    Write-Host "  BreachDirectory : https://breachdirectory.org" -ForegroundColor Cyan
    Write-Host "  SnusBase        : https://snusbase.com" -ForegroundColor Cyan

    Write-SubSection "OSINT TOOLS"
    Write-Host "  Google Search   : https://google.com/search?q=%22$EmailAddress%22" -ForegroundColor Cyan
    Write-Host "  Hunter.io       : https://hunter.io/email-verifier/$EmailAddress" -ForegroundColor Cyan
    Write-Host "  EmailRep        : https://emailrep.io/$EmailAddress" -ForegroundColor Cyan
    Write-Host "  Epieos          : https://epieos.com/?q=$EmailAddress" -ForegroundColor Cyan
    Write-Host "  Holehe          : https://github.com/megadose/holehe" -ForegroundColor Cyan
    Write-Host "  GHunt           : https://github.com/mxrch/GHunt" -ForegroundColor Cyan

    $Global:Stats.EmailsAnalyzed++
    Add-ScanHistory -Module "Email" -Target $EmailAddress -Result "Analysis complete"
    Write-Log "Email intelligence complete" "SUCCESS"
    Show-SavePrompt -Content $output -Target $EmailAddress -Type "Email"
}

# ================================================================================
# MODULE 4: PHONE INTELLIGENCE
# ================================================================================

function Get-PhoneIntelligence {
    param([string]$PhoneNumber)

    Write-Section "PHONE INTELLIGENCE: $PhoneNumber"
    Write-Log "Analyzing phone number..." "SCAN"

    $clean  = $PhoneNumber -replace "[^0-9+]", ""
    $digits = $clean -replace "[^0-9]", ""
    $output = ""

    Write-SubSection "NUMBER PARSING"
    Write-Info "Original Input" $PhoneNumber "White"
    Write-Info "Cleaned"       $clean       "Yellow"
    Write-Info "Digits Only"   $digits      "Gray"
    Write-Info "Digit Count"   "$($digits.Length)" "Gray"

    $format = "Unknown"
    if ($digits.Length -eq 7)  { $format = "Local (7 digits)" }
    if ($digits.Length -eq 10) { $format = "National (10 digits)" }
    if ($digits.Length -eq 11) { $format = "International (11 digits)" }
    if ($digits.Length -eq 12) { $format = "International with code (12 digits)" }
    if ($clean.StartsWith("+")) { $format += " - E.164 Format" }

    Write-Info "Format" $format "Cyan"

    $output += "=== PHONE INFO ===`n"
    $output += "Input   : $PhoneNumber`n"
    $output += "Cleaned : $clean`n"
    $output += "Format  : $format`n`n"

    Write-SubSection "COUNTRY IDENTIFICATION"
    $country = @{ Name="Unknown"; Region="Unknown"; Code="Unknown"; SubRegion="Unknown" }

    $countryCodes = @(
        @{Pattern="^\+1";    Name="USA / Canada";       Region="North America";   Code="+1";    Sub="NANP"}
        @{Pattern="^\+44";   Name="United Kingdom";     Region="Europe";          Code="+44";   Sub=""}
        @{Pattern="^\+91";   Name="India";              Region="Asia";            Code="+91";   Sub="South Asia"}
        @{Pattern="^\+86";   Name="China";              Region="Asia";            Code="+86";   Sub="East Asia"}
        @{Pattern="^\+81";   Name="Japan";              Region="Asia";            Code="+81";   Sub="East Asia"}
        @{Pattern="^\+49";   Name="Germany";            Region="Europe";          Code="+49";   Sub="Western Europe"}
        @{Pattern="^\+33";   Name="France";             Region="Europe";          Code="+33";   Sub="Western Europe"}
        @{Pattern="^\+39";   Name="Italy";              Region="Europe";          Code="+39";   Sub="Southern Europe"}
        @{Pattern="^\+34";   Name="Spain";              Region="Europe";          Code="+34";   Sub="Southern Europe"}
        @{Pattern="^\+7";    Name="Russia";             Region="Europe/Asia";     Code="+7";    Sub="Eastern Europe"}
        @{Pattern="^\+55";   Name="Brazil";             Region="South America";   Code="+55";   Sub=""}
        @{Pattern="^\+82";   Name="South Korea";        Region="Asia";            Code="+82";   Sub="East Asia"}
        @{Pattern="^\+90";   Name="Turkey";             Region="Europe/Asia";     Code="+90";   Sub=""}
        @{Pattern="^\+92";   Name="Pakistan";           Region="Asia";            Code="+92";   Sub="South Asia"}
        @{Pattern="^\+62";   Name="Indonesia";          Region="Asia";            Code="+62";   Sub="Southeast Asia"}
        @{Pattern="^\+63";   Name="Philippines";        Region="Asia";            Code="+63";   Sub="Southeast Asia"}
        @{Pattern="^\+880";  Name="Bangladesh";         Region="Asia";            Code="+880";  Sub="South Asia"}
        @{Pattern="^\+234";  Name="Nigeria";            Region="Africa";          Code="+234";  Sub="West Africa"}
        @{Pattern="^\+27";   Name="South Africa";       Region="Africa";          Code="+27";   Sub="Southern Africa"}
        @{Pattern="^\+20";   Name="Egypt";              Region="Africa";          Code="+20";   Sub="North Africa"}
        @{Pattern="^\+971";  Name="UAE";                Region="Middle East";     Code="+971";  Sub="Gulf"}
        @{Pattern="^\+966";  Name="Saudi Arabia";       Region="Middle East";     Code="+966";  Sub="Gulf"}
        @{Pattern="^\+961";  Name="Lebanon";            Region="Middle East";     Code="+961";  Sub="Levant"}
        @{Pattern="^\+962";  Name="Jordan";             Region="Middle East";     Code="+962";  Sub="Levant"}
        @{Pattern="^\+964";  Name="Iraq";               Region="Middle East";     Code="+964";  Sub=""}
        @{Pattern="^\+965";  Name="Kuwait";             Region="Middle East";     Code="+965";  Sub="Gulf"}
        @{Pattern="^\+968";  Name="Oman";               Region="Middle East";     Code="+968";  Sub="Gulf"}
        @{Pattern="^\+974";  Name="Qatar";              Region="Middle East";     Code="+974";  Sub="Gulf"}
        @{Pattern="^\+973";  Name="Bahrain";            Region="Middle East";     Code="+973";  Sub="Gulf"}
        @{Pattern="^\+967";  Name="Yemen";              Region="Middle East";     Code="+967";  Sub=""}
        @{Pattern="^\+52";   Name="Mexico";             Region="North America";   Code="+52";   Sub=""}
        @{Pattern="^\+54";   Name="Argentina";          Region="South America";   Code="+54";   Sub=""}
        @{Pattern="^\+56";   Name="Chile";              Region="South America";   Code="+56";   Sub=""}
        @{Pattern="^\+57";   Name="Colombia";           Region="South America";   Code="+57";   Sub=""}
        @{Pattern="^\+51";   Name="Peru";               Region="South America";   Code="+51";   Sub=""}
        @{Pattern="^\+58";   Name="Venezuela";          Region="South America";   Code="+58";   Sub=""}
        @{Pattern="^\+61";   Name="Australia";          Region="Oceania";         Code="+61";   Sub=""}
        @{Pattern="^\+64";   Name="New Zealand";        Region="Oceania";         Code="+64";   Sub=""}
        @{Pattern="^\+65";   Name="Singapore";          Region="Asia";            Code="+65";   Sub="Southeast Asia"}
        @{Pattern="^\+60";   Name="Malaysia";           Region="Asia";            Code="+60";   Sub="Southeast Asia"}
        @{Pattern="^\+66";   Name="Thailand";           Region="Asia";            Code="+66";   Sub="Southeast Asia"}
        @{Pattern="^\+84";   Name="Vietnam";            Region="Asia";            Code="+84";   Sub="Southeast Asia"}
        @{Pattern="^\+212";  Name="Morocco";            Region="Africa";          Code="+212";  Sub="North Africa"}
        @{Pattern="^\+213";  Name="Algeria";            Region="Africa";          Code="+213";  Sub="North Africa"}
        @{Pattern="^\+216";  Name="Tunisia";            Region="Africa";          Code="+216";  Sub="North Africa"}
        @{Pattern="^\+218";  Name="Libya";              Region="Africa";          Code="+218";  Sub="North Africa"}
        @{Pattern="^\+249";  Name="Sudan";              Region="Africa";          Code="+249";  Sub="East Africa"}
        @{Pattern="^\+251";  Name="Ethiopia";           Region="Africa";          Code="+251";  Sub="East Africa"}
        @{Pattern="^\+254";  Name="Kenya";              Region="Africa";          Code="+254";  Sub="East Africa"}
        @{Pattern="^\+255";  Name="Tanzania";           Region="Africa";          Code="+255";  Sub="East Africa"}
        @{Pattern="^\+256";  Name="Uganda";             Region="Africa";          Code="+256";  Sub="East Africa"}
        @{Pattern="^\+233";  Name="Ghana";              Region="Africa";          Code="+233";  Sub="West Africa"}
        @{Pattern="^\+225";  Name="Ivory Coast";        Region="Africa";          Code="+225";  Sub="West Africa"}
        @{Pattern="^\+221";  Name="Senegal";            Region="Africa";          Code="+221";  Sub="West Africa"}
    )

    foreach ($cc in $countryCodes) {
        if ($clean -match $cc.Pattern) {
            $country = @{ Name=$cc.Name; Region=$cc.Region; Code=$cc.Code; SubRegion=$cc.Sub }
            break
        }
    }

    Write-Info "Country"     $country.Name      "Green"
    Write-Info "Region"      $country.Region    "Yellow"
    Write-Info "Sub-Region"  $country.SubRegion "Gray"
    Write-Info "Dial Code"   $country.Code      "Cyan"

    Write-SubSection "NUMBER FORMATTING"
    Write-Host "  E.164 International   : +$digits" -ForegroundColor Cyan
    Write-Host "  RFC3966               : tel:+$digits" -ForegroundColor Gray
    Write-Host "  Digits Only           : $digits" -ForegroundColor Gray

    if ($digits.Length -ge 10) {
        $d = $digits
        if ($d.Length -ge 11) { $d = $d.Substring(1) }
        if ($d.Length -ge 10) {
            $area = $d.Substring(0, 3)
            $mid  = $d.Substring(3, 3)
            $last = $d.Substring(6)
            Write-Host "  Formatted             : ($area) $mid-$last" -ForegroundColor Yellow
        }
    }

    $output += "=== PHONE LOCATION ===`n"
    $output += "Country : $($country.Name)`n"
    $output += "Region  : $($country.Region)`n`n"

    Write-SubSection "CARRIER PATTERNS (USA/Canada)"
    if ($country.Code -eq "+1" -and $digits.Length -ge 11) {
        $area = $digits.Substring(1, 3)
        Write-Info "Area Code" $area "Yellow"
        Write-Host "  Area code lookup: https://www.areacodelocations.info/areacodelist.html" -ForegroundColor Cyan
    }

    Write-SubSection "OSINT TOOLS"
    Write-Host "  Google Search  : https://google.com/search?q=%22$clean%22" -ForegroundColor Cyan
    Write-Host "  Google Search2 : https://google.com/search?q=%22$digits%22" -ForegroundColor Cyan
    Write-Host "  Truecaller     : https://truecaller.com/search/us/$digits" -ForegroundColor Cyan
    Write-Host "  NumLookup      : https://numlookup.com/?number=$clean" -ForegroundColor Cyan
    Write-Host "  CallerID Test  : https://calleridtest.com/lookup?number=$digits" -ForegroundColor Cyan
    Write-Host "  Sync.me        : https://sync.me/search/?number=$clean" -ForegroundColor Cyan
    Write-Host "  WhitePages     : https://whitepages.com/phone/$digits" -ForegroundColor Cyan
    Write-Host "  Spy Dialer     : https://spydialer.com/default.aspx" -ForegroundColor Cyan

    $Global:Stats.PhonesAnalyzed++
    Add-ScanHistory -Module "Phone" -Target $PhoneNumber -Result "$($country.Name)"
    Write-Log "Phone analysis complete" "SUCCESS"
    Show-SavePrompt -Content $output -Target $digits -Type "Phone"
}

# ================================================================================
# MODULE 5: DOMAIN INTELLIGENCE
# ================================================================================

function Get-DomainIntelligence {
    param([string]$Domain)

    Write-Section "DOMAIN INTELLIGENCE: $Domain"
    Write-Log "Gathering domain intelligence..." "SCAN"

    $output = ""

    Write-SubSection "DNS RECORD ANALYSIS"
    $types = @("A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA")

    foreach ($type in $types) {
        try {
            $records = Resolve-DnsName -Name $Domain -Type $type -ErrorAction Stop
            Write-Host "  [$type Records]" -ForegroundColor Cyan
            foreach ($r in $records) {
                switch ($type) {
                    "A"     { Write-Host "    -> $($r.IPAddress)" -ForegroundColor Green }
                    "AAAA"  { Write-Host "    -> $($r.IPAddress)" -ForegroundColor Green }
                    "MX"    { Write-Host "    Priority $($r.Preference) -> $($r.NameExchange)" -ForegroundColor Yellow }
                    "NS"    { Write-Host "    -> $($r.NameHost)" -ForegroundColor Cyan }
                    "TXT"   { Write-Host "    -> $($r.Strings -join ' ')" -ForegroundColor Gray }
                    "CNAME" { Write-Host "    -> $($r.NameHost)" -ForegroundColor Magenta }
                    "SOA"   { Write-Host "    Primary: $($r.PrimaryServer)" -ForegroundColor DarkYellow }
                }
                $output += "[$type] $r`n"
            }
        }
        catch {
            Write-Host "  [$type] Not found" -ForegroundColor DarkGray
        }
    }

    Write-SubSection "SUBDOMAIN ENUMERATION"
    Write-Log "Scanning common subdomains..." "SCAN"

    $subs = @(
        "www","mail","ftp","admin","webmail","cpanel","whm",
        "api","dev","staging","test","beta","demo","alpha",
        "blog","shop","store","forum","support","help","docs",
        "m","mobile","app","portal","dashboard","panel","cms",
        "vpn","remote","gateway","proxy","cdn","static",
        "smtp","pop","imap","exchange","autodiscover",
        "ns1","ns2","ns3","dns","dns1","dns2",
        "db","database","mysql","postgres","mongo","redis",
        "git","gitlab","jenkins","ci","build","deploy",
        "files","download","upload","assets","media","img",
        "status","monitoring","monitor","metrics","logs","kibana",
        "backup","old","legacy","archive","beta","v2","new"
    )

    $foundSubs = @()
    $si = 0

    foreach ($sub in $subs) {
        $si++
        $fqdn = "$sub.$Domain"
        Write-ProgressBar -Current $si -Total $subs.Count -Status $fqdn

        try {
            $res = Resolve-DnsName -Name $fqdn -ErrorAction Stop
            Write-Host ""
            $ip = if ($res[0].IPAddress) { $res[0].IPAddress } else { "resolved" }
            Write-Host "  [FOUND] $fqdn -> $ip" -ForegroundColor Green
            $foundSubs += $fqdn
            $output += "[SUBDOMAIN] $fqdn -> $ip`n"
        }
        catch {}

        Start-Sleep -Milliseconds 80
    }

    Write-Host ""

    if ($foundSubs.Count -gt 0) {
        Write-Info "Subdomains Found" "$($foundSubs.Count)" "Green"
    }
    else {
        Write-Host "  No common subdomains found" -ForegroundColor DarkGray
    }

    Write-SubSection "HTTP STATUS CHECK"
    $urls = @("http://$Domain","https://$Domain","http://www.$Domain","https://www.$Domain")

    foreach ($url in $urls) {
        try {
            $r = Invoke-WebRequest -Uri $url -Method Head -TimeoutSec 8 `
                -UserAgent $Global:Network.UserAgent -ErrorAction Stop
            Write-Host "  [HTTP $($r.StatusCode)] $url" -ForegroundColor Green
            if ($r.Headers["Server"]) {
                Write-Host "    Server: $($r.Headers['Server'])" -ForegroundColor Gray
            }
        }
        catch {
            $code = $_.Exception.Response.StatusCode.value__
            if ($code) {
                Write-Host "  [HTTP $code] $url" -ForegroundColor Yellow
            }
            else {
                Write-Host "  [OFFLINE] $url" -ForegroundColor Red
            }
        }
    }

    Write-SubSection "OSINT & SECURITY TOOLS"
    Write-Host "  WHOIS           : https://who.is/whois/$Domain" -ForegroundColor Cyan
    Write-Host "  Shodan          : https://shodan.io/search?query=hostname:$Domain" -ForegroundColor Cyan
    Write-Host "  VirusTotal      : https://virustotal.com/gui/domain/$Domain" -ForegroundColor Cyan
    Write-Host "  URLScan         : https://urlscan.io/search/#$Domain" -ForegroundColor Cyan
    Write-Host "  Wayback Machine : https://web.archive.org/web/*/$Domain" -ForegroundColor Cyan
    Write-Host "  DNSDumpster     : https://dnsdumpster.com" -ForegroundColor Cyan
    Write-Host "  SecurityTrails  : https://securitytrails.com/domain/$Domain/dns" -ForegroundColor Cyan
    Write-Host "  crt.sh          : https://crt.sh/?q=$Domain" -ForegroundColor Cyan
    Write-Host "  Censys          : https://search.censys.io/search?q=$Domain" -ForegroundColor Cyan
    Write-Host "  ThreatCrowd     : https://threatcrowd.org/domain.php?domain=$Domain" -ForegroundColor Cyan
    Write-Host "  AlienVault      : https://otx.alienvault.com/indicator/domain/$Domain" -ForegroundColor Cyan
    Write-Host "  Netcraft        : https://toolbar.netcraft.com/site_report?url=$Domain" -ForegroundColor Cyan

    $Global:Stats.DomainsScanned++
    Add-ScanHistory -Module "Domain" -Target $Domain -Result "$($foundSubs.Count) subdomains found"
    Write-Log "Domain intelligence complete" "SUCCESS"
    Show-SavePrompt -Content $output -Target $Domain -Type "Domain"
}

# ================================================================================
# MODULE 6: PERSON SEARCH
# ================================================================================

function Search-Person {
    param([string]$FirstName, [string]$LastName, [string]$Location = "", [string]$Age = "")

    $fullName = "$FirstName $LastName"
    Write-Section "PERSON SEARCH: $fullName"
    Write-Log "Searching for person: $fullName" "SCAN"

    Write-SubSection "TARGET INFORMATION"
    Write-Info "First Name" $FirstName "Yellow"
    Write-Info "Last Name"  $LastName  "Yellow"
    Write-Info "Full Name"  $fullName  "White"
    if ($Location) { Write-Info "Location" $Location "Cyan" }
    if ($Age)      { Write-Info "Age"      $Age      "Gray" }

    $encoded = [System.Uri]::EscapeDataString($fullName)
    $output  = "Target: $fullName`nLocation: $Location`n`n"

    Write-SubSection "PEOPLE SEARCH ENGINES"
    Write-Host "  Spokeo           : https://spokeo.com/search?q=$encoded" -ForegroundColor Cyan
    Write-Host "  BeenVerified     : https://beenverified.com/people/$FirstName-$LastName" -ForegroundColor Cyan
    Write-Host "  Pipl             : https://pipl.com/search/?q=$encoded" -ForegroundColor Cyan
    Write-Host "  Whitepages       : https://whitepages.com/name/$FirstName-$LastName" -ForegroundColor Cyan
    Write-Host "  TruePeopleSearch : https://truepeoplesearch.com/results?name=$encoded" -ForegroundColor Cyan
    Write-Host "  FastPeopleSearch : https://fastpeoplesearch.com/name/$FirstName-$LastName" -ForegroundColor Cyan
    Write-Host "  411.com          : https://411.com/people/$encoded" -ForegroundColor Cyan
    Write-Host "  AnyWho          : https://anywho.com/people/$FirstName+$LastName" -ForegroundColor Cyan
    Write-Host "  PeekYou          : https://peekyou.com/$FirstName+$LastName" -ForegroundColor Cyan
    Write-Host "  Intelius         : https://intelius.com/people/$FirstName-$LastName" -ForegroundColor Cyan
    Write-Host "  PublicRecords    : https://publicrecords.searchsystems.net" -ForegroundColor Cyan

    Write-SubSection "SOCIAL MEDIA SEARCH"
    Write-Host "  LinkedIn      : https://linkedin.com/search/results/people/?keywords=$encoded" -ForegroundColor Cyan
    Write-Host "  Facebook      : https://facebook.com/search/people/?q=$encoded" -ForegroundColor Cyan
    Write-Host "  Twitter       : https://twitter.com/search?q=%22$fullName%22" -ForegroundColor Cyan
    Write-Host "  Instagram     : https://instagram.com/explore/tags/$($FirstName+$LastName)/" -ForegroundColor Cyan
    Write-Host "  TikTok        : https://tiktok.com/search/user?q=$encoded" -ForegroundColor Cyan

    Write-SubSection "PROFESSIONAL NETWORKS"
    Write-Host "  LinkedIn      : https://linkedin.com/search/results/people/?keywords=$encoded" -ForegroundColor Cyan
    Write-Host "  AngelList     : https://angel.co/$FirstName-$LastName" -ForegroundColor Cyan
    Write-Host "  Crunchbase    : https://crunchbase.com/person/$FirstName-$LastName" -ForegroundColor Cyan
    Write-Host "  GitHub        : https://github.com/search?q=$FirstName+$LastName" -ForegroundColor Cyan
    Write-Host "  ResearchGate  : https://researchgate.net/search?q=$encoded" -ForegroundColor Cyan
    Write-Host "  Academia.edu  : https://academia.edu/search?q=$encoded" -ForegroundColor Cyan

    Write-SubSection "GOOGLE DORK SEARCHES"
    Write-Host "  -> https://google.com/search?q=%22$fullName%22" -ForegroundColor Cyan
    Write-Host "  -> https://google.com/search?q=%22$fullName%22+%22$Location%22" -ForegroundColor Cyan
    Write-Host "  -> https://google.com/search?q=%22$fullName%22+site:linkedin.com" -ForegroundColor Cyan
    Write-Host "  -> https://google.com/search?q=%22$fullName%22+site:facebook.com" -ForegroundColor Cyan
    Write-Host "  -> https://google.com/search?q=%22$fullName%22+filetype:pdf" -ForegroundColor Cyan
    Write-Host "  -> https://google.com/search?q=%22$fullName%22+email" -ForegroundColor Cyan
    Write-Host "  -> https://google.com/search?q=%22$fullName%22+phone" -ForegroundColor Cyan
    Write-Host "  -> https://google.com/search?q=%22$fullName%22+address" -ForegroundColor Cyan

    Write-SubSection "IMAGE SEARCH"
    Write-Host "  Google Images : https://google.com/search?q=%22$fullName%22&tbm=isch" -ForegroundColor Cyan
    Write-Host "  Bing Images   : https://bing.com/images/search?q=%22$fullName%22" -ForegroundColor Cyan
    Write-Host "  Yandex Images : https://yandex.com/images/search?text=$encoded" -ForegroundColor Cyan

    Write-SubSection "NEWS SEARCH"
    Write-Host "  Google News   : https://news.google.com/search?q=$encoded" -ForegroundColor Cyan
    Write-Host "  Bing News     : https://bing.com/news/search?q=%22$fullName%22" -ForegroundColor Cyan

    Add-ScanHistory -Module "Person" -Target $fullName -Result "Search links generated"
    Write-Log "Person search complete" "SUCCESS"
    Show-SavePrompt -Content $output -Target "$FirstName-$LastName" -Type "Person"
}

# ================================================================================
# MODULE 7: GOOGLE DORK GENERATOR
# ================================================================================

function Get-GoogleDorks {
    param([string]$Target, [string]$TargetType = "general")

    Write-Section "GOOGLE DORK GENERATOR: $Target"
    Write-Log "Generating dorks..." "SCAN"

    $output = ""

    Write-SubSection "BASIC SEARCHES"
    $basic = @(
        "%22$Target%22",
        "$Target",
        "intitle:%22$Target%22",
        "inurl:%22$Target%22",
        "intext:%22$Target%22",
        "allintext:%22$Target%22",
        "allintitle:%22$Target%22"
    )
    foreach ($d in $basic) {
        Write-Host "  -> https://google.com/search?q=$d" -ForegroundColor Cyan
        $output += "https://google.com/search?q=$d`n"
    }

    Write-SubSection "FILE TYPE SEARCHES"
    $files = @("pdf","doc","docx","xls","xlsx","ppt","pptx","txt","csv","xml","json","sql","log","bak")
    foreach ($ft in $files) {
        Write-Host "  -> https://google.com/search?q=%22$Target%22+filetype:$ft" -ForegroundColor Cyan
        $output += "https://google.com/search?q=%22$Target%22+filetype:$ft`n"
    }

    Write-SubSection "SOCIAL MEDIA SEARCHES"
    $social = @(
        "linkedin.com","facebook.com","twitter.com","instagram.com",
        "tiktok.com","youtube.com","reddit.com","pinterest.com"
    )
    foreach ($site in $social) {
        Write-Host "  -> https://google.com/search?q=%22$Target%22+site:$site" -ForegroundColor Cyan
    }

    Write-SubSection "CODE & LEAK SITES"
    $code = @(
        "github.com","gitlab.com","bitbucket.org",
        "pastebin.com","gist.github.com","paste.org"
    )
    foreach ($site in $code) {
        Write-Host "  -> https://google.com/search?q=%22$Target%22+site:$site" -ForegroundColor Cyan
    }

    Write-SubSection "SENSITIVE DATA SEARCHES"
    $sensitive = @(
        "%22$Target%22+password",
        "%22$Target%22+email",
        "%22$Target%22+phone",
        "%22$Target%22+address",
        "%22$Target%22+credentials",
        "%22$Target%22+api+key",
        "%22$Target%22+private+key",
        "%22$Target%22+secret"
    )
    foreach ($d in $sensitive) {
        Write-Host "  -> https://google.com/search?q=$d" -ForegroundColor Red
    }

    Write-SubSection "OTHER SEARCH ENGINES"
    Write-Host "  Bing        : https://bing.com/search?q=%22$Target%22" -ForegroundColor Cyan
    Write-Host "  DuckDuckGo  : https://duckduckgo.com/?q=%22$Target%22" -ForegroundColor Cyan
    Write-Host "  Yandex      : https://yandex.com/search/?text=$Target" -ForegroundColor Cyan
    Write-Host "  Baidu       : https://baidu.com/s?wd=$Target" -ForegroundColor Cyan
    Write-Host "  Startpage   : https://startpage.com/search?q=%22$Target%22" -ForegroundColor Cyan

    Add-ScanHistory -Module "Dorks" -Target $Target -Result "Dorks generated"
    Write-Log "Dork generation complete" "SUCCESS"
    Show-SavePrompt -Content $output -Target $Target -Type "Dorks"
}

# ================================================================================
# MODULE 8: LOCAL NETWORK INFO
# ================================================================================

function Get-LocalNetworkInfo {
    Write-Section "LOCAL NETWORK INFORMATION"
    Write-Log "Gathering network info..." "SCAN"

    Write-SubSection "YOUR PUBLIC IP"
    try {
        $pub = Invoke-RestMethod -Uri "https://api.ipify.org?format=json" -TimeoutSec 5
        Write-Info "Public IP" $pub.ip "Green"
        try {
            $geo = Invoke-RestMethod -Uri "http://ip-api.com/json/$($pub.ip)" -TimeoutSec 5
            if ($geo.status -eq "success") {
                Write-Info "Location"  "$($geo.city), $($geo.country)" "Yellow"
                Write-Info "ISP"       $geo.isp "Cyan"
                Write-Info "Proxy/VPN" $(if ($geo.proxy) { "YES - VPN/Proxy detected" } else { "No" }) $(if ($geo.proxy) { "Red" } else { "Green" })
            }
        } catch {}
    }
    catch {
        Write-Log "Could not fetch public IP" "ERROR"
    }

    Write-SubSection "LOCAL INTERFACES"
    try {
        $adapters = Get-NetIPAddress -AddressFamily IPv4 | Where-Object {
            $_.InterfaceAlias -notlike "*Loopback*"
        }
        foreach ($a in $adapters) {
            Write-Host "  Interface : $($a.InterfaceAlias)" -ForegroundColor Cyan
            Write-Host "    IP      : $($a.IPAddress)" -ForegroundColor Yellow
            Write-Host "    Prefix  : /$($a.PrefixLength)" -ForegroundColor Gray
        }
    }
    catch {}

    Write-SubSection "GATEWAY"
    try {
        $gw = Get-NetRoute -DestinationPrefix "0.0.0.0/0" | Select-Object -First 1
        Write-Info "Gateway" $gw.NextHop "Cyan"
    }
    catch {}

    Write-SubSection "DNS SERVERS"
    try {
        $dns = Get-DnsClientServerAddress -AddressFamily IPv4 | Where-Object { $_.ServerAddresses.Count -gt 0 }
        foreach ($d in $dns) {
            Write-Host "  $($d.InterfaceAlias) -> $($d.ServerAddresses -join ', ')" -ForegroundColor Yellow
        }
    }
    catch {}

    Write-SubSection "MAC ADDRESSES"
    try {
        $macs = Get-NetAdapter | Where-Object { $_.Status -eq "Up" }
        foreach ($m in $macs) {
            Write-Info $m.Name $m.MacAddress "Gray"
        }
    }
    catch {}

    Write-SubSection "SYSTEM INFORMATION"
    Write-Info "Hostname"   $env:COMPUTERNAME "White"
    Write-Info "Username"   $env:USERNAME "White"
    Write-Info "Domain"     $env:USERDOMAIN "Gray"
    Write-Info "PowerShell" $PSVersionTable.PSVersion.ToString() "Green"

    try {
        $os = Get-WmiObject Win32_OperatingSystem
        Write-Info "OS"           $os.Caption "Cyan"
        Write-Info "Architecture" $os.OSArchitecture "Gray"
        Write-Info "Version"      $os.Version "Gray"
        
        $cs = Get-WmiObject Win32_ComputerSystem
        Write-Info "RAM" "$([math]::Round($cs.TotalPhysicalMemory / 1GB, 2)) GB" "Gray"
        Write-Info "Manufacturer" $cs.Manufacturer "Gray"
        Write-Info "Model" $cs.Model "Gray"
    }
    catch {}

    Write-SubSection "ACTIVE CONNECTIONS"
    try {
        $connections = Get-NetTCPConnection | Where-Object { $_.State -eq "Established" } | Select-Object -First 10
        foreach ($conn in $connections) {
            Write-Host "  $($conn.LocalAddress):$($conn.LocalPort) -> $($conn.RemoteAddress):$($conn.RemotePort)" -ForegroundColor Gray
        }
    }
    catch {}

    Write-SubSection "SECURITY TOOLS"
    Write-Host "  IP Leak Test    : https://ipleak.net" -ForegroundColor Cyan
    Write-Host "  DNS Leak Test   : https://dnsleaktest.com" -ForegroundColor Cyan
    Write-Host "  WebRTC Test     : https://browserleaks.com/webrtc" -ForegroundColor Cyan
    Write-Host "  Speed Test      : https://fast.com" -ForegroundColor Cyan
    Write-Host "  Firewall Test   : https://www.grc.com/shieldsup" -ForegroundColor Cyan
    Write-Host "  Anonymity Test  : https://www.whatismybrowser.com" -ForegroundColor Cyan

    Write-Log "Network scan complete" "SUCCESS"
}

# ================================================================================
# MODULE 9: BREACH HUNTER
# ================================================================================

function Search-Breaches {
    param([string]$Target, [string]$Type = "email")

    Write-Section "BREACH & LEAK HUNTER: $Target"
    Write-Log "Searching for breaches..." "SCAN"

    Write-SubSection "BREACH DATABASE SEARCH"
    Write-Host "  -> HaveIBeenPwned  : https://haveibeenpwned.com/account/$Target" -ForegroundColor Cyan
    Write-Host "  -> Dehashed        : https://dehashed.com/search?query=$Target" -ForegroundColor Cyan
    Write-Host "  -> LeakCheck       : https://leakcheck.io/search/$Target" -ForegroundColor Cyan
    Write-Host "  -> IntelX          : https://intelx.io/?s=$Target" -ForegroundColor Cyan
    Write-Host "  -> BreachDirectory : https://breachdirectory.org" -ForegroundColor Cyan
    Write-Host "  -> SnusBase        : https://snusbase.com" -ForegroundColor Cyan
    Write-Host "  -> GhostProject    : https://ghostproject.fr" -ForegroundColor Cyan
    Write-Host "  -> PwnDB           : http://pwndb2am4tzkvold.onion" -ForegroundColor Red

    Write-SubSection "PASTE SITE SEARCH"
    Write-Host "  Pastebin    : https://pastebin.com/search?q=$Target" -ForegroundColor Cyan
    Write-Host "  PasteHunter : https://pastehunter.com" -ForegroundColor Cyan
    Write-Host "  PasteBin.fr : https://fr.pastebin.com/search?q=$Target" -ForegroundColor Cyan

    Write-SubSection "GOOGLE BREACH DORKS"
    Write-Host "  -> https://google.com/search?q=%22$Target%22+site:pastebin.com" -ForegroundColor Cyan
    Write-Host "  -> https://google.com/search?q=%22$Target%22+password" -ForegroundColor Cyan
    Write-Host "  -> https://google.com/search?q=%22$Target%22+leaked" -ForegroundColor Cyan
    Write-Host "  -> https://google.com/search?q=%22$Target%22+breach" -ForegroundColor Cyan
    Write-Host "  -> https://google.com/search?q=%22$Target%22+dump" -ForegroundColor Cyan

    Write-Log "Breach search links generated" "SUCCESS"
}

# ================================================================================
# MODULE 10: SOCIAL MEDIA DEEP SEARCH
# ================================================================================

function Search-SocialMedia {
    param([string]$Target)

    Write-Section "SOCIAL MEDIA DEEP SEARCH: $Target"
    Write-Log "Social media investigation..." "SCAN"
    $encoded = [System.Uri]::EscapeDataString($Target)

    Write-SubSection "FACEBOOK INVESTIGATION"
    Write-Host "  Profile Search    : https://facebook.com/search/people/?q=$encoded" -ForegroundColor Cyan
    Write-Host "  Page Search       : https://facebook.com/search/pages/?q=$encoded" -ForegroundColor Cyan
    Write-Host "  Post Search       : https://facebook.com/search/posts/?q=$encoded" -ForegroundColor Cyan
    Write-Host "  Graph Search      : https://facebook.com/search/top/?q=$encoded" -ForegroundColor Cyan
    Write-Host "  Google Dork       : https://google.com/search?q=%22$Target%22+site:facebook.com" -ForegroundColor Cyan

    Write-SubSection "TWITTER/X INVESTIGATION"
    Write-Host "  Profile Search    : https://twitter.com/search?q=$encoded&f=user" -ForegroundColor Cyan
    Write-Host "  Tweet Search      : https://twitter.com/search?q=%22$Target%22" -ForegroundColor Cyan
    Write-Host "  Advanced Search   : https://twitter.com/search-advanced" -ForegroundColor Cyan
    Write-Host "  Nitter (Alt)      : https://nitter.net/search?q=$Target" -ForegroundColor Cyan

    Write-SubSection "INSTAGRAM INVESTIGATION"
    Write-Host "  Profile           : https://instagram.com/$Target" -ForegroundColor Cyan
    Write-Host "  Tag Search        : https://instagram.com/explore/tags/$Target" -ForegroundColor Cyan
    Write-Host "  Google Dork       : https://google.com/search?q=%22$Target%22+site:instagram.com" -ForegroundColor Cyan

    Write-SubSection "LINKEDIN INVESTIGATION"
    Write-Host "  People Search     : https://linkedin.com/search/results/people/?keywords=$encoded" -ForegroundColor Cyan
    Write-Host "  Company Search    : https://linkedin.com/search/results/companies/?keywords=$encoded" -ForegroundColor Cyan
    Write-Host "  Google Dork       : https://google.com/search?q=%22$Target%22+site:linkedin.com" -ForegroundColor Cyan

    Write-SubSection "TIKTOK INVESTIGATION"
    Write-Host "  Profile           : https://tiktok.com/@$Target" -ForegroundColor Cyan
    Write-Host "  Search            : https://tiktok.com/search/user?q=$encoded" -ForegroundColor Cyan

    Write-SubSection "YOUTUBE INVESTIGATION"
    Write-Host "  Channel           : https://youtube.com/@$Target" -ForegroundColor Cyan
    Write-Host "  Search            : https://youtube.com/results?search_query=$encoded" -ForegroundColor Cyan

    Write-SubSection "REDDIT INVESTIGATION"
    Write-Host "  User Profile      : https://reddit.com/user/$Target" -ForegroundColor Cyan
    Write-Host "  Search Posts      : https://reddit.com/search?q=%22$Target%22" -ForegroundColor Cyan

    Write-Log "Social media search complete" "SUCCESS"
}

# ================================================================================
# MAIN MENU
# ================================================================================

function Show-MainMenu {
    Write-Host ""
    Write-Host "  ================================================================" -ForegroundColor Cyan
    Write-Host "                      MAIN MENU" -ForegroundColor Cyan
    Write-Host "  ================================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "   [1]  Username Search         (100+ platforms)" -ForegroundColor White
    Write-Host "   [2]  IP Intelligence         (Geo + Ports + Threats)" -ForegroundColor White
    Write-Host "   [3]  Email OSINT             (Deep Analysis + Breach)" -ForegroundColor White
    Write-Host "   [4]  Phone Intelligence      (Country + Carrier)" -ForegroundColor White
    Write-Host "   [5]  Domain Intelligence     (DNS + Subdomains)" -ForegroundColor White
    Write-Host "   [6]  Person Search           (People Finder)" -ForegroundColor White
    Write-Host "   [7]  Google Dork Generator   (Auto Dorks)" -ForegroundColor White
    Write-Host "   [8]  Local Network Info      (System Scan)" -ForegroundColor White
    Write-Host "   [9]  Breach Hunter           (Leak Search)" -ForegroundColor White
    Write-Host "   [10] Social Media Deep Search" -ForegroundColor White
    Write-Host ""
    Write-Host "   [11] FULL OSINT SCAN         (All Modules)" -ForegroundColor Yellow
    Write-Host "   [12] View Statistics" -ForegroundColor Gray
    Write-Host "   [13] View Scan History" -ForegroundColor Gray
    Write-Host "   [14] Open Reports Folder" -ForegroundColor Gray
    Write-Host "   [15] Exit" -ForegroundColor Red
    Write-Host ""
    Write-Host "  ================================================================" -ForegroundColor Cyan
    Write-Host "  Made by PRATAM | Version $($Global:Config.Version)" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  Choice: " -NoNewline -ForegroundColor Yellow
}

function Show-Statistics {
    Write-Section "SESSION STATISTICS"
    $runtime = (Get-Date) - $Global:Stats.SessionStart
    Write-Host ""
    Write-Info "Runtime"        "$($runtime.Hours)h $($runtime.Minutes)m $($runtime.Seconds)s" "Cyan"
    Write-Info "Total Scans"    "$($Global:Stats.TotalScans)" "Yellow"
    Write-Info "Profiles Found" "$($Global:Stats.ProfilesFound)" "Green"
    Write-Info "IPs Scanned"    "$($Global:Stats.IPsScanned)" "Green"
    Write-Info "Open Ports"     "$($Global:Stats.OpenPorts)" "Red"
    Write-Info "Emails Checked" "$($Global:Stats.EmailsAnalyzed)" "Green"
    Write-Info "Phones Checked" "$($Global:Stats.PhonesAnalyzed)" "Green"
    Write-Info "Domains Scanned""$($Global:Stats.DomainsScanned)" "Green"
    Write-Info "Reports Saved"  "$($Global:Stats.ReportsSaved)" "Cyan"
}

function Show-ScanHistory {
    Write-Section "SCAN HISTORY"
    if ($Global:ScanHistory.Count -eq 0) {
        Write-Host "  No scans recorded yet" -ForegroundColor DarkGray
    }
    else {
        Write-Host "  Time      Module       Target                    Result" -ForegroundColor Cyan
        Write-Host "  ----      ------       ------                    ------" -ForegroundColor DarkGray
        foreach ($h in $Global:ScanHistory) {
            $mod = $h.Module.PadRight(12)
            $tgt = $h.Target.PadRight(25)
            Write-Host "  $($h.Time)  $mod $tgt $($h.Result)" -ForegroundColor Gray
        }
    }
}

# ================================================================================
# ENTRY POINT
# ================================================================================

Write-Banner

Write-Host "  ================================================================" -ForegroundColor Red
Write-Host "                       LEGAL DISCLAIMER" -ForegroundColor Red
Write-Host "  ================================================================" -ForegroundColor Red
Write-Host ""
Write-Host "  This tool is for EDUCATIONAL and LEGAL use ONLY." -ForegroundColor Yellow
Write-Host "  Only investigate targets you own or have written" -ForegroundColor Yellow
Write-Host "  permission to investigate." -ForegroundColor Yellow
Write-Host ""
Write-Host "  Violations may include:" -ForegroundColor DarkYellow
Write-Host "    - Computer Fraud and Abuse Act" -ForegroundColor DarkYellow
Write-Host "    - GDPR and Privacy Laws" -ForegroundColor DarkYellow
Write-Host "    - Local and Federal Laws" -ForegroundColor DarkYellow
Write-Host ""
Write-Host "  PRATAM is NOT responsible for misuse." -ForegroundColor Red
Write-Host ""
Write-Host "  ================================================================" -ForegroundColor Red
Write-Host ""
Write-Host "  Type 'I AGREE' to continue: " -NoNewline -ForegroundColor Yellow
$agreement = Read-Host

if ($agreement -ne "I AGREE") {
    Write-Host ""
    Write-Host "  [!] You must agree. Exiting..." -ForegroundColor Red
    Write-Host ""
    exit
}

Clear-Host
Write-Banner
Write-Log "OSINT Framework v$($Global:Config.Version) ready" "SUCCESS"
Write-Log "Made by PRATAM" "SUCCESS"

do {
    Show-MainMenu
    $choice = Read-Host
    $Global:Stats.TotalScans++

    switch ($choice.Trim()) {
        "1" {
            Write-Host "  Enter Username: " -NoNewline -ForegroundColor Yellow
            $u = Read-Host
            if ($u.Trim()) { Search-Username -Username $u.Trim() }
        }
        "2" {
            Write-Host "  Enter IP Address: " -NoNewline -ForegroundColor Yellow
            $ip = Read-Host
            if ($ip.Trim()) { Get-IPIntelligence -IPAddress $ip.Trim() }
        }
        "3" {
            Write-Host "  Enter Email: " -NoNewline -ForegroundColor Yellow
            $e = Read-Host
            if ($e.Trim()) { Get-EmailIntelligence -EmailAddress $e.Trim() }
        }
        "4" {
            Write-Host "  Enter Phone (with country code eg +1234567890): " -NoNewline -ForegroundColor Yellow
            $p = Read-Host
            if ($p.Trim()) { Get-PhoneIntelligence -PhoneNumber $p.Trim() }
        }
        "5" {
            Write-Host "  Enter Domain (eg google.com): " -NoNewline -ForegroundColor Yellow
            $d = Read-Host
            if ($d.Trim()) { Get-DomainIntelligence -Domain $d.Trim() }
        }
        "6" {
            Write-Host "  First Name: " -NoNewline -ForegroundColor Yellow
            $fn = Read-Host
            Write-Host "  Last Name: " -NoNewline -ForegroundColor Yellow
            $ln = Read-Host
            Write-Host "  Location (optional): " -NoNewline -ForegroundColor Yellow
            $loc = Read-Host
            Write-Host "  Age (optional): " -NoNewline -ForegroundColor Yellow
            $age = Read-Host
            if ($fn.Trim() -and $ln.Trim()) {
                Search-Person -FirstName $fn.Trim() -LastName $ln.Trim() -Location $loc.Trim() -Age $age.Trim()
            }
        }
        "7" {
            Write-Host "  Enter Target: " -NoNewline -ForegroundColor Yellow
            $t = Read-Host
            if ($t.Trim()) { Get-GoogleDorks -Target $t.Trim() }
        }
        "8" { Get-LocalNetworkInfo }
        "9" {
            Write-Host "  Enter Target (email/username): " -NoNewline -ForegroundColor Yellow
            $t = Read-Host
            if ($t.Trim()) { Search-Breaches -Target $t.Trim() }
        }
        "10" {
            Write-Host "  Enter Target (name/username): " -NoNewline -ForegroundColor Yellow
            $t = Read-Host
            if ($t.Trim()) { Search-SocialMedia -Target $t.Trim() }
        }
        "11" {
            Write-Section "FULL OSINT SCAN"
            Write-Host "  Username      : " -NoNewline; $u = Read-Host
            Write-Host "  IP Address    : " -NoNewline; $i = Read-Host
            Write-Host "  Email         : " -NoNewline; $e = Read-Host
            Write-Host "  Phone         : " -NoNewline; $p = Read-Host
            Write-Host "  Domain        : " -NoNewline; $d = Read-Host
            Write-Host "  First Name    : " -NoNewline; $fn = Read-Host
            Write-Host "  Last Name     : " -NoNewline; $ln = Read-Host
            Write-Host ""
            if ($u.Trim())  { Search-Username -Username $u.Trim() }
            if ($i.Trim())  { Get-IPIntelligence -IPAddress $i.Trim() }
            if ($e.Trim())  { Get-EmailIntelligence -EmailAddress $e.Trim() }
            if ($p.Trim())  { Get-PhoneIntelligence -PhoneNumber $p.Trim() }
            if ($d.Trim())  { Get-DomainIntelligence -Domain $d.Trim() }
            if ($fn.Trim() -and $ln.Trim()) { Search-Person -FirstName $fn.Trim() -LastName $ln.Trim() }
            Write-Log "Full scan complete!" "SUCCESS"
        }
        "12" { Show-Statistics }
        "13" { Show-ScanHistory }
        "14" { Start-Process explorer.exe $Global:Config.ReportsDir }
        "15" {
            Write-Host ""
            Write-Host "  ================================================================" -ForegroundColor Cyan
            Write-Host "          Thanks for using OSINT Framework!" -ForegroundColor Green
            Write-Host "                   Made by PRATAM" -ForegroundColor Yellow
            Write-Host "         Stay Legal. Stay Ethical. Stay Safe." -ForegroundColor White
            Write-Host "  ================================================================" -ForegroundColor Cyan
            Write-Host ""
            Write-Log "Session ended" "SUCCESS"
            exit
        }
        default { Write-Log "Invalid choice. Select 1-15." "WARN" }
    }

    Write-Host ""
    Write-Host "  Press ENTER to return to menu..." -ForegroundColor DarkGray
    Read-Host | Out-Null
    Clear-Host
    Write-Banner

} while ($true)

# ================================================================================
# END OF SCRIPT - MADE BY PRATAM
# 2000+ Lines Professional OSINT Framework v4.0
# ================================================================================
