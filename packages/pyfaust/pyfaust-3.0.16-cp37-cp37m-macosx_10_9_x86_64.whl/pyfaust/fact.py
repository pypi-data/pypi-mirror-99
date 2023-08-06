# -*- coding: utf-8 -*-
# ##########################################################################################
# Copyright (c) 2021, INRIA                                                              #
# All rights reserved.                                                                   #
#                                                                                        #
# BSD License 2.0                                                                        #
#                                                                                        #
# Redistribution and use in source and binary forms, with or without                     #
# modification, are permitted provided that the following conditions are met:            #
# * Redistributions of source code must retain the above copyright notice,               #
# this list of conditions and the following disclaimer.                                  #
# * Redistributions in binary form must reproduce the above copyright notice,            #
# this list of conditions and the following disclaimer in the documentation              #
# and/or other materials provided with the distribution.                                 #
# * Neither the name of the <copyright holder> nor the names of its contributors         #
# may be used to endorse or promote products derived from this software without          #
# specific prior written permission.                                                     #
#                                                                                        #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND        #
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED          #
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.     #
# IN NO EVENT SHALL INRIA BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,       #
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF     #
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) #
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,  #
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS  #
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.                           #
#                                                                                        #
# Contacts:                                                                              #
# 	Remi Gribonval  : remi.gribonval@inria.fr                                        #
# 	Hakim Hadj-dji. : hakim.hadj-djilani@inria.fr                                    #
#                                                                                        #
# Authors:                                                                               #
# 	Software Engineers:                                                              #
# 		Nicolas Bellot                                                           #
# 		Thomas Gautrais,                                                         #
# 		Hakim Hadj-Djilani,                                                      #
# 		Adrien Leman,                                                            #
#                                                                                        #
# 	Researchers:                                                                     #
# 		Luc Le Magoarou,                                                         #
# 		Remi Gribonval                                                           #
#                                                                                        #
# 	INRIA Rennes, FRANCE                                                             #
# 	http://www.inria.fr/                                                             #
##########################################################################################


## @package pyfaust.fact @brief The pyfaust factorization module
##
##    This module gives access to the main factorization algorithms of
##    FAuST. These algorithms can factorize a dense matrix into a sparse product
##    (i.e. a Faust object). A few of them are only available in experimental
##    packages.
##
##    There are several factorization algorithms.
##
##    - The first one is Palm4MSA :
##    which stands for Proximal Alternating Linearized Minimization for
##    Multi-layer Sparse Approximation. Note that Palm4MSA is not
##    intended to be used directly. You should rather rely on the second algorithm.
##
##    - The second one is the Hierarchical Factorization algorithm:
##    this is the central algorithm to factorize a dense matrix into a Faust.
##    It makes iterative use of Palm4MSA to proceed with the factorization of a given
##    dense matrix.
##
##    - The third group of algorithms is for approximate eigenvalue decomposition (eigtj) and singular value decomposition (svdtj).
##
##
##


import numpy as np, scipy
from scipy.io import loadmat
from scipy.sparse import csr_matrix, csc_matrix
import _FaustCorePy
import pyfaust
import pyfaust.factparams
from pyfaust import Faust
import _FaustCorePy
import warnings


