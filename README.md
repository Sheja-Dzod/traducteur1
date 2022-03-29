# tx-template
template for translating Tibetan texts on Transifex

exclusion regexes for DocFetcher:
excludes:
 - all files without `_` in them
 - all files ending with `_translation.txt`
 - all files ending with `.po`
```
[^_]+\.txt
.*?_translation\.txt
.*\.po
```

TODO: 
 - implement paragraph transfer on the translation file of the reader version.
 - implement `oe` to `œ`
 
Segmentation rules :

- keep a single sentence per line. it can contain only one inflected verb (one that is not nominalized)
- སྙམ་དུ་ and ཞེས་ etc. are kept as part of the preceding sentence, but the verb right after is made into another sentence.
- འདི་སྐད་ཅེས་གསོལ་ ཞུ་ etc. are all kept as a single sentence because of carrying the same meaning.
- separate in digestible bits the long and recurrent passages such as the enumeration of the ten sets of qualities of a Buddha, or the way a Buddha looks at the world, or as the description of the qualities of an arhat when he reaches this state.
- separate all the expression of address
- separate ཅི་ at the beginning of a sentence when it means "what about this?"/"how is this?"
- separate nominalized expression that are used to introduce direct speech (དེས་བསམས་པ། etc.)
- list of exceptions : 
    - ལས་ཅི་བགྱིས་ན།
    - ཅི་བགྱི། preceded by a verb
