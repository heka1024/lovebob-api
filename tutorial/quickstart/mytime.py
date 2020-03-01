from datetime import datetime, timedelta, date

def time2meal():
    def check(t):
        if t <= 10:
            return 'b'
        elif t <= 15:
            return 'l'
        else:
            return 'd'
        
    now = datetime.today()
    h = now.hour
    return check(h)
    
def date2string(delta = 0):
    d = date.today() + timedelta(days = 1) * delta
    return d.isoformat()