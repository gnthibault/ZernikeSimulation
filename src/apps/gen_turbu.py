# Generic imports
import argparse
import logging
import os

# Numerical stuff
import numpy as np

# Viz stuff
import matplotlib.pyplot as plt
import matplotlib.dates as mpldates
from matplotlib import cm as cmap
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import FormatStrFormatter
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Astropy stuff
import astropy.units as u
import poppy

def main(radius_mm):
    logging.getLogger('poppy').setLevel(logging.WARN)
    n_samples = 50
    psfs = []
    wavelen = 500 * u.nm
    focuses = np.array([7.5]) * u.um
    nwaves = (focuses.to(u.nm) / wavelen.to(u.nm)).value
    telescope_radius = 100 * u.mm

    #turbulence.display(what='both', opd_vmax=150 * u.nm)

    fig, ax = plt.subplots(1, 1, figsize=(9, 9))

    for i in range(n_samples):
        osys = poppy.OpticalSystem()
        primary = poppy.CircularAperture(radius=telescope_radius)
        secondary = poppy.SecondaryObscuration(secondary_radius=40 * u.mm,
                                               n_supports=4,
                                               support_width=5 * u.mm)
        defocus = poppy.ThinLens(nwaves=nwaves[0],
                                 reference_wavelength=wavelen,
                                 radius=telescope_radius)
        # Simulate turbulence
        turbulence = poppy.wfe.StatisticalPSDWFE(index=3.0,
                                                 wfe=50 * u.nm,
                                                 radius=radius_mm,
                                                 seed=None)

        newtonian = poppy.CompoundAnalyticOptic(
            opticslist=[primary, secondary, defocus, turbulence], name='newtonian')

        osys.add_pupil(newtonian)
        osys.add_detector(pixelscale=0.05, fov_arcsec=100.0)  # image plane coordinates in arcseconds

        psf = osys.calc_psf(wavelength=wavelen, normalize="exit_pupil")
        psfs.append(psf)

        # poppy.display_psf(psf, ax=ax[i], title=f"Defocused by {focuses[i]:.2f}",
        #    colorbar_orientation='horizontal')


    def update(i):
        # Update the image and the axes if needed. Return a tuple of
        # "artists" that have to be redrawn for this frame.
        if i < n_samples:
            #heatmap = ax3.imshow(imgs[i].filled(0), cmap='jet', vmin=0, vmax=1)
            heatmap = ax.imshow(psfs[i][0].data, cmap='jet')
            ax.axis('off')
            #divider = make_axes_locatable(ax)
            #cax = divider.append_axes("right", size="5%", pad=0.05)
            #plt.colorbar(heatmap, format=FormatStrFormatter('%.2e'), cax=cax, shrink=0.82)
            return ax
        else:
            return None

    animation = FuncAnimation(fig,
                              update,
                              frames=n_samples,
                              interval=200)
    filename = os.path.join("./", f"turbu_radius_{radius_mm.value}.gif")
    animation.save(filename, dpi=80, writer='imagemagick')

# main routine
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Small tool to generate atmospheric turbulence gif')
    parser.add_argument('--radius_mm', help='radius option for poppy StatisticalPSDWFE', type=str,
                        default=7)
    args = parser.parse_args()
    main(radius_mm=float(args.radius_mm)*u.mm)

