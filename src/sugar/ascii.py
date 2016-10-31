from __future__ import division, print_function

def progress_bar(now, N, blocks=50, marker='#'):
    """Print a progress bar on command line"""
    a = int(now*blocks/N) # No. of blocks to show
    b = "%0.1f"%(now/N*100) # Percentage progress 
    print('\r[{0}] {1}%'.format(marker*a, b), end='')