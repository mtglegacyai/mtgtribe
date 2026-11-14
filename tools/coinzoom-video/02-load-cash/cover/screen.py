# The cover's phone screen: the clip's own store map (source frame 388), screen only, x2. Nothing private on this screen.
import os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
im = Image.open(os.path.join(HERE, '..', 'src1080', 'f0388.jpg')).crop((1172, 74, 1608, 1016))
im.resize((im.width * 2, im.height * 2), Image.LANCZOS).save(os.path.join(HERE, 'screen.jpg'), quality=94)
