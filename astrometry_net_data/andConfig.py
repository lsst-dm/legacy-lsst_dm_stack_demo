root.starGalaxyColumn = "starnotgal"
filters = ('u', 'g', 'r', 'i', 'z', 'y')
root.magColumnMap = dict([(f,f) for f in filters])
root.magErrorColumnMap = dict([(f, f + '_err') for f in filters])
root.indexFiles = ['index-120319000.fits',
                   'index-120319001.fits',
                   'index-120319002.fits',
                   'index-120319003.fits',
                   ]

