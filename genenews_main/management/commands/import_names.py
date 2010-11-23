import simplejson as json
import urllib
from django.core.management.base import BaseCommand
from genenews.genenews_main.models import Gene
from genenews.genenews_main.models import Sequence

class Command(BaseCommand):
    args = "<url>"
    help = "Queries the specified URL to populate the database of sequences and genes"

    def handle(self, *args, **options):
        file = urllib.urlopen("http://genenews.dyndns.org/jbrowse/data/names/root.json")
        input = file.read()
        decoded_input = json.loads(input)

        for i in range(2, len(decoded_input)):
            for j in range(2, len(decoded_input[i])):
                for k in range(2, len(decoded_input[i][j])):
                    templist = []
                    if decoded_input[i][j][k][1] == None:
                        for l in range(2, len(decoded_input[i][j][k])):
                            templist.append(decoded_input[i][j][k][l][1])
                    else:
                        templist.append(decoded_input[i][j][k][1])
                    for temparray in templist:
                        for item in temparray:
                            seq, created_seq = Sequence.objects.get_or_create(name=item[2])
                            gene, created_gene = Gene.objects.get_or_create(name=item[1], sequence=seq)
                            gene.sequence = seq
                            gene.save()
                            if created_seq and created_gene:
                                print "%s: created sequence and gene" % gene.fullname()
                            elif created_gene:
                                print "%s: created new gene for existing sequence" % gene.fullname()
                            else:
                                print "%s: skipped because it's already in the db" % gene.fullname()
