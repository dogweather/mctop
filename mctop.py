#
# Top-like app for showing memcached stats.
#

import time
from blessings import Terminal              # https://pypi.python.org/pypi/blessings/
from memcached_stats import MemcachedStats  # https://github.com/dlrust/python-memcached-stats

# Configuration
interval = 3


def percent_change_in_interval(a0, a1, b0, b1):
    a_delta = a1 - a0
    b_delta = b1 - b0
    try:
        return float(a_delta) / (a_delta + b_delta)
    except:
        return '-'


print "Interval is", interval, "seconds. Ctrl-c to quit."
t  = Terminal()
mc = MemcachedStats()
time_0   = mc.stats()
hits_0   = int(time_0['get_hits'])
misses_0 = int(time_0['get_misses'])

time_a = time_0
while True:
    try:
        time.sleep(interval)
        print t.clear()
        time_b = mc.stats()

        hits_a   = int(time_a['get_hits'])
        hits_b   = int(time_b['get_hits'])
        misses_a = int(time_a['get_misses'])
        misses_b = int(time_b['get_misses'])
        
        print '              Efficiency   Requests'

        try:
            requests   = "{0:>10,}".format((hits_b - hits_a) + (misses_b - misses_a))
            efficiency = "{:>10.1%}".format(percent_change_in_interval(hits_a, hits_b, misses_a, misses_b))
        except:
            efficiency = "      ----"
        print 'Interval:    ', t.bold(efficiency), t.bold(requests)


        try:
            requests   = "{0:>10,}".format((hits_b - hits_0) + (misses_b - misses_0))
            efficiency = "{:>10.1%}".format(percent_change_in_interval(hits_0, hits_b, misses_0, misses_b))
        except:
            efficiency = "      ----"
        print 'Cumulative:  ', t.bold(efficiency), t.bold(requests)


        try:
            requests   = "{0:>10,}".format(hits_b + misses_b)
            efficiency = "{:>10.1%}".format(percent_change_in_interval(0, hits_b, 0, misses_b))
        except:
            efficiency = "      ----"
        print 'Total:       ', t.bold(efficiency), t.bold(requests)


        # Start the next interval at this one's end.
        time_a = time_b

    except KeyboardInterrupt:
        # TODO: Clean-up code
        break
