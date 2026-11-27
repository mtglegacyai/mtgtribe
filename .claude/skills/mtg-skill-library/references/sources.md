# Sources: every video MTG sent and every project it led to

Newest entry at the bottom. Each entry: the video, its corrected transcript, each upstream project (owner/repo, licence,
the exact version read), the verdict, the caveats, and where it now lives in the library.

## Deeper reading, by job

When a library file is not enough, clone the upstream repo read-only (SKILL.md, intake step 4) and read only this part.

| Job | Upstream (repo at the version we checked) |
|---|---|
| SEO audit, technical SEO | `coreyhaines31/marketingskills` skills/seo-audit |
| Structured data | marketingskills skills/schema |
| Many pages from one template (watch pages, glossary) | marketingskills skills/programmatic-seo |
| AI search in depth (prompts to track, accuracy of AI answers) | marketingskills skills/ai-seo/references |
| Page copy, line edits | marketingskills skills/copywriting, skills/copy-editing |
| Conversion review of a page or form | marketingskills skills/cro |
| Offers, bonuses, honest urgency | marketingskills skills/offers (references/scarcity-urgency.md) |
| Ads (hooks, angles, platform specs, awareness stages) | marketingskills skills/ad-creative (references/hook-system.md, awareness-headlines.md) |
| Social posts and repurposing | marketingskills skills/social (references/post-templates.md) |
| WhatsApp, SMS | marketingskills skills/sms (references/whatsapp.md) |
| Email sequences | marketingskills skills/emails |
| Referral and affiliate programmes | marketingskills skills/referrals |
| PDF guides as lead magnets | marketingskills skills/lead-magnets |
| Calculators and free tools as marketing | marketingskills skills/free-tools |
| Launches, events, webinars | marketingskills skills/launch, skills/events |
| Persuasion, and whether a tactic is honest | marketingskills skills/marketing-psychology |
| Design critique, audit, polish | `pbakaus/impeccable` plugin/skills/impeccable/reference (critique-rubric.md, audit.md, polish.md, craft-floor.md) |
| Long explainer visuals | `nateherkai/herk-edit-kit` .claude/skills/video-storytelling |
| Reels and shorts editing | herk-edit-kit .claude/skills/short-form-edit, docs/EDITING-PLAYBOOK.md |
| HTML-to-video, motion blocks | `heygen-com/hyperframes` skills/hyperframes, registry/ |
| Product-shot and image-style ideas | `bhaiyasingh45/chatgpt-slash-image-commands` README (ideas only, no licence file); our recipes: `shot-library.md` |

## #001: "5 Claude skills to get ahead of 99%" (sent 25 Nov 2026)

**The video:** vertical reel, 59 s, 720 x 1280. A presenter talks to camera; each item gets a title card and its GitHub
page or demo on screen; ends with "comment SKILL". Transcribed with faster-whisper medium.en; names corrected from the
screen.

**Transcript:**

> Here are 5 Claude skills you need to install right now to get ahead of 99% of people. So first, make sure to save this
> video so you can come back to the one you need. Number 1 is HyperFrames. If you've been seeing those viral animations,
> you can make them using this skill. It edits your videos, adds motion graphics and captions for you. Number 2 is Stop
> Slop. This one gets rid of every sign of AI writing, so your text actually sounds like a real human wrote it. Number 3
> is Marketing Skills. If you run a business and you need solid marketing, you need to get this skill. It has over 50
> marketing skills for copywriting, ads, emails, SEO and landing pages, and it lets Claude act like a whole marketing team
> for you. Number 4 is the Herk Edit Kit. If you film talking head videos, you need this one. It cuts every pause and
> mistakes so you sound natural in all of your videos. And number 5 is Impeccable Skill. This one teaches Claude to
> design like a professional designer for your websites, your flyers, your posters, your landing pages, so your design
> actually looks premium. Share this with someone who needs it, and if you comment the word SKILL, I'll send you the
> links plus a guide on how to set them up.

**The projects** (all read from source on 25 and 26 Nov 2026; none installed or run):

| Project | Repo, licence, version read | What it really is | Verdict for MTG | Lives in |
|---|---|---|---|---|
| Impeccable (Paul Bakaus) | `pbakaus/impeccable`, Apache 2.0, b49177d32788 (18 Nov 2026), v4.10.0 | Design direction for agents: 24 commands (critique, audit, polish, bolder ...), a quality floor, modes, a 62-rule checker with no AI | **High** | `design-review.md` |
| HyperFrames (HeyGen) | `heygen-com/hyperframes`, Apache 2.0, cb9dfa8f0c9e (25 Nov 2026), CLI 0.9.92 | HTML to MP4 for agents; about 470 registry blocks; skills incl. reverse-any-video, media-use | **Medium to high** (our engine already works this way) | `video-story.md` |
| Marketing Skills (Corey Haines) | `coreyhaines31/marketingskills`, MIT, 8fd2fcade2fd (23 Nov 2026) | 53 marketing playbooks, mostly for software companies; about 15 fit MTG | **Medium**, selectively | `conversion-copy.md`, `ai-search.md`, the table above |
| Stop Slop (Hardik Pandya) | `hardikpandya/stop-slop`, MIT, 8da1f030185b (18 Mar 2026) | One-page rulebook against AI-sounding prose | **Medium, adapted** (several rules clash with MTG's teaching style) | `voice-pass.md` |
| Herk Edit Kit (Nate Herk) | `nateherkai/herk-edit-kit`, MIT, 10511e5af86f (14 Oct 2026) | 15 skills for editing talking-head footage, built on HyperFrames; optional paid ElevenLabs and Kie.ai | **Low now** (MTG records his screen silently); its storytelling rules are gold | `video-story.md` |

**Caveats found (not in the video):**

- Impeccable's live mode, when no chat is connected, starts an agent with permission checks turned off. Keep it off.
  Its checker downloads a binary on first run. Running it was blocked on 25 Nov 2026 until MTG approves outside code.
- HyperFrames can make HeyGen voiceovers: V3 only, credits only with MTG's OK.
- Stop Slop's own example contains an em dash; several of its rules (skip hand-holding, two items beat three, no "How"
  starts) would hurt MTG's beginner-friendly teaching and search headings.
