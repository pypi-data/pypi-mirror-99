WDT
===

Watch Dog Timer and Timer for python

`Github <https://github.com/mastnk/WDT/>`__
`PyPI <https://pypi.org/project/WDT/>`__

Instalation
-----------

``% pip install WDT``

python 3.6.0 or later is required.

*class* WatchDogTimer(Thread)
-----------------------------

The WatchDogTimer is used to invoke a callback function when the timeout
happens. After starting the WatchDogTimer, the application need “feed”
the WatchDogTimer periodically if you want to prevent to invoke the
callback.

If you do not “feed”, the callback function would be invoked after the
setting time from the last “feed”.

Methods
~~~~~~~

-  \__init__( self, time_sec, callback, \*args, \**kwargs )

   Constructor.

   **time_sec**: a setting time,

   **callback**: a function or a functor,

   **args**\ *,*\ \*\ **kwargs**: arguemnts of the function,

-  start( self, daemon=True ) -> None

   Start the WatchDogTimer.

   **daemon**: If it is true, the thread is daemonized.

-  stop( self ) -> None

   Stop the WatchDogTimer. The callback function is not invoked.

-  feed( self ) -> None

   Feed to the WatchDogTimer.

-  set_callback( self, callback, \*args, \**kwargs ) -> None

   Change the *callback* and the *args_dict* if they are not None.

   **callback**: a function or a functor,

   **args**\ *,*\ \*\ **kwargs**: arguemnts of the function.

-  set_time_sec( self, time_sec ) -> None

   Change the *time_sec*.

   **time_sec**: a setting time.

Variables
~~~~~~~~~

-  ret

   It holds a retun velue of the callback function. If the callback
   function is not invoked, it is *None*.

-  is_timeout

   It is boolean which represents the WatchDogTimer is timeout or not.

-  is_running

   It is boolean which represents the WatchDogTimer is running or not.

*class* Periodic
----------------

The Periodic is used to invoke a callback function periodically. If
*compensate* is *True*, the period is the setting time. If *compensate*
is *False*, the period is the settin time and the elapsed time of the
callback function.

.. _methods-1:

Methods
~~~~~~~

-  \__init__( self, time_sec, callback, \*args, \**kwargs )

   Constructor.

   **time_sec**: a setting time,

   **callback**: a function or a functor,

   **args**\ *,*\ \*\ **kwargs**: arguemnts of the function,

-  start( self, daemon=True, compensate=True ) -> None

   Start the WatchDogTimer.

   **daemon**: If it is true, the thread is daemonized.

   **compensate**:

-  stop( self ) -> None

   Stop the WatchDogTimer. The callback function is not invoked.

-  set_callback( self, callback, \*args, \**kwargs ) -> None

   Change the *callback* and the *args_dict* if they are not None.

   **callback**: a function or a functor,

   **args**\ *,*\ \*\ **kwargs**: arguemnts of the function.

-  set_time_sec( self, time_sec ) -> None

   Change the *time_sec*.

   **time_sec**: a setting time.

.. _variables-1:

Variables
~~~~~~~~~

-  ret

   It holds a retun velue of the callback function. If the callback
   function is not invoked, it is *None*.

-  is_running

   It is boolean which represents the WatchDogTimer is running or not.

*class* PerfTimer
-----------------

It is a timer to measure the time with time.perf_counter.

.. _methods-2:

Methods
~~~~~~~

-  \__init__( self )

   The constructor

-  start( self ) -> None

   Start the timer.

-  stop( self ) -> float

   Stop the timer. It return the time in seconds.

-  reset( self )

   It reset the accumulate time to zero.

-  restart( self )

   Reset and start.

-  get_time( self ) -> float

   Return the time.

*class* SleepForPeriodic
------------------------

It is sleep for periodic process.

.. _methods-3:

Methods
~~~~~~~

-  \__init__( self, interval )

   The constructor. *interval* is specfied in sec.

-  start( self )

   It is called at the begining of periodical process.

-  sleep( self )

   It is called at the end of periodical process. Then, sleep necessary
   time for periodic process.

Sample code
-----------

sample1.py

.. code:: python


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

sample2.py

.. code:: python

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

   sfp = SleepForPeriodic( 1 ) # in sec
   while( True ):
       sfp.start()
   ​
       ## some process
       t = random.random()
       print( t )
       time.sleep( t )
       ##
   ​
       sfp.sleep()
