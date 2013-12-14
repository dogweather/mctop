#
# Top-like app for showing memcached stats.
#

import time
# See https://github.com/dlrust/python-memcached-stats
from memcached_stats import MemcachedStats

# Configuration
interval = 3


def percent_change(a0, a1, b0, b1):
    a_delta = a1 - a0
    b_delta = b1 - b0
    try:
        return float(a_delta) / (a_delta + b_delta) * 100
    except:
        return '-'


# First version: Do a simple repeating report
print "Interval is", interval, "seconds. Ctrl-c to quit."
mc = MemcachedStats()
time_0   = mc.stats()
hits_0   = int(time_0['get_hits'])
misses_0 = int(time_0['get_misses'])

time_a = time_0
while True:
    try:
        time.sleep(interval)
        time_b = mc.stats()

        hits_a   = int(time_a['get_hits'])
        hits_b   = int(time_b['get_hits'])
        misses_a = int(time_a['get_misses'])
        misses_b = int(time_b['get_misses'])
        
        print 'Efficiency'
        try:
            print("  Interval:     %5.1f %%" % percent_change(hits_a, hits_b, misses_a, misses_b))
        except:
            print("  Interval:      ----")
        try:
            print("  Cumulative:   %5.1f %%" % percent_change(hits_0, hits_b, misses_0, misses_b))
        except:
            print('  Cumulative:    ----')

        print 'Requests'
        print "  Interval:   {0:>5}".format((hits_b - hits_a) + (misses_b - misses_a))
        print "  Cumulative: {0:>5}".format((hits_b - hits_0) + (misses_b - misses_0))
        
        print " "
        
        # Start the next interval at this one's end.
        time_a = time_b

    except KeyboardInterrupt:
        # TODO: Clean-up code
        break
