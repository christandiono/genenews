import json
import urllib, glob
from django.core.management.base import BaseCommand
from genenews.genenews_main.models import Gene, Sequence, Track

from optparse import make_option



class Command(BaseCommand):
    args = "<data_dir, seq_names=..., track_names=...>"
    help = "Looks in the data_dir to populate the database of sequences and genes"
    option_list = BaseCommand.option_list + (make_option('--seq_names', dest="seq_names"), make_option('--track_names', dest="track_names"), make_option('--data_dir', dest="data_dir"))

    def handle(self, *args, **options):
        data_dir = options['data_dir']
        print options
        for seq in glob.glob(data_dir+"/tracks/*"):
            sequence_name = seq.split("/")[-1]
            if sequence_name not in options['seq_names'].split(','):
                continue
#            print sequence_name
#            continue
            sequence_object, created_seq = Sequence.objects.get_or_create(name=sequence_name)
            for filename in glob.glob(seq+"/*/names.json"):
                track_name = filename.split("/")[-2]
                if track_name not in options['track_names'].split(','):
                    continue
#                print track_name
#                continue
                track_object, created_track = Track.objects.get_or_create(name=track_name, sequence=sequence_object)
                print filename    
                file = open(filename)
                input = file.read()
                file.close()
                decoded_input = json.loads(input)
                for item in decoded_input:
                    for alias in item[0]:
    
                        gene, created_gene = Gene.objects.get_or_create(name=alias, sequence=sequence_object, track=track_object)
#                        if created_seq and created_gene:
#                            print "%s: created sequence and gene" % gene.fullname()
#                        elif created_gene:
#                            print "%s: created new gene for existing sequence" % gene.fullname()
#                        else:
#                            print "%s: skipped because it's already in the db" % gene.fullname()
