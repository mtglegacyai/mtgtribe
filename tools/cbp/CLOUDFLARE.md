# ClickBaitPays on Cloudflare (set up with MTG on 22 Nov 2026)

ClickBaitPays has its own Cloudflare account, separate from Bellver and Bitcoin Wealth (MTG: so the videos play from his
own storage, not YouTube: "if YouTube decides that they're gonna take down my channel, then that will be a problem").

| Part | Value |
|---|---|
| Account | MTG's third Cloudflare account (its own email, created 22 Nov 2026). His Bellver login is a member (Super Administrator), so the API token saved on his Default cloud environment (host api.cloudflare.com) reaches it |
| Domain | clickbaitpaysus.com, Free plan, active since 22 Nov 2026 about 15:43 UTC. Registrar GoDaddy; nameservers aryanna.ns.cloudflare.com and henrik.ns.cloudflare.com (undo: GoDaddy > domain > DNS > Nameservers > GoDaddy Nameservers) |
| DNS | The 10 GoDaddy records, copied and checked one by one: 4 A records to GitHub Pages (185.199.108 to 111.153), www CNAME, MX 0 smtp.secureserver.net and MX 10 mailstore1.secureserver.net (GoDaddy email), SPF and DMARC TXT, _domainconnect CNAME. All **DNS only** (grey cloud): the website runs straight from GitHub Pages with its own certificate |
| R2 bucket | `clickbaitpays-media`, Western Europe (closest to South Africa), Standard |
| Video address | https://media.clickbaitpaysus.com/ (R2 custom domain, TLS 1.2+, serving since 22 Nov 2026). Files go under `videos/` |

How a video goes up (same as Bitcoin Wealth, `bw/_build/build/r2.py`): MTG shares the file from Google Drive; download
it, make a 720p file for phones and a `-1080p` file for screens 1200 px and wider, upload both to
`clickbaitpays-media/videos/`, check size and MD5 against the bucket, then point the video's entry in `V`
(`cbp/_build/build.py`) at it with `src` instead of `yt`, rebuild, run the checks, and publish. The address of a bare
bucket shows "Object not found": normal, it is a storage shelf, not a website.

Open items:
- `https://www.clickbaitpaysus.com` failed with a certificate error, as it did before the move: the www record pointed to
  clickbaitpaysus.com instead of musathegiant.github.io, so GitHub Pages never made a certificate for www (http://www
  redirected fine). MTG said "yes, fix www" (22 Nov 2026): www CNAME now points to musathegiant.github.io, DNS only (as
  bitcoinwealthpays.com). GitHub issues the www certificate on its own; if it still fails after a day, remove and re-add
  the custom domain in the repo's Settings > Pages to trigger it.
- `videos/_test.mp4` (2 seconds, 30 KB) is the setup test; remove it once the first real video is up.
