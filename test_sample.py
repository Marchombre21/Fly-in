import pytest
from pathlib import Path
from pydantic import ValidationError
from hub_class import Hub
from simulation_engine import SimEngine
from parsing import parsing
from errors import ConfigError, KeysError, FormatMetadatasError, FormatHubError, FirstLineError

ALL = [
    'tests_maps/meta_bad_key.txt', 'tests_maps/too_much_equals.txt',
    'tests_maps/same_coord.txt', 'tests_maps/too_much_spaces.txt',
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

    # def test_parsing_fail(self):
    #     res: list[int] = []
    #     sim: SimEngine = SimEngine(True)
    #     for path in ALL:
    #         try:
    #             parsing(sim, path)
    #         except FormatHubError:
    #             res.append(2)
    #         except FormatMetadatasError:
    #             res.append(3)
    #         except KeysError:
    #             res.append(4)
    #         except FirstLineError:
    #             res.append(5)
    #         except ConfigError:
    #             res.append(1)
    #     assert 1 in res
    #     assert 2 in res
    #     assert 3 in res
    #     assert 4 in res
    #     assert 5 in res

    # def test_parsing_invalid_file(self) -> None:
    #     """Check the behavior with unknown file"""
    #     with pytest.raises(FileNotFoundError):
    #         parsing_config("unknown_file.txt")

    # def test_parsing_bad_values(self, tmp_path: Path) -> None:
    #     """Check the behavior with negative values"""

    #     # Creating a temp_file with wrong values
    #     d = tmp_path / "sub"
    #     d.mkdir()
    #     bad_config = d / "bad_config.txt"
    #     bad_config.write_text("width=-10\nheight=20\ncell_size=10\nentry=10\n"
    #                           "exit=10\nOUTPUT_FILE=maze.txt\nPERFECT=true\n")

    #     # Check that the program raise the expected error
    #     with pytest.raises(ConfigError):
    #         parsing_config(str(bad_config))

    # def test_high_sizes(self, tmp_path: Path) -> None:
    #     """Check the behavior with out of range values"""
    #     # Creating a temp_file with wrong values
    #     d = tmp_path / "sub"
    #     d.mkdir()
    #     bad_config = d / "bad_config.txt"
    #     bad_config.write_text("width=1000\nheight=20\nentry=10,19\n"
    #                           "exit=10\nOUTPUT_FILE=maze.txt\nPERFECT=true\n")

    #     # Check that the program raise the expected error
    #     with pytest.raises(ConfigError):
    #         parsing_config(str(bad_config))

    # def test_wrong_output_file(self, tmp_path: Path) -> None:
    #     """Check the behavior with an output file not in .txt"""
    #     # Creating a temp_file with wrong values
    #     d = tmp_path / "sub"
    #     d.mkdir()
    #     bad_config = d / "bad_config.txt"
    #     bad_config.write_text("width=30\nheight=20\nentry=10,19\n"
    #                           "exit=10,6\nOUTPUT_FILE=maze.py\nPERFECT=true\n")

    #     # Check that the program raise the expected error
    #     with pytest.raises(FormatError):
    #         parsing_config(str(bad_config))
