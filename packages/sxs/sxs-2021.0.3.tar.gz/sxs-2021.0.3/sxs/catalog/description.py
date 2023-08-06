"""Full documentation for the contents of the catalog.json file"""


# NOTE: This string is placed into the top of the catalog JSON file as a JSON string.  JSON strings
# are enclosed in double quotes, so it would quickly get ugly if we used double quotes within this
# description, even though python makes that easy.
catalog_file_description = """
    This JSON file has the following format.  Comments are, of course, not present (since JSON does not support
    comments).  Single quotes here are, of course, double quotes in the rest of the file (since JSON encloses
    strings in double quotes).  Anything inside <angle brackets> is just standing in for the relevant value.  An
    ellipsis ... indicates that the preceding structure can be repeated.  Also note that the metadata entries for
    simulations may not be present if the record on zenodo is closed-access; see catalog_private_metadata.json if
    you have access to those simulations, which will contain the missing information.  That file should be read
    and written automatically by functions in this module, so that the catalog dict returned will contain all
    available information.

    {
        'catalog_file_description': '<this description>',
        'modified': '<YYYY-MM-DDThh:mm:ss.ssssss>',  # UTC time of last-modified record in this file
        'records': {  # Includes *all* records published on Zenodo in the 'sxs' community, not just simulations
            '<doi_url>': {  # This is precisely the value of the 'doi_url' key below
                # More details about this 'representation' object at http://developers.zenodo.org/#depositions
                'conceptdoi': '10.5281/zenodo.<conceptrecid>',  # Permanent DOI for all versions of this record
                'conceptrecid': '<conceptrecid>',  # ~7-digit integer (as string) collectively identifying all versions of this record
                'created': '<YYYY-MM-DDThh:mm:ss.ssssss>',  # UTC time of creation of this record on Zenodo
                'doi': '10.5281/zenodo.<id>',  # Permanent DOI for this record
                'doi_url': 'https://doi.org/10.5281/zenodo.<id>',  # URL for permanent DOI of this record
                'id': <id>,  # ~7-digit integer uniquely identifying this record
                'links': {
                     'badge': 'https://zenodo.org/badge/doi/10.5281/zenodo.<id>.svg',
                     'bucket': 'https://zenodo.org/api/files/<uuid>',  # Base URL for file uploads and downloads
                     'conceptbadge': 'https://zenodo.org/badge/doi/10.5281/zenodo.<conceptrecid>.svg',
                     'conceptdoi': 'https://doi.org/10.5281/zenodo.<conceptrecid>',  # Permanent link to webpage for most-recent version
                     'discard': 'https://zenodo.org/api/deposit/depositions/<id>/actions/discard',  # API action to discard a draft
                     'doi': 'https://doi.org/10.5281/zenodo.<id>',  # Permanent URL for this version
                     'edit': 'https://zenodo.org/api/deposit/depositions/<id>/actions/edit',  # API action to edit this record
                     'files': 'https://zenodo.org/api/deposit/depositions/<id>/files',  # Only present for author
                     'html': 'https://zenodo.org/deposit/<id>',  # Webpage for this version
                     'latest': 'https://zenodo.org/api/records/<id>',  # API endpoint for most-recent version
                     'latest_html': 'https://zenodo.org/record/<id>',  # Webpage for most-recent version
                     'publish': 'https://zenodo.org/api/deposit/depositions/<id>/actions/publish',  # Only present for author
                     'record': 'https://zenodo.org/api/records/<id>',  # Only present for author
                     'record_html': 'https://zenodo.org/record/<id>',  # Webpage for this particular version; only present for author
                     'self': 'https://zenodo.org/api/deposit/depositions/<id>'
                },
                'metadata': {  # Note that this is Zenodo metadata, and is different from the SXS metadata found below
                    'access_right': '<access>',  # Can be 'open', 'closed', 'embargoed', or 'restricted'
                    'communities': [
                        {'identifier': '<community_name>'},  # Names may include 'sxs' and 'zenodo'
                        ...
                    ],
                    'creators': [
                        {
                            'name': '<name>',  # Name of this creator in the format Family name, Given names
                            'affiliation': '<affiliation>',  # (Optional) Affiliation of this creator
                            'orcid': '<orcid>',  # (Optional) ORCID identifier of this creator
                            'gnd': '<gnd>'  # (Optional) GND identifier of this creator
                        },
                        ...
                    ],
                    'description': '<description>',  # Text description of this record
                    'doi': '10.5281/zenodo.<id>',  # Permanent DOI of this record
                    'keywords': [
                        '<keyword>',  # Optional; this array may be empty
                        ...
                    ],
                    'license': '<license_type>',  # Usually 'CC-BY-4.0' for SXS
                    'prereserve_doi': {'doi': '10.5281/zenodo.<id>', 'recid': <id>},
                    'publication_date': '<YYYY-MM-DD>',  # Possibly meaningless date (UTC)
                    'title': '<title>',
                    'upload_type': 'dataset'
                },
                'modified': '<YYYY-MM-DDThh:mm:ss.ssssss>',  # (UTC) Last modification of this record (possibly just Zenodo metadata modified)
                'owner': <user_id>,  # ~5-digit integer identifying the user who owns this record
                'record_id': <id>,  # Same as 'id'
                'state': '<state>',  # Can be 'done', 'inprogress', 'error', 'unsubmitted', possibly others
                'submitted': <submitted>,  # True or false (always true for published records)
                'title': '<title>'  # Same as ['metadata']['title'],
                'files': [  # May not be present if this simulation is closed-access; see catalog_private_metadata.json as noted above
                    # See https://data.black-holes.org/waveforms/documentation.html for
                    # detailed descriptions of the *contents* of the files in each record.
                    {
                        'checksum': '<checksum>',  # MD5 checksum of file on Zenodo
                        'filename': '<filename>',  # Name of file; may contain slashes denoting directories
                        'filesize': <filesize>,  # Number of bytes in the file
                        'id': '<fileid>',  # A standard UUID (hexadecimal with characters in the pattern 8-4-4-4-12)
                        'links': {
                            'download': 'https://zenodo.org/api/files/<bucket>/<filename>',  # The URL to use to download this file
                            'self': 'https://zenodo.org/api/deposit/depositions/<deposition_id>/files/<fileid>'  # Ignore this
                        }
                    },
                    ...  # Other file descriptions in the order in which they were uploaded (not necessarily a meaningful order)
                ]
            },
            ...
        },
        'simulations': {  # Physical data (masses, spins, etc.) for all available SXS simulations
            '<sxs_id>': {  # The SXS ID is a string like SXS:BHNS:0001 or SXS:BBH:1234
                'url': '<URL>',  # The URL of the Zenodo 'conceptdoi' link, which *resolves to* the most-recent version
                #
                # NOTE: All of the following may be absent if this simulation is closed-access, or simply does not have metadata.
                #
                # Variable content describing (mostly) physical parameters of the system.  It's basically a
                # python-compatible version of the information contained in 'metadata.txt' from the
                # highest-resolution run in the most-recent version of this simulation.  That file is meant to
                # be more-or-less as suggested in <https://arxiv.org/abs/0709.0093>.  The conversion to a
                # python-compatible format means that keys like 'simulation-name' have had hyphens replaced by
                # underscores so that they can be used as variable names in python and any other sane language
                # (with apologies to Lisp).  As far as possible, values that are just strings in that file
                # have been converted into the relevant types -- like numbers, integers, and arrays.  Note
                # that some keys like eccentricity are sometimes numbers and sometimes the string '<number'
                # (meaning that the eccentricity is less than the number), which is necessarily a string.
                #
                # Below are just the first few keys that *may* be present.  Note that closed-access
                # simulations will have empty dictionaries here.
                #
                'simulation_name': '<directory_name>',  # This may be distinctly uninformative
                'alternative_names': '<sxs_id>',  # This may be a list of strings
                'initial_data_type': '<type>',  # Something like 'BBH_CFMS'
                'object_types': '<type>',  # Currently 'BHBH', 'BHNS', or 'NSNS'
                'number_of_orbits': <number>,  # This is a float, rather than an integer
                'reference_mass_ratio': <q>,  # Usually greater than 1 (exceptions are due to junk radiation)
                'reference_chi_eff': <chi_eff>,  # Dimensionless effective spin quantity
                'reference_chi1_perp': <chi1_perp>,  # Magnitude of component of chi1 orthogonal to 'reference_orbital_frequency'
                'reference_chi2_perp': <chi2_perp>,  # Magnitude of component of chi2 orthogonal to 'reference_orbital_frequency'
                'reference_mass1': <m2>,
                'reference_mass2': <m1>,
                'reference_dimensionless_spin1': [
                    <chi1_x>,
                    <chi1_y>,
                    <chi1_z>
                ],
                'reference_dimensionless_spin2': [
                    <chi2_x>,
                    <chi2_y>,
                    <chi2_z>
                ],
                'reference_eccentricity': <eccentricity>,  # A float or possibly a string containing '<' and a float
                'reference_orbital_frequency': [
                    <omega_x>,
                    <omega_y>,
                    <omega_z>
                ],
                'reference_time': <time>,
                ...
            },
            ...
        }
    }
"""
