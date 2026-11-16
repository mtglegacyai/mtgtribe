import html
# JetUP live on Zoom: the weekly schedule of JetUP's Zoom sessions, in the JetUP guide at /jetup/zoom/ (MTG, 16 Nov 2026).
# The sessions are JetUP's (organizer JetUP); MTG shares the Zoom link in the MTG TRIBE WhatsApp group and visitors can
# message him for it. Never write that MTG hosts them. Page CSS: /jetup/assets/zoom-live.css. Page script (the tested
# schedule maths, countdown, calendar dates, time zones): /jetup/assets/zoom-live.js.
from layout import *

PATH = '/jetup/zoom/'
ICS = PATH + 'jetup-live-zoom-schedule.ics'
# MTG's exact words (16 Nov 2026), so he knows the visitor came from the JetUP Zoom page and wants the link
WA_ZOOM_TEXT = 'Hi MTG,\n\nPlease send me the Zoom link for your next JetUp session.\n\nThank you 😊'
WA_ZOOM = WA_MTG + '?text=Hi%20MTG%2C%0A%0APlease%20send%20me%20the%20Zoom%20link%20for%20your%20next%20JetUp%20session.%0A%0AThank%20you%20%F0%9F%98%8A'

# The five weekly sessions, South African time. data-s matches S[] in zoom-live.js.
# (index, weekday, kind, emoji, name, SA time, Nigeria, UK, Canada and US East, Australia, Australia day)
SESSIONS = [
 (0, 'Tuesday', 'pres', '📣', 'Presentation', '8pm', '7pm', '6pm', '1pm', '5am', 'Wed'),
 (1, 'Thursday', 'pres', '📣', 'Presentation', '8pm', '7pm', '6pm', '1pm', '5am', 'Fri'),
 (2, 'Saturday', 'pres', '📣', 'Presentation', '8pm', '7pm', '6pm', '1pm', '5am', 'Sun'),
 (3, 'Sunday', 'intl', '🌍', 'International presentation', '3pm', '2pm', '1pm', '8am', '12 midnight', 'Mon'),
 (4, 'Sunday', 'train', '🎓', 'Training night', '8pm', '7pm', '6pm', '1pm', '5am', 'Mon'),
]
ZONES = [('South Africa (SAST)', 'Africa/Johannesburg'), ('Nigeria (Lagos)', 'Africa/Lagos'), ('United Kingdom (London)', 'Europe/London'),
         ('Canada and US East (Toronto, New York)', 'America/Toronto'), ('Australia (Sydney)', 'Australia/Sydney')]

FAQ_LIVE = [
 ('How do I get the Zoom link?',
  f'The Zoom link is shared in the MTG TRIBE WhatsApp group. <a href="{GROUP}">Join the group</a>, or <a href="{WA_ZOOM}" data-wa-text="{html.escape(WA_ZOOM_TEXT)}" target="_blank" rel="noopener">message MTG directly on WhatsApp<span class="sr"> (opens in a new tab)</span></a> and ask him for the link.'),
 ('What time is it where I live?',
  'Every time on this page is South African time (SAST, UTC+2, no daylight saving). The <a href="#timezones">time zone table</a> shows Nigeria, the United Kingdom, Canada and US East and Australia, plus a Your time column worked out from your own device.'),
 ('Can I join from my phone?',
  'Yes. Zoom works on phones, tablets and computers. Install the Zoom app on your phone, then tap the link when it is shared in the group.'),
 ('Who can attend the training night?',
  'Sunday 8pm is the back office training night, for members. If you are not sure whether it is for you, ask in the MTG TRIBE WhatsApp group.'),
]