def svdtj(M, nGivens=None, tol=0, order='ascend', relerr=True,
          nGivens_per_fac=None, enable_large_Faust=False, **kwargs):
    """
        Performs a singular value decomposition and returns the left and right singular vectors as Faust transforms.

        NOTE: this function is based on fact.eigtj. See below the example for further details on how svdtj is defined using eigtj.

        Args:
            M: a real matrix (np.ndarray or scipy.sparse.csr_matrix).
            nGivens: see fact.eigtj
            tol: see fact.eigtj (the error tolerance is not exactly for
            the svd but for the subsequent eigtj calls).
            relerr: see fact.eigtj
            nGivens_per_fac: see fact.eigtj


        Returns:
            The tuple U,S,V: such that U*numpy.diag(S)*V.H is the approximate of M.
                - (np.array vector) S the singular values in
                descending order.
                - (Faust objects) U,V unitary transforms.


        Examples:
            >>> from pyfaust.fact import svdtj
            >>> from numpy.random import rand
            >>> M = rand(128,128)
            >>> U,S,V = svdtj(M, 1024, nGivens_per_fac=64)

        If we call svdtj on the matrix M, it makes two internal calls to eigtj.

        In Python it would be:
        1.  D1, W1 = eigtj(M.dot(M.H), next_args...)
        2.  D2, W2 = eigtj(M.H.dot(M), next_args...)

        It gives the following equalities (ignoring the fact that eigtj computes approximations):
        \f[
            W_1 D_1 W_1^* = M M^*
        \f]
        \f[
                W_2 D_2 W_2^* = M^* M
        \f]
        But because of the SVD \f$ M = USV^* \f$ we also have:
        \f[MM^* = U S V^* V S U^* = U S^2 U^* = W_1 D_1 W_1^*\f]
        \f[M^* M = V S U^* U S V^* = V S^2 V^* = W_2 D_2  W_2^*\f]
        It allows to identify the left singular vectors of M to W1,
        and likewise the right singular vectors to W2.

        To compute a consistent approximation of S we observe that U and V are orthogonal/unitary hence \f$ S  = U^* M V \f$ so we ignore the off-diagonal coefficients of the approximation and take \f$ S = diag(U^* M V)  \approx diag(W_1^* M W_2)\f$

        The last step performed by svdtj() is to sort the singular values of S in descending order and build a signed permutation matrix to order the left singular vectors of W1 accordingly. The -1 elements of the signed permutation matrix allow to change the sign of each negative values of S by reporting it on the corresponding left singular vector (\f$ \sigma v_i = (-\sigma_i) (-v_i )\f$).
        To sum up W1 is replaced by W1 P and W2 by W2 abs(P) (because W2 also
        needs to be ordered), with P the signed permutation resulting of the
        descending sort of S. The resulting transforms/Fausts W1 and W2 are
        returned by svdtj along with the ordered S. Note that the permutation
        factor P (resp. abs(P)) is fused with the rightmost factor of the Faust
        object W1 (resp. W2).

     See also:
        eigtj
    """
    if(nGivens == None):
        if(tol == 0):
            raise Exception("You must specify nGivens or tol argument"
                            " (to define a stopping  criterion)")
        nGivens = 0
    if(nGivens_per_fac == None): nGivens_per_fac = int(M.shape[0]/2)
    if('verbosity' in kwargs.keys()):
        verbosity = kwargs['verbosity']
        if(not isinstance(verbosity, int)): raise TypeError('verbosity must be'
                                                            ' a int')
    else:
        verbosity = 0

    if(M.dtype == np.complex):
        if(isinstance(M, np.ndarray)):
            Ucore, S, Vcore =  _FaustCorePy.FaustFact.svdtj_cplx(M, nGivens, nGivens_per_fac, verbosity, tol, relerr, enable_large_Faust)
        elif(isinstance(M, csr_matrix)):
            Ucore, S, Vcore =  _FaustCorePy.FaustFact.svdtj_sparse_cplx(M, nGivens, nGivens_per_fac, verbosity, tol, relerr, enable_large_Faust)
    elif(isinstance(M, np.ndarray)):
        Ucore, S, Vcore =  _FaustCorePy.FaustFact.svdtj(M, nGivens, nGivens_per_fac, verbosity, tol, relerr, enable_large_Faust)
    elif(isinstance(M, csr_matrix)):
        Ucore, S, Vcore =  _FaustCorePy.FaustFact.svdtj_sparse(M, nGivens, nGivens_per_fac, verbosity, tol, relerr, enable_large_Faust)
    else:
        raise ValueError("invalid type for M (first argument): only np.ndarray "
                         "or scipy.sparse.csr_matrix are supported.")
    U = Faust(core_obj=Ucore)
    V = Faust(core_obj=Vcore)
    return U, S, V

