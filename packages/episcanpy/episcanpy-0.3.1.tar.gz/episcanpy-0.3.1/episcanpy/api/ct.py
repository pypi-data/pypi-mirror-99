from ..count_matrix._features import load_features, make_windows, size_feature_norm, plot_size_features, name_features
from ..count_matrix._features import load_features_gff, load_features_gtf
from ..count_matrix._load_input_file import read_cyt_summary
from ..count_matrix._bld_met_mtx import build_count_mtx
from ..count_matrix._atac_mtx import bld_atac_mtx, save_sparse_mtx
from ..count_matrix._load_met_ct_mtx import load_met_noimput
from ..count_matrix._peak_fct import load_peaks, norm_peaks

#from ..count_matrix._bld_atac_mtx2 import bld_mtx_fly


import platform
if platform.system() != "Windows":
    #Note pysam doesn't support Windows
    from ..count_matrix._bld_atac_mtx import bld_mtx_fly
    from ..count_matrix._bld_atac_mtx_parallel import bld_mtx_bed, bld_mtx_bed_per_chr
    #from ..count_matrix._bld_atac_mtx_parallel import bld_mtx_bed, as build_matrix