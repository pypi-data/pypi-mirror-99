"""
Collect `Line of Route (LOR/PRIDE) <http://www.railwaycodes.org.uk/pride/pride0.shtm>`_ codes.
"""

import copy
import os
import re
import socket
import urllib.error
import urllib.parse

import bs4
import pandas as pd
import requests
from pyhelpers.dir import cd, validate_input_data_dir
from pyhelpers.ops import confirmed, fake_requests_headers
from pyhelpers.store import load_pickle, save_pickle

from pyrcs.utils import cd_dat, get_catalogue, get_last_updated_date, homepage_url, \
    parse_tr, print_conn_err, is_internet_connected, print_connection_error


class LOR:
    """
    A class for collecting Line of Route (LOR/PRIDE) codes.

    - PRIDE: Possession Resource Information Database
    - LOR: Line Of Route

    :param data_dir: name of data directory, defaults to ``None``
    :type data_dir: str or None
    :param update: whether to do an update check (for the package data), defaults to ``False``
    :type update: bool
    :param verbose: whether to print relevant information in console, defaults to ``True``
    :type verbose: bool or int

    :ivar str Name: name of the data
    :ivar str Key: key of the dict-type LOR data
    :ivar str PKey: key of the dict-type prefixes
    :ivar str ELCKey: key of the dict-type ELR/LOR converter data
    :ivar str HomeURL: URL of the main homepage
    :ivar str SourceURL: URL of the data web page
    :ivar str LUDKey: key of the last updated date
    :ivar str LUD: last updated date
    :ivar dict Catalogue: catalogue of the data
    :ivar str DataDir: path to the data directory
    :ivar str CurrentDataDir: path to the current data directory

    **Example**::

        >>> from pyrcs.line_data import LOR

        >>> lor = LOR()

        >>> print(lor.Name)
        Possession Resource Information Database (PRIDE)/Line Of Route (LOR) codes

        >>> print(lor.SourceURL)
        http://www.railwaycodes.org.uk/pride/pride0.shtm
    """

    def __init__(self, data_dir=None, update=False, verbose=True):
        """
        Constructor method.
        """
        if not is_internet_connected():
            print_connection_error(verbose=verbose)

        self.Name = 'Possession Resource Information Database (PRIDE)/Line Of Route (LOR) codes'
        self.Key = 'LOR'
        self.PKey = 'Key to prefixes'
        self.ELCKey = 'ELR/LOR converter'

        self.HomeURL = homepage_url()
        self.SourceURL = urllib.parse.urljoin(self.HomeURL, '/pride/pride0.shtm')

        self.LUDKey = 'Last updated date'
        self.LUD = get_last_updated_date(url=self.SourceURL, parsed=True, as_date_type=False)

        self.Catalogue = get_catalogue(
            url=self.SourceURL, update=update, confirmation_required=False)

        if data_dir:
            self.DataDir = validate_input_data_dir(data_dir)
        else:
            self.DataDir = cd_dat("line-data", self.Key.lower().replace(" ", "-"))
        self.CurrentDataDir = copy.copy(self.DataDir)

    def _cdd_lor(self, *sub_dir, **kwargs):
        """
        Change directory to package data directory and sub-directories (and/or a file).

        The directory for this module: ``"dat\\line-data\\lor-codes"``.

        :param sub_dir: sub-directory or sub-directories (and/or a file)
        :type sub_dir: str
        :param kwargs: optional parameters of `os.makedirs`_, e.g. ``mode=0o777``
        :return: path to the backup data directory for ``LOR``
        :rtype: str

        .. _`os.makedirs`: https://docs.python.org/3/library/os.html#os.makedirs

        :meta private:
        """

        path = cd(self.DataDir, *sub_dir, mkdir=True, **kwargs)

        return path

    def get_keys_to_prefixes(self, prefixes_only=True, update=False, verbose=False):
        """
        Get key to PRIDE/LOR code prefixes.

        :param prefixes_only: whether to get only prefixes, defaults to ``True``
        :type prefixes_only: bool
        :param update: whether to do an update check (for the package data), defaults to ``False``
        :type update: bool
        :param verbose: whether to print relevant information in console, defaults to ``True``
        :type verbose: bool or int
        :return: keys to LOR code prefixes
        :rtype: list or dict

        **Examples**::

            >>> from pyrcs.line_data import LOR

            >>> lor = LOR()

            >>> # keys_to_pfx = lor.get_keys_to_prefixes(update=True, verbose=True)
            >>> keys_to_pfx = lor.get_keys_to_prefixes()

            >>> print(keys_to_pfx)
            ['CY', 'EA', 'GW', 'LN', 'MD', 'NW', 'NZ', 'SC', 'SO', 'SW', 'XR']

            >>> keys_to_pfx = lor.get_keys_to_prefixes(prefixes_only=False)

            >>> type(keys_to_pfx)
            dict
            >>> list(keys_to_pfx.keys())
            ['Key to prefixes', 'Last updated date']

            >>> keys_to_pfx_codes = keys_to_pfx['Key to prefixes']

            >>> type(keys_to_pfx_codes)
            pandas.core.frame.DataFrame
            >>> keys_to_pfx_codes.head()
              Prefixes                                    Name
            0       CY                                   Wales
            1       EA         South Eastern: East Anglia area
            2       GW  Great Western (later known as Western)
            3       LN                  London & North Eastern
            4       MD       North West: former Midlands lines
        """

        path_to_pickle = self._cdd_lor(
            "{}prefixes.pickle".format("" if prefixes_only else "keys-to-"))

        if os.path.isfile(path_to_pickle) and not update:
            keys_to_prefixes = load_pickle(path_to_pickle)

        else:
            try:
                source = requests.get(self.SourceURL, headers=fake_requests_headers())

                soup = bs4.BeautifulSoup(source.text, 'lxml')
                span_tags = soup.find_all('span', attrs={'class': 'tab2'})

                dat = [(span_tag.text, span_tag.next_sibling.strip().replace('=  ', ''))
                       for span_tag in span_tags]

                lor_pref = pd.DataFrame(dat, columns=['Prefixes', 'Name'])

            except (urllib.error.URLError, socket.gaierror):
                verbose_ = \
                    True if (update and verbose != 2) else (False if verbose == 2 else verbose)
                print_conn_err(update=update, verbose=verbose_)

                keys_to_prefixes = load_pickle(path_to_pickle)

            else:
                try:
                    if prefixes_only:
                        keys_to_prefixes = lor_pref.Prefixes.tolist()
                    else:
                        keys_to_prefixes = {self.PKey: lor_pref, self.LUDKey: self.LUD}

                    save_pickle(keys_to_prefixes, path_to_pickle, verbose=verbose)

                except Exception as e:
                    print("Failed to get the keys to LOR prefixes. {}.".format(e))
                    if prefixes_only:
                        keys_to_prefixes = []
                    else:
                        keys_to_prefixes = {self.PKey: None, self.LUDKey: None}

        return keys_to_prefixes

    def get_lor_page_urls(self, update=False, verbose=False):
        """
        Get URLs to PRIDE/LOR codes with different prefixes.

        :param update: whether to do an update check (for the package data), defaults to ``False``
        :type update: bool
        :param verbose: whether to print relevant information in console, defaults to ``True``
        :type verbose: bool or int
        :return: a list of URLs of web pages hosting LOR codes for each prefix
        :rtype: list

        **Example**::

            >>> from pyrcs.line_data import LOR

            >>> lor = LOR()

            >>> # lor_urls = lor.get_lor_page_urls(update=True, verbose=True)
            >>> lor_urls = lor.get_lor_page_urls()

            >>> lor_urls[:2]
            ['http://www.railwaycodes.org.uk/pride/pridecy.shtm',
             'http://www.railwaycodes.org.uk/pride/prideea.shtm']
        """

        path_to_pickle = self._cdd_lor("prefix-page-urls.pickle")

        if os.path.isfile(path_to_pickle) and not update:
            lor_page_urls = load_pickle(path_to_pickle)

        else:
            try:
                source = requests.get(self.SourceURL, headers=fake_requests_headers())
            except requests.ConnectionError:
                verbose_ = \
                    True if (update and verbose != 2) else (False if verbose == 2 else verbose)
                print_conn_err(update=update, verbose=verbose_)
                lor_page_urls = load_pickle(path_to_pickle)

            else:
                try:
                    soup = bs4.BeautifulSoup(source.text, 'lxml')

                    links = soup.find_all(
                        'a', href=re.compile('^pride|elrmapping'),
                        text=re.compile('.*(codes|converter|Historical)'))

                    lor_page_urls = list(dict.fromkeys([self.SourceURL.replace(
                        os.path.basename(self.SourceURL), x['href'])
                        for x in links]))

                    save_pickle(lor_page_urls, path_to_pickle, verbose=verbose)

                except Exception as e:
                    print("Failed to get the URLs to LOR codes web pages. {}.".format(e))
                    lor_page_urls = []

        return lor_page_urls

    def _update_catalogue(self, confirmation_required=True, verbose=False):
        """
        Update catalogue data including keys to prefixes and LOR page URLs.

        :param confirmation_required: whether to confirm before proceeding, defaults to ``True``
        :type confirmation_required: bool
        :param verbose: whether to print relevant information in console, defaults to ``False``
        :type verbose: bool or int

        **Examples**::

            >>> from pyrcs.line_data import LOR

            >>> lor = LOR()

            >>> lor._update_catalogue()
            To update catalogue? [No]|Yes: >? yes
            Updating "keys-to-prefixes.pickle" at "pyrcs\\dat\\line-data\\lor" ... Done.
            Updating "prefix-page-urls.pickle" at "pyrcs\\dat\\line-data\\lor" ... Done.

        :meta private:
        """

        if confirmed("To update catalogue?", confirmation_required=confirmation_required):
            self.get_keys_to_prefixes(prefixes_only=True, update=True, verbose=verbose)
            self.get_keys_to_prefixes(prefixes_only=False, update=True, verbose=2)
            self.get_lor_page_urls(update=True, verbose=2)

    def collect_lor_codes_by_prefix(self, prefix, update=False, verbose=False):
        """
        Collect `PRIDE/LOR codes <http://www.railwaycodes.org.uk/pride/pride0.shtm>`_
        by a given prefix.

        :param prefix: prefix of LOR codes
        :type prefix: str
        :param update: whether to do an update check (for the package data), defaults to ``False``
        :type update: bool
        :param verbose: whether to print relevant information in console, defaults to ``False``
        :type verbose: bool or int
        :return: LOR codes for the given ``prefix``
        :rtype: dict or None

        **Examples**::

            >>> from pyrcs.line_data import LOR

            >>> lor = LOR()

            >>> lor_codes_cy = lor.collect_lor_codes_by_prefix(prefix='CY')

            >>> type(lor_codes_cy)
            dict
            >>> list(lor_codes_cy.keys())
            ['CY', 'Notes', 'Last updated date']

            >>> cy_codes = lor_codes_cy['CY']

            >>> type(cy_codes)
            pandas.core.frame.DataFrame
            >>> cy_codes.head()
                 Code  ... Line Name Note
            0   CY240  ...           None
            1  CY1540  ...           None
            [2 rows x 5 columns]

            >>> lor_codes_nw = lor.collect_lor_codes_by_prefix(prefix='NW')

            >>> type(lor_codes_nw)
            dict
            >>> list(lor_codes_nw.keys())
            ['NW/NZ', 'Notes', 'Last updated date']

            >>> lor_codes_ea = lor.collect_lor_codes_by_prefix(prefix='EA')

            >>> ea_codes = lor_codes_ea['EA']

            >>> type(ea_codes)
            dict
            >>> list(ea_codes.keys())
            ['Current system', 'Original system']

            >>> ea_codes['Current system']['EA'].head()
                 Code  ... Line Name Note
            0  EA1000  ...           None
            1  EA1010  ...           None
            2  EA1011  ...           None
            3  EA1012  ...           None
            4  EA1013  ...           None
            [5 rows x 5 columns]
        """

        available_prefixes = self.get_keys_to_prefixes(prefixes_only=True)

        prefix_ = prefix.upper()

        assert prefix_ in available_prefixes, \
            "`prefix` must be one of {}".format(", ".join(available_prefixes))

        pickle_filename = \
            "{}.pickle".format("nw-nz" if prefix_ in ("NW", "NZ") else prefix_.lower())
        path_to_pickle = self._cdd_lor("prefixes", pickle_filename)

        if os.path.isfile(path_to_pickle) and not update:
            lor_codes_by_initials = load_pickle(path_to_pickle)

        else:
            if prefix_ in ("NW", "NZ"):
                url = self.HomeURL + '/pride/pridenw.shtm'
                prefix_ = "NW/NZ"
            else:
                url = self.HomeURL + '/pride/pride{}.shtm'.format(prefix_.lower())

            if verbose == 2:
                print("To collect LOR codes prefixed by \"{}\". ".format(prefix_), end=" ... ")

            lor_codes_by_initials = None

            try:
                source = requests.get(url, headers=fake_requests_headers())
            except requests.ConnectionError:
                print("Failed.") if verbose == 2 else ""
                print_conn_err(verbose=verbose)

            else:
                try:
                    source_text = source.text
                    source.close()

                    soup = bs4.BeautifulSoup(source_text, 'lxml')

                    # Parse the column of Line Name
                    def parse_line_name(x):
                        # re.search('\w+.*(?= \(\[\')', x).group()
                        # re.search('(?<=\(\[\')\w+.*(?=\')', x).group()
                        try:
                            line_name, line_name_note = x.split(' ([\'')
                            line_name_note = line_name_note.strip('\'])')
                        except ValueError:
                            line_name, line_name_note = x, None
                        return line_name, line_name_note

                    def parse_h3_table(tbl_soup):
                        header, code = tbl_soup
                        header_text = [
                            h.text.replace('\n', ' ') for h in header.find_all('th')]
                        code_dat = pd.DataFrame(
                            parse_tr(header_text, code.find_all('tr')), columns=header_text)
                        line_name_info = code_dat['Line Name'].map(parse_line_name).apply(pd.Series)
                        line_name_info.columns = ['Line Name', 'Line Name Note']
                        code_dat = pd.concat([code_dat, line_name_info], axis=1, sort=False)
                        try:
                            note_dat = dict(
                                [(x['id'].title(), x.text.replace('\xa0', ''))
                                 for x in soup.find('ol').findChildren('a')])
                        except AttributeError:
                            note_dat = dict([('Note', None)])
                        return code_dat, note_dat

                    h3, table_soup = soup.find_all('h3'), soup.find_all('table')
                    if len(h3) == 0:
                        code_data, code_data_notes = parse_h3_table(table_soup)
                        lor_codes_by_initials = {prefix_: code_data, 'Notes': code_data_notes}
                    else:
                        code_data_and_notes = [
                            dict(zip([prefix_, 'Notes'], parse_h3_table(x)))
                            for x in zip(*[iter(table_soup)] * 2)]
                        lor_codes_by_initials = {
                            prefix_: dict(zip([x.text for x in h3], code_data_and_notes))}

                    last_updated_date = get_last_updated_date(url)
                    lor_codes_by_initials.update({self.LUDKey: last_updated_date})

                    print("Done.") if verbose == 2 else ""

                    save_pickle(lor_codes_by_initials, path_to_pickle, verbose=verbose)

                except Exception as e:
                    print("Failed. {}".format(e))

        return lor_codes_by_initials

    def fetch_lor_codes(self, update=False, pickle_it=False, data_dir=None, verbose=False):
        """
        Fetch `PRIDE/LOR codes <http://www.railwaycodes.org.uk/pride/pride0.shtm>`_
        from local backup.

        :param update: whether to do an update check (for the package data), defaults to ``False``
        :type update: bool
        :param pickle_it: whether to save the data as a pickle file, defaults to ``False``
        :type pickle_it: bool
        :param data_dir: name of a folder where the pickle file is to be saved, defaults to ``None``
        :type data_dir: str or None
        :param verbose: whether to print relevant information in console, defaults to ``False``
        :type verbose: bool or int
        :return: LOR codes
        :rtype: dict

        **Example**::

            >>> from pyrcs.line_data import LOR

            >>> lor = LOR()

            >>> # lor_codes_dat = lor.fetch_lor_codes(update=True, verbose=True)
            >>> lor_codes_dat = lor.fetch_lor_codes()

            >>> type(lor_codes_dat)
            dict

            >>> l_codes = lor_codes_dat['LOR']

            >>> type(l_codes)
            dict
            >>> list(l_codes.keys())
            ['CY', 'EA', 'GW', 'LN', 'MD', 'NW/NZ', 'SC', 'SO', 'SW', 'XR']

            >>> cy_codes = l_codes['CY']

            >>> type(cy_codes)
            dict
            >>> list(cy_codes.keys())
            ['CY', 'Notes', 'Last updated date']
        """

        prefixes = self.get_keys_to_prefixes(prefixes_only=True, verbose=verbose)

        verbose_ = False if (data_dir or not verbose) else (2 if verbose == 2 else True)

        lor_codes = [
            self.collect_lor_codes_by_prefix(
                prefix=p, update=update, verbose=verbose_ if is_internet_connected() else False)
            for p in prefixes if p != 'NZ']

        if all(x is None for x in lor_codes):
            if update:
                print_conn_err(verbose=verbose)
                print("No data of the {} has been freshly collected.".format(self.Key.lower()))
            lor_codes = [
                self.collect_lor_codes_by_prefix(prefix=p, update=False, verbose=verbose_)
                for p in prefixes if p != 'NZ']

        prefixes[prefixes.index('NW')] = 'NW/NZ'
        prefixes.remove('NZ')

        lor_codes_data = {self.Key: dict(zip(prefixes, lor_codes))}

        # Get the latest updated date
        last_updated_dates = (item[self.LUDKey] for item, _ in zip(lor_codes, prefixes))
        latest_update_date = max(d for d in last_updated_dates if d is not None)

        lor_codes_data.update({self.LUDKey: latest_update_date})

        if pickle_it and data_dir:
            self.CurrentDataDir = validate_input_data_dir(data_dir)
            path_to_pickle = os.path.join(
                self.CurrentDataDir, self.Key.lower().replace(" ", "-") + ".pickle")
            save_pickle(lor_codes_data, path_to_pickle, verbose=verbose)

        return lor_codes_data

    def collect_elr_lor_converter(self, confirmation_required=True, verbose=False):
        """
        Collect `ELR/LOR converter <http://www.railwaycodes.org.uk/pride/elrmapping.shtm>`_
        from source web page.

        :param confirmation_required: whether to confirm before proceeding, defaults to ``True``
        :type confirmation_required: bool
        :param verbose: whether to print relevant information in console, defaults to ``False``
        :type verbose: bool or int
        :return: data of ELR/LOR converter
        :rtype: dict or None

        **Example**::

            >>> from pyrcs.line_data import LOR

            >>> lor = LOR()

            >>> elr_lor_conv = lor.collect_elr_lor_converter()
            To collect data of ELR/LOR converter? [No]|Yes: yes

            >>> type(elr_lor_conv)
            dict
            >>> list(elr_lor_conv.keys())
            ['ELR/LOR converter', 'Last updated date']

            >>> elr_loc_conv_data = elr_lor_conv['ELR/LOR converter']

            >>> type(elr_loc_conv_data)
            pandas.core.frame.DataFrame
            >>> elr_loc_conv_data.head()
                ELR  ...                                            LOR_URL
            0   AAV  ...  http://www.railwaycodes.org.uk/pride/pridesw.s...
            1   ABD  ...  http://www.railwaycodes.org.uk/pride/pridegw.s...
            2   ABE  ...  http://www.railwaycodes.org.uk/pride/prideln.s...
            3  ABE1  ...  http://www.railwaycodes.org.uk/pride/prideln.s...
            4  ABE2  ...  http://www.railwaycodes.org.uk/pride/prideln.s...
            [5 rows x 6 columns]
        """

        if confirmed("To collect data of {}?".format(self.ELCKey),
                     confirmation_required=confirmation_required):

            url = self.Catalogue[self.ELCKey]

            if verbose == 2:
                print("Collecting data of {}".format(self.ELCKey), end=" ... ")

            elr_lor_converter = None

            try:
                headers, elr_lor_dat = pd.read_html(url)
            except (urllib.error.URLError, socket.gaierror):
                print("Failed.")
                print_conn_err(verbose=verbose)
                return None

            else:
                try:
                    elr_lor_dat.columns = list(headers)
                    #
                    source = requests.get(url, headers=fake_requests_headers())
                    soup = bs4.BeautifulSoup(source.text, 'lxml')
                    # tds = soup.find_all('td')
                    # links = [x.get('href') for x in [y.find('a', href=True) for y in tds]
                    #          if x is not None]
                    elr_links = soup.find_all('td', text=re.compile(r'([A-Z]{3})(\d)?'))
                    lor_links = soup.find_all('a', href=re.compile(r'pride([a-z]{2})\.shtm#'))
                    #
                    # if len(elr_links) != len(elr_lor_dat):
                    #     duplicates = \
                    #         elr_lor_dat[elr_lor_dat.duplicated(['ELR', 'LOR code'], keep=False)]
                    #     for i in duplicates.index:
                    #         if not duplicates['ELR'].loc[i].lower() in elr_links[i]:
                    #             elr_links.insert(i, elr_links[i - 1])
                    #         if not lor_links[i].endswith(
                    #                 duplicates['LOR code'].loc[i].lower()):
                    #             lor_links.insert(i, lor_links[i - 1])
                    #
                    elr_lor_dat['ELR_URL'] = [
                        urllib.parse.urljoin(self.HomeURL, x.a.get('href')) if x.a else None
                        for x in elr_links]
                    elr_lor_dat['LOR_URL'] = [
                        urllib.parse.urljoin(self.HomeURL, 'pride/' + x.get('href'))
                        for x in lor_links]
                    #
                    elr_lor_converter = {self.ELCKey: elr_lor_dat,
                                         self.LUDKey: get_last_updated_date(url)}

                    print("Done.") if verbose == 2 else ""

                    pickle_filename_ = re.sub(r"[/ ]", "-", self.ELCKey.lower())
                    save_pickle(elr_lor_converter, self._cdd_lor(pickle_filename_ + ".pickle"),
                                verbose=verbose)

                except Exception as e:
                    print("Failed. {}".format(e))

            return elr_lor_converter

    def fetch_elr_lor_converter(self, update=False, pickle_it=False, data_dir=None, verbose=False):
        """
        Fetch `ELR/LOR converter <http://www.railwaycodes.org.uk/pride/elrmapping.shtm>`_
        from local backup.

        :param update: whether to do an update check (for the package data), defaults to ``False``
        :type update: bool
        :param pickle_it: whether to save the data as a pickle file, defaults to ``False``
        :type pickle_it: bool
        :param data_dir: name of a folder where the pickle file is to be saved, defaults to ``None``
        :type data_dir: str or None
        :param verbose: whether to print relevant information in console, defaults to ``False``
        :type verbose: bool or int
        :return: data of ELR/LOR converter
        :rtype: dict

        **Example**::

            >>> from pyrcs.line_data import LOR

            >>> lor = LOR()

            >>> # elr_lor_conv = lor.fetch_elr_lor_converter(update=True, verbose=True)
            >>> elr_lor_conv = lor.fetch_elr_lor_converter()

            >>> type(elr_lor_conv)
            dict
            >>> list(elr_lor_conv.keys())
            ['ELR/LOR converter', 'Last updated date']

            >>> elr_loc_conv_data = elr_lor_conv['ELR/LOR converter']

            >>> type(elr_loc_conv_data)
            pandas.core.frame.DataFrame
            >>> elr_loc_conv_data.head()
                ELR  ...                                            LOR_URL
            0   AAV  ...  http://www.railwaycodes.org.uk/pride/pridesw.s...
            1   ABD  ...  http://www.railwaycodes.org.uk/pride/pridegw.s...
            2   ABE  ...  http://www.railwaycodes.org.uk/pride/prideln.s...
            3  ABE1  ...  http://www.railwaycodes.org.uk/pride/prideln.s...
            4  ABE2  ...  http://www.railwaycodes.org.uk/pride/prideln.s...
            [5 rows x 6 columns]
        """

        pickle_filename = re.sub(r"[/ ]", "-", self.ELCKey.lower()) + ".pickle"
        path_to_pickle = self._cdd_lor(pickle_filename)

        if os.path.isfile(path_to_pickle) and not update:
            elr_lor_converter = load_pickle(path_to_pickle)

        else:
            verbose_ = False if (data_dir or not verbose) \
                else (2 if verbose == 2 else True)

            elr_lor_converter = self.collect_elr_lor_converter(
                confirmation_required=False, verbose=verbose_)

            if elr_lor_converter:  # codes_for_ole is not None
                if pickle_it and data_dir:
                    self.CurrentDataDir = validate_input_data_dir(data_dir)
                    path_to_pickle = os.path.join(self.CurrentDataDir, pickle_filename)
                    save_pickle(elr_lor_converter, path_to_pickle, verbose=verbose)
            else:
                print("No data of {} has been freshly collected.".format(self.ELCKey))
                elr_lor_converter = load_pickle(path_to_pickle)

        return elr_lor_converter
