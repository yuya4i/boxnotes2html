#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Box notesファイルをHTML、DOCX、またはテキストに変換するツール

このスクリプトは、Box notesファイル（.boxnote）をHTML、DOCX、またはテキスト形式に
変換するためのコマンドラインツールです。

__editor__ = 'Yuya Takahashi'
__version__ = '1.1.0'
__date__ = '2024/06/12'
"""

import sys
import os
from pathlib import Path
from boxnote2converter.html_parser import parse as parse_html
from boxnote2converter.docx_parser import parse_docx
import warnings

# python-docxの警告を無視
warnings.filterwarnings("ignore", category=UserWarning, module='docx.styles.styles', lineno=130)

class BoxNotesConverter:
    """Box notesファイルを変換するクラス"""
    
    def __init__(self, option, input_file_path, output_file_path, token=None, work_dir="./output"):
        """
        コンバーターの初期化
        
        Args:
            option (str): 変換オプション（-h: HTML, -x: DOCX, -t: テキスト）
            input_file_path (str): 入力ファイルのパス
            output_file_path (str): 出力ファイルのパス
            token (str, optional): 認証トークン（必要な場合）
            work_dir (str, optional): 作業ディレクトリ
        """
        self.option = option
        self.input_file_path = Path(input_file_path)
        self.output_file_path = Path(output_file_path)
        self.token = token
        self.work_dir = Path(work_dir)

        self.validate_paths()

    def validate_paths(self):
        """入力ファイルパスの検証"""
        if not self.input_file_path.exists():
            raise FileNotFoundError(f"エラー: 入力ファイル {self.input_file_path} が存在しません。")

        if not self.input_file_path.is_file():
            raise FileNotFoundError(f"エラー: {self.input_file_path} はファイルではありません。")

    def convert_to_html(self):
        """BoxnoteファイルをHTMLに変換"""
        try:
            with open(self.input_file_path, 'r', encoding="utf-8") as f:
                boxnote_content = f.read()
            html_content = parse_html(boxnote_content, self.input_file_path.stem, self.work_dir, self.token)
            output_html_file = self.output_file_path.with_suffix('.html')
            with open(output_html_file, 'w', encoding="utf-8") as f:
                f.write(html_content)
            self.print_message(output_html_file, 'HTML')
            return True
        except Exception as e:
            print(f"HTMLへの変換に失敗しました: {e}")
            return False

    def convert_to_docx(self):
        """BoxnoteファイルをDOCXに変換"""
        try:
            parse_docx(self.token, self.work_dir, self.input_file_path, self.input_file_path.stem,
                      self.output_file_path, self.output_file_path, None)
            self.print_message(self.output_file_path, 'DOCX')
            return True
        except Exception as e:
            print(f"DOCXへの変換に失敗しました: {e}")
            return False

    def convert_to_text(self):
        """Boxnoteファイルをテキストに変換"""
        try:
            with open(self.input_file_path, 'r', encoding="utf-8") as f:
                boxnote_content = f.read()
            
            # 簡易的なテキスト変換処理
            # HTMLタグや特殊な書式を除去してプレーンテキストを抽出
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(boxnote_content, 'html.parser')
            text_content = soup.get_text()
            
            output_text_file = self.output_file_path.with_suffix('.txt')
            with open(output_text_file, 'w', encoding="utf-8") as f:
                f.write(text_content)
            self.print_message(output_text_file, 'テキスト')
            return True
        except Exception as e:
            print(f"テキストへの変換に失敗しました: {e}")
            return False

    def print_message(self, output_file, extension):
        """変換完了メッセージの表示"""
        print(f"{extension}に変換しました: {output_file}")

    def run(self):
        """変換処理の実行"""
        if self.option == '-h':
            return self.convert_to_html()
        elif self.option == '-x':
            return self.convert_to_docx()
        elif self.option == '-t':
            return self.convert_to_text()
        else:
            print("無効なオプションです。-h (HTML), -x (DOCX), -t (テキスト) を使用してください。")
            return False

def main():
    """メイン関数"""
    # コマンドライン引数の検証
    if len(sys.argv) < 4:
        print("使用方法: python convBoxNotes.py <-h|-x|-t> <入力ファイルパス> <出力ファイルパス>")
        sys.exit(1)
        
    option = sys.argv[1]
    input_file_path = sys.argv[2]
    output_file_path = sys.argv[3]
    token = None
    work_dir = "./output"

    # 追加のオプション引数処理（将来の拡張用）
    if len(sys.argv) >= 6 and sys.argv[4] == '-t':
        token = sys.argv[5]
    if len(sys.argv) >= 8 and sys.argv[6] == '-d':
        work_dir = sys.argv[7]

    try:
        # 出力ディレクトリが存在しない場合は作成
        output_dir = os.path.dirname(output_file_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        converter = BoxNotesConverter(option, input_file_path, output_file_path, token, work_dir)
        success = converter.run()
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        # エラー発生時には出力ファイルを削除
        if os.path.exists(output_file_path):
            os.remove(output_file_path)
        sys.exit(1)

if __name__ == '__main__':
    main()
