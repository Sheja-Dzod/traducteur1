from pathlib import Path
import re

import polib
from antx import transfer

from text_formatting import format_fr
from utils import normalize


class Po:
    def __init__(self, infile):
        self.infile = Path(infile)
        self.infile.write_text(normalize(self.infile.read_text(encoding='utf-8')), encoding='utf-8')
        self.file = polib.pofile(self.infile)
        self._format_fields()

    def format_entries(self):
        entries = []
        for entry in self.file:
            text = entry.msgid
            text = text.replace(' ', '').replace('␣', '').replace(' ', ' ')
            text = text.replace('\n', ' ')
            trans = entry.msgstr.replace('\n', ' ')
            entries.append((text, trans))
        return '\n'.join(['\n'.join([e[0], '\t' + e[1]]) for e in entries]), \
               '\n'.join([e[1].strip() for e in entries]), \
               '\n'.join(['\n'.join([e[0], '\t' + e[1]]) for e in entries])

    def write_txt(self):
        orig_trans, trans, pars_trans = self.format_entries()
        if '5_4-2.7.t' in self.infile.stem:
            print()
        bitext = self.infile.parent / (self.infile.stem + '.txt')
        bitext.write_text(orig_trans, encoding='utf-8')

        translation = self.infile.parent / (self.infile.stem + '_only.txt')
        translation.write_text(trans, encoding='utf-8')

        pars = Path(copy_folder) / (self.infile.stem + '.txt')
        if not pars.is_file():
            pars.write_text(pars_trans, encoding='utf-8')
        else:
            # update file retaining the paragraph delimitations
            pars_old = normalize(pars.read_text(encoding='utf-8'))
            if pars_old.replace('\n\n\n', '\n') != orig_trans:
                updated = self._update_pars(pars_old, orig_trans)
                pars.write_text(normalize(updated), encoding='utf-8')

    @staticmethod
    def _update_pars(source, target):
        pattern = [["pars", "(\n\n\n)"]]
        updated = transfer(source, pattern, target, "txt")
        # updated = '\n'.join([u.strip() for u in updated.split('\n')])  # strip lines for applying the hack below
        updated = re.sub(r'\n[  \t]*\n[  \t]*\n[  \t]*\n[  \t]*', '\n\n\n', updated)
        updated = updated.replace('\n\n\n\n', '\n\n\n')  # hack for a strange behaviour
        return updated

    def _format_fields(self):
        for entry in self.file:
            entry.msgstr = format_fr(entry.msgstr)


if __name__ == '__main__':
    folder = 'literal/translation'
    copy_folder = 'communicative/paragraphs'
    for file in Path(folder).glob('*.po'):
        po = Po(file)
        po.write_txt()
