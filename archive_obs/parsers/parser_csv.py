"""
@created_at 2017-08-13
@author Exequiel Fuentes Lettura <efulet@gmail.com>
"""

import logging
import os
import progressbar

from astropy.io.fits import Header

from archive_obs.base.util import parse_input_date, daterange
from archive_obs.conf import settings


class ParserCsv:
    """
    Parse FITS header files and convert them in CSV format
    """

    HEADER = [
        'archive',
        'filename',
        'date',
        'ra',
        'dec',
        'instrument',
        'object',
        'obstype',
        'obsid',
        'telescope',
        'elevation',
        'azimuth',
        'ut',
        'exptime',
        'release',
    ]

    def __init__(self, kwargs, logger=None):
        progressbar.streams.wrap_stderr()
        self._logger = logger or logging.getLogger(__name__)

        self.from_date = kwargs.get('from_date')
        self.to_date = kwargs.get('to_date')

        self._data = []

    def parse(self):
        """
        Parse FITS header files, extract filename, date, RA, and Dec and store them as CSV format
        """
        self._logger.info('Parsing all FITS header files '
                          'from {} to {}'.format(self.from_date.strftime('%Y-%m-%d'),
                                                 self.to_date.strftime('%Y-%m-%d')))

        all_archives = settings.SCRAPER_ARCHIVE_URLS.keys()
        self._data = []

        for archive in all_archives:
            self._logger.info('Reading FITS header files for archive {}'.format(archive.title()))

            for single_date in daterange(self.from_date, self.to_date):
                path = os.path.join(settings.RAW_PATH, archive, single_date.strftime('%Y%m%d'))

                file_list = os.listdir(path)

                # For be nicer, we use progressbar ;)
                bar_msg = 'Processing FITS header at {}: '.format(single_date.strftime('%Y-%m-%d'))
                with progressbar.ProgressBar(widgets=[bar_msg, progressbar.Percentage()],
                                             max_value=len(file_list),
                                             redirect_stdout=True) as bar:
                    bar_counter = 0
                    bar.update(bar_counter)

                    # Read all dat files from folder. Maybe here we need to add a kind of filter.
                    # We don't know what FITS header file is useful for our purpose, so we read
                    # all of them
                    for file in file_list:
                        bar_counter += 1
                        bar.update(bar_counter)

                        if file.endswith('{}'.format(settings.FITS_HEADER_EXTENSION)):
                            filepath = os.path.join(path, file)
                            try:
                                self._read_data(single_date, os.path.splitext(file)[0],
                                                archive, filepath)
                            except Exception as err:
                                # Only show this error on debug mode
                                # self._logger.debug('Oops, got an error while parsing FITS '
                                #                    'headers: {}'.format(str(err)))
                                continue

        self._to_csv()

    def _read_data(self, single_date, file, archive, filepath):
        header = Header.fromfile(filepath, sep='\n', endcard=False, padding=False)

        # The coordinates are required for this program, so we don't store data without coordinates
        ra = str(header['RA']).strip()
        dec = str(header['DEC']).strip()

        date_f = single_date.strftime('%Y-%m-%d')
        try:
            date_f = str(header['DATE']).strip()
            try:
                date_f = parse_input_date(date_f).strftime('%Y-%m-%d')
            except ValueError:
                pass
        except Exception as err:
            pass

        instrument = ''
        try:
            instrument = str(header['INSTRUME']).strip()
        except Exception as err:
            pass

        object_f = ''
        try:
            object_f = str(header['OBJECT']).strip()
        except Exception as err:
            pass

        obstype = ''
        try:
            obstype = str(header['OBSTYPE']).strip()
        except Exception as err:
            pass

        obsid = ''
        try:
            obsid = str(header['OBSID']).strip()
        except Exception as err:
            pass

        telescope = ''
        try:
            telescope = str(header['TELESCOP']).strip()
        except Exception as err:
            pass

        elevation = ''
        try:
            elevation = str(header['ELEVATIO']).strip()
        except Exception as err:
            pass

        azimuth = ''
        try:
            azimuth = str(header['AZIMUTH']).strip()
        except Exception as err:
            pass

        ut = ''
        try:
            ut = str(header['UT']).strip()
        except Exception as err:
            pass

        exptime = ''
        try:
            exptime = str(header['EXPTIME']).strip()
        except Exception as err:
            pass

        release = ''
        try:
            release = str(header['RELEASE']).strip()
        except Exception as err:
            pass

        # 'archive', 'filename', 'date', 'ra', 'dec', 'instrument', 'object', 'obstype',
        # 'obsid', 'telescope', 'elevation', 'azimuth', 'ut', 'exptime', 'release'
        self._data.append([
            archive.title(),
            file,
            str(date_f),
            ra,
            dec,
            instrument,
            object_f,
            obstype,
            obsid,
            telescope,
            elevation,
            azimuth,
            ut,
            exptime,
            release,
        ])

    def _to_csv(self):
        """
        Write all FITS header as CSV format
        """
        self._logger.info('Writing CSV file representation...')
        path = os.path.join(settings.CSV_PATH, 'fits_headers.csv')
        with open(path, 'w') as f:
            f.write('\t'.join(self.HEADER) + '\n')
            for data in self._data:
                f.write('\t'.join(data) + '\n')
        self._logger.info('CSV file wrote at: {}'.format(path))