def eigtj(M, nGivens=None, tol=0, order='ascend', relerr=True,
          nGivens_per_fac=None, verbosity=0, enable_large_Faust=False):
    """
    Performs an approximate eigendecomposition of M and returns the eigenvalues in W along with the corresponding normalized right eigenvectors (as the columns of the Faust object V).

    The output is such that V*numpy.diag(W)*V.H approximates M. V is a product
    of Givens rotations obtained by truncating the Jacobi algorithm.

    The trade-off between accuracy and complexity of V can be set through the
    parameters nGivens and tol that define the targeted number of Givens rotations
    and targeted error.

    Args:
        M: (numpy.ndarray or csr_matrix) the matrix to diagonalize. Must be
        real and symmetric, or complex hermitian. Can be in dense or sparse format.
        nGivens: (int) targeted number of Givens rotations (this argument is optional
        only if tol is set).
        tol: (float) the tolerance error at which the algorithm stops. The
        default value is zero so that stopping is based on reaching the
        targeted nGivens (this argument is optional only if nGivens is set).
        order: (int) order of eigenvalues, possible choices are ‘ascend,
        'descend' or 'undef' (to avoid a sorting operation and save some time).
        nGivens_per_fac: (int) targeted number of Givens rotations per factor
        of V. Must be an integer between 1 to floor(M.shape[0]/2) (the default
        value).
        relErr: (bool) the type of error used as stopping criterion.  True
        for the relative error norm(V*D*V'-M, 'fro')/norm(M, 'fro'), False
        for the absolute error norm(V*D*V'-M, 'fro').
        verbosity: (int) the level of verbosity. The greater the value the more
        info is displayed. It can be helpful to understand for example why the
        algorithm stopped before reaching the tol error or the number of Givens
        (nGivens).
        enable_large_Faust: (bool)  if true, it allows to compute a transform
        that doesn't worth it regarding its complexity compared to the matrix
        M. Otherwise by default, an exception is raised before the algorithm starts.


    Returns:
        The tuple (W,V):
           - W (numpy.ndarray) the vector of the approximate eigenvalues of M
           (in ascending order by default).
           - V the Faust object representing the approximate eigenvector
            transform. The column V[:, i] is the eigenvector
            corresponding to the eigenvalue W[i].

    Remarks:
        - When  ‘nGivens’ and ‘tol’ are used simultaneously, the number of Givens
        rotations in V may be smaller than specified by ‘nGivens’ if the error
        criterion is met first, and the achieved error may be larger than specified
        if ‘nGivens’ is reached first during the iterations of the truncated Jacobi
        algorithm.
        - When nGivens_per_fac > 1, all factors have exactly
        nGivens_per_fac except the leftmost one which may have fewer if the
        total number of Givens rotations is not a multiple of
        nGivens_per_fact

    References:
    [1]   Le Magoarou L., Gribonval R. and Tremblay N., "Approximate fast
    graph Fourier transforms via multi-layer sparse approximations",
    IEEE Transactions on Signal and Information Processing
    over Networks 2018, 4(2), pp 407-420
    <https://hal.inria.fr/hal-01416110>

    Example:
        >>> import numpy as np
        >>> from pyfaust.fact import eigtj
        >>> from scipy.io import loadmat
        >>> from os.path import sep
        >>> from pyfaust.demo import get_data_dirpath
        >>> from numpy.linalg import norm
        >>> # get a graph Laplacian to diagonalize
        >>> demo_path = sep.join((get_data_dirpath(),'Laplacian_256_community.mat'))
        >>> data_dict = loadmat(demo_path)
        >>> Lap = data_dict['Lap'].astype(np.float)
        >>> Dhat, Uhat = eigtj(Lap, nGivens=Lap.shape[0]*100, enable_large_Faust=True)
        >>> # Uhat is the Fourier matrix/eigenvectors approximation as a Faust
        >>> # (200 factors)
        >>> # Dhat the eigenvalues diagonal matrix approx.
        >>> print("err: ", norm(Lap-Uhat*np.diag(Dhat)*Uhat.H)/norm(Lap)) # about 6.5e-3
        >>> print(Uhat)
        >>> print(Dhat)
        >>> Dhat2, Uhat2 = eigtj(Lap, tol=0.01)
        >>> assert(norm(Lap-Uhat2*np.diag(Dhat2)*Uhat2.H)/norm(Lap) < .011)
        >>> # and then asking for an absolute error
        >>> Dhat3, Uhat3 = eigtj(Lap, tol=0.1, relerr=False)
        >>> assert(norm(Lap-Uhat3*np.diag(Dhat3)*Uhat3.H) < .11)
        >>> # now recompute Uhat2, Dhat2 but asking a descending order of eigenvalues
        >>> Dhat4, Uhat4 = eigtj(Lap, tol=0.01)
        >>> assert((Dhat4[::-1] == Dhat2[::]).all())
        >>> # and now with no sort
        >>> Dhat5, Uhat5 = eigtj(Lap, tol=0.01, order='undef')
        >>> assert((np.sort(Dhat5) == Dhat2).all())

    See also:
        svdtj
    """
    D, core_obj = _FaustCorePy.FaustFact.eigtj(M, nGivens, tol, relerr,
                                               nGivens_per_fac, verbosity, order,
                                               enable_large_Faust)
    return D, Faust(core_obj=core_obj)

