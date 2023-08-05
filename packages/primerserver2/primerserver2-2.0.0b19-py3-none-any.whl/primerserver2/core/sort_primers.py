import json
import os
import sys

from primerserver2.core import global_var

def sort_rank(primers, dbs, max_num_return=10, use_isoforms=False):
    '''
        sort primers within each site based on their amplicons number in the main db
        Input:
            primers: generated by run_blast
            dbs: used in run_blast

        Optional:
            max_num_return: only output this number of primers
        Return:
            updated primers with PRIMER_PAIR_AMPLICON_NUM_RANK_X attribute
    '''
    if global_var.stop_run is True:
        return {'error': 'Stop running'}
        
    main_db = os.path.basename(dbs[0])
    if use_isoforms is True:
        isoform_data = json.load(open(dbs[0]+'.isoforms.json'))

    for (id, primer) in primers.items():
        if use_isoforms is True:
            template = id.split('-')[0]
            isoforms = []
            if template in isoform_data:
                isoforms = isoform_data[template]

        rank_to_amplicon_valid_num = {}
        for rank in range(0, primer['PRIMER_PAIR_NUM_RETURNED']):
            if f'PRIMER_PAIR_{rank}_AMPLICONS' not in primer[main_db]:
                continue
            if use_isoforms is False:
                rank_to_amplicon_valid_num[rank] = len(primer[main_db][f'PRIMER_PAIR_{rank}_AMPLICONS'])
            else:
                rank_to_amplicon_valid_num[rank] = 1
                for (i, amplicon) in enumerate(primer[main_db][f'PRIMER_PAIR_{rank}_AMPLICONS']):
                    sseqid = amplicon['plus']['sseqid']
                    if sseqid not in isoforms:
                        rank_to_amplicon_valid_num[rank] += 1
                        primer[main_db][f'PRIMER_PAIR_{rank}_AMPLICONS'][i]['isoform'] = False
                    else:
                        primer[main_db][f'PRIMER_PAIR_{rank}_AMPLICONS'][i]['isoform'] = True

        
        num_output_primers = 0
        for (i, rank) in enumerate(sorted(rank_to_amplicon_valid_num, key=rank_to_amplicon_valid_num.__getitem__)):
            primers[id][f'PRIMER_PAIR_AMPLICON_NUM_RANK_{i}'] = rank
            num_output_primers += 1
            if num_output_primers==max_num_return:
                break
        
        primers[id]['PRIMER_PAIR_NUM_RETURNED_FINAL'] = num_output_primers
    
    return primers

if __name__ == "__main__":
    global_var.init()
    primers = json.load(open('tests/_internal_/run_blast.json'))
    dbs = ['example.fa']
    print(json.dumps(sort_rank(primers, dbs), indent=4))

