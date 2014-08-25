import types


class PWT(object):

    def __init__(self, index1='geks', index2='gk', bm='all', chn='pwt', norm=False):
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
        bm : string or int, optional (default='all')
            By default, use all available benchmark data. Set to 2005 to keep
            only 2005 benchmark results (mimicking PWT version 7.x);
            alternative values: 1970, 1975, 1980, 1985 and 1996.
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
        self._index1 = self._validate_index(value)

    @property
    def index2(self):
        return self._index2

    @index2.setter
    def index2(self, value):
        self._index2 = self._validate_index(value)

    def _validate_index(self, value):
        """Validate the index1 and index2 attribute values."""
        if not isinstance(value, types.StringType):
            mesg = "Attribute type must be a string, not a {}"
            raise AttributeError(mesg.format(value.__class__))
        if value not in ['geks', 'gk']:
            mesg = "Attribute must be one of 'geks' or 'gk', not {}"
            raise AttributeError(mesg.format(value))
        else:
            return value

    @property
    def bm(self):
        return self._bm

    @bm.setter
    def bm(self, value):
        self._bm = self._validate_bm(value)

    def _validate_bm(self, value):
        """Validate the bm attribute value."""
        valid_bms = ['all', 1970, 1975, 1980, 1985, 1996]
        if not isinstance(value, (types.IntType, types.StringType)):
            mesg = "Attribute type must be an int or string, not a {}"
            raise AttributeError(mesg.format(value.__class__))
        if value not in valid_bms:
            mesg = "Attribute must be one of " + str(valid_bms) + ", not {}"
            raise AttributeError(mesg.format(value))
        else:
            return value

    @property
    def chn(self):
        return self._chn

    @chn.setter
    def chn(self, value):
        self._chn = value

    def _validate_chn(self, value):
        """Validate the chn attribute value."""
        if not isinstance(value, types.StringType):
            mesg = "Attribute type must be a string, not a {}"
            raise AttributeError(mesg.format(value.__class__))
        if value not in ['pwt', 'icp']:
            mesg = "Attribute must be one of 'pwt' or 'icp', not {}"
            raise AttributeError(mesg.format(value))
        else:
            return value

    @property
    def norm(self):
        return self._norm

    @norm.setter
    def norm(self, value):
        self._norm = self._validate_norm(value)

    def _validate_norm(self, value):
        """Validate the norm attribute value."""
        if not isinstance(value, types.BooleanType):
            mesg = "Attribute type must be a boolean, not a {}"
            raise AttributeError(mesg.format(value.__class__))
        if value not in [True, False]:
            mesg = "Attribute must be one of True or False, not {}"
            raise AttributeError(mesg.format(value))
        else:
            return value
