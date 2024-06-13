#!/bin/bash

# Convert Box notes files to HTML, DOCX, or Text
# __author__ = 'Kei Hikino'
# __editor__ = 'Yuya Takahashi'
# __version__ = '1.1.0'
# __date__ = '2024/06/12'

# Display usage if the number of arguments is incorrect
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 [-x|-t|-h] <Input directory path>"
  exit 1
fi

type=$1
inp_dir=$2
output_dir="$inp_dir/output"

# Check for valid conversion type
if [[ "$type" != "-h" && "$type" != "-x" && "$type" != "-t" ]]; then
  echo "Error: Invalid conversion type specified. Use -h for HTML, -x for DOCX, -t for Text."
  exit 1
fi

# Check if the input directory exists
if [ ! -d "$inp_dir" ]; then
  echo "Error: Input directory does not exist."
  exit 1
fi

# Create the output directory if it does not exist
mkdir -p "$output_dir"

# Convert all .boxnote files in the directory
for file in "$inp_dir"/*.boxnote; do
  filename=$(basename -- "$file" .boxnote)
  output_file="$output_dir/$filename"
  # Call the Python conversion script
  python convBoxNotes.py $type "$file" "$output_file"
  # Delete at the end because a temporary file is created
  # Delete only if type = -x
  if [ "$type" = "-x" ]; then
    rm "$output_file"
  fi
done

