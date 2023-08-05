""" opentrons.calibration_storage.file_operators: functions that
manipulate the file system.

These methods should only be imported inside the calibration_storage
module, except in the special case of v2 labware support in
the v1 API.
"""
import json
import datetime
import typing

from .types import StrPath
from .encoder_decoder import DateTimeEncoder, DateTimeDecoder


DecoderType = typing.Type[json.JSONDecoder]
EncoderType = typing.Type[json.JSONEncoder]


def read_cal_file(
        filepath: StrPath,
        decoder: DecoderType = DateTimeDecoder) -> typing.Dict:
    """
    Function used to read data from a file

    :param filepath: path to look for data at
    :param decoder: if there is any specialized decoder needed.
    The default decoder is the date time decoder.
    :return: Data from the file
    """
    # TODO(6/16): We should use tagged unions for
    # both the calibration and tip length dicts to better
    # categorize the Typed Dicts used here.
    # This can be done when the labware endpoints
    # are refactored to grab tip length calibration
    # from the correct locations.
    with open(filepath, 'r') as f:
        calibration_data = json.load(f, cls=decoder)
    if isinstance(calibration_data.values(), dict):
        for value in calibration_data.values():
            if value.get('lastModified'):
                assert isinstance(
                    value['lastModified'], datetime.datetime), \
                    "invalid decoded value type for lastModified: got " \
                    f"{type(value['lastModified']).__name__}," \
                    "expected datetime"
    return calibration_data


def save_to_file(
        filepath: StrPath,
        data: typing.Mapping,
        encoder: EncoderType = DateTimeEncoder):
    """
    Function used to save data to a file

    :param filepath: path to save data at
    :param data: data to save
    :param encoder: if there is any specialized encoder needed.
    The default encoder is the date time encoder.
    """
    with open(filepath, 'w') as f:
        json.dump(data, f, cls=encoder)
