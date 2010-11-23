import simplejson as json
import urllib, glob
from django.core.management.base import BaseCommand
from genenews.genenews_main.models import Gene, Sequence, Track

class Command(BaseCommand):
    args = "<data_dir>"
    help = "Looks in the data_dir to populate the database of sequences and genes"

    def handle(self, *args, **options):
        for seq in glob.glob(args[0]+"/tracks/*"):
            sequence_name = seq.split("/")[-1]
#            print sequence_name
#            continue
            sequence_object, created_seq = Sequence.objects.get_or_create(name=sequence_name)
            for filename in glob.glob(seq+"/*/names.json"):
                track_name = filename.split("/")[-2]
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
