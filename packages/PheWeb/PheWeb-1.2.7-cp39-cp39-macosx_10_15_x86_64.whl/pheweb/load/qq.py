
'''
This script creates json files which can be used to render QQ plots.
'''

# TODO: share the `VariantFileReader` with `manhattan.py`.
# TODO: make gc_lambda for maf strata, and show them if they're >1.1?
# TODO: copy some changes from <https://github.com/statgen/encore/blob/master/plot-epacts-output/make_qq_json.py>

# TODO: reduce QQ memory using Counter(v.qval for v in variants).
#      - but we still need to split into 4 strata using MAF. Can that be done efficiently?
#          a) we could keep balanced lists for the 4 strata, but we can only be confidently start processing variants once we've read 3/4 of all variants
#          b) we could assume that, since we're sorted by chr-pos-ref-alt, MAF should be pretty randomly ordered.
#               - then we could start processing variants after reading only 10% of all variants
#               - if we're wrong, `raise StrataGuessingFailed()` and try again with sorting.
#          c) we could run manhattan before this, and make it track Counter(rounded(v.maf,2) for v in variants).

# NOTE: `qval` means `-log10(pvalue)`

from ..utils import round_sig, approx_equal
from ..file_utils import VariantFileReader, write_json, get_pheno_filepath
from .load_utils import get_maf, parallelize_per_pheno, get_phenos_subset, get_phenolist

from typing import Dict,Any,List,Iterator
import argparse
import boltons.mathutils
import boltons.iterutils
import collections
import math
import scipy.stats

NUM_BINS = 400
NUM_MAF_RANGES = 4


def run(argv:List[str]) -> None:
    parser = argparse.ArgumentParser(description="Make a QQ plot for each phenotype.")
    parser.add_argument('--phenos', help="Can be like '4,5,6,12' or '4-6,12' to run on only the phenos at those positions (0-indexed) in pheno-list.json (and only if they need to run)")
    args = parser.parse_args(argv)

    phenos = get_phenos_subset(args.phenos) if args.phenos else get_phenolist()

    parallelize_per_pheno(
        get_input_filepaths = lambda pheno: get_pheno_filepath('pheno_gz', pheno['phenocode']),
        get_output_filepaths = lambda pheno: get_pheno_filepath('qq', pheno['phenocode'], must_exist=False),
        convert = make_json_file,
        cmd = 'qq',
        phenos = phenos,
    )


def make_json_file(pheno:Dict[str,Any]) -> None:
    make_json_file_explicit(
        get_pheno_filepath('pheno_gz', pheno['phenocode']),
        get_pheno_filepath('qq', pheno['phenocode'], must_exist=False),
        pheno
    )

def make_json_file_explicit(in_filepath:str, out_filepath:str, pheno:Dict[str,Any]) -> None:
    with VariantFileReader(in_filepath) as variant_dicts:
        variants = list(augment_variants(variant_dicts, pheno))
    rv: Dict[str,Any] = {}
    if variants:
        if variants[0].maf is not None:
            rv['overall'] = make_qq_unstratified(variants, include_qq=False)
            rv['by_maf'] = make_qq_stratified(variants)
            rv['ci'] = list(get_confidence_intervals(len(variants) / len(rv['by_maf'])))
        else:
            rv['overall'] = make_qq_unstratified(variants, include_qq=True)
            rv['ci'] = list(get_confidence_intervals(len(variants)))
    write_json(filepath=out_filepath, data=rv)


Variant = collections.namedtuple('Variant', ['qval', 'maf'])
def augment_variants(variants:Iterator[Dict[str,Any]], pheno:Dict[str,Any]) -> Iterator[Variant]:
    for v in variants:
        # TODO: make an option "convert_pval0_to = [num|None]"
        qval: float = 1000 if v['pval']==0 else -math.log10(v['pval'])
        maf = get_maf(v, pheno)
        yield Variant(qval=qval, maf=maf)


