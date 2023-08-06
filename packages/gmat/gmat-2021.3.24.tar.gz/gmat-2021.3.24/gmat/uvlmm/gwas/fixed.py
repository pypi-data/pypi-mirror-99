import logging
import numpy as np
import pandas as pd
from scipy import linalg
from pysnptools.snpreader import Bed
from tqdm import tqdm
from gmat.process_plink.process_plink import impute_geno
from scipy.stats import chi2


def fixed(pheno_file, bed_file, agmat_file, out_file='res.txt', npart=20):
    """
    run GWAS based on linear mixed model and put one snp in each analysis.
    :param pheno_file: phenotypic file. The fist column is individual id . The second column is always a column of 1s
    for population mean. The last column is phenotypic values. The other covariates can be added between columns for
    population mean and phenotypic values. Missing values in the phenotypic file can be
    expressed as 'NA', 'NaN', 'nan' or 'na'.
    :param bed_file: the prefix for the plink binary file.
    :param agmat_file: the prefix for the additive genomic relationship matrix file.
    :param out_file: the output file. Default is 'res.txt'.
    :param npart: divide the SNPs into n parts. Default is 20.
    :return:
    """
    logging.info("###Prepare the phenotypic values, covariates and genomic matrix")
    y, xmat, ag, id_keep = _pre_pheno(pheno_file, agmat_file)
    logging.info("###Estimate the variances in the null model.")
    init = np.array([np.var(y) / 2] * 2)
    gmat_eigenvals, gmat_eigenvecs = linalg.eigh(ag)
    gmat_eigenvals = np.array(gmat_eigenvals).reshape(-1, 1)
    y_trans = np.dot(gmat_eigenvecs.T, y)  # transform the phenotypic values
    xmat_trans = np.dot(gmat_eigenvecs.T, xmat)  # transform the fixed effects
    var, convergence = _weight_emai_eigen(y_trans, xmat_trans, gmat_eigenvals, init=init, maxiter=100, cc=1.0e-8)
    logging.info('Whether converge?: {}'.format(convergence))
    logging.info('The estimated variances: {}'.format(var))
    snp_on_disk = Bed(bed_file, count_A1=False)
    num_snp = snp_on_disk.sid_count
    fam_df = pd.read_csv(bed_file + '.fam', header=None, sep='\s+')
    id_in_fam = list(np.array(fam_df.iloc[:, 1], dtype=np.str))
    id_keep_ind = []
    for val in id_keep:
        id_keep_ind.append(id_in_fam.index(val))
    snp_index = []
    for i in range(npart):
        snp_index.append(int(num_snp / npart) * i)
    snp_index.append(num_snp)
    logging.info('###Start the association')
    with open(out_file, 'w') as fout:
        fout.write('\t'.join(['chro', 'snp_ID', 'pos', 'allele1', 'allele2', 'cc', 'eff', 'se', 'p_wald']))
        fout.write('\n')
    maxiter = 100
    if not convergence:
        maxiter = 0
    for i in range(npart):
        logging.info('The {}/{} part'.format(i+1, npart))
        snp_info = pd.read_csv(bed_file + '.bim', sep='\s+', header=None, skiprows=snp_index[i],
                               nrows=snp_index[i+1]-snp_index[i])
        res_df = snp_info.iloc[:, [0, 1, 3, 4, 5]]
        res_df.columns = ['chro', 'snp_ID', 'pos', 'allele1', 'allele2']
        snp_mat = snp_on_disk[id_keep_ind, snp_index[i]:snp_index[i + 1]].read().val
        if np.any(np.isnan(snp_mat)):
            snp_mat = impute_geno(snp_mat)
        cc_vec = []
        eff_vec = []
        se_vec = []
        p_vec = []
        for k in tqdm(range(snp_mat.shape[1])):
            snpk = np.dot(gmat_eigenvecs.T, snp_mat[:, k:(k+1)])
            xmat_trans_k = np.concatenate([xmat_trans, snpk], axis=1)
            cc_val, snp_eff, se, p_val = _weight_emai_eigen_snp(y_trans, xmat_trans_k, gmat_eigenvals, var,
                                                                     maxiter=maxiter, cc=1.0e-8)
            cc_vec.append(cc_val)
            eff_vec.append(snp_eff)
            se_vec.append(se)
            p_vec.append(p_val)
        res_df.loc[:, 'cc_val'] = cc_vec
        res_df.loc[:, 'eff_val'] = eff_vec
        res_df.loc[:, 'se_val'] = se_vec
        res_df.loc[:, 'p_val'] = p_vec
        res_df.to_csv(out_file, sep='\t', index=False, header=False, mode='a')
    return 0


