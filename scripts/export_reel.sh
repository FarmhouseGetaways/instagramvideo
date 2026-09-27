#!/usr/bin/env bash
# Export any video as an Instagram-ready Reel (see knowledge/instagram-specs.md).
#
# Usage: scripts/export_reel.sh input.mov output.mp4 [crop|blur] [--mute]
#   crop (default): fill 9:16 by center-cropping
#   blur          : fit the whole frame, blurred copy fills the background
#   --mute        : drop audio (trending audio gets added in the Instagram app)
set -euo pipefail

in="$1"; out="$2"; mode="${3:-crop}"; mute="${4:-}"
[ "$mode" = "--mute" ] && { mode=crop; mute=--mute; }

# iPhone HDR (HLG/PQ) looks washed out on Instagram, so tone-map it to SDR
transfer=$(ffprobe -v error -select_streams v:0 -show_entries stream=color_transfer -of csv=p=0 "$in")
tonemap=""
if [[ "$transfer" == "arib-std-b67" || "$transfer" == "smpte2084" ]]; then
  tonemap="zscale=t=linear:npl=100,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,"
fi

if [ "$mode" = "blur" ]; then
  vf="${tonemap}split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5[bg];[b]scale=1080:1920:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2"
else
  vf="${tonemap}scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
fi
vf="${vf},fps=30,format=yuv420p,setsar=1"

if [ "$mute" = "--mute" ]; then
  audio=(-an)
else
  audio=(-af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k -ar 48000 -ac 2)
fi

ffmpeg -hide_banner -loglevel error -y -i "$in" -filter_complex "$vf" \
  -c:v libx264 -profile:v high -preset slow -crf 18 -maxrate 25M -bufsize 50M \
  -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  "${audio[@]}" -movflags +faststart "$out"

ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate:format=duration,size -of compact "$out"
