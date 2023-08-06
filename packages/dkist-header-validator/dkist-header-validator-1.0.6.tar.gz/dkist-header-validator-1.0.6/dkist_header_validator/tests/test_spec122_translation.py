from io import BytesIO
from pathlib import Path

import numpy as np
import pytest
from astropy.io import fits

from dkist_header_validator import spec122_validator
from dkist_header_validator import Spec122ValidationException


def test_translate_spec122(valid_spec_122_header):
    """
    Validates and tries to translate a fits header against the SPEC-122 schema
    Given: A valid SPEC-122 fits header
    When: Validating headers
    Then: return translated HDUList and do not raise an exception
    """
    # raises exception on failure
    spec122_validator.validate_and_translate(valid_spec_122_header)


def test_translate_spec122_return_dictionary(
    valid_spec_122_header,
):
    """
    Validates and tries to translate a fits header against the SPEC-122 schema
    Given: A valid SPEC-122 fits header
    When: Validating headers
    Then: return translated dictionary and do not raise an exception
    """
    # raises exception on failure
    spec122_validator.validate_and_translate(valid_spec_122_header, return_type=dict)


def test_translate_spec122_return_header(
    valid_spec_122_header,
):
    """
    Validates and tries to translate a fits header against the SPEC-122 schema
    Given: A valid SPEC-122 fits header
    When: Validating headers
    Then: return translated fits.header.Header object and do not raise an exception
    """
    # raises exception on failure
    spec122_validator.validate_and_translate(valid_spec_122_header, return_type=fits.header.Header)


def test_translate_spec122_return_BytesIO(valid_spec_122_file):
    """
    Validates and tries to translate a fits header against the SPEC-122 schema
    Given: A valid SPEC-122 fits header
    When: Validating headers
    Then: return translated BytesIO object and do not raise an exception
    """
    # raises exception on failure
    spec122_validator.validate_and_translate(valid_spec_122_file, return_type=BytesIO)


def test_translate_spec122_return_file(valid_spec_122_file):
    """
    Validates and tries to translate a fits file against the SPEC-122 schema
    Given: A valid SPEC-122 fits file
    When: Validating file
    Then: return translated file object and do not raise an exception
    """
    # raises exception on failure
    spec122_validator.validate_and_translate(valid_spec_122_file, return_type=Path)