def _ld():
    u = SITE + PATH
    img = SITE + '/assets/og/jetup-live.jpg'
    org = {"@type": "Organization", "name": "JetUP", "url": "https://jet-up.ai/"}
    note = 'The Zoom link is shared in the MTG TRIBE WhatsApp group.'
    def event(i, name, desc, start, end, sched):
        return {"@type": "Event", "@id": u + '#' + i, "name": name, "description": desc + ' ' + note, "url": u, "image": img,
                "startDate": start, "endDate": end, "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
                "eventStatus": "https://schema.org/EventScheduled", "location": {"@type": "VirtualLocation", "url": u},
                "organizer": org, "superEvent": {"@id": u + '#series'}, "eventSchedule": sched}
    def sched(start, days, t0, t1):
        return {"@type": "Schedule", "startDate": start, "repeatFrequency": "P1W", "byDay": days, "startTime": t0, "endTime": t1,
                "duration": "PT1H", "scheduleTimezone": "Africa/Johannesburg"}
    return [
     {"@type": "Organization", "@id": SITE + "/#tribe", "name": "MTG TRIBE", "url": SITE + "/", "logo": SITE + "/assets/icon-512.png",
      "sameAs": [YT, TT, TG, FB]},
     {"@type": "EventSeries", "@id": u + "#series", "name": "JetUP live Zoom sessions",
      "description": "Five live JetUP Zoom sessions every week, in South African time. " + note, "url": u, "image": img,
      "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode", "eventStatus": "https://schema.org/EventScheduled",
      "startDate": "2026-11-17T20:00:00+02:00", "location": {"@type": "VirtualLocation", "url": u}, "organizer": org,
      "subEvent": [{"@id": u + "#presentation"}, {"@id": u + "#international"}, {"@id": u + "#training"}]},
     event('presentation', 'JetUP Presentation on Zoom', 'Live JetUP presentation on Zoom, every Tuesday, Thursday and Saturday at 8pm South African time.',
           '2026-11-17T20:00:00+02:00', '2026-11-17T21:00:00+02:00',
           sched('2026-11-17', ["https://schema.org/Tuesday", "https://schema.org/Thursday", "https://schema.org/Saturday"], '20:00:00', '21:00:00')),
     event('international', 'JetUP International Presentation on Zoom', 'Live JetUP international presentation on Zoom, every Sunday at 3pm South African time.',
           '2026-11-22T15:00:00+02:00', '2026-11-22T16:00:00+02:00', sched('2026-11-22', "https://schema.org/Sunday", '15:00:00', '16:00:00')),
     event('training', 'JetUP Training Night on Zoom (back office training)', 'The JetUP back office training night on Zoom, every Sunday at 8pm South African time.',
           '2026-11-22T20:00:00+02:00', '2026-11-22T21:00:00+02:00', sched('2026-11-22', "https://schema.org/Sunday", '20:00:00', '21:00:00')),
     {"@type": "FAQPage", "@id": u + "#faq", "mainEntity": [
      {"@type": "Question", "name": "How do I get the Zoom link?", "acceptedAnswer": {"@type": "Answer", "text": "The Zoom link is shared in the MTG TRIBE WhatsApp group. Join the group at mtgtribe.com/group, or message MTG directly on WhatsApp and ask him for the link."}},
      {"@type": "Question", "name": "What time is it where I live?", "acceptedAnswer": {"@type": "Answer", "text": "Every time on this page is South African time (SAST, UTC+2, no daylight saving). The time zone table shows Nigeria, the United Kingdom, Canada and US East and Australia, and a Your time column worked out from your own device."}},
      {"@type": "Question", "name": "Can I join from my phone?", "acceptedAnswer": {"@type": "Answer", "text": "Yes. Zoom works on phones, tablets and computers. Install the Zoom app on your phone, then tap the link when it is shared in the group."}},
      {"@type": "Question", "name": "Who can attend the training night?", "acceptedAnswer": {"@type": "Answer", "text": "Sunday 8pm is the back office training night, for members. If you are not sure whether it is for you, ask in the MTG TRIBE WhatsApp group."}}]},
    ]

