import simplejson as json
import urllib, glob
from django.core.management.base import BaseCommand
from genenews.genenews_main.models import Gene, Sequence, Track

from optparse import make_option



class Command(BaseCommand):
    args = "<data_dir, seq_names=..., track_names=...>"
    help = "Looks in the data_dir to populate the database of sequences and genes"
    option_list = BaseCommand.option_list + (make_option('--seq_names', dest="seq_names"), make_option('--track_names', dest="track_names"), make_option('--data_dir', dest="data_dir"))

    def handle(self, *args, **options):
        '''
        Similar to import_names, but sets the urlTemplate variable appropriately instead.
        '''
        data_dir = options['data_dir']
        print options
        for seq in glob.glob(data_dir+"/tracks/*"):
            sequence_name = seq.split("/")[-1]
            if sequence_name not in options['seq_names'].split(','):
                continue
            sequence_object, created_seq = Sequence.objects.get_or_create(name=sequence_name)
            for filename in glob.glob(seq+"/*/trackData.json"):
                track_name = filename.split("/")[-2]
                if track_name not in options['track_names'].split(','):
                    continue
                track_object, created_track = Track.objects.get_or_create(name=track_name, sequence=sequence_object)
                print filename
                file = open(filename)
                input = file.read()
                file.close()
                decoded_input = json.loads(input)
                decoded_input['urlTemplate'] = "/gene/{name}/"
                file = open(filename, 'w')
                file.write(json.dumps(decoded_input))
                file.close()
#                print decoded_input
