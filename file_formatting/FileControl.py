from tools.resources import *


class FileControl:
    def __init__(self, batchCount='2', recordCount='5', entryCount='2', hashTotal='422745543',
                 creditTotal='1999.68', debitTotal='1999.68'):
        self.batchCount = str(batchCount)
        self.recordCount = str(recordCount)
        self.entryCount = str(entryCount)
        self.hashTotal = str(hashTotal)
        self.creditTotal = str(creditTotal)
        self.debitTotal = str(debitTotal)

    @property
    def RecordType(self):
        '''
        len 1
        :return:
        '''
        return '9'

    @property
    def BatchCount(self):
        '''
        len 6
        :return:
        '''
        return pad_zeros(6, self.batchCount)

    @property
    def BlockCount(self):
        '''
        len 6
        :return:
        '''
        val = int(self.recordCount)
        if val < 10:
            return pad_zeros(6, '1')
        else:
            val //= 10
            val += 1
            return pad_zeros(6, str(val))

    @property
    def EntryCount(self):
        '''
        len 8
        :return:
        '''
        return pad_zeros(8, self.entryCount)

    @property
    def HashTotal(self):
        '''
        len 10
        :return:
        '''
        return truncate_hash(self.hashTotal)

    @property
    def TotalDebit(self):
        '''
        len 12
        :return:
        '''
        return clean_amount(self.debitTotal, 12)

    @property
    def TotalCredit(self):
        '''
        len 12
        :return:
        '''
        return clean_amount(self.creditTotal, 12)

    @property
    def Reserved(self):
        '''
        len 39
        :return:
        '''
        return fillspace(39, ' ')

    def line_create(self):
        a = self.RecordType
        b = self.BatchCount
        c = self.BlockCount
        d = self.EntryCount
        e = self.HashTotal
        f = self.TotalDebit
        g = self.TotalCredit
        h = self.Reserved

        val = [a, b, c, d, e, f, g, h]
        return ''.join(val)


