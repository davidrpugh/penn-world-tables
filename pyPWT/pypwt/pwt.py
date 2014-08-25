class PWT(object):

    def __init__(self, index1='geks', index2='gk', bm=None, chn='pwt', norm=False):
        """
        Create an instance of the PWT class.

        Attributes
        ----------

        index1 : string, optional (default='geks')
            Determines aggregation method for aggregating basic headings. Must
            be one of either 'geks' or 'gk'.
        index2 : string, optional (default='gk')
            Determines aggregation method for aggregating main expenditure
            categories. Must be one of either set to 'geks' or 'gk'.
        bm : int, optional (default=None)
            By default, use all available benchmark data. Set to 2005 to keep
            only 2005 benchmark results (mimicking PWTv7); alternative values:
            1970, 1975, 1980, 1985 and 1996.
        chn : string, optional (default='pwt')
            Set to "pwt" for adjusted basic headings and NA time series; set to
            "icp" for original basic headings and NA time series.
        norm : bool, optional (default=False)
            Set to False to normalise to USA=GDP deflator; set to True to
            normalise to USA=1 in every year.

        Notes
        -----
        Default values should recreate Penn World Tables (PWT) version 8.0.

        """
        self.index1 = index1
        self.index2 = index2
        self.bm = bm
        self.chn = chn
        self.norm = norm

    @property
    def index1(self):
        return self._index1

    @index1.setter
    def index1(self, value):
        self._index1 = value

    @property
    def index2(self):
        return self._index2

    @index2.setter
    def index2(self, value):
        self._index2 = value

    @property
    def bm(self):
        return self._bm

    @bm.setter
    def bm(self, value):
        self._bm = value

    @property
    def chn(self):
        return self._chn

    @chn.setter
    def chn(self, value):
        self._chn = value

    @property
    def norm(self):
        return self._norm

    @norm.setter
    def norm(self, value):
        self._norm = value
    