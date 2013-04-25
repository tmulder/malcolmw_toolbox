import sys
import os

from Tkinter import *

sys.path.append( os.environ['MW_SRC'] + '/GUI' )

import InitMenu as im

root = Tk()
im.InitMenu(root)
root.mainloop()
