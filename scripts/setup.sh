#!/usr/bin/env bash
# Installs the video toolkit in a fresh cloud container. Safe to re-run.
set -e
if ! command -v ffmpeg >/dev/null; then
  (apt-get update -qq && apt-get install -y -qq ffmpeg) >/dev/null 2>&1 || echo "ffmpeg install failed" >&2
fi
python3 -c "import whisper" 2>/dev/null || pip install -q openai-whisper >/dev/null 2>&1 || echo "whisper install failed" >&2
exit 0
