from file_formatting import BatchHeader
from tools.resources import *

class BatchControl:
    def __init__(self, bh=BatchHeader, entryCount='2', entryHash='422745543', totalDebit='$1,999.68', totalCredit='$1999.68',):
        self.bh = bh
        self.entryCount = str(entryCount)
        self.entryHash = str(entryHash)
        self.totalDebit = str(totalDebit)
        self.totalCredit = str(totalCredit)

    @property
    def RecordType(self):
        '''
        len 8
        :return:
        '''
        return '8'

    @property
    def ServiceClass(self):
        '''
        len 3
        :return:
        '''
        return self.bh.ServiceClass

    @property
    def EntryCount(self):
        '''
        len 6
        :return:
        '''
        return pad_zeros(6, self.entryCount)

    @property
    def EntryHash(self):
        '''
        len 10
        :return:
        '''
        val = truncate_hash(self.entryHash)
        return val

    @property
    def TotalDebit(self):
        '''
        len 12
        :return:
        '''
        return clean_amount(self.totalDebit, 12)

    @property
    def TotalCredit(self):
        '''
        len 12
        :return:
        '''
        return clean_amount(self.totalCredit, 12)

    @property
    def CompanyID(self):
        '''
        len 10
        :return:
        '''
        return self.bh.CompanyID

    @property
    def MessageAuth(self):
        '''
        len 19
        :return:
        '''
        val = fillspace(19, ' ')
        return val

    @property
    def Reserved(self):
        '''
        len 6
        :return:
        '''
        val = fillspace(6, ' ')
        return val

    @property
    def OriginID(self):
        '''
        len 8
        :return:
        '''
        return self.bh.OriginID

    @property
    def BatchNumber(self):
        '''
        len 7
        :return:
        '''
        return self.bh.BatchNumber

    def line_create(self):
        a = self.RecordType
        b = self.ServiceClass
        c = self.EntryCount
        d = self.EntryHash
        e = self.TotalDebit
        f = self.TotalCredit
        g = self.CompanyID
        h = self.MessageAuth
        i = self.Reserved
        j = self.OriginID
        k = self.BatchNumber

        val = [a, b, c, d, e, f, g, h, i, j, k]
        return ''.join(val)
