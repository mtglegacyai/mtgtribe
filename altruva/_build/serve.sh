#!/bin/bash
p=$(cat /home/claude/site/srv.pid 2>/dev/null)
if [ -n "$p" ] && tr '\0' ' ' < /proc/$p/cmdline 2>/dev/null | grep -q "http.server 8765"; then kill $p; fi
cd /home/claude/site/out/prod && nohup python3 -m http.server 8765 >/dev/null 2>&1 &
echo $! > /home/claude/site/srv.pid
sleep 1
