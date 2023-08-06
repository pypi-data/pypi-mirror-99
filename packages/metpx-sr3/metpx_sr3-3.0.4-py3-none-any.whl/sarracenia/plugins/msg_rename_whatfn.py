import sys, os, os.path, time, stat
"""
 this renamer strips of everything from the first colon in the file name to the end.
 This does the same thing as a 'WHATFN' config on a sundew sender.

 takes px name     : /apps/dms/dms-metadata-updater/data/international_surface/import/mdicp4d:pull-international-metadata:CMC:DICTIONARY:4:ASCII:20160223124648
 rename for        : /apps/dms/dms-metadata-updater/data/international_surface/import/mdicp4d

"""


class Renamer(object):
    def __init__(self):
        pass

    def on_message(self, parent):
        import time

        parts = parent.msg.new_file.split(':')

        # join mets les ':' entre les parts... donc ajout de ':' au debut
        extra = ':' + ':'.join(parts[1:])

        parent.msg.new_file = parent.msg.new_file.replace(extra, '')
        parent.msg.headers['rename'] = parent.msg.headers['rename'].replace(
            extra, '')

        return True


renamer = Renamer()
self.on_message = renamer.on_message

# test interactif
#print renamer.on_message(sys.argv[1])
