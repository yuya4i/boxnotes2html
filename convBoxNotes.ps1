# Box notesファイルをHTML、DOCX、またはテキストに変換するスクリプト
# __author__ = 'Kei Hikino'
# __editor__ = 'Yuya Takahashi'
# __version__ = '1.2.0'
# __date__ = '2024/06/12'

# 引数の数が正しくない場合は使用方法を表示
if ($args.Count -ne 2) {
  Write-Host "使用方法: ./convBoxNotes.ps1 [-x|-t|-h] <入力ディレクトリパス>"
  Write-Host "  -h: HTMLに変換"
  Write-Host "  -x: DOCXに変換"
  Write-Host "  -t: テキストに変換"
  Exit 1
}

$type = $args[0]
$inp_dir = $args[1]
$output_dir = Join-Path $inp_dir "output"

# 変換タイプが有効かチェック
if ($type -ne "-h" -and $type -ne "-x" -and $type -ne "-t") {
  Write-Host "エラー: 無効な変換タイプが指定されました。-h (HTML), -x (DOCX), -t (テキスト) を使用してください。"
  Exit 1
}

# 入力ディレクトリが存在するかチェック
if (!(Test-Path $inp_dir -PathType Container)) {
  Write-Host "エラー: 入力ディレクトリが存在しません。"
  Exit 1
}

# 出力ディレクトリが存在しない場合は作成
New-Item -ItemType Directory -Path $output_dir -Force | Out-Null

# 出力ファイルの拡張子を設定
if ($type -eq "-h") {
    $ext = ".html"
    $format = "HTML"
} elseif ($type -eq "-x") {
    $ext = ".docx"
    $format = "DOCX"
} elseif ($type -eq "-t") {
    $ext = ".txt"
    $format = "テキスト"
}

# ディレクトリ内のすべての.boxnoteファイルを変換
$files = Get-ChildItem -Path $inp_dir -Filter *.boxnote
$foundFiles = $false

if ($files.Count -eq 0) {
    Write-Host "警告: 指定されたディレクトリに.boxnoteファイルが見つかりませんでした。"
    Exit 0
}

foreach ($file in $files) {
    $foundFiles = $true
    $filename = $file.BaseName
    $output_file = "$output_dir\$filename"
    Write-Host "変換中: $file を $format 形式に変換しています..."
    
    # Pythonスクリプトを呼び出して変換
    try {
        # Python 3を明示的に指定
        python3 convBoxNotes.py $type $file.FullName $output_file
        if ($LASTEXITCODE -ne 0) {
            Write-Host "エラー: ファイル '$file' の変換に失敗しました。" -ForegroundColor Red
            continue
        }
        
        # DOCXの場合は一時ファイルを削除
        if ($type -eq "-x") {
            if (Test-Path $output_file) {
                Remove-Item $output_file -Force
            }
        }
    }
    catch {
        Write-Host "エラー: 変換処理中に例外が発生しました: $_" -ForegroundColor Red
    }
}

# 変換結果を表示
Write-Host "変換完了。出力ディレクトリの内容:"
Get-ChildItem -Path $output_dir | Format-Table Name, Length, LastWriteTime