CLOCK = '''<svg class="clock" viewBox="0 0 100 100" aria-hidden="true" focusable="false">
      <defs><linearGradient id="lv-cg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4ffd9"/><stop offset=".45" stop-color="#cbfb61"/><stop offset="1" stop-color="#7fae12"/></linearGradient>
      <radialGradient id="lv-cf" cx=".4" cy=".35" r=".8"><stop offset="0" stop-color="#3a2b75"/><stop offset="1" stop-color="#120d26"/></radialGradient></defs>
      <circle cx="50" cy="50" r="47" fill="url(#lv-cg)"/><circle cx="50" cy="50" r="40" fill="url(#lv-cf)"/>
      <g stroke="#cbfb61" stroke-width="3" stroke-linecap="round"><path d="M50 14v6M50 80v6M14 50h6M80 50h6"/></g>
      <g stroke="#cbfb61" stroke-opacity=".55" stroke-width="2" stroke-linecap="round"><path d="M68 18.8l-2 3.5M81.2 32l-3.5 2M81.2 68l-3.5-2M68 81.2l-2-3.5M32 81.2l2-3.5M18.8 68l3.5-2M18.8 32l3.5 2M32 18.8l2 3.5"/></g>
      <path d="M50 50L31 61" stroke="#fff" stroke-width="5" stroke-linecap="round"/><path d="M50 50V22" stroke="url(#lv-cg)" stroke-width="3.5" stroke-linecap="round"/>
      <circle cx="50" cy="50" r="4.5" fill="#cbfb61"/>
     </svg>'''

def _calendar():
    def ev(s):
        i, day, kind, emo, name = s[:5]
        return (f'<div class="ev {kind}" data-s="{i}"><span class="tm">{s[5]} <small>SAST</small></span>'
                f'<span class="nm"><span class="e" aria-hidden="true">{emo}</span>{name}</span><span class="yt"></span></div>')
    days = []
    for dow, short, full in [(1, 'Mon', 'Monday'), (2, 'Tue', 'Tuesday'), (3, 'Wed', 'Wednesday'), (4, 'Thu', 'Thursday'),
                             (5, 'Fri', 'Friday'), (6, 'Sat', 'Saturday'), (0, 'Sun', 'Sunday')]:
        evs = [s for s in SESSIONS if s[1] == full]
        inner = ''.join(ev(s) for s in evs) if evs else '<p class="none">No live session</p>'
        days.append(f'<div class="day{"" if evs else " quiet"}" role="listitem" data-dow="{dow}"><div class="dh"><span class="dn">{short}</span>'
                    f'<span class="dt"></span><span class="tdy">Today</span></div><div class="evs">{inner}</div></div>')
    return '\n     '.join(days)

def _tz_rows():
    rows = []
    for s in SESSIONS:
        i, day, kind, emo, name = s[:5]
        times = s[5:10]
        cells = []
        for k, ((label, tz), t) in enumerate(zip(ZONES, times)):
            cls = ' class="sa"' if k == 0 else ''
            dy = f'<span class="dy">{s[10]}</span>' if k == 4 else ''
            cells.append(f'<td{cls} data-label="{label}" data-tz="{tz}"><span class="tt">{t}</span>{dy}</td>')
        cells.append('<td class="you js-only" data-label="Your time" data-tz="local"><span class="tt"></span></td>')
        sub = name + (' (back office training)' if i == 4 else '')
        rows.append(f'<tr data-s="{i}"><th scope="row">{day}<small>{sub}</small></th>\n      ' + '\n      '.join(cells) + '</tr>')
    return '\n     '.join(rows)

