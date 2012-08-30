root.starGalaxyColumn = "starnotgal"
filters = ('u', 'g', 'r', 'i', 'z')
root.magColumnMap = dict([(f,f) for f in filters])
root.magErrorColumnMap = dict([(f, f + '_err') for f in filters])
root.indexFiles = [
    'index-120830001.fits',
    'index-120830002.fits',
    'index-120830003.fits',
    'index-120830004.fits',
    'index-120830000.fits',
    ]
