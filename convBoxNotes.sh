#!/bin/bash

# Box notesファイルをHTML、DOCX、またはテキストに変換するスクリプト
# __author__ = 'Kei Hikino'
# __editor__ = 'Yuya Takahashi'
# __version__ = '1.2.0'
# __date__ = '2024/06/12'

# 引数の数が正しくない場合は使用方法を表示
if [ "$#" -ne 2 ]; then
  echo "使用方法: $0 [-x|-t|-h] <入力ディレクトリパス>"
  echo "  -h: HTMLに変換"
  echo "  -x: DOCXに変換"
  echo "  -t: テキストに変換"
  exit 1
fi

type="$1"
inp_dir="$2"
output_dir="$inp_dir/output"

# 変換タイプが有効かチェック
if [[ "$type" != "-h" && "$type" != "-x" && "$type" != "-t" ]]; then
  echo "エラー: 無効な変換タイプが指定されました。-h (HTML), -x (DOCX), -t (テキスト) を使用してください。"
  exit 1
fi

# 入力ディレクトリが存在するかチェック
if [ ! -d "$inp_dir" ]; then
  echo "エラー: 入力ディレクトリが存在しません。"
  exit 1
fi

# 出力ディレクトリが存在しない場合は作成
mkdir -p "$output_dir"

# ディレクトリ内のすべての.boxnoteファイルを変換
found_files=false
for file in "$inp_dir"/*.boxnote; do
  # .boxnoteファイルが見つからない場合はスキップ
  [ -e "$file" ] || continue
  
  found_files=true
  echo "変換中: \"$file\"..."
  filename=$(basename -- "$file" .boxnote)
  output_file="$output_dir/$filename"
  
  # Pythonスクリプトを呼び出して変換
  python3 convBoxNotes.py "$type" "$file" "$output_file"
  exit_code=$?
  
  # 変換が成功したかチェック
  if [ $exit_code -ne 0 ]; then
    echo "エラー: ファイル \"$file\" の変換に失敗しました。"
    continue
  fi
  
  # DOCXの場合は一時ファイルを削除
  if [ "$type" = "-x" ]; then
    rm -f "$output_file"
  fi
done

# ファイルが見つからなかった場合はメッセージを表示
if [ "$found_files" = false ]; then
  echo "警告: 指定されたディレクトリに.boxnoteファイルが見つかりませんでした。"
  exit 0
fi

# 変換結果を表示
echo "変換完了。出力ディレクトリの内容:"
ls -la "$output_dir"
