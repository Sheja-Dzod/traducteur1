from pathlib import Path
import re
import sys
import polib
from text_formatting import format_fr
from utils import normalize


class Po:
    def __init__(self):
        self.par_marker = '\n\n\n'
        self.trans_pattern = r'(.*?\n\t.*)\n'
        self.trans_delimiter = '\n(?:\t|[ ]{4})'
        self.file = polib.POFile()
        self.file.metadata = {
            'MIME-Version': '1.0',
            'Content-Type': 'text/plain; charset=utf-8',
            'Content-Transfer-Encoding': '8bit',
        }

    def _create_entry(self, msgid, msgstr="", msgctxt=None, comment=None, tcomment=None):
        entry = polib.POEntry(
            msgid=msgid,
            msgstr=msgstr,
            msgctxt=msgctxt,
            comment=comment,
            tcomment=tcomment
        )
        self.file.append(entry)

    def write_to_file(self, filename):
        self.file.save(filename)

    def dump_po_entries(self, dump, origin):
        sent_num = 0
        for num, par in enumerate(dump.strip().split(self.par_marker)):
            pairs = re.split(self.trans_pattern, par)
            pairs = [p for p in pairs if p]
            source = []
            comment = []
            for pair in pairs:
                try:
                    c, s = re.split(self.trans_delimiter, pair)
                except ValueError as e:
                    print('The input file is not well formated. Most likely a Windows line-sep error.')
                    print(num + 1, pair)
                    raise SyntaxError(e)
                source.append(s)
                comment.append(f' {sent_num+1}. {c}')
                sent_num += 1
            source = ' '.join(source)
            source = format_fr(source)
            # segment tibetan original into lines of 13 syllables
            c_parts = ''.join(comment).split('་')
            c_parts = [f'{c}་\n\n' if num > 0 and not num % 13 else f'{c}་' for num, c in enumerate(c_parts)]
            comment = ''.join(c_parts)
            self._create_entry(msgid=source, msgctxt=f'line {num + 1}, {origin}', tcomment=comment)

    def txt_to_po(self, filename):
        lines = normalize(filename.read_text(encoding='utf-8'))
        # cleanup
        lines = '\n'.join([l.rstrip() for l in lines.split('\n')])

        if self.par_marker not in lines:
            print(' — has no paragraphs. passing...')
            return
        else:
            print('')

        self.dump_po_entries(lines, filename.name)
        self.write_to_file((filename.parent / (filename.stem + ".po")))


if __name__ == '__main__':
    folder = 'communicative/paragraphs'
    if len(sys.argv) > 1:
        stem = sys.argv[1]
        file = Path(folder) / (stem + '.txt')
        print(file, end='')
        po = Po()
        po.txt_to_po(file)
    else:
        files = sorted(list(Path(folder).glob('*.txt')))
        for file in files:
            print(file, end='')
            po = Po()
            po.txt_to_po(file)
