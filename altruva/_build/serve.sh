#!/bin/bash
kill $(cat /home/claude/site/srv.pid) 2>/dev/null
cd /home/claude/site/out/prod && nohup python3 -m http.server 8765 >/dev/null 2>&1 &
echo $! > /home/claude/site/srv.pid
sleep 1
