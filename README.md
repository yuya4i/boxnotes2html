# convBoxNotes

Box notesドキュメントを素早く検索することは困難です。`convBoxNotes`は、`boxnotes2html` OSSを使用してBox notesドキュメントをHTML、DOCX、またはテキスト形式に一括変換するツールです。

## 特徴

- Box notesファイル（.boxnote）をHTML、DOCX、またはテキスト形式に変換
- ディレクトリ内のすべてのBox notesファイルを一括処理
- シンプルなコマンドラインインターフェース
- Windows（PowerShell）とMac/Linux（Bash）の両方に対応

## インストール

このツールはMacとWindows（WSL1またはWSL2使用）の両方で利用可能です。Windowsで使用する場合は、シェル（bash）を使用するためにWSL1またはWSL2をインストールする必要があります。

0. Python 3が必要です。
1. ```boxnote2converter```ディレクトリに移動します。（このソースコードはalexwennerbergの[boxnotes2html](https://github.com/alexwennerberg/boxnotes2html)を使用しています）
2. 以下のコマンドでリポジトリをセットアップします：
```shell
pip install -r requirements.txt
```

## 依存関係

- python-docx==0.8.11
- beautifulsoup4==4.12.2
- requests==2.32.3

## 使用方法

### Bash (Mac/Linux)
```shell
./convBoxNotes.sh <-h|-x|-t> <*.boxnotesが保存されているディレクトリパス>
```

### PowerShell (Windows)
```powershell
./convBoxNotes.ps1 <-h|-x|-t> <*.boxnotesが保存されているディレクトリパス>
```

### オプション
- `-h`: HTMLに変換
- `-x`: DOCXに変換
- `-t`: テキストに変換

変換されたファイルは自動的に `<*.boxnotesが保存されているディレクトリパス>/output/` に保存されます。

## 例

```shell
# ディレクトリ内のすべてのboxnoteファイルをHTMLに変換
./convBoxNotes.sh -h /path/to/boxnotes

# ディレクトリ内のすべてのboxnoteファイルをDOCXに変換
./convBoxNotes.sh -x /path/to/boxnotes

# ディレクトリ内のすべてのboxnoteファイルをテキストに変換
./convBoxNotes.sh -t /path/to/boxnotes
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細については、boxnote2converterディレクトリ内のLICENSEファイルを参照してください。

## 謝辞

このツールは[alexwennerberg/boxnotes2html](https://github.com/alexwennerberg/boxnotes2html)をベースにしています。