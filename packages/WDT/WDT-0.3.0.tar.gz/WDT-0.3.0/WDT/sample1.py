from WDT import *

import time

def callback_func( x, y=1 ):
    z = x+y
    print( 'func: {}+{} -> {}'.format(x,y,z) )
    return z

pt0 = PerfTimer()
pt1 = PerfTimer()

# the callback is not invoked because wdt is feed before timeout
pt0.start()
pt1.start()
print( 'Sample1' )
wdt = WatchDogTimer( 0.2, callback_func, 1 )
wdt.start()
for i in range(5):
    wdt.feed()
    time.sleep(0.1)
wdt.stop()
print( 'ret: ', wdt.ret )
pt0.stop()
pt1.stop()
print( pt0.get_time(), pt1.get_time() )

# invoke callback after some seconds
pt0.restart()
pt1.start()
print( 'Sample2' )
wdt = WatchDogTimer( 0.2, callback_func, x=1 )
wdt.start()
time.sleep(0.3)
print( 'ret: ', wdt.ret )
pt0.stop()
pt1.stop()
print( pt0.get_time(), pt1.get_time() )

###
pt0.restart()
pt1.start()
print( 'Sample3' )
wdt = WatchDogTimer( 0.2, callback_func, 1, y=1 )
wdt.start()
for i in range(5):
    wdt.feed()
    wdt.set_callback( callback_func, 1, y=2 )
    time.sleep(0.1)
time.sleep(0.3)
print( 'ret: ', wdt.ret )
pt0.stop()
pt1.stop()
print( pt0.get_time(), pt1.get_time() )