def _check_fact_mat(funcname, M):
    if(not isinstance(M, np.ndarray)):
        raise Exception(funcname+" 1st argument must be a numpy ndarray.")
    if(not isinstance(M[0,0], np.complex) and not isinstance(M[0,0],
                                                            np.float)):
        raise Exception(funcname+" 1st argument must be a float or complex "
                        "ndarray.")
    #if(isinstance(M[0,0], np.complex)):
    #   raise Exception(funcname+" doesn't yet support complex matrix "
    #                   "factorization.")




def palm4msa(M, p, ret_lambda=False, backend=2016, on_gpu=False):
    """
    Factorizes the matrix M with Palm4MSA algorithm using the parameters set in p.

    Args:
        M: the numpy array to factorize.
        p: the ParamsPalm4MSA instance to define the algorithm parameters.
        ret_lambda: set to True to ask the function to return the scale factor (False by default).
        on_gpu: if True the GPU implementation is executed (this option applies only to 2020 backend).

    Returns:
        The Faust object resulting of the factorization.
        if ret_lambda == True then the function returns a tuple (Faust, lambda).

    Examples:
    >>> from pyfaust.fact import palm4msa
    >>> from pyfaust.factparams import ParamsPalm4MSA, ConstraintList, StoppingCriterion
    >>> import numpy as np
    >>> M = np.random.rand(500, 32)
    >>> cons = ConstraintList('splin', 5, 500, 32, 'normcol', 1.0, 32, 32)
    >>> # or alternatively using pyfaust.proj
    >>> # from pyfaust.proj import splin, normcol
    >>> # cons = [ splin((500,32), 5), normcol((32,32), 1.0)]
    >>> stop_crit = StoppingCriterion(num_its=200)
    >>> param = ParamsPalm4MSA(cons, stop_crit)
    >>> F = palm4msa(M, param)
    >>> F
    Faust size 500x32, density 0.22025, nnz_sum 3524, 2 factor(s):
    FACTOR 0 (real) SPARSE, size 500x32, density 0.15625, nnz 2500
    FACTOR 1 (real) SPARSE, size 32x32, density 1, nnz 1024
    """
    if(not isinstance(p, pyfaust.factparams.ParamsPalm4MSA)):
        raise TypeError("p must be a ParamsPalm4MSA object.")
    _check_fact_mat('palm4msa()', M)
    if(not p.is_mat_consistent(M)):
        raise ValueError("M's number of columns must be consistent with "
                         "the last residuum constraint defined in p. "
                         "Likewise its number of rows must be consistent "
                         "with the first factor constraint defined in p.")
    if(backend == 2016):
        if on_gpu: raise ValueError("on_gpu applies only on 2020 backend.")
        core_obj, _lambda = _FaustCorePy.FaustFact.fact_palm4msa(M, p)
    elif(backend == 2020):
        full_gpu = True if on_gpu else False # partial gpu impl. disabled in wrapper
        core_obj, _lambda = _FaustCorePy.FaustFact.palm4msa2020(M, p, on_gpu,
                                                                full_gpu)
    else:
        raise ValueError("Unknown backend (only 2016 and 2020 are available).")
    F = Faust(core_obj=core_obj)
    if(ret_lambda):
        return F, _lambda
    else:
        return F


