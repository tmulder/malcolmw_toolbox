import sys
import os
sys.path.append('%s/data/python' % os.environ['ANTELOPE'])

from antelope.datascope import Dbptr

def distance(lat1, lon1, lat2, lon2, in_km=False):
    """
    Returns the distance in degrees between a point with latitude and
    longitude of lat1, lon1 respectively and a point with latitude and
    longitude of lat2, lon2 respectively. Returns the distance in km if
    in_km is set to a True value.
    """
    if in_km:
        return Dbptr().ex_eval('deg2km(%f)' %
            Dbptr().ex_eval('distance(%f, %f, %f, %f)'
                % (lat1, lon1, lat2, lon2)))
    else: return Dbptr().ex_eval('distance(%f ,%f ,%f, %f)'
            % (lat1, lon1, lat2, lon2))

def azimuth(lat1, lon1, lat2, lon2):
    """
    Returns the azimuth from (lat1, lon1) to (lat2, lon2)
    """
    return Dbptr().ex_eval('azimuth(%f, %f, %f, %f)'
            % (lat1, lon1, lat2, lon2))

def get_null_value(table, field):
    nulls = {'origin': {\
                'lat': -999.0000,\
                'lon': -999.000,\
                'depth': -999.000,\
                'time': -9999999999.99900,\
                'orid': -1,\
                'evid': -1,\
                'jdate': -1,\
                'nass': -1,\
                'ndef': -1,\
                'ndp': -1,\
                'grn': -1,\
                'srn': -1,\
                'etype': '-',\
                'review': '-',\
                'depdp': -999.0000,\
                'dtype': '-',\
                'mb': -999.00,\
                'mbid': -1,\
                'ms': -999.00,\
                'msid': -1,\
                'ml': -999.00,\
                'mlid': -1,\
                'algorithm': '-',\
                'commid': -1,\
                'auth': '-',\
                'lddate': -9999999999.99900
                },\
            'arrival': {
                'sta': '-',\
                'time': -9999999999.99900,\
                'arid': -1,\
                'jdate': -1,\
                'stassid': -1,\
                'chanid': -1,\
                'chan': '-',\
                'iphase': '-',\
                'stype': '-',\
                'deltim': -1.000,\
                'azimuth': -1.00,\
                'delaz': -1.00,\
                'slow': -1.00,\
                'delslo': -1.00,\
                'ema': -1.00,\
                'rect': -1.000,\
                'amp': -1.0,\
                'per': -1.00,\
                'logat': -999.00,\
                'clip': '-',\
                'fm': '-',\
                'snr': -1,\
                'qual': '-',\
                'auth': '-',\
                'commid': -1,\
                'lddate': -9999999999.99900
                },\
            'assoc': {
                    'arid': -1,\
                    'orid': -1,\
                    'sta': '-',\
                    'phase': '-',\
                    'belief': 9.99,\
                    'delta': -1.000,\
                    'seaz': -999.00,\
                    'esaz': -999.00,\
                    'timeres': -999.000,\
                    'timedef': '-',\
                    'azres': -999.0,\
                    'azdef': '-',\
                    'slores': -999.00,\
                    'slodef': '-',\
                    'emares': -999.0,\
                    'wgt': -1.000,\
                    'vmodel': '-',\
                    'commid': -1,\
                    'lddate': -9999999999.99900
                    }
            }
    return nulls[table][field]