def build_live():
    path = PATH
    crumbs_vis = [('MTG TRIBE', '/'), ('JetUP Guide', '/jetup/'), ('Live on Zoom', None)]
    faq_html = ''.join('<details><summary>%s</summary><p>%s</p></details>' % qa for qa in FAQ_LIVE)
    rings = '<i></i>' * 10
    main = f'''
<section class="phead lv lv-hero" aria-labelledby="lv-h1"><div class="wrap lv-hcq">
 {crumbs(crumbs_vis)}
 <div class="lv-hgrid">
  <div>
   <div class="lv-emos" aria-hidden="true"><span>📣</span><span>🕗</span></div>
   <p class="eyebrow">Live on Zoom · 5 sessions a week</p>
   <h1 id="lv-h1">JetUP live <span class="grad">on Zoom</span></h1>
   <p class="lede">Five live sessions every week: three presentations, an international presentation and a training night. Pick your session, then get the Zoom link on WhatsApp.</p>
   <p class="lv-tz">{icon('i-clock2')}All times are South African time (SAST, UTC+2)</p>
   <div class="ctas">
    <a class="btn btn-pri" href="#link">{icon('i-whatsapp')}Get the Zoom link</a>
    <a class="btn btn-ghost" href="#calendar">{icon('i-down')}See the calendar</a>
   </div>
  </div>
  <div class="card glass nxcard rv" id="next" aria-labelledby="next-h">
   <p class="nx-lab"><span class="dot" aria-hidden="true"></span><span id="nx-lab">Next live session</span></p>
   <h2 id="next-h"><span id="nx-name" class="grad">Every week on Zoom</span></h2>
   <p class="nx-when" id="nx-when">Tuesday, Thursday and Saturday at 8pm. Sunday at 3pm (international) and 8pm (training night). South African time.</p>
   <p class="cd js-only" id="nx-cd" role="timer" aria-label="Time until the session starts">
    <span class="cdu"><b id="cd-d">0</b><span>Days</span></span>
    <span class="cdu"><b id="cd-h">0</b><span>Hours</span></span>
    <span class="cdu"><b id="cd-m">0</b><span>Minutes</span></span>
   </p>
   <p class="nx-local js-only" id="nx-local"></p>
   <p class="nx-after js-only" id="nx-after"></p>
   <a class="btn btn-lime" href="#link">{icon('i-whatsapp')}Get the Zoom link</a>
  </div>
 </div>
</div></section>

<section class="sec tight lv" id="calendar" aria-labelledby="cal-h">
 <div class="wrap lv-calq">
  <div class="shead"><p class="eyebrow rv">The weekly calendar</p><h2 class="h2 rv" style="--d:1" id="cal-h">Five sessions. <span class="grad">Every week.</span></h2></div>
  <div class="cal-wrap rv">
   <div class="cal">
    <div class="rings" aria-hidden="true">{rings}</div>
    <div class="band">
     <div class="ttl">
      <p class="kick">JetUP · Live on Zoom</p>
      <p class="bt">Weekly Zoom <span class="lime">calendar</span></p>
      <p class="tzl">South African time (SAST, UTC+2)<span id="cal-week"></span></p>
     </div>
     {CLOCK}
    </div>
    <div class="days" role="list">
     {_calendar()}
    </div>
    <div class="cal-foot">
     <div class="legend"><span><i></i>Presentation</span><span><i class="intl"></i>International presentation</span><span><i class="train"></i>Training night (back office training)</span></div>
     <span>Zoom link: in the WhatsApp group</span>
    </div>
   </div>
  </div>
 </div>
</section>

<section class="sec tight lv" id="timezones" aria-labelledby="tz-h">
 <span class="seam" aria-hidden="true"></span>
 <div class="wrap lv-tzq">
  <div class="shead"><p class="eyebrow rv">Time zones</p><h2 class="h2 rv" style="--d:1" id="tz-h">What time is that <span class="grad">where you are?</span></h2>
   <p class="lede rv" style="--d:2">The same five sessions in the tribe's biggest time zones. Daylight saving is taken care of: the times follow the clocks in each country.</p></div>
  <div class="card tzcard rv">
   <table class="tzt own-cards">
    <caption class="sr">Each JetUP Zoom session in South African time and in other time zones</caption>
    <thead><tr>
     <th scope="col">Session</th>
     <th scope="col" class="sa">South Africa<small>SAST, <span class="off" data-tz="Africa/Johannesburg">UTC+2</span></small></th>
     <th scope="col">Nigeria<small>Lagos, <span class="off" data-tz="Africa/Lagos">UTC+1</span></small></th>
     <th scope="col">United Kingdom<small>London, <span class="off" data-tz="Europe/London">UTC+0</span></small></th>
     <th scope="col">Canada and US East<small>Toronto, New York, <span class="off" data-tz="America/Toronto">UTC-5</span></small></th>
     <th scope="col">Australia<small>Sydney, <span class="off" data-tz="Australia/Sydney">UTC+11</span></small></th>
     <th scope="col" class="you js-only">Your time<small id="you-zone">your device</small></th>
    </tr></thead>
    <tbody>
     {_tz_rows()}
    </tbody>
   </table>
  </div>
  <p class="tznote">A day tag (like <span class="dy">Wed</span>) means the session falls on a different day there. Somewhere else? Your own time is worked out for you above, or use any time zone converter.</p>
 </div>
</section>

<section class="sec tight lv" id="link" aria-labelledby="link-h">
 <span class="seam" aria-hidden="true"></span>
 <div class="wrap lv-wq">
  <div class="shead"><p class="eyebrow rv">How to get the Zoom link</p><h2 class="h2 rv" style="--d:1" id="link-h">The link lives on <span class="lime">WhatsApp</span></h2>
   <p class="lede rv" style="--d:2">MTG shares the Zoom link for the sessions in the MTG TRIBE WhatsApp group. Choose the way that suits you: join the group, or ask MTG for the link in a private chat.</p></div>
  <div class="ways">
   <div class="card pad way rv">
    <p class="eyebrow num">Way 1 · The group</p>
    <h3>Join the MTG TRIBE group</h3>
    <a class="btn btn-lime" href="{GROUP}">{icon('i-whatsapp')}Join the WhatsApp group</a>
    <p class="what">Opens WhatsApp and joins the MTG TRIBE group, where the Zoom link for every session is posted.</p>
   </div>
   <div class="card pad way rv" style="--d:1">
    <p class="eyebrow num">Way 2 · One on one</p>
    <h3>Ask MTG directly</h3>
    <a class="btn btn-ghost" href="{WA_ZOOM}" data-wa-text="{html.escape(WA_ZOOM_TEXT)}" target="_blank" rel="noopener">{icon('i-msg')}Message MTG on WhatsApp<span class="sr"> (opens in a new tab)</span></a>
    <p class="what">Opens a private WhatsApp chat with MTG, one on one, if you prefer not to join a group.</p>
   </div>
  </div>
 </div>
</section>

<section class="sec tight lv" id="add" aria-labelledby="add-h">
 <div class="wrap lv-aq">
  <div class="card glass pad addcal rv">
   <span class="big" aria-hidden="true">🗓️</span>
   <div>
    <h2 id="add-h">Add the schedule to <span class="lime">your calendar</span></h2>
    <p>Five weekly reminders, set in South African time, so your phone or computer shows each one in your own time. No Zoom link inside: the link is shared in the WhatsApp group.</p>
   </div>
   <a class="btn btn-pri" href="{ICS}" download="jetup-live-zoom-schedule.ics">{icon('i-calplus')}Add to my calendar</a>
  </div>
 </div>
</section>

<section class="sec tight lv" id="faq" aria-labelledby="faq-h">
 <div class="narrow">
  <div class="shead"><p class="eyebrow rv">Questions</p><h2 class="h2 rv" style="--d:1" id="faq-h">Good to <span class="grad">know</span></h2></div>
  <div class="faq">{faq_html}</div>
 </div>
</section>
{join_cta()}'''
    head = '\n<link rel="stylesheet" href="/jetup/assets/zoom-live.css?v=%s">' % ver('/jetup/assets/zoom-live.css')
    foot = '\n<script src="/jetup/assets/zoom-live.js?v=%s" defer></script>' % ver('/jetup/assets/zoom-live.js')
    return page(path, 'JetUP Live on Zoom: Presentations & Training Schedule | MTG',
                'JetUP live on Zoom, five sessions a week: presentations Tuesday, Thursday and Saturday at 8pm, a Sunday 3pm international presentation and a Sunday 8pm training night (SA time).',
                main, [('MTG TRIBE', '/'), ('JetUP Guide', '/jetup/'), ('Live on Zoom', path)], _ld(),
                keywords='JetUP Zoom, JetUP live, JetUP presentation, JetUP training, JetUP Zoom schedule, JetUP Zoom link, JetUP SA time, TAG Markets, MTG TRIBE',
                head_extra=head, foot_extra=foot)
