from pathlib import Path

from botok import Text


if __name__ == '__main__':
    to_segment_path = 'to_segment'
    segmented_path = 'literal/tibetan'
    files = sorted(list(Path(to_segment_path).glob('*.txt')))
    for f in files:
        seg_file = Path(segmented_path) / f.name
        if not seg_file.is_file():
            dump = f.read_text()
            sentences = Text(dump.replace('\n', '')).tokenize_sentences_plaintext
            seg_file.write_text(sentences)
