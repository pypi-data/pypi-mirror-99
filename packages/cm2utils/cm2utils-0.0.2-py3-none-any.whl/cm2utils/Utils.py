import os, errno
import  numpy
from scipy.linalg import qr

class Util:
    def __init__(self):
        pass
    def address_file(self, subDir, fileName):
        #region doc. string
        """Function to get the current file location.

        - If you change the location of the "Utils.py" file, you should revise this function.

        Parameters
            - subDir - :class:`String`. sub-directory.
            - fileName - :class:`String`. file name.
        
        Returns
            - R - :class:`String`. current path + subDir + fileName.
        """
        #endregion doc. string
        
        current_dir = os.path.dirname(__file__) #<kr> 파일이 있는 곳의 폴더.
        parent_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))
        #parent_dir = Path(current_dir).parent
        rel_path = subDir + "/" + fileName
        abs_path = os.path.join(parent_dir, rel_path)
        
        # ⬇︎ make directory if the directory does not exist.
        if not os.path.exists(os.path.dirname(abs_path)):
            try:
                os.makedirs(os.path.dirname(abs_path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        return abs_path

    def factorial(self, n):
        #region doc. string
        """factorial calculation

        Parameters
            - n - :class:`int`.
        
        Returns
            - R - :class:`int`.
        """
        #endregion doc. string
        if n == 0:
            return 1
        else:
            return n * self.factorial(n-1)


    def inducedK(self, m, n, s_k):
        #region doc. string
        """Calculating the K value for KD tree for Meshfree analysis

        Parameters
            - m - :class:`int`. Polynomial Order
            - n - :class:`int`. Problem Dimension
            - s_k - :class:`float`. Safe factor for K
        
        Returns
            - R - :class:`int`. Induced K value for KD tree
        """
        #endregion doc. string
        return int(s_k * self.factorial(m+n) / (self.factorial(m) * self.factorial(n)))


    def mldivide(self, A, b):
        #region doc. string
        """mldivide function (\ operator) of Matlab. (solving simultaneous equations (연립방정식) A*x = B)

        - ref site: https://pythonquestion.com/post/how-can-i-obtain-the-same-special-solutions-to-underdetermined-linear-systems-that-matlab-s-a-b-mldivide-operator-returns-using-numpy-scipy/
        - ref site: https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html#numpy.linalg.lstsq

        Parameters
            - [param1] - :class:`[type]`. [Description].
            - [param2] - :class:`[type]`. [Description].
        
        Returns
            - R1 ([value]) - :class:`[type]`. [Description]
            - R2 ([value]) - :class:`[type]`. [Description]
        """
        #endregion doc. string
        x1, res, rnk, s = numpy.linalg.lstsq(A, b)
        if rnk == A.shape[1]:
            return x1   # nothing more to do if A is full-rank
        Q, R, P = qr(A.T, mode='full', pivoting=True)
        Z = Q[:, rnk:].conj()
        C = numpy.linalg.solve(Z[rnk:], -x1[rnk:])
        return x1 + Z.dot(C)