- Marketing Skills' text uses em dashes throughout and SaaS framing; MTG's rules override. Its offers playbook warns
  that gold logos with "secret method" copy and fake urgency look like a scam: a useful check for MTG's crypto niche.
- A scan of 111 site pages (25 Nov 2026) for Stop Slop's main patterns found about 29 matches in all, so the site copy
  is already fairly clean; the voice pass matters most for scripts, captions, posts and prospect messages.
- The video's "ahead of 99% of people" is hype, not evidence.

**Tests run with MTG's OK (26 Nov 2026):**

- Impeccable 4.10.0 checker on four main pages, file scan then rendered at 360 px and 1280 px: about 195 findings per
  width, mostly style flags; the real readability issues are listed in `design-review.md`. Needed a Chromium wrapper
  with `--no-sandbox` (the container runs as root).
- HyperFrames 0.9.92: a silent 13.5 s vertical ClickBaitPays hook with two registry blocks (`headline-slam`,
  `cta-lockup`) edited for vertical; its checker passed after fixes; rendered in 41 s. Project kept in
  `tools/hyperframes/cbp-hook-test/`. Telemetry off, nothing published.

## #002: "Type this, get this" AI product-shot reel (sent 27 Nov 2026)

**The video:** vertical reel, 33.5 s, 720 x 1280. A presenter at a desk raises a finger as a "slash command" appears on
screen, then an AI product shot plays. Seven commands: `/bullettime` (earbuds), `/gravitydefy` (a gold watch with
ribbons), `/explodedview` (a phone coming apart), `/orbit_sweep` (headphones), `/softsunbeam` (a hair-oil bottle in a
forest), `/splashfreeze` (earbuds, then perfume), `/3dblueprint` (a sneaker drawn as a wireframe). It ends with "Comment
Anything" and "DM" on screen. Google's visible sparkle watermark sits in the corner of the product shots and of some
presenter shots, so the shots were made with Google's Gemini, Veo or Flow (the presenter may be AI-made too). No tool or
source is named. Transcribed with faster-whisper medium.en; the ending re-transcribed with filtering.

**Transcript:**

> Type this, get this. Type this, get this. [repeated over the seven commands] Type this, and get this. If you want to
> see more of our next level products [partly unclear] ... 100 plus slash commands. Comment anything ... [on screen:
> "Comment Anything", "DM"]

**What it really is:** none of these is a feature of ChatGPT, Gemini or Flow. They are shorthand words from "100+
commands" lists sold or given away as lead magnets; a model reads them as plain text, so results vary.

| Source (read 27 Nov 2026) | What it says | Use |
|---|---|---|
| `bhaiyasingh45/chatgpt-slash-image-commands` at bd2c8e6 (15 Nov 2026), no licence file ("educational and creative use") | "These are not official ChatGPT slash commands. They are shorthand prompt patterns"; for reliable results "describe exactly what you want" | Ideas only, nothing copied |
| Slash Image Commander (slashimagecommander.com, Hampton Network LLC, $47, 30 commands), sales page only | "These are prompt shortcuts, not features baked into ChatGPT"; motion prompts are run "through a video generator such as Sora, Veo, Kling or Runway" | Not bought |
| weboptech, "99 Google Flow prompts and commands" | The slash notation is "creative shorthand", not an official Flow command language; Flow's guidance: describe subject, action, environment, lighting and style in detail | Confirms the method |
| GitHub issue `candidmarketingltd-art/ai-news-reels#1`, "FAKE SLASH COMMANDS" | "They're just plain text"; save your own shortcut in Custom Instructions or a Project | The idea we kept |
| Google's visible watermark (BGR, TechRepublic) | A sparkle at the bottom right of Gemini, Veo and Flow media; optional since Nov 2026 (Settings > Media Watermark); the invisible SynthID mark stays | Identified the tool |

**Verdict:** the claim is hype; the idea underneath is useful. **Medium** overall, **high** for two looks that fit MTG
exactly: `/blueprint` (his brand, "Your Digital Architect") and `/explodedview` (his "show the idea" rule). Kept as his
own named looks with full recipes, free to render in our three.js engine: `shot-library.md`.

**Caveats:** the reel shows other companies' products; realistic AI presenters need the platforms' AI labels; the
comment-to-DM ending again needs a real reward and the compliance gate; never remove a watermark.