def _pre_pheno(pheno_file, agmat_file):
    id_in_agmat = []
    with open(agmat_file + '.id') as fin:
        for line in fin:
            arr = line.split()
            id_in_agmat.append(arr[0])
    y = []
    xmat = []
    id_keep = []  # keep the id both in the agmat file and pheno file, without missing phenotypes and covariates.
    with open(pheno_file) as fin:
        for line in fin:
            arr = line.split()
            if arr[0] in id_in_agmat:
                try:
                    vec = np.array(arr[1:], dtype=float)
                    y.append(vec[-1])
                    xmat.append(vec[:-1])
                    id_keep.append(arr[0])
                except Exception as e:
                    del e
    y = np.array(y).reshape(-1, 1)
    xmat = np.array(xmat)
    id_dct = dict(zip(id_keep, range(len(id_keep))))
    ag = np.zeros((len(id_keep), len(id_keep)))
    with open(agmat_file + '.agrm.id_fmt') as fin:
        for line in fin:
            arr = line.split()
            try:
                ag[id_dct[arr[0]], id_dct[arr[1]]] = ag[id_dct[arr[1]], id_dct[arr[0]]] = float(arr[2])
            except Exception as e:
                del e
    return y, xmat, ag, id_keep


def _weight_emai_eigen(y_trans, xmat_trans, gmat_eigenvals, init=None, maxiter=100, cc=1.0e-8):
    fd_mat = np.zeros(2)
    ai_mat = np.zeros((2, 2))
    em_mat = np.zeros((2, 2))
    num_id = gmat_eigenvals.shape[0]
    cc_val = 1000.0
    var = np.array(init)
    var_update = var * 1000
    delta = var_update - var
    convergence = False
    for i in range(maxiter):
        logging.info("Iteration: {}".format(i+1))
        vmat = 1.0 / (gmat_eigenvals * var[0] + var[1])
        vx = np.multiply(vmat, xmat_trans)
        xvx = np.dot(xmat_trans.T, vx)
        xvx = linalg.inv(xvx)
        # py
        xvy = np.dot(vx.T, y_trans)
        y_xb = y_trans - np.dot(xmat_trans, np.dot(xvx, xvy))
        py = np.multiply(vmat, y_xb)
        # add_py p_add_py
        add_py = np.multiply(gmat_eigenvals, py)
        xvy = np.dot(vx.T, add_py)
        y_xb = add_py - np.dot(xmat_trans, np.dot(xvx, xvy))
        p_add_py = np.multiply(vmat, y_xb)
        # res_py p_res_py
        res_py = py.copy()
        xvy = np.dot(vx.T, res_py)
        y_xb = res_py - np.dot(xmat_trans, np.dot(xvx, xvy))
        p_res_py = np.multiply(vmat, y_xb)
        # fd
        tr_vd = np.sum(np.multiply(vmat, gmat_eigenvals))
        xvdvx = np.dot(xmat_trans.T, vmat * gmat_eigenvals * vx)
        tr_2d = np.sum(np.multiply(xvdvx, xvx))
        ypvpy = np.sum(np.dot(py.T, add_py))
        fd_mat[0] = 0.5 * (-tr_vd + tr_2d + ypvpy)
        tr_vd = np.sum(vmat)
        xvdvx = np.dot(xmat_trans.T, vmat * vx)
        tr_2d = np.sum(np.multiply(xvdvx, xvx))
        ypvpy = np.sum(np.dot(py.T, res_py))
        fd_mat[1] = 0.5 * (-tr_vd + tr_2d + ypvpy)
        # AI
        ai_mat[0, 0] = np.sum(np.dot(add_py.T, p_add_py))
        ai_mat[0, 1] = ai_mat[1, 0] = np.sum(np.dot(add_py.T, p_res_py))
        ai_mat[1, 1] = np.sum(np.dot(res_py.T, p_res_py))
        ai_mat = 0.5 * ai_mat
        # EM
        em_mat[0, 0] = num_id / (2 * var[0] * var[0])
        em_mat[1, 1] = num_id / (2 * var[1] * var[1])
        for j in range(0, 51):
            gamma = j * 0.02
            wemai_mat = (1 - gamma) * ai_mat + gamma * em_mat
            delta = np.dot(linalg.inv(wemai_mat), fd_mat)
            var_update = var + delta
            if min(var_update) > 0:
                logging.info('EM weight value: {}'.format(gamma))
                break
        # Convergence criteria
        logging.info('Updated variances: {}'.format(var_update))
        cc_val = np.sum(pow(delta, 2)) / np.sum(pow(var_update, 2))
        cc_val = np.sqrt(cc_val)
        var = var_update.copy()
        logging.info("CC: {}".format(cc_val))
        if cc_val < cc:
            break
    if cc_val < cc:
        convergence = True
    return var, convergence


