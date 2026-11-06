# Build every page of the JetUP and TAG Markets guide (Python 3.12 or newer).
#   python3 jetup/_build/build.py
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from pages_home import build_home
from pages_start import build_start
from pages_learn import build_checks, build_how, build_plan, build_promo, build_bix
from pages_tools import build_exposure, build_split, build_videos, build_downloads, build_faq, build_disclaimer

if __name__ == '__main__':
    for fn in (build_home, build_start, build_checks, build_how, build_plan, build_promo, build_bix,
               build_exposure, build_split, build_videos, build_downloads, build_faq, build_disclaimer):
        out = fn()
        print('wrote', os.path.relpath(out, os.path.join(os.path.dirname(__file__), '..', '..')), os.path.getsize(out), 'bytes')
