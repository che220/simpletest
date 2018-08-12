import sys, subprocess, re, traceback

def func():
    raise Exception('123132')

try:
    func()
    a = subprocess.check_output(['lss', '-la']).decode('utf-8')
    flds = re.split('\n', a)
    print(a)
    print(len(flds))
    for i, fld in enumerate(flds):
        fld = fld.strip()
        if len(fld) > 0 and not fld.startswith('total'):
            print(i, ": ", fld)
except:
    traceback.print_exc(file=sys.stdout)