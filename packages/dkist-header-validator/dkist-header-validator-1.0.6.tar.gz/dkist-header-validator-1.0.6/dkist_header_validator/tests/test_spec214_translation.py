from io import BytesIO
from pathlib import Path

import pytest
from astropy.io import fits

from dkist_header_validator import spec214_validator
from dkist_header_validator.exceptions import ValidationException


def test_translate_spec214(valid_spec_214_header):
    """
    Validates and tries to translate a fits header against the SPEC-0214 schema
    Given: A valid SPEC-0214 fits header
    When: Validating headers
    Then: return translated HDUList and do not raise an exception
    """
    # raises exception on failure
    spec214_validator.validate_and_translate(valid_spec_214_header)


def test_translate_spec214_return_dictionary(valid_spec_214_header):
    """
    Validates and tries to translate a fits header against the SPEC-0214 schema
    Given: A valid SPEC-0214 fits header
    When: Validating headers
    Then: return translated dictionary and do not raise an exception
    """
    # raises exception on failure
    spec214_validator.validate_and_translate(valid_spec_214_header, return_type=dict)


def test_translate_spec214_return_fits_header(valid_spec_214_header):
    """
    Validates and tries to translate a fits header against the SPEC-0214 schema
    Given: A valid SPEC-0214 fits header
    When: Validating headers
    Then: return translated fits.header.Header object and do not raise an exception
    """
    # raises exception on failure
    spec214_validator.validate_and_translate(valid_spec_214_header, return_type=fits.header.Header)


def test_translate_spec214_return_BytesIO(valid_spec_214_file):
    """
    Validates and tries to translate a fits header against the SPEC-0214 schema
    Given: A valid SPEC-0214 fits header
    When: Validating headers
    Then: return translated BytesIO object and do not raise an exception
    """
    # raises exception on failure
    spec214_validator.validate_and_translate(valid_spec_214_file, return_type=BytesIO)


def test_and_translate_spec214_return_file(valid_spec_214_file):
    """
    Validates and tries to translate a fits header against the SPEC-0214 schema
    Given: A valid SPEC-0214 fits header
    When: Validating headers
    Then: return translated file object and do not raise an exception
    """
    # raises exception on failure
    spec214_validator.validate_and_translate(valid_spec_214_file, return_type=Path)


def test_translate_toomanyHDUs(valid_spec_214_header_toomanyHDUs):
    """
    Validates headers with too many (more than 2) HDUs
    Given: A valid SPEC-214 file or HDUList with more than two headers
    When: Validating and translating headers
    Then: Raise an exception
    """
    # raises exception on failure
    with pytest.raises(ValidationException):
        spec214_validator.validate_and_translate(valid_spec_214_header_toomanyHDUs)


def test_translate_datainsecondHDU(valid_spec_214_header_datainsecondHDU):
    """
    Validates headers with data stored in second HDU
    Given: A valid SPEC-214 file or with data stored in second HDU
    When: Validating and translating headers
    Then: Raise an exception
    """
    # raises exception on failure
    spec214_validator.validate_and_translate(
        valid_spec_214_header_datainsecondHDU, return_type=Path
    )
