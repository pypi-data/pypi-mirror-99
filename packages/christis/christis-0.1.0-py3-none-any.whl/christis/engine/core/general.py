import hashlib

def get_sha2(attr):
    return hashlib.sha224(attr.encode('utf-8')).hexdigest()

def get_domain_part_from_dn(dn):
    
    list_St = dn.split(',')
    dc = []
    for s in list_St:
        if(s.startswith('DC=')):
            t = s.split('=')[1]
            dc.append(t)

    return '-'.join(dc)