def _weight_emai_eigen_snp(y_trans, xmat_trans, gmat_eigenvals, var, maxiter=20, cc=1.0e-8):
    fd_mat = np.zeros(2)
    ai_mat = np.zeros((2, 2))
    em_mat = np.zeros((2, 2))
    num_id = gmat_eigenvals.shape[0]
    var_update = var * 1000
    delta = var_update - var
    cc_val = 1000.0
    for i in range(maxiter):
        # logging.info("Iteration: {}".format(i+1))
        vmat = 1.0 / (gmat_eigenvals * var[0] + var[1])
        vx = np.multiply(vmat, xmat_trans)
        xvx = np.dot(xmat_trans.T, vx)
        xvx = linalg.inv(xvx)
        # py
        xvy = np.dot(vx.T, y_trans)
        y_xb = y_trans - np.dot(xmat_trans, np.dot(xvx, xvy))
        py = np.multiply(vmat, y_xb)
        # add_py p_add_py
        add_py = np.multiply(gmat_eigenvals, py)
        xvy = np.dot(vx.T, add_py)
        y_xb = add_py - np.dot(xmat_trans, np.dot(xvx, xvy))
        p_add_py = np.multiply(vmat, y_xb)
        # res_py p_res_py
        res_py = py.copy()
        xvy = np.dot(vx.T, res_py)
        y_xb = res_py - np.dot(xmat_trans, np.dot(xvx, xvy))
        p_res_py = np.multiply(vmat, y_xb)
        # fd
        tr_vd = np.sum(np.multiply(vmat, gmat_eigenvals))
        xvdvx = np.dot(xmat_trans.T, vmat * gmat_eigenvals * vx)
        tr_2d = np.sum(np.multiply(xvdvx, xvx))
        ypvpy = np.sum(np.dot(py.T, add_py))
        fd_mat[0] = 0.5 * (-tr_vd + tr_2d + ypvpy)
        tr_vd = np.sum(vmat)
        xvdvx = np.dot(xmat_trans.T, vmat * vx)
        tr_2d = np.sum(np.multiply(xvdvx, xvx))
        ypvpy = np.sum(np.dot(py.T, res_py))
        fd_mat[1] = 0.5 * (-tr_vd + tr_2d + ypvpy)
        # AI
        ai_mat[0, 0] = np.sum(np.dot(add_py.T, p_add_py))
        ai_mat[0, 1] = ai_mat[1, 0] = np.sum(np.dot(add_py.T, p_res_py))
        ai_mat[1, 1] = np.sum(np.dot(res_py.T, p_res_py))
        ai_mat = 0.5 * ai_mat
        # EM
        em_mat[0, 0] = num_id / (2 * var[0] * var[0])
        em_mat[1, 1] = num_id / (2 * var[1] * var[1])
        for j in range(0, 51):
            gamma = j * 0.02
            wemai_mat = (1 - gamma) * ai_mat + gamma * em_mat
            delta = np.dot(linalg.inv(wemai_mat), fd_mat)
            var_update = var + delta
            if min(var_update) > 0:
                # logging.info('EM weight value: {}'.format(gamma))
                break
        # Convergence criteria
        # logging.info('Updated variances: {}'.format(var_update))
        cc_val = np.sum(pow(delta, 2)) / np.sum(pow(var_update, 2))
        cc_val = np.sqrt(cc_val)
        var = var_update.copy()
        # logging.info("CC: {}".format(cc_val))
        if cc_val < cc:
            break
    vmat = 1.0 / (gmat_eigenvals * var[0] + var[1])
    vx = np.multiply(vmat, xmat_trans)
    xvx = np.dot(xmat_trans.T, vx)
    xvx = linalg.inv(xvx)
    # py
    xvy = np.dot(vx.T, y_trans)
    b_hat = np.dot(xvx, xvy)
    snp_eff = b_hat[-1, -1]
    se = np.sqrt(xvx[-1, -1])
    t_val = snp_eff / se
    p_val = chi2.sf(t_val*t_val, 1)
    return cc_val, snp_eff, se, p_val



if __name__=='__main__':
    import logging
    import os
    from gmat.gmatrix import agmat
    logging.basicConfig(level=logging.INFO)
    pheno_file = '/nfs1/ningc/WORK/Acode/GMAT/PKG/examples/data/mouse/pheno'
    bed_file = '/nfs1/ningc/WORK/Acode/GMAT/PKG/examples/data/mouse/plink'
    # id-id-value form
    agmat_file = '/nfs1/ningc/WORK/Acode/GMAT/PKG/examples/data/mouse/test'
    agmat2 = agmat(bed_file, out_file=agmat_file, inv=False, small_val=0.001, out_fmt='id_id_val')
    fixed(pheno_file, bed_file, agmat_file,
               out_file='/nfs1/ningc/WORK/Acode/GMAT/PKG/examples/data/mouse/res.txt', npart=1)