@pytest.fixture(scope="module")
def spec_122_headers_extrakeys(tmpdir_factory):
    """
    Create a dict of valid spec 122 headers to be used in successful
    header tests below with extra keys.
    """
    valid_spec_122_dict_extrakeys = {
        "NAXIS": 3,
        "BITPIX": 16,
        "NAXIS1": 1,
        "NAXIS2": 1,
        "NAXIS3": 1,
        "INSTRUME": "VBI-BLUE",
        "WAVELNTH": 430.0,
        "DATE-BGN": "2017-05-29T12:00:13.345",
        "DATE-END": "2017-05-30T20:00:13.345",
        "CHECKSUM": "POLETJWHTN2PMM1ZPPLPWQ1KBAKIUF",
        "DATE-OBS": "2017-05-30T00:46:13.952",
        "ID___002": "YVPS4YRBSXUT9Z17Z4HRH3VIH7T6KO",
        "ID___008": "JX3O8NXFI6FGTVZ1D7G7U8OVUWDZQL",
        "ID___012": "1XXPIDR5CEXMZ0SQ8LT3HMF83FW4HJ",
        "ID___013": "2KJBWEFB4OUUBSFUIB5JKBSDF8JBSK",
        "DKIST003": "OSZ4FBHWKXRWQGOVG9BJNUWNG5795B",
        "DKIST004": "Observation",
        "WCSAXES": 3,
        "WCSNAME": "Helioprojective Cartesian",
        "CRPIX1": 13.4,
        "CRPIX2": 14.6,
        "CRPIX3": 15.6,
        "CRVAL1": 16.7,
        "CRVAL2": 18.5,
        "CRVAL3": 18.6,
        "CDELT1": 20.4,
        "CDELT2": 67.8,
        "CDELT3": 78.8,
        "CUNIT1": "deg",
        "CUNIT2": "deg",
        "CUNIT3": "deg",
        "CTYPE1": "x",
        "CTYPE2": "y",
        "CTYPE3": "z",
        "PC1_1": 13.5,
        "PC1_2": 13.5,
        "PC2_1": 13.5,
        "PC2_2": 13.5,
        "PC1_3": 13.5,
        "PC3_2": 13.5,
        "PC2_3": 13.5,
        "PC3_1": 13.5,
        "PC3_3": 13.5,
        "BUNIT": "ct",
        "DATE": "2017-05-30T00:46:13.952",
        "ORIGIN": "4L6XY2SM39CNQTOO4L04Y3RV0H2MTW",
        "TELESCOP": "DKIST",
        "OBSERVAT": "NSO",
        "NETWORK": "ABCD",
        "OBJECT": "SUNSPOT N62",
        "DATASUM": "E5O2YIVIP04EOEL59NGM",
        "XTRAKEY1": "ABCDEFG",
        "XTRAKEY2": "HIJKLMN",
        "XTRAKEY3": "OPQRSTU",
        "XTRAKEY4": "VWXYZAB",
    }

    temp_dir = tmpdir_factory.mktemp("valid spec_122_headers_extrakeys_temp")
    file_name = temp_dir.join("tmp_fits_file_extrakeys.fits")
    temp_array = np.ones((1, 1, 1), dtype=np.int16)
    valid_hdu_extrakeys = fits.PrimaryHDU(temp_array)
    # Use the valid_spec_122_dict from above to overwrite the default header
    for (key, value) in valid_spec_122_dict_extrakeys.items():
        valid_hdu_extrakeys.header[key] = value
    valid_hdu_list_extrakeys = fits.HDUList([valid_hdu_extrakeys])
    valid_hdu_list_extrakeys.writeto(str(file_name))

    yield {
        "valid_dkist_hdr_extrakeys.fits": Path(file_name),
        "valid_spec_122_dict_extrakeys": valid_spec_122_dict_extrakeys,
        "valid_HDUList_extrakeys": valid_hdu_list_extrakeys,
        "valid header_extrakeys": valid_hdu_extrakeys.header,
    }


@pytest.fixture(
    scope="function",
    params=[
        "valid_dkist_hdr_extrakeys.fits",
        "valid_spec_122_dict_extrakeys",
        "valid_HDUList_extrakeys",
        "valid header_extrakeys",
    ],
)
def spec_122_header_extrakeys(request, spec_122_headers_extrakeys):
    yield spec_122_headers_extrakeys[request.param]


def test_spec122_extrakeys_allowed(spec_122_header_extrakeys):
    """
    Validates a fits header against the SPEC-0122 schema
    Given: A valid SPEC-0122 fits header with extra keys
    When: Validating headers
    Then: return HDUList and do not raise an exception
    """
    # raises exception on failure
    spec122_validator.validate_and_translate(spec_122_header_extrakeys)


def test_spec122_valid_extrakeys_not_allowed(spec_122_header_extrakeys):
    """
    Validates a fits header against the SPEC-0122 schema
    Given: A valid SPEC-0122 fits header with extra keys
    When: Validating headers
    Then: Raise a Spec122ValidationException
    """
    with pytest.raises(Spec122ValidationException):
        spec122_validator.validate_and_translate(spec_122_header_extrakeys, extra=False)


def test_translate_compressed_spec122(valid_compressed_spec_122_header):
    """
    Validates and translates a compressed spec122 compliant file
    Given: A valid compressed SPEC-0122 file
    When: Validating headers
    Then: return valid HDUList and do not raise an exception
    """
    spec122_validator.validate_and_translate(valid_compressed_spec_122_header)


def test_visp_translate(valid_visp_122_header):
    """
    Validates a visp fits header against the SPEC-122 schema
    Given: A valid visp SPEC-122 fits header
    When: Validating headers
    Then: return validated HDUList and do not raise an exception
    """
    # raises exception on failure
    spec122_validator.validate_and_translate(valid_visp_122_header, return_type=dict)


def test_translate_datainsecondHDU(valid_spec_122_header_datainsecondHDU):
    """
    Validates headers with data stored in second HDU
    Given: A valid SPEC-122 file or with data stored in second HDU
    When: Validating and translating headers
    Then: Raise an exception
    """
    # raises exception on failure
    spec122_validator.validate_and_translate(
        valid_spec_122_header_datainsecondHDU, return_type=Path
    )
