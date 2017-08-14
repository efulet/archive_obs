"""
@created_at 2017-08-13
@author Exequiel Fuentes Lettura <efulet@gmail.com>
"""

import os
import numpy as np

import matplotlib.pyplot as plt

import astropy.coordinates as coord
import astropy.units as u

from astropy.io import ascii

from archive_obs.base.util import parse_input_date
from archive_obs.conf import settings


def show(save=False):
    """
    A very simple method for reading a CSV and plot RA and Dec
    """
    path = os.path.join(settings.CSV_PATH, 'fits_headers.csv')
    data = ascii.read(path, format='csv', fast_reader=False, data_start=1, delimiter='\t')

    org = 0
    ra = coord.Angle(data['ra'].filled(np.nan) * u.degree)
    ra = ra.wrap_at(180 * u.degree)
    dec = coord.Angle(data['dec'].filled(np.nan) * u.degree)

    x = np.remainder(data['ra'] + 360 - org, 360)  # shift RA values
    ind = x > 180
    x[ind] -= 360  # scale conversion to [-180, 180]
    x = -x  # reverse the scale: East to the left
    tick_labels = np.array([150, 120, 90, 60, 30, 0, 330, 300, 270, 240, 210])
    tick_labels = np.remainder(tick_labels + 360 + org, 360)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='mollweide')
    ax.scatter(ra.radian, dec.radian)
    ax.set_xticklabels(tick_labels)
    ax.grid(True)

    min_date = min(data['date'])
    try:
        min_date = parse_input_date(min_date).strftime('%Y-%m-%d')
    except:
        pass
    max_date = max(data['date'])
    try:
        max_date = parse_input_date(max_date).strftime('%Y-%m-%d')
    except:
        pass

    ax.set_title('Observations made by Gemini at dates: {},{}'.format(min_date, max_date))
    ax.title.set_fontsize(15)
    ax.set_xlabel('RA')
    ax.xaxis.label.set_fontsize(12)
    ax.set_ylabel('Dec')
    ax.yaxis.label.set_fontsize(12)

    plt.show()

    if save:
        fig.savefig(os.path.join(settings.DATA_PATH, 'map.pdf'))
