#!/usr/bin/env bash
# Make a copy of a finished video that fits the Claude app's 30 MB file limit (two-pass, highest bitrate that fits).
# Usage: scripts/fit_for_chat.sh input.mp4   → input_share.mp4
set -euo pipefail
in="$1"; out="${in%.mp4}_share.mp4"
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$in")
# 28 MiB budget minus 192k audio, capped at 20 Mbps
vk=$(python3 -c "print(min(20000, int((28*1024*1024*8/$dur - 192000)/1000)))")
cd "$(dirname "$in")"
ffmpeg -loglevel error -y -i "$(basename "$in")" -c:v libx264 -preset slow -b:v ${vk}k -pass 1 -an -f mp4 /dev/null
ffmpeg -loglevel error -y -i "$(basename "$in")" -c:v libx264 -preset slow -b:v ${vk}k -maxrate $((vk*3/2))k -bufsize $((vk*2))k \
  -pass 2 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -c:a copy -movflags +faststart "$(basename "$out")"
rm -f ffmpeg2pass-0.log ffmpeg2pass-0.log.mbtree
echo "$out ${vk}k $(du -m "$(basename "$out")" | cut -f1)MB"
