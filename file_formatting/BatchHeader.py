from datetime_ACH import Date_Time
from conversion_codes.ServiceClassCodes import ServiceClassCodes
from conversion_codes.StandardEntryClass import SEC_Codes
from tools.resources import *

class BatchHeader:
    def __init__(self, serviceClass='mixed', originator_name='Test Business Inc.',
                 originatorID='223334444', sec='business', discretionary='test file',
                 entry='EFT', entryDate='10/09/2020', odfi='211374020', batch_num='1'):
        """
        destination and origin are both routing numbers.
        destination must have a leading blank
        origin must have a leading one
        """
        self.serviceClass = serviceClass
        self.originator_name = originator_name
        self.originatorID = originatorID
        self.sec = sec
        self.discretionary = discretionary
        self.entry = entry
        self.entryDate = entryDate
        self.odfi = odfi
        self.batch_num = batch_num

    @property
    def RecordType(self):
        return '5'

    @property
    def ServiceClass(self):
        type = ServiceClassCodes.CONVERTER[self.serviceClass]
        return type

    @property
    def CompanyName(self):
        return name_truncate(self.originator_name).upper()

    @property
    def Discrectionary(self):
        '''
        field length 20
        field position 21-40
        alphameric
        :return:
        '''
        return fillspace(20, self.discretionary).upper()

    @property
    def CompanyID(self):
        return '1' + self.originatorID

    @property
    def SEC(self):
        code = SEC_Codes.CONVERTER[self.sec]
        return code

    @property
    def EntryDescription(self):
        '''
        len = 10
        :return:
        '''
        entry = fillspace(10, self.entry)
        return entry.upper()

    @property
    def DescriptiveDate(self):
        '''
        len = 6
        :return:
        '''
        dt = Date_Time()
        return dt.create_date()

    @property
    def EffectiveDate(self):
        '''
        len = 10
        :return:
        '''
        return date_convert(self.entryDate)

    @property
    def SettlementDate(self):
        return '   '

    @property
    def StatusCode(self):
        return '1'

    @property
    def OriginID(self):
        '''
        len = 8
        :return:
        '''
        return fillspace(8, self.odfi)

    @property
    def BatchNumber(self):

        return pad_zeros(7, self.batch_num)

    def line_create(self):
        a = self.RecordType
        b = self.ServiceClass
        c = self.CompanyName
        d = self.Discrectionary
        e = self.CompanyID
        f = self.SEC
        g = self.EntryDescription
        h = self.DescriptiveDate
        i = self.EffectiveDate
        j = self.SettlementDate
        k = self.StatusCode
        l = self.OriginID
        m = self.BatchNumber
        val = [a, b, c, d, e, f, g, h, i, j, k, l, m]
        return ''.join(val)
