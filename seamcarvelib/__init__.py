# This file will be executed when this library is imported so keep it minimal
import subprocess
if subprocess.getstatusoutput('magick')[0] != 0:
    raise EnvironmentError('ImageMagick is not installed (https://imagemagick.org/script/download.php)')
