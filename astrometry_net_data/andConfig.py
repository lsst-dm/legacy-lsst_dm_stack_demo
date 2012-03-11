root.starGalaxyColumn = "starnotgal"
filters = ('u', 'g', 'r', 'i', 'z', 'y')
root.magColumnMap = dict([(f,f) for f in filters])
root.magErrorColumnMap = dict([(f, f + '_err') for f in filters])
root.indexFiles = ['index-120304000.fits',
                   'index-120304001.fits',
                   'index-120304002.fits',
                   'index-120304003.fits',
                   ]

