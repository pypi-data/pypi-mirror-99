
import math
import json
import os
import csv
import boltons.mathutils
import urllib.parse
from typing import List,Dict,Optional,Any,Tuple,Iterator


class PheWebError(Exception):
    '''implies that an exception is being handled by PheWeb, so its message should just be printed.'''

def round_sig(x:float, digits:int) -> float:
    if x == 0:
        return 0
    elif abs(x) == math.inf or math.isnan(x):
        raise ValueError("Cannot round infinity or NaN")
    else:
        log = math.log10(abs(x))
        digits_above_zero = int(math.floor(log))
        return round(x, digits - 1 - digits_above_zero)
assert round_sig(0.00123, 2) == 0.0012
assert round_sig(1.59e-10, 2) == 1.6e-10

def approx_equal(a:float, b:float, tolerance:float = 1e-4) -> bool:
    return abs(a-b) <= max(abs(a), abs(b)) * tolerance
assert approx_equal(42, 42.0000001)
assert not approx_equal(42, 42.01)

def fmt_seconds(seconds:float) -> str:
    if seconds < 5*60: return '{} seconds'.format(int(seconds))
    if seconds < 5*60*60: return '{} minutes'.format(int(seconds//60))
    return '{} hours'.format(int(seconds//60//60))
assert fmt_seconds(9) == '9 seconds'
assert fmt_seconds(900) == '15 minutes'
assert fmt_seconds(90000) == '25 hours'


def get_phenolist(filepath:Optional[str] = None) -> List[Dict[str,Any]]:
    # TODO: should this be memoized?
    from .file_utils import get_filepath
    filepath = filepath or get_filepath('phenolist')  # Allow override for unit testing
    try:
        with open(os.path.join(filepath)) as f:
            phenolist = json.load(f)
    except (FileNotFoundError, PermissionError):
        raise PheWebError(
            "You need a file to define your phenotypes at '{}'.\n".format(filepath) +
            "For more information on how to make one, see <https://github.com/statgen/pheweb#3-make-a-list-of-your-phenotypes>")
    except json.JSONDecodeError as exc:
        raise PheWebError("Your file at '{}' contains invalid json.\n".format(filepath)) from exc
    for pheno in phenolist:
        pheno['phenocode'] = urllib.parse.quote_plus(pheno['phenocode'])
    return phenolist


def pad_gene(start:int, end:int) -> Tuple[int,int]:
    '''
    Calculates a range to show in LocusZoom region views for a gene.
    Adds 100kb on each side, but never go below 0 or pad longer than 500kb (LocusZoom's max_region_scale).
    '''
    total_padding = boltons.mathutils.clamp(int(500e3) - (end - start), 0, int(200e3))
    padding_on_left = min(total_padding//2, start)  # if start < padding//2, use `start` to avoid going below 0.
    padding_on_right = min(int(100e3), total_padding - padding_on_left)  # put the remaining padding on the right, but not more than 100kb.
    return (start - padding_on_left, end + padding_on_right)
assert pad_gene(1000,     2345) == (0,      102345), pad_gene(1000,     2345)
assert pad_gene(1000,   400000) == (0,      500000), pad_gene(1000,   400000)
assert pad_gene(200000, 400000) == (100000, 500000), pad_gene(200000, 400000)
assert pad_gene(200000, 500000) == (100000, 600000), pad_gene(200000, 500000)
assert pad_gene(200000, 500001) == (100001, 600001), pad_gene(200000, 500001)
assert pad_gene(200000, 600000) == (150000, 650000), pad_gene(200000, 600000)
assert pad_gene(200000, 700000) == (200000, 700000), pad_gene(200000, 700000)
assert pad_gene(200000, 800000) == (200000, 800000), pad_gene(200000, 800000)


chrom_order_list = [str(i) for i in range(1,22+1)] + ['X', 'Y', 'MT']
chrom_order = {chrom: index for index,chrom in enumerate(chrom_order_list)}
chrom_aliases = {'23': 'X', '24': 'Y', '25': 'MT', 'M': 'MT'}
for chrom in chrom_order_list: chrom_aliases['chr{}'.format(chrom)] = chrom
for alias, chrom in list(chrom_aliases.items()): chrom_aliases['chr{}'.format(alias)] = chrom


def get_gene_tuples_with_ensg() -> Iterator[Tuple[str,int,int,str,str]]:
    from .file_utils import get_filepath
    with open(get_filepath('genes')) as f:
        for row in csv.reader(f, delimiter='\t'):
            assert row[0] in chrom_order, row[0]
            yield (row[0], int(row[1]), int(row[2]), row[3], row[4])
def get_gene_tuples() -> Iterator[Tuple[str,int,int,str]]:
    for chrom,start,end,genename,ensg in get_gene_tuples_with_ensg():
        yield (chrom,start,end,genename)
