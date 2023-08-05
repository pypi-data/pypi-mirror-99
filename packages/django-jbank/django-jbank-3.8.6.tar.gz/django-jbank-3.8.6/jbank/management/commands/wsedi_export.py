import json
import os
import zipfile
from datetime import datetime, date
from django.conf import settings
from django.core.management.base import CommandParser
from jutil.command import SafeCommand
from jbank.models import WsEdiConnection


class Command(SafeCommand):
    help = "Export WS-EDI connection"

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("ws", type=int)
        parser.add_argument("--file", type=str)

    def do(self, *args, **options):
        ws = WsEdiConnection.objects.all().get(id=options["ws"])
        assert isinstance(ws, WsEdiConnection)

        filename = "ws{}.zip".format(ws.id)
        if options["file"]:
            filename = options["file"]

        files = []
        ws_data = {}
        for k, v in ws.__dict__.items():
            if not k.startswith("_") and k != "id":
                if isinstance(v, datetime):
                    v = v.isoformat()
                elif isinstance(v, date):
                    v = v.isoformat()
                ws_data[k] = v
                if k.endswith("_file"):
                    files.append(os.path.join(settings.MEDIA_ROOT, v))

        zf = zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED)
        zf.writestr("ws.json", json.dumps(ws_data))
        for file in files:
            zf.write(file, os.path.basename(file))
        zf.close()
        print("{} written".format(filename))
