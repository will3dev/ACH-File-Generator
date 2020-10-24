from file_formatting import BatchHeader
from file_formatting import BatchControl
from file_formatting import EntryDetail
from file_formatting import FileHeader
from file_formatting import FileControl

class Create_ACH_File:
    def __init__(self, transaction_listing):
        self.transaction_listing = transaction_listing

    def generate_entries(self, entries: list, originator: dict, batch_header: classmethod):
        '''
        entries param must include the following fields or else this operation
        will result in zeros for fields.

        'transcode': 'credit checking',
        'receivingID': '211371502',
        'acct': '123456789',
        'amt': '$1,999.68',
        'id_num': '0001112223',
        'name':'JOHN TEST'

        :param entries:
        :param entry_list:
        :return:
        '''
        trans_totals = {
            'block_count': 0,
            'hash_total': 0,
            'credit_total': 0,
            'debit_total': 0,
            'entry_count': 0,
            'batch_total': 0,
            'file': ''
        }

        for entry in entries:
            ed = EntryDetail(
                transcode=entry.get('transcode'),
                receivingID=entry.get('receivingID'),
                acct=entry.get('acct'),
                id_num=entry.get('id_num'),
                name=entry.get('name'),
                amt=entry.get('amt'),
                bh=batch_header
            )
            trans_totals['file'] += ed.line_create()
            trans_totals['file'] += '\n'

            trans_totals['block_count'] += 1
            trans_totals['entry_count'] += 1
            trans_totals['hash_total'] += int(ed.RDFI_ID)
            if '22' == ed.TransCode or '32' == ed.TransCode:
                trans_totals['credit_total'] += int(ed.Amount)

            elif '27' == ed.TransCode or '37' == ed.TransCode:
                trans_totals['debit_total'] += int(ed.Amount)

        if trans_totals.get('credit_total') != 0:
            ed_offset = EntryDetail(
                transcode='debit checking',
                receivingID=originator.get('odfi'),
                acct=originator.get('account'),
                id_num=originator.get('originatorID')[4:9],
                name=originator.get('originator_name'),
                amt=str(trans_totals.get('credit_total')),
                bh=batch_header
            )

            trans_totals['file'] += ed_offset.line_create()
            trans_totals['file'] += '\n'

            return trans_totals

        elif trans_totals.get('debit_total') != 0:
            ed_offset = EntryDetail(
                transcode='credit checking',
                receivingID=originator.get('odfi'),
                acct=originator.get('account'),
                id_num=originator.get('originatorID')[4:9],
                name=originator.get('originator_name'),
                amt=str(trans_totals.get('debit_total')),
                bh=batch_header
            )

            trans_totals['file'] += ed_offset.line_create()
            trans_totals['file'] += '\n'

            return trans_totals

    def generate_batch(self, entry_list, originator_info, batch_num):

        bh = BatchHeader(
            serviceClass=originator_info.get('serviceClass'),
            originator_name=originator_info.get('originator_name'),
            originatorID=originator_info.get('originatorID'),
            sec=originator_info.get('sec'),
            discretionary=originator_info.get('discretionary'),
            entry=originator_info.get('entry'),
            entryDate=originator_info.get('effective_entry'),
            odfi=originator_info.get('odfi'),
            batch_num=batch_num
        )
        header = bh.line_create() + '\n'

        entries = self.generate_entries(entry_list, originator_info, bh)

        bc = BatchControl(
            bh=bh,
            entryCount=str(entries.get('entry_count')),
            entryHash=str(entries.get('hash_total')),
            totalCredit=str(entries.get('credit_total')),
            totalDebit=str(entries.get('debit_total'))
        )
        control = bc.line_create() + '\n'

        entries['block_count'] += 2
        entries['file'] = header + entries['file']
        entries['file'] += control

        return entries

    def generate_file(self):

        details = {
            'block_count': 2,
            'hash_total': 0,
            'credit_total': 0,
            'debit_total': 0,
            'entry_count': 0,
            'batch_total': 0,
            'file': ''
        }

        for batch in self.transaction_listing:
            originator = batch.get('originator')
            entries = batch.get('entries')
            batch_num = details.get('batch_total') + 1

            transaction = self.generate_batch(entries, originator, str(batch_num))

            details['block_count'] += transaction.get('block_count')
            details['hash_total'] += transaction.get('hash_total')
            details['credit_total'] += transaction.get('credit_total')
            details['debit_total'] += transaction.get('debit_total')
            details['entry_count'] += transaction.get('entry_count')
            details['batch_total'] += 1
            details['file'] += transaction.get('file')

        fh = FileHeader()

        file = details.get('file')
        file = fh.line_create() + '\n' + file

        fc = FileControl(
            batchCount=details.get('batch_total'),
            recordCount=details.get('block_count'),
            entryCount=details.get('entry_count'),
            hashTotal=details.get('hash_total'),
            creditTotal=details.get('credit_total'),
            debitTotal=details.get('debit_total')
        )

        if details.get('block_count') % 10:
            val = 10 - (details.get('block_count') % 10)
            file += fc.line_create() + '\n'
            for x in range(val - 1):
                line = '9' * 94 + '\n'
                file += line

            return file

        else:
            file += fc.line_create()
            return file
