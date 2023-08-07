# Script from JWST tools workshop.

from matplotlib import rcParams
import matplotlib.pyplot as plt

from astropy.stats import gaussian_sigma_to_fwhm

from photutils.datasets import make_random_gaussians
from photutils.datasets import make_noise_image
from photutils.datasets import make_gaussian_sources

from photutils import psf
from photutils import MMMBackground
from photutils.psf import IntegratedGaussianPRF
from photutils.psf import BasicPSFPhotometry
from photutils.detection import DAOStarFinder

num_sources = 1
min_flux = 500
max_flux = 5000
min_xmean = 16
max_xmean = 240
sigma_psf = 0.5

starlist = make_random_gaussians(num_sources, [min_flux, max_flux],
                                 [min_xmean, max_xmean],
                                 [min_xmean, max_xmean],
                                 [sigma_psf, sigma_psf],
                                 [sigma_psf, sigma_psf],
                                 random_state=1234)

shape = (15, 15)
image = (make_gaussian_sources(shape, starlist) +
         make_noise_image(shape, type='poisson', mean=6., random_state=1234) + 
         make_noise_image(shape, type='gaussian', mean=0., stddev=2., random_state=1234))

rcParams['image.cmap'] = 'magma'
rcParams['image.aspect'] = 1  # to get images with square pixels
rcParams['figure.figsize'] = (20,10)
rcParams['image.interpolation'] = 'nearest'
rcParams['image.origin'] = 'lower'
rcParams['font.size'] = 14

plt.imshow(img)
plt.title('Simulated data')
plt.colorbar(orientation='horizontal', fraction=0.046, pad=0.04)

daogroup = psf.DAOGroup(crit_separation=2.0*sigma_psf*gaussian_sigma_to_fwhm)
mmm_bkg = MMMBackground()

daofinder = DAOStarFinder(threshold=2.5*mmm_bkg(img),
                          fwhm=sigma_psf*gaussian_sigma_to_fwhm)

fitshape = 5
gaussian_psf = IntegratedGaussianPRF(sigma=sigma_psf)
basic_photometry = BasicPSFPhotometry(group_maker=daogroup,
                         bkg_estimator=MMMBackground(),
                         psf_model=gaussian_psf, fitshape=fitshape,
                         finder=daofinder)

photometry_results = basic_photometry(img)

fig, (ax1, ax2) = plt.subplots(1,2)
im1 = ax1.imshow(basic_photometry.get_residual_image())
ax1.set_title('Residual Image')
plt.colorbar(orientation='horizontal', fraction=0.046, pad=0.04,
             ax=ax1, mappable=im1)

im2 = ax2.imshow(img)
ax2.set_title('Simulated data')
plt.colorbar(orientation='horizontal', fraction=0.046, pad=0.04,
             ax=ax2, mappable=im2)



from astropy.table import Table
positions = Table(names=['x_0', 'y_0'], data=[starlist['x_mean'], starlist['y_mean']])
photometry_results = basic_photometry(image=image, positions=positions)

