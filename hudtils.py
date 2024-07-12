#!/usr/bin/python
import time, sys


def filename_with_rollover(filename='hud.log', opts = ['year','month','day']):

    """
    
    HELP:
    filename     = text.txt
    new_filename = filename_with_rollover(filename, opts = ['year','month','day'])
    
    
    """

    allowed = ['year','month','day','hour','mins','sec']
    name    = ''
    schema  = ''
    localtime = time.localtime(time.time())
    timer   = {}

    timer['year']  = str(localtime.tm_year)
    timer['month'] = str(localtime.tm_mon)
    timer['day']   = str(localtime.tm_mday)
    timer['hour']  = str(localtime.tm_hour)
    timer['mins']  = str(localtime.tm_min)
    timer['sec']   = str(localtime.tm_sec)

    for n in opts:
        if n not in allowed:
            print """
            
            The filename_with_rollover function must contain 
            one of the following:
            ['year','month','day','hour','mins','sec']
            
            """
            sys.exit()
        else:
            name   = name+timer[n]
            schema = schema+n+'_'        
    filen_ = name + '_' + filename
    
    return filen_