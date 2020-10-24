
from datetime_ACH import Date_Time as dt


class FileHeader:
    def __init__(self, destination='011000015', origin='067016574',
                 destination_name='Federal Reserve Bank', origin_name='Professional Bank'):
        """
        destination and origin are both routing numbers.
        destination must have a leading blank
        origin must have a leading one
        """
        self.destination = destination
        self.origin = origin
        self.destination_name = destination_name
        self.origin_name = origin_name

    @property
    def RecordType(self):
        return '1'

    @property
    def PriorityCode(self):
        return '01'

    @property
    def ImmediateDest(self):
        new_dest = ' ' + self.destination
        return new_dest

    @property
    def ImmediateOrig(self):
        new_orig = '1' + self.origin
        return new_orig

    @property
    def FileCreate(self):
        DT = dt()
        date = DT.create_date()
        return date

    @property
    def FileTime(self):
        DT = dt()
        time = DT.fh_create_time()
        return time

    @property
    def Modifier(self):
        return 'A'

    @property
    def Size(self):
        return '094'

    @property
    def Factor(self):
        return '10'

    @property
    def Format(self):
        return '1'

    @property
    def DestinationName(self):
        a = 23 - len(self.destination_name)
        b = ' ' * a
        new_name = self.destination_name + b
        return new_name

    @property
    def OriginName(self):
        a = 23 - len(self.origin_name)
        b = ' ' * a
        new_name = self.origin_name + b
        return new_name

    @property
    def Reference(self):
        return ' ACH GEN'

    def line_create(self):
        a = self.RecordType
        b = self.PriorityCode
        c = self.ImmediateDest
        d = self.ImmediateOrig
        e = self.FileCreate
        f = self.FileTime
        g = self.Modifier
        h = self.Size
        i = self.Factor
        j = self.Format
        k = self.DestinationName
        l = self.OriginName
        m = self.Reference
        val = [a, b, c, d, e, f, g, h, i, j, k, l, m]
        return ''.join(val)


