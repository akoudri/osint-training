#!/bin/bash

# Configuration
INPUT_FILE="${1:-input.mp4}"
OUTPUT_FILE="${2:-output.mp4}"

# Timestamps for video segments (format: start-end in HH:MM:SS-HH:MM:SS)
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

echo "Extracting ${#SEGMENTS[@]} segments from '$INPUT_FILE'..."

# Create temp directory in current dir (not /tmp which may be small)
TEMP_DIR="./temp_extract_$$"
mkdir -p "$TEMP_DIR"
trap "rm -rf $TEMP_DIR" EXIT

# Create concat list file
CONCAT_FILE="$TEMP_DIR/concat.txt"

# Extract each segment with stream copy (no re-encoding)
for i in "${!SEGMENTS[@]}"; do
    IFS='-' read -r START END <<< "${SEGMENTS[$i]}"
    SEGMENT_FILE="$TEMP_DIR/segment_$i.webm"

    # Calculate duration (convert HH:MM:SS to seconds)
    START_SEC=$(echo "$START" | awk -F: '{print $1*3600 + $2*60 + $3}')
    END_SEC=$(echo "$END" | awk -F: '{print $1*3600 + $2*60 + $3}')
    DURATION=$((END_SEC - START_SEC))

    echo "  Extracting segment $((i+1)): $START -> $END (${DURATION}s)"

    ffmpeg -ss "$START" -i "$INPUT_FILE" -t "$DURATION" -c copy -avoid_negative_ts 1 "$SEGMENT_FILE" -loglevel error -y

    if [ $? -eq 0 ] && [ -f "$SEGMENT_FILE" ]; then
        # Use absolute path for concat file
        echo "file '$(realpath "$SEGMENT_FILE")'" >> "$CONCAT_FILE"
    else
        echo "Error extracting segment $((i+1))"
        exit 1
    fi
done

echo "Concatenating segments and converting to MP4..."

# Concatenate all segments
ffmpeg -f concat -safe 0 -i "$CONCAT_FILE" \
-c:v libx264 -crf 23 -preset veryfast -pix_fmt yuv420p \
-vf "scale=-2:1080:flags=lanczos" \
-c:a aac -b:a 192k \
-movflags +faststart \
-max_muxing_queue_size 1024 \
"$OUTPUT_FILE" -loglevel warning -stats -y

if [ $? -eq 0 ]; then
    echo "✓ Video segments extracted successfully to '$OUTPUT_FILE'"
    rm -rf "$TEMP_DIR"
else
    echo "✗ Error during concatenation"
    exit 1
fi
