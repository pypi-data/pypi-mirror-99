
from ..file_utils import VariantFileReader, common_filepaths

import os
import marisa_trie


def parse_line(line):
    chrom, pos, ref, alt, rsid, genes = line.rstrip('\n').split('\t')
    # Keys in marisa_trie must be unicode. Values in BytesTrie must be bytes.
    return ('{}-{}-{}-{}'.format(chrom, pos, ref, alt), rsid.encode())


sites_filepath = common_filepaths['sites']()
cpra_to_rsids_trie_filepath = common_filepaths['cpra-to-rsids-trie']()
rsid_to_cpra_trie_filepath  = common_filepaths['rsid-to-cpra-trie']()
def should_replace(filepath):
    return not os.path.exists(filepath) or os.stat(filepath).st_mtime < os.stat(sites_filepath).st_mtime

def run(argv):

    if '-h' in argv or '--help' in argv:
        print('Make tries for converting between chr-pos-ref-alt and rsid')
        exit(1)

    if not should_replace(cpra_to_rsids_trie_filepath) and not should_replace(rsid_to_cpra_trie_filepath):
        print('tries are up-to-date!')

    else:
        # Note: two identical VariantFileReaders are made in order to allow streaming to reduce memory usage.
        #       a different trie library might allow feeding both tries while reading from a file, but marisa_trie doesn't.
        with VariantFileReader(sites_filepath) as reader:
            cpras_and_rsids = (('{chrom}-{pos}-{ref}-{alt}'.format(**v), v['rsids'].encode('ascii')) for v in reader)
            cpra_to_rsids_trie = marisa_trie.BytesTrie(cpras_and_rsids, order=marisa_trie.LABEL_ORDER)
        cpra_to_rsids_trie.save(cpra_to_rsids_trie_filepath)
        print('done with cpra->rsids trie at ' + cpra_to_rsids_trie_filepath)

        # Note: if several different chrom-pos-ref-alts have the same rsid, then `trie[rsid]` = `[cpra1, cpra2, ...]`.
        with VariantFileReader(sites_filepath) as reader:
            def get_rsids_and_cpras():
                for v in reader:
                    if v['rsids']:
                        cpra = '{chrom}-{pos}-{ref}-{alt}'.format(**v).encode('ascii')
                        for rsid in v['rsids'].split(','):
                            yield (rsid, cpra)
            rsid_to_cpra_trie = marisa_trie.BytesTrie(get_rsids_and_cpras(), order=marisa_trie.LABEL_ORDER)
        rsid_to_cpra_trie.save(rsid_to_cpra_trie_filepath)
        print('done with rsid->cpra trie at ' + rsid_to_cpra_trie_filepath)
