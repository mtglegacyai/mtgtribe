"""First-pass compliance scan for MTG's scripts, captions, titles and descriptions.

Flags phrases that platform fraud, scam, spam and gambling rules (and MTG's own rules) treat as risky, plus em and en
dashes. It is a helper, not a judge: every flag is read in context, and a clean scan still needs the human check in
references/compliance.md section 3.

Usage: python3 compliance_scan.py script.md [more files...]
Exit code 1 when something is flagged, so it can gate a build.
"""
import re
import sys

# (pattern, why it matters)
RULES = [
    (r'\bguarantee[ds]?\b|\bguaranteed\b', 'guaranteed returns or results (Meta, YouTube scams rules)'),
    (r'\brisk[- ]free\b|\bno risk\b|\bzero risk\b', 'risk-free claims (Meta prohibits)'),
    (r'\bdouble (?:your|my) (?:money|investment|deposit)\b|\bmoney flipping\b|\bflip (?:your|my) money\b', 'money doubling or flipping (Meta prohibits)'),
    (r'\bget rich\b|\bgetting rich\b|\brich quick\b|\bquick (?:money|cash|returns?|profits?)\b|\bfast (?:money|cash)\b', 'get-rich-quick wording (YouTube, Meta, TikTok)'),
    (r'\bpassive income\b|\bearn while you sleep\b|\bfinancial freedom in\b|\bquit your job\b', 'unrealistic reward for minimal effort (Meta)'),
    (r'\b\d+(?:[.,]\d+)?\s?%\s?(?:per|a|every)\s?(?:day|week|month)\b|\bdaily (?:returns?|profits?|income)\b', 'return rates (past or promised performance)'),
    (r'\bjoin my team\b|\bdownlines?\b|\brecruit(?:s|ing|ment)?\b|\bpeople (?:below|under) you\b|\bbuild your (?:team|network) and earn\b', 'recruitment pitch (Meta, TikTok MLM rules)'),
    (r'\bpartner plan\b|\bcompensation plan\b|\binfinity bonus\b|\bglobal pool\b|\blevel matching\b|\bglobal leg\b|\bworking levels?\b|\bmatrix\b', 'compensation plan detail: websites and tribe only'),
    (r'\blucky (?:tickets?|draws?)\b|\blotter(?:y|ies)\b|\bjackpot\b|\bcasino\b|\bbetting\b|\bgambl\w*', 'gambling or paid draws (YouTube, TikTok)'),
    (r'\bmy (?:earnings|profits?|withdrawals?)\b|\bi (?:made|earned|withdrew)\b|\bproof of (?:payment|earnings|withdrawal)\b', 'earnings or withdrawal proof claims'),
    (r'\bsubscribe (?:and|to) win\b|\bgiveaway\b|\bfree (?:money|crypto|usdt|bitcoin)\b|\bsub for sub\b', 'rewarding engagement or free money bait (YouTube spam)'),
    (r'\bcomment yes\b|\btype yes\b|\blike if\b|\bshare if\b', 'engagement bait (Facebook demotes)'),
    (r'\byou should (?:buy|sell|invest)\b|\bbuy (?:it|this) now\b|\bput (?:all )?your (?:money|savings)\b', 'personal financial advice (FAIS) or pressure'),
    (r'\bdownliners?\b|\bdemo\b', "MTG's wording rule (business partners; training)"),
    (r'[\u2013\u2014]', 'em or en dash (MTG rule: never use them)'),
]


def scan(path):
    flags = 0
    with open(path, encoding='utf-8') as f:
        for n, line in enumerate(f, 1):
            for pattern, why in RULES:
                for m in re.finditer(pattern, line, re.I):
                    flags += 1
                    print(f'{path}:{n}: "{m.group(0)}" ({why})\n    {line.strip()[:160]}')
    return flags


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    total = sum(scan(p) for p in sys.argv[1:])
    if total:
        print(f'\n{total} flag(s). Read each in context: fix it, or note why it is fine (for example a scam-awareness video).')
        sys.exit(1)
    print('No flags. Now do the human check in references/compliance.md section 3.')


if __name__ == '__main__':
    main()
