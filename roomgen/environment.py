from .parameters import *

def overrideParams():

    global visualize, target_amount_samples, exportFigures, showPerformanceSummary, figureDpi, head_size, verbose
    visualize = False
    target_amount_samples = 50
    exportFigures = True
    figureDpi = None  
    verbose = 1
    showPerformanceSummary = False