def make_qq_stratified(variants:List[Variant]) -> List[Dict[str,Any]]:
    variants.sort(key=lambda v: v.maf)  # Sort in-place to save RAM

    def make_strata(idx:int) -> Dict[str,Any]:
        # Note: slice_indices[1] is the same as slice_indices[0] of the next slice.
        # But that's not a problem, because range() ignores the last index.
        slice_indices = (len(variants) * idx//NUM_MAF_RANGES,
                         len(variants) * (idx+1)//NUM_MAF_RANGES)
        qvals = sorted((variants[i].qval for i in range(*slice_indices)), reverse=True)
        return {
            'maf_range': (variants[slice_indices[0]].maf,
                          variants[slice_indices[1]-1].maf),
            'count': len(qvals),
            'qq': compute_qq(qvals),
        }

    return [make_strata(i) for i in range(NUM_MAF_RANGES)]

def make_qq_unstratified(variants:List[Variant], include_qq:bool) -> Dict[str,Any]:
    qvals = sorted((v.qval for v in variants), reverse=True)
    rv: Dict[str,Any] = {}
    if include_qq:
        rv['qq'] = compute_qq(qvals)
    rv['count'] = len(qvals)
    rv['gc_lambda'] = {}
    for perc in ['0.5', '0.1', '0.01', '0.001']:
        gc = gc_value_from_list(qvals, float(perc))
        if math.isnan(gc) or abs(gc) == math.inf:
            print('WARNING: got gc_value {!r}'.format(gc))
        else:
            rv['gc_lambda'][perc] = round_sig(gc, 5)
    return rv



def compute_qq(qvals:List[float]) -> Dict[str,Any]:
    # qvals must be in decreasing order.
    assert all(a >= b for a,b in boltons.iterutils.pairwise(qvals))

    if len(qvals) == 0 or qvals[0] == 0:
        return {}  # the js detects that the values for each key are undefined

    max_exp_qval = -math.log10(0.5 / len(qvals))
    # Our QQ plot will only show `obs_qval` up to `ceil(2*max_exp_pval)`.
    # So we can drop any obs_qval above that, to save space and make sure the visible range gets all the NUM_BINS.

    # this calculation must avoid dropping points that would be shown by the calculation done in javascript.
    # `max_obs_qval` means the largest observed -log10(pvalue) that will be shown in the plot. It's usually NOT the largest in the data.
    max_obs_qval = boltons.mathutils.clamp(qvals[0],
                                           lower = max_exp_qval,
                                           upper = math.ceil(2*max_exp_qval))
    if qvals[0] > max_obs_qval:
        for qval in qvals:
            if qval <= max_obs_qval:
                max_obs_qval = qval
                break

    occupied_bins = set()
    for i, obs_qval in enumerate(qvals):
        if obs_qval > max_obs_qval: continue
        exp_qval = -math.log10( (i+0.5) / len(qvals))
        exp_bin = int(exp_qval / max_exp_qval * NUM_BINS)
        # TODO: it'd be great if the `obs_bin`s started right at the lowest qval in that `exp_bin`.
        #       that way we could have fewer bins but still get a nice straight diagonal line without that stair-stepping appearance.
        obs_bin = int(obs_qval / max_obs_qval * NUM_BINS)
        occupied_bins.add( (exp_bin,obs_bin) )

    bins = []
    for exp_bin, obs_bin in occupied_bins:
        assert 0 <= exp_bin <= NUM_BINS, exp_bin
        assert 0 <= obs_bin <= NUM_BINS, obs_bin
        bins.append((
            exp_bin / NUM_BINS * max_exp_qval,
            obs_bin / NUM_BINS * max_obs_qval
        ))
    bins.sort()
    return {
        'bins': bins,
        'max_exp_qval': max_exp_qval,
    }


def gc_value_from_list(qvals:List[float], quantile:float = 0.5) -> float:
    # qvals must be in decreasing order.
    assert all(a >= b for a,b in boltons.iterutils.pairwise(qvals))
    qval = qvals[int(len(qvals) * quantile)]
    pval = 10 ** -qval
    return gc_value(pval, quantile)
def gc_value(pval:float, quantile:float = 0.5) -> float:
    # This should be equivalent to this R: `qchisq(median_pval, df=1, lower.tail=F) / qchisq(quantile, df=1, lower.tail=F)`
    return scipy.stats.chi2.ppf(1 - pval, 1) / scipy.stats.chi2.ppf(1 - quantile, 1)
assert approx_equal(gc_value(0.49), 1.047457) # I computed these using that R code.
assert approx_equal(gc_value(0.5), 1)
assert approx_equal(gc_value(0.50001), 0.9999533)
assert approx_equal(gc_value(0.6123), 0.5645607)



def get_confidence_intervals(num_variants:float, confidence:float = 0.95) -> Iterator[Dict[str,float]]:
    one_sided_doubt = (1-confidence) / 2

    # `variant_counts` are the numbers of variants at which we'll calculate the confidence intervals
    # any `1 <= variant_count <= num_variants-1` could be used, but we scale in powers of 2 to make the CI visually pretty smooth.
    variant_counts = []
    for x in range(0, int(math.ceil(math.log2(num_variants)))):
        variant_counts.append(2**x)
    variant_counts.append(num_variants-1)
    variant_counts.reverse()

    for variant_count in variant_counts:
        rv = scipy.stats.beta(variant_count, num_variants-variant_count)
        yield {
            'x': round(-math.log10((variant_count-0.5)/num_variants),2),
            'y_min': round(-math.log10(rv.ppf(1-one_sided_doubt)),2),
            'y_max': round(-math.log10(rv.ppf(one_sided_doubt)),2),
        }
