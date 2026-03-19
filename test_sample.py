import pytest
from pydantic import ValidationError
from hub_class import Hub
from simulation_engine import SimEngine
from parsing import parsing
from errors import (
    ConfigError,
    KeysError,
    FormatMetadatasError,
    FormatHubError,
    FirstLineError
    )

ALL = [
    'tests_maps/meta_bad_key.txt', 'tests_maps/too_much_equals.txt',
    'tests_maps/same_coord.txt', 'tests_maps/bad_key.txt',
    'tests_maps/two_start.txt', 'tests_maps/first_line_error.txt'
]


class TestMazeProject:

    def test_bad_hub_name(self) -> bool:
        hub_dict: dict = {
            'x': -1,
            'y': 5,
            'name': 'tr-uc',
            'zone': 'restricted',
            'color': 'red',
            'max_drones': 2,
            'role': 'start'
        }
        with pytest.raises(ValidationError):
            Hub(**hub_dict)

    def test_bad_hub_color(self) -> bool:
        hub_dict: dict = {
            'x': -1,
            'y': 5,
            'name': 'truc',
            'zone': 'restricted',
            'color': 'red_light',
            'max_drones': 2,
            'role': 'start'
        }
        with pytest.raises(ValidationError):
            Hub(**hub_dict)

    def test_bad_hub_nb_drones(self) -> bool:
        hub_dict: dict = {
            'x': -1,
            'y': 5,
            'name': 'tr-uc',
            'zone': 'restricted',
            'color': 'red',
            'max_drones': -2,
            'role': 'start'
        }
        with pytest.raises(ValidationError):
            Hub(**hub_dict)

    def test_missing_key(self) -> bool:
        hub_dict: dict = {
            'x': -1,
            'name': 'truc',
            'zone': 'restricted',
            'color': 'red',
            'max_drones': 2,
            'role': 'start'
        }
        with pytest.raises(ValidationError):
            Hub(**hub_dict)

    def test_parsing_fail(self):
        res: list[int] = []
        for path in ALL:
            try:
                sim: SimEngine = SimEngine(True)
                parsing(sim, path)
            except FormatHubError:
                res.append(2)
            except FormatMetadatasError:
                res.append(3)
            except KeysError:
                res.append(4)
            except FirstLineError:
                res.append(5)
            except ConfigError:
                res.append(1)
        assert 1 in res
        assert 2 in res
        assert 3 in res
        assert 4 in res
        assert 5 in res
