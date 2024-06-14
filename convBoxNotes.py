# Convert Box notes files to html, Docx, or text
# -*- coding: utf-8 -*-
# __editor__ = 'Yuya Takahashi'
# __version__ = '1.0.0'
# __date__ = '2024/06/12'
import sys
import os
from pathlib import Path
from boxnote2converter.html_parser import parse as parse_html
from boxnote2converter.docx_parser import parse_docx
import warnings

# 特定の警告を無視
warnings.filterwarnings("ignore", category=UserWarning, module='docx.styles.styles', lineno=130)

class BoxNotesConverter:
    def __init__(self, option, input_file_path, output_file_path, token=None, work_dir="./output"):
        self.option = option
        self.input_file_path = Path(input_file_path)
        self.output_file_path = Path(output_file_path)
        self.token = token
        self.work_dir = Path(work_dir)

        self.validate_paths()

    def validate_paths(self):
        if not self.input_file_path.exists():
            raise FileNotFoundError(f"Error: Input file {self.input_file_path} does not exist.")

        if not self.input_file_path.is_file():
            raise FileNotFoundError(f"Error: {self.input_file_path} is not a file.")

    def convert_to_html(self):
        try:
            with open(self.input_file_path, 'r') as f:
                boxnote_content = f.read()
            html_content = parse_html(boxnote_content, self.input_file_path.stem, self.work_dir, self.token)
            output_html_file = self.output_file_path.with_suffix('.html')
            with open(output_html_file, 'w') as f:
                f.write(html_content)
            self.print_message(output_html_file, 'html')
        except Exception as e:
            print(f"Failed to convert to HTML: {e}")

    def convert_to_docx(self):
        try:
            parse_docx(self.token, self.work_dir, self.input_file_path, self.input_file_path.stem, self.output_file_path, self.output_file_path, None)
            self.print_message(self.output_file_path, 'docx')
        except Exception as e:
            print(f"Failed to convert to DOCX: {e}")

    # def convert_to_text(self):
    #     try:
    #         with open(self.input_file_path, 'r') as f:
    #             boxnote_content = f.read()
    #         text_content = boxnote_content  # This should be replaced with an actual text conversion function
    #         output_text_file = self.output_file_path.with_suffix('.txt')
    #         with open(output_text_file, 'w') as f:
    #             f.write(text_content)
    #         self.print_message(output_text_file, 'txt')
    #     except Exception as e:
    #         print(f"Failed to convert to text: {e}")

    def print_message(self, output_file, extension):
        print(f"Converted to {extension}: {output_file}")

    def run(self):
        if self.option == '-h':
            self.convert_to_html()
        elif self.option == '-x':
            self.convert_to_docx()
        # elif self.option == '-t':
        #     self.convert_to_text()
        else:
            print("Invalid option. Use -h for HTML, -x for DOCX.")
            sys.exit(1)

def main():    
    option = sys.argv[1]
    input_file_path = sys.argv[2]
    output_file_path = sys.argv[3]
    token = None
    work_dir = "./output"

    # if len(sys.argv) >= 6:
    #     if sys.argv[4] == '-t':
    #         token = sys.argv[5]
    #     if len(sys.argv) == 7 and sys.argv[6] == '-d':
    #         work_dir = sys.argv[7]

    try:
        converter = BoxNotesConverter(option, input_file_path, output_file_path, token, work_dir)
        converter.run()
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        # エラー発生時には出力ファイルを削除
        if os.path.exists(output_file_path):
            os.remove(output_file_path)
        sys.exit(1)

if __name__ == '__main__':
    main()
