from tools.resources import *
from conversion_codes import TransCodes as ts

from file_formatting.BatchHeader import BatchHeader


class EntryDetail:
    def __init__(self, bh=BatchHeader, transcode='credit checking', receivingID='211371502',
                 acct='123456789', amt='$1,999.68', id_num='0001112223', name='JOHN TEST'):
        self.bh = bh
        self.transcode = transcode
        self.receivingID = receivingID
        self.acct = acct
        self.amt = amt
        self.id_num = id_num
        self.name = name

    @property
    def RecordType(self):
        return '6'

    @property
    def TransCode(self):
        '''
        len = 2
        :return:
        '''
        return ts.CONVERTER[self.transcode]

    @property
    def RDFI_ID(self):
        '''
        len = 8
        :return:
        '''
        return self.receivingID[:8]

    @property
    def CheckDig(self):
        '''
        len 1
        :return:
        '''
        return self.receivingID[8:9]

    @property
    def AcctNum(self):
        '''
        len 17
        :return:
        '''
        return fillspace(17, self.acct)

    @property
    def Amount(self):
        '''
        len 10
        $$$$$$$$cc
        :return:
        '''
        return clean_amount(self.amt, 10)

    @property
    def IndividualID(self):
        '''
        len 15
        alphameric
        :return:
        '''
        return nameFill(15, self.id_num)

    @property
    def Name(self):
        '''
        len 22
        alphameric
        :return:
        '''
        return nameFill(22, self.name)

    @property
    def Discretionary(self):
        '''
        2
        :return:
        '''
        return '  '

    @property
    def Addenda(self):
        return '0'

    @property
    def Trace(self):
        bh = BatchHeader()
        return generate_trace(bh.originatorID)

    def line_create(self):
        a = self.RecordType
        b = self.TransCode
        c = self.RDFI_ID
        d = self.CheckDig
        e = self.AcctNum
        f = self.Amount
        g = self.IndividualID
        h = self.Name
        i = self.Discretionary
        j = self.Addenda
        k = self.Trace

        val = [a, b, c, d, e, f, g, h, i, j, k]
        return ''.join(val)
