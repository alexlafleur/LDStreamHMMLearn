import numpy as np
import pyemma
import math
from pyemma.msm.models.msm import MSM as _MM
from msmtools.estimation import transition_matrix as _tm
from pyemma.util.linalg import mdot



class SpectralMM(_MM):
    """
    This class is for spectral MMs. which are MMs specified in terms of a
    particular Jordan decomposition of the
    transition matrix.
    """

    def __init__(self, transd, transu, transv=None, trans=None):
        """

       :param transd: ndarray - diagonal array, the Jordan form of the transition matrix
       :param transu: ndarray - the left eigenvector matrix of the transition matrix
       :param transv: ndarray (default=None) - inverse of transu, right eigenvector matrix
       :param trans: ndarray (default=None) - dot product transd * transu * transv, the transition matrix
       """

        assert len(transd.shape) is 2, "transd is not a matrix"
        assert len(transu.shape) is 2, "transu is not a matrix"
        assert transd.shape[0] is transd.shape[1], "transd is not square"
        assert transu.shape[0] is transu.shape[1], "transu is not square"
        assert transu.shape[0] is transd.shape[0], "transd and transu do not have the same number of rows"

        self.transD = transd
        # FIXME another case would be to pass in the right eigenvector matrix transV and then calculate transU
        self.transU = transu

        assert not np.isclose(np.linalg.det(transu), 0.0), "transu is not invertible"
        if transv is None:
            self.transV = np.linalg.inv(self.transU)
        else:
            # if the right eigenvector matrix is known, it can be passed in
            self.transV = transv
        if trans is None:
            # calculate the transition matrix by definition:
            # the right eigenvector matrix times the Jordan form times the left eigenvector matrix
            self.trans = _tm(np.dot(np.dot(self.transV, self.transD), self.transU))
        else:
            # if the transition matrix is known, it can be passed in
            self.trans = _tm(trans)
        # apply the MM constructor
        super(SpectralMM, self).__init__(self.trans)

    def isdiagonal(self):
        """
        returns whether the Jordan form of the transition matrix is diagonal

        :return: bool - True if the Jordan form of the transition matrix if diagonal, otherwise False
        """

        return np.allclose(self.transD, np.diag(np.diag(self.transD)))

    def lincomb(self, other, mu):
        """
        Constructs a matrix M that is a combination of self and other in the following sense:
        1) The eigenvalues (diagonal of transd) of M are the weighted geometric mean (https://en.wikipedia.org/wiki/Weighted_geometric_mean) of the eigenvalues of self and other 
        2) the left eigenvectors (rows of transu) of M are the weighted average (linear combination) of the left eigenvectors of self and other
        In each case the weights are (1-mu) and mu. Cases: 
          - When mu = 0, self is returned.
          - When mu = 1, other is returned.
          - When 0 < mu < 1, M is in some sense "between" self and other.
        The conditions above are not sufficient to define a unique matrix M.
        This implementation requires the matrices self and other to be diagonalizable and 
        provided as a Jordan decomposition.
        The weight mu is required to be between 0 and 1, inclusive.
        :param other: SpectralMM
        :param mu:
        :return: SpectralMM based on transd and transu
        
        """

        assert -1e-8 <= mu <= 1 + 1e-8, "weight is not between 0 and 1, inclusive"
        assert self.isdiagonal(), "self is not diagonal"
        assert other.isdiagonal(), "other is not diagonal"
        # FIXME check that both self and other have only positive eigenvalues less than or equal 1

        def lincc(x, y):
            return (1 - mu) * x + mu * y

        def logcc(x, y):
            return np.exp((1 - mu) * np.log(x) + mu * np.log(y))

        lincc = np.vectorize(lincc)
        logcc = np.vectorize(logcc)

        transd = np.diag(logcc(np.diag(self.transD), np.diag(other.transD)))
        transu = lincc(self.transU , other.transU)

        return SpectralMM(transd, transu)

    def scale(self, tau):
        """
        scales the Jordan form of the transition matrix (transd) by factor tau

        :param tau: scaling factor > 0
        :return: SpectralHMM based on scaled transd, transu and pobs
        """

        assert tau > 0, "scaling factor is not positive"
        assert self.isdiagonal(), "self is not diagonal"

        transd_scaled = np.diag(np.power(np.diag(self.transD), 1.0 / tau))
        return SpectralMM(transd_scaled, self.transU)

    def isclose(self, other):
        """
        returns if two SpectralMMs are close based on their transition matrices and observation probabilities

        :param other: SpectralMM
        :return: bool - True if the SpectralMMs are close to each other, otherwise False
        """

        return np.allclose(self.transition_matrix, other.transition_matrix)

    def simulate(self, N, start=None, dt=1, M=1):
        """
        ToDo Document HMM or MM?
        generates a realization of the Hidden Markov Model

        :param N: int  trajectory length in steps of the lag time
        :param start: int (default=None) - starting hidden state. If not given, will sample from the stationary
            distribution of the hidden transition matrix
        :param stop: int or int-array-like (default=None) - stopping hidden set. If given, the trajectory will be stopped before
            N steps once a hidden state of the stop set is reached
        :param dt: int - trajectory will be saved every dt time steps. Internally, the dt'th power of P is taken to ensure a more efficient simulation
        :return: ndarray - M discrete trajectories with length N/dt in a ndarray of shape (M, N/dt)

        """

        import msmtools.generation as msmgen
        # sample hidden trajectory
        dtraj = msmgen.generate_trajs(self.transition_matrix, M, N, start=start, stop=None, dt=dt)
        dtraj = np.asarray(dtraj)
        return dtraj


    def is_scalable_tm(self):
        """
        ToDo Document

        :param transd: ndarray - diagonal array
        :param transu: ndarray - left eigenvector matrix
        :param transv: ndarray (default=None) - inverse matrix of transu
        :return: bool - True if D*U*V is scalable, otherwise False
        """

        # For large scaling factors (tau), the scaling of the transition matrix approaches
        #
        #   I + (1/tau) ln(trans)
        #
        # This will be a  transition matrix for sufficiently large tau if
        #    1. all diagonal elements of ln(trans) are <= 0
        #    2. all off-diagonal elements ln(trans) are >= 0
        #
        # Therefore the matrix is called "scalable" if it satisfies these properties.
        #
        # The diagonal decomposition is used for a fast calculation of the natural log
        lntransd = np.diag(np.log(np.diag(self.transD)))
        delta = mdot(self.transV, lntransd, self.transU)
        # FIXME: This is not optimized, it does twice as many sign checks as necessary
        deltadiag = np.diag(delta)
        deltatril = np.tril(delta, -1)
        deltatriu = np.triu(delta, 1)
        if np.all(deltadiag <= 0) and np.all(deltatril >= 0) and np.all(deltatriu >= 0):
            return True
        else:

            return False
