#!/bin/bash

# Configuration
INPUT_FILE="${1:-input.mp4}"
OUTPUT_FILE="${2:-output.mp4}"

# Timestamps for video segments (format: start-end in HH:MM:SS-HH:MM:SS)
# Edit these arrays to configure which segments to extract
SEGMENTS=(
    "00:02:13-00:02:43"
    "00:06:13-00:06:43"
    "00:11:18-00:12:14"
    "00:22:08-00:23:08"
)

# Validate input file
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' not found"
    echo "Usage: $0 [input_file] [output_file]"
    exit 1
fi

# Build filter_complex string dynamically
FILTER=""
CONCAT_INPUTS=""
SEGMENT_COUNT=${#SEGMENTS[@]}

for i in "${!SEGMENTS[@]}"; do
    IFS='-' read -r START END <<< "${SEGMENTS[$i]}"
    INDEX=$((i + 1))

    FILTER+="[0:v]trim=start=$START:end=$END,setpts=PTS-STARTPTS[v$INDEX]; "
    FILTER+="[0:a]atrim=start=$START:end=$END,asetpts=PTS-STARTPTS[a$INDEX]; "
    CONCAT_INPUTS+="[v$INDEX][a$INDEX]"
done

FILTER+="${CONCAT_INPUTS}concat=n=$SEGMENT_COUNT:v=1:a=1[outv][outa]"

echo "Extracting $SEGMENT_COUNT segments from '$INPUT_FILE' to '$OUTPUT_FILE'..."

ffmpeg -i "$INPUT_FILE" \
-filter_complex "$FILTER" \
-map "[outv]" -map "[outa]" \
-c:v libx264 -crf 23 -preset veryfast \
-c:a aac -b:a 192k \
-movflags +faststart \
-max_muxing_queue_size 1024 \
-threads 0 \
"$OUTPUT_FILE"

if [ $? -eq 0 ]; then
    echo "✓ Video segments extracted successfully to '$OUTPUT_FILE'"
else
    echo "✗ Error during extraction"
    exit 1
fi
