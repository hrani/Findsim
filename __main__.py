"""__main__.py: 
Entry point for this package.
"""
    
""" setup.py : Script for FindSim """
__author__      = "HarshaRani"
__copyright__   = "Copyright 2021 FindSim, NCBS"
__maintainer__  = "HarshaRani"
__email__       = "hrani@ncbs.res.in"



def run():
    from FindSim import findSim
    findSim.main()

def run_parallel():
    from FindSim import runAllParallel
    runAllParallel.main()

if __name__ == '__main__':
    run()
