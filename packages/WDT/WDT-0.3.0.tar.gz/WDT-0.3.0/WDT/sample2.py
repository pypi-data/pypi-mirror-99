from WDT import *

import time

def callback_func( pt, x, y=1 ):
    z = x+y
    print( 'func: {}+{} -> {} ({})'.format(x,y,z, pt.get_time()) )
    time.sleep(0.1)
    return z

pt = PerfTimer()
pt.start()
prd = Periodic( 0.2, callback_func, pt, 1 )
prd.start(compensate=True)
time.sleep(1)
prd.stop()
print()

pt = PerfTimer()
pt.start()
prd = Periodic( 0.2, callback_func, pt, 2 )
prd.start(compensate=False)
time.sleep(1)
prd.stop()
print()

pt = PerfTimer()
pt.start()
prd = Periodic( 0.1, callback_func, pt, 3 )
prd.start(compensate=True)
time.sleep(1)
prd.stop()
print()