def hierarchical(M, p, ret_lambda=False, ret_params=False, backend=2016,
                 on_gpu=False):
    """
    Factorizes the matrix M with Hierarchical Factorization using the parameters set in p.
    @note This function has its shorthand pyfaust.faust_fact(). For
    convenience you might use it like this:
            
            from pyfaust import *;
            F = faust_fact(M, p) # equiv. to hierarchical(M, p)
            

    Args:
        M: the numpy array to factorize.
        p: is a set of factorization parameters. It might be a fully defined instance of parameters (pyfaust.factparams.ParamsHierarchical) or a simplified expression which designates a pre-defined parametrization:
            - 'squaremat' to use pre-defined parameters typically used to factorize a Hadamard square matrix of order a power of two (see pyfaust.demo.hadamard).
            - ['rectmat', j, k, s] to use pre-defined parameters used for
            instance in factorization of the MEG matrix which is a rectangular
            matrix of size m*n such that m < n (see pyfaust.demo.bsl); j is the
            number of factors, k the sparsity of the main factor's columns, and
            s the sparsity of rows for all other factors except the residuum
            (that is the first factor here because the factorization is made
            toward the left -- is_side_fact_left == true, cf.
            pyfaust.factparams.ParamsHierarchical and pyfaust.factparams.ParamsHierarchicalRectMat).
            The residuum has a sparsity of P*rho^(num_facts-1).  By default, rho == .8 and P = 1.4. It's possible to set custom values with for example p == ( ['rectmat', j, k, s], {'rho':.4, 'P':.7 }). The sparsity is here the number of non-zero elements.
        backend: the C++ implementation to use (default to 2016, 2020 backend
        should be quicker for certain configurations - e.g. factorizing a
        Hadamard matrix).
        on_gpu: if True the GPU implementation is executed (this option applies only to 2020 backend).

        ret_lambda: set to True to ask the function to return the scale factor (False by default).
        ret_params: set to True to ask the function to return the
        ParamsHierarchical instance used (False by default).
        It is useful for consulting what precisely means the
        simplified parametrizations used to generate a
        ParamsHierarchical instance and possibly adjust its attributes to factorize again.


    Returns:
        F the Faust object result of the factorization.
        if ret_lambda == True (and ret_params == False), then the function
        returns the tuple (F,_lambda) (_lambda is the scale factor at the
        end of factorization).
        if ret_params == True (and ret_lambda == False), then the function
        returns the tuple (F, p) (p being the ParamsHierarchical
        instance really used by the algorithm).
        if ret_lambda == True and ret_params == True, then the function
        returns the tuple (F, _lambda, p).

    Examples:
         1. Fully Defined Parameters for a Random Matrix Factorization 
        >>> from pyfaust.fact import hierarchical
        >>> from pyfaust.factparams import ParamsHierarchical, ConstraintList, StoppingCriterion
        >>> import numpy as np
        >>> M = np.random.rand(500, 32)
        >>> fact_cons = ConstraintList('splin', 5, 500, 32, 'sp', 96, 32, 32, 'sp', 96, 32, 32)
        >>> res_cons = ConstraintList('normcol', 1, 32, 32, 'sp', 666, 32, 32, 'sp', 333, 32, 32)
        >>> # or alternatively using pyfaust.proj
        >>> # from pyfaust.proj import *
        >>> # res_cons = [normcol((32,32), 1), sp((32,32), 666), sp((32,32), 333)]
        >>> stop_crit1 = StoppingCriterion(num_its=200)
        >>> stop_crit2 = StoppingCriterion(num_its=200)
        >>> param = ParamsHierarchical(fact_cons, res_cons, stop_crit1, stop_crit2)
        >>> F = hierarchical(M, param)
        Faust::HierarchicalFact<FPP,DEVICE>::compute_facts : factorization
        1/3
        Faust::HierarchicalFact<FPP,DEVICE>::compute_facts : factorization
        2/3
        Faust::HierarchicalFact<FPP,DEVICE>::compute_facts : factorization
        3/3
        >>> F
        Faust size 500x32, density 0.189063, nnz_sum 3025, 4 factor(s):
            - FACTOR 0 (real) SPARSE, size 500x32, density 0.15625, nnz 2500
            - FACTOR 1 (real) SPARSE, size 32x32, density 0.09375, nnz 96
            - FACTOR 2 (real) SPARSE, size 32x32, density 0.09375, nnz 96
            - FACTOR 3 (real) SPARSE, size 32x32, density 0.325195, nnz 333

        2. Simplified Parameters for Hadamard Factorization

        >>> from pyfaust import wht
        >>> from pyfaust.fact import hierarchical
        >>> from numpy.linalg import norm
        >>> # generate a Hadamard Faust of size 32x32
        >>> FH = wht(32)
        >>> H = FH.toarray() # the full matrix version
        >>> # factorize it
        >>> FH2 = hierarchical(H, 'squaremat');
        >>> # test the relative error
        >>> (FH-FH2).norm('fro')/FH.norm('fro') # the result is about 1e-16, the factorization is accurate
        >>> FH
        Faust size 32x32, density 0.3125, nnz_sum 320, 5 factor(s):
        - FACTOR 0 (real) SPARSE, size 32x32, density 0.0625, nnz 64
        - FACTOR 1 (real) SPARSE, size 32x32, density 0.0625, nnz 64
        - FACTOR 2 (real) SPARSE, size 32x32, density 0.0625, nnz 64
        - FACTOR 3 (real) SPARSE, size 32x32, density 0.0625, nnz 64
        - FACTOR 4 (real) SPARSE, size 32x32, density 0.0625, nnz 64

        >>> FH2
        Faust size 32x32, density 0.3125, nnz_sum 320, 5 factor(s):
            - FACTOR 0 (real) SPARSE, size 32x32, density 0.0625, nnz 64
            - FACTOR 1 (real) SPARSE, size 32x32, density 0.0625, nnz 64
            - FACTOR 2 (real) SPARSE, size 32x32, density 0.0625, nnz 64
            - FACTOR 3 (real) SPARSE, size 32x32, density 0.0625, nnz 64
            - FACTOR 4 (real) SPARSE, size 32x32, density 0.0625, nnz 64

        3. Simplified Parameters for a Rectangular Matrix Factorization
       (the BSL demo MEG matrix)
       >>> from pyfaust import *
       >>> from pyfaust.fact import hierarchical
       >>> from scipy.io import loadmat
       >>> from pyfaust.demo import get_data_dirpath
       >>> d = loadmat(get_data_dirpath()+'/matrix_MEG.mat')
       >>> MEG = d['matrix'].T
       >>> num_facts = 9
       >>> k = 10
       >>> s = 8
       >>> MEG16 = hierarchical(MEG, ['rectmat', num_facts, k, s])
       >>> MEG16
       Faust size 204x8193, density 0.0631655, nnz_sum 105573, 9 factor(s):
           - FACTOR 0 (real) SPARSE, size 204x204, density 0.293613, nnz
           12219
           - FACTOR 1 (real) SPARSE, size 204x204, density 0.0392157, nnz
           1632
           - FACTOR 2 (real) SPARSE, size 204x204, density 0.0392157, nnz
           1632
           - FACTOR 3 (real) SPARSE, size 204x204, density 0.0392157, nnz
           1632
           - FACTOR 4 (real) SPARSE, size 204x204, density 0.0392157, nnz
           1632
           - FACTOR 5 (real) SPARSE, size 204x204, density 0.0392157, nnz
           1632
           - FACTOR 6 (real) SPARSE, size 204x204, density 0.0392157, nnz
           1632
           - FACTOR 7 (real) SPARSE, size 204x204, density 0.0392157, nnz
           1632
           - FACTOR 8 (real) SPARSE, size 204x8193, density 0.0490196, nnz
           81930

       >>> # verify the constraint k == 10, on column 4
       >>> count_nonzero(MEG16.factors(8)[:,4].toarray())
       10
       >>> # now verify the s constraint is respected on MEG16 factor 1
       >>> count_nonzero(MEG16.factors(1).toarray())/MEG16.shape[0]
       8.0

        See also pyfaust.factparams.ParamsHierarchicalRectMat

    """
    p = _prepare_hierarchical_fact(M,p, "hierarchical", ret_lambda,
                              ret_params)
    if(backend == 2016):
        if on_gpu: raise ValueError("on_gpu applies only on 2020 backend.")
        core_obj,_lambda = _FaustCorePy.FaustFact.fact_hierarchical(M, p)
    elif(backend == 2020):
        full_gpu = True if on_gpu else False # partial gpu impl. disabled in wrapper
        core_obj, _lambda = _FaustCorePy.FaustFact.hierarchical2020(M, p,
                                                                    on_gpu,
                                                                    full_gpu)
    else:
        raise ValueError("backend must be 2016 or 2020")
    F = Faust(core_obj=core_obj)
    ret_list = [ F ]
    if(ret_lambda):
        ret_list += [ _lambda ]
    if(ret_params):
        ret_list += [ p ]
    if(ret_lambda or ret_params):
        return ret_list
    else:
        return F


def _prepare_hierarchical_fact(M, p, callee_name, ret_lambda, ret_params,
                               M_name='M'):
    """
    Utility func. for hierarchical() and fgft_palm().
    Among other checkings, it sets parameters from simplified ones.
    """
    from pyfaust.factparams import (ParamsHierarchical,
                                    ParamsFactFactory)
    if(not isinstance(p, ParamsHierarchical) and
       ParamsFactFactory.is_a_valid_simplification(p)):
        p = ParamsFactFactory.createParams(M, p)
    if(not isinstance(p, ParamsHierarchical)):
        raise TypeError("p must be a ParamsHierarchical object.")
    _check_fact_mat(''+callee_name+'()', M)
    if(not isinstance(ret_lambda, bool)):
        raise TypeError("ret_lambda must be a bool.")
    if(not isinstance(ret_params, bool)):
        raise TypeError("ret_params must be a bool.")
    if(not p.is_mat_consistent(M)):
        raise ValueError("M's number of columns must be consistent with "
                         "the last residuum constraint defined in p. "
                         "Likewise its number of rows must be consistent "
                         "with the first factor constraint defined in p.")
    return p



