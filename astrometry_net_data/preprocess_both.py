from astrometry.util.pyfits_utils import *
from numpy import *

def mag2flux(mag):
    return 2.5**-mag

def flux2mag(flux):
    return -log(flux)/log(2.5)

if __name__ == '__main__':
    T = fits_table('both3.fits')
    print 'Got %i sources' % len(T)

    ids = T.id
    U = unique(ids)
    print '%i unique IDs' % len(U)

    #Assertion not valid since star and galaxy ids overlap.  The isGalaxy flag
    #breaks this degeneracy
    #assert(len(U) == len(T))

    # Secret decoder ring says ignore brighter than 10.
    M = 10
    keep = (T.u > M) * (T.g > M) * (T.r > M) * (T.i > M) * (T.z > M) * (T.y > M)

    if False:
        # Find limiting mags and cut 1 mag fainter.
	step = 0.1
	lmag = []
	for band in 'ugrizy':
		mag = T.get(band)
		bins = arange(floor(mag.min() / step) * step, ceil(mag.max() / step) * step + step, step)
		n,b = histogram(mag, bins=bins)
		I = argmax(n)
		lmag.append(b[I])
	bright = zeros_like(keep)
	for i,band in enumerate('ugrizy'):
		mag = T.get(band)
		bright = logical_or(bright, mag < (lmag[i] + 1))
	keep *= bright

    else:
	# Cut at any band brighter than ...
	#cut = 22.
        ''''
        Got 12235294 sources
        Band u : keeping 6009584 above mag 23.4
        8 millionth mag: 24.313249588
        Band g : keeping 7228012 above mag 22.4
        8 millionth mag: 22.8702201843
        Band r : keeping 7964639 above mag 22
        8 millionth mag: 22.0967559814
        Band i : keeping 7813477 above mag 21.7
        8 millionth mag: 21.7739124298
        Band z : keeping 7634632 above mag 21.5
        8 millionth mag: 21.6284103394
        Band y : keeping 7682476 above mag 21.4
        8 millionth mag: 21.5253562927
        After mag cuts: 8198432 sources
        '''
        cuts = [ 24.3, 22.9, 22.0, 21.8, 21.6, 21.5 ]

	magkeep = zeros_like(keep)
	for band,cut in zip('ugrizy', cuts):
		mag = T.get(band)
		I = (mag < cut)
		print 'Band', band, ': keeping %i above mag %g' % (sum(I), cut)

                #J = argsort(mag)
                #print '8 millionth mag:', mag[J[8000000]]

		magkeep[I] = True
	keep *= magkeep

	lmag = ones(6) * cut

    T = T[keep]
    print 'After mag cuts: %i sources' % len(T)

    for i,band in enumerate('ugrizy'):
	mag = T.get(band)
	# Invent magnitude errors
	flux0 = mag2flux(lmag[i])
	# assume that's 5-sigma;
	nsigma = 5.
	# assume sky counts / pixel
	sky = 100.
	fluxscale = sqrt(sky) / (flux0 / nsigma)

	# assumed minimum magnitude error level.
	noisefloor = 0.01

	flux = fluxscale * mag2flux(mag)
	#magerr = flux2mag(sqrt(flux  +	 sky) / flux)
	magerr = hypot(noisefloor, flux2mag(1. + sqrt(flux  +  sky) / flux))

	T.set(band + '_err', magerr)

    # Seems I messed this up!

    print 'variable:', T.variable.shape
    print 'variable:', unique(T.variable)

    T.starnotgal = T.starnotgal[:,0]
    T.variable = T.variable[:,0]

    # down-convert
    for band in 'ugrizy':
	T.set(band, T.get(band).astype(float32))
	T.set(band + '_err', T.get(band + '_err').astype(float32))
    for c in ['mura','mudec','parallax']:
	T.set(c, T.get(c).astype(float32))

    T.about()

    T.writeto('both4.fits')
