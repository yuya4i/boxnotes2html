# Convert Box notes files to HTML, DOCX, or Text
# __author__ = 'Kei Hikino'
# __editor__ = 'Yuya Takahashi'
# __version__ = '1.1.0'
# __date__ = '2024/06/12'



$type = $args[0]
$inp_dir = $args[1]

# Display usage if the number of arguments is incorrect
if ($args.Count -ne 2) {
  Write-Host "Usage: ./convBoxNotes.ps1 [-x|-h] <Input directory path>"
  Exit 1
}

$type = $args[0]
$inp_dir = $args[1]
$output_dir = Join-Path $inp_dir "output"

# Check for valid conversion type
if ($type -ne "-h" -and $type -ne "-x" -and $type -ne "-t") {
  Write-Host "Error: Invalid conversion type specified. Use -h for HTML, -x for DOCX, -t for Text."
  Exit 1
}

# Check if the input directory exists
if (!(Test-Path $inp_dir -PathType Container)) {
  Write-Host "Error: Input directory does not exist."
  Exit 1
}

# Create the output directory if it does not exist
New-Item -ItemType Directory -Path $output_dir -Force

# Convert all .boxnote files in the directory
Get-ChildItem -Path $inp_dir -Filter *.boxnote | ForEach-Object {
    $filename = $_.BaseName
    $output_file = "$output_dir\$filename"
    Write-Host "Converting $_ to $output_file"
    # Call the Python conversion script
    python convBoxNotes.py $type $_.FullName $output_file
    # Delete at the end because a temporary file is created
    # Delete only if type = -x
    if ($type -eq "-x") {
        Remove-Item $output_file
    }
}