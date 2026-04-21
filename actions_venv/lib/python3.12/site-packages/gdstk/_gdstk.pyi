import pathlib
import datetime
import sys
from typing import Optional, Iterable, Any
from collections.abc import Callable, Sequence

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

import numpy
from numpy.typing import ArrayLike # type: ignore

class Cell:
    labels: list[Label]
    name: str
    paths: list[FlexPath | RobustPath]
    polygons: list[Polygon]
    properties: list[list[str | bytes | float]]
    references: list[Reference]
    def __init__(self, name: str) -> None: ...
    def add(self, *elements: Polygon | FlexPath | RobustPath | Label | Reference) -> Self: ...
    def area(self, by_spec: bool = False) -> float | dict[tuple[int, int], float]: ...
    def bounding_box(self) -> Optional[tuple[tuple[float, float], tuple[float, float]]]: ...
    def convex_hull(self) -> numpy.ndarray[Any, numpy.dtype[numpy.float64]]: ...
    def copy(
        self,
        name: str,
        translation: tuple[float, float] | complex = (0, 0),
        rotation: float = 0,
        magnification: float = 1,
        x_reflection: bool = False,
        deep_copy: bool = True,
    ) -> Cell: ...
    def delete_property(self, name: str) -> Self: ...
    def dependencies(self, recursive: bool = True) -> Sequence[Cell | RawCell]: ...
    def filter(
        self,
        spec: Iterable[tuple[int, int]],
        remove: bool = True,
        polygons: bool = True,
        paths: bool = True,
        labels: bool = True,
    ) -> Self: ...
    def flatten(self, apply_repetitions: bool = True) -> Self: ...
    def get_labels(
        self,
        apply_repetitions: bool = True,
        depth: Optional[int] = None,
        layer: Optional[int] = None,
        texttype: Optional[int] = None,
    ) -> list[Label]: ...
    def get_paths(
        self,
        apply_repetitions: bool = True,
        depth: Optional[int] = None,
        layer: Optional[int] = None,
        datatype: Optional[int] = None,
    ) -> list[RobustPath | FlexPath]: ...
    def get_polygons(
        self,
        apply_repetitions: bool = True,
        include_paths: bool = True,
        depth: Optional[int] = None,
        layer: Optional[int] = None,
        datatype: Optional[int] = None,
    ) -> list[Polygon]: ...
    def get_property(self, name: str) -> Optional[list[list[str | bytes | float]]]: ...
    def remove(self, *elements: Label | Polygon | RobustPath | FlexPath | Reference) -> Self: ...
    def set_property(
        self, name: str, value: str | bytes | float | Sequence[str | bytes | float]
    ) -> Self: ...
    def write_svg(
        self,
        outfile: str | pathlib.Path,
        scaling: float = 10,
        precision: int = 6,
        shape_style: Optional[dict[tuple[int, int], dict[str, str]]] = None,
        label_style: Optional[dict[tuple[int, int], dict[str, str]]] = None,
        background: str = "#222222",
        pad: float | str = "5%",
        sort_function: Optional[Callable[[Polygon, Polygon], bool]] = None,
    ) -> Self: ...

class Curve:
    tolerance: float
    def __init__(self, xy: tuple[float, float] | complex, tolerance: float = 0.01) -> None: ...
    def arc(
        self,
        radius: float | tuple[float, float],
        initial_angle: float,
        final_angle: float,
        rotation: float = 0,
    ) -> Self: ...
    def bezier(
        self, xy: Sequence[tuple[float, float] | complex], relative: bool = False
    ) -> Self: ...
    def commands(self, *args: float | str) -> Self: ...
    def cubic(
        self, xy: Sequence[tuple[float, float] | complex], relative: bool = False
    ) -> Self: ...
    def cubic_smooth(
        self, xy: Sequence[tuple[float, float] | complex], relative: bool = False
    ) -> Self: ...
    def horizontal(self, x: Sequence[float] | float, relative: bool = False) -> Self: ...
    def interpolation(
        self,
        points: Sequence[tuple[float, float]],
        angles: Optional[Sequence[float]] = None,
        tension_in: float | Sequence[float] = 1,
        tension_out: float | Sequence[float] = 1,
        initial_curl: float = 1,
        final_curl: float = 1,
        cycle: bool = False,
        relative: bool = False,
    ) -> Self: ...
    def parametric(
        self,
        curve_function: Callable[[float], tuple[float, float] | complex],
        relative: bool = True,
    ) -> Self: ...
    def points(self) -> numpy.ndarray[Any, numpy.dtype[numpy.float64]]: ...
    def quadratic(
        self, xy: Sequence[tuple[float, float] | complex], relative: bool = False
    ) -> Self: ...
    def quadratic_smooth(
        self, xy: Sequence[tuple[float, float] | complex], relative: bool = False
    ) -> Self: ...
    def segment(
        self,
        xy: tuple[float, float] | complex | Sequence[tuple[float, float] | complex],
        relative: bool = False,
    ) -> Self: ...
    def turn(self, radius: float, angle: float) -> Self: ...
    def vertical(self, y: float | Sequence[float], relative: bool = False) -> Self: ...

class RaithData:
    base_cell_name: str
    dwelltime_selection: int
    pitch_parallel_to_path: float
    pitch_perpendicular_to_path: float
    pitch_scale: float
    periods: int
    grating_type: int
    dots_per_cycle: int
    def __init__(
        self,
        base_cell_name: str,
        dwelltime_selection: int,
        pitch_parallel_to_path: float,
        pitch_perpendicular_to_path: float,
        pitch_scale: float,
        periods: int,
        grating_type: int,
        dots_per_cycle: int,
    ) -> None: ...

class FlexPath:
    bend_function: tuple[
        Optional[Callable[[float, float, float, float], list[tuple[float, float]]]], ...
    ]
    bend_radius: tuple[float, ...]
    datatypes: tuple[int, ...]
    ends: tuple[
        Literal["flush", "extended", "round", "smooth"]
        | tuple[float, float]
        | Callable[[float, float, float, float], list[tuple[float, float]]],
        ...,
    ]
    joins: tuple[
        Literal["natural", "miter", "bevel", "round", "smooth"]
        | Callable[[float, float, float, float, float, float], list[tuple[float, float]]],
        ...,
    ]
    layers: tuple[int, ...]
    num_paths: int
    properties: list[list[str | bytes | float]]
    repetition: Repetition
    scale_width: bool
    simple_path: bool
    size: int
    tolerance: float
    raith_data: RaithData
    def __init__(
        self,
        points: tuple[float, float] | complex | Sequence[tuple[float, float] | complex],
        width: float | Sequence[float],
        offset: float | Sequence[float] = 0,
        joins: Literal["natural", "miter", "bevel", "round", "smooth"]
        | Callable[
            [float, float, float, float, float, float], Sequence[tuple[float, float] | complex]
        ]
        | Sequence[
            Literal["natural", "miter", "bevel", "round", "smooth"]
            | Callable[
                [float, float, float, float, float, float], Sequence[tuple[float, float] | complex]
            ]
        ] = "natural",
        ends: Literal["flush", "extended", "round", "smooth"]
        | tuple[float, float]
        | Callable[[float, float, float, float], Sequence[tuple[float, float] | complex]]
        | Sequence[
            Literal["flush", "extended", "round", "smooth"]
            | tuple[float, float]
            | Callable[[float, float, float, float], Sequence[tuple[float, float] | complex]]
        ] = "flush",
        bend_radius: float | Sequence[float] = 0,
        bend_function: Optional[
            Callable[[float, float, float, float], Sequence[tuple[float, float] | complex]]
        ]
        | Sequence[
            Callable[[float, float, float, float], Sequence[tuple[float, float] | complex]]
        ] = None,
        tolerance: float = 1e-2,
        simple_path: bool = False,
        scale_width: bool = True,
        layer: int | Sequence[int] = 0,
        datatype: int | Sequence[int] = 0,
    ) -> None: ...
    def apply_repetition(self) -> list[Self]: ...
    def arc(
        self,
        radius: float | tuple[float, float],
        initial_angle: float,
        final_angle: float,
        rotation: float = 0,
        width: Optional[float] | Sequence[float] = None,
        offset: Optional[float] | Sequence[float] = None,
    ) -> Self: ...
    def bezier(
        self,
        xy: Sequence[tuple[float, float] | complex],
        width: Optional[float] | Sequence[float] = None,
        offset: Optional[float] | Sequence[float] = None,
        relative: bool = False,
    ) -> Self: ...
    def commands(self, *args: str | float) -> Self: ...
    def copy(self) -> Self: ...
    def cubic(
        self,
        xy: Sequence[tuple[float, float] | complex],
        width: Optional[float] | Sequence[float] = None,
        offset: Optional[float] | Sequence[float] = None,
        relative: bool = False,
    ) -> Self: ...
    def cubic_smooth(
        self,
        xy: Sequence[tuple[float, float] | complex],
        width: Optional[float] | Sequence[float] = None,
        offset: Optional[float] | Sequence[float] = None,
        relative: bool = False,
    ) -> Self: ...
    def delete_gds_property(self, attr: int) -> Self: ...
    def delete_property(self, name: str) -> Self: ...
    def get_gds_property(self, attr: int) -> Optional[str]: ...
    def get_property(self, name: str) -> Optional[list[list[str | bytes | float]]]: ...
    def horizontal(
        self,
        x: float | Sequence[float],
        width: Optional[float] | Sequence[float] = None,
        offset: Optional[float] | Sequence[float] = None,
        relative: bool = False,
    ) -> Self: ...
    def interpolation(
        self,
        points: Sequence[tuple[float, float] | complex],
        angles: Optional[Sequence[float]] = None,
        tension_in: float | Sequence[float] = 1,
        tension_out: float | Sequence[float] = 1,
        initial_curl: float = 1,
        final_curl: float = 1,
        cycle: bool = False,
        width: Optional[float] | Sequence[float] = None,
        offset: Optional[float] | Sequence[float] = None,
        relative: bool = False,
    ) -> Self: ...
    def mirror(
        self, p1: tuple[float, float] | complex, p2: tuple[float, float] | complex = (0, 0)
    ) -> Self: ...
    def offsets(self) -> numpy.ndarray[Any, numpy.dtype[numpy.float64]]: ...
    def parametric(
        self,
        path_function: Callable[[float], tuple[float, float] | complex],
        width: Optional[float] | Sequence[float] = None,
        offset: Optional[float] | Sequence[float] = None,
        relative: bool = True,
    ) -> Self: ...
    def path_spines(self) -> list[numpy.ndarray[Any, numpy.dtype[numpy.float64]]]: ...
    def quadratic(
        self,
        xy: Sequence[tuple[float, float] | complex],
        width: Optional[float] | Sequence[float] = None,
        offset: Optional[float] | Sequence[float] = None,
        relative: bool = False,
    ) -> Self: ...
    def quadratic_smooth(
        self,
        xy: Sequence[tuple[float, float] | complex],
        width: Optional[float] | Sequence[float] = None,
        offset: Optional[float] | Sequence[float] = None,
        relative: bool = False,
    ) -> Self: ...
    def rotate(self, angle: float, center: tuple[float, float] | complex = (0, 0)) -> Self: ...
    def scale(self, s: float, center: tuple[float, float] | complex = (0, 0)) -> Self: ...
    def segment(
        self,
        xy: Sequence[tuple[float, float] | complex] | tuple[float, float] | complex,
        width: Optional[float] | Sequence[float] = None,
        offset: Optional[float] | Sequence[float] = None,
        relative: bool = False,
    ) -> Self: ...
    def set_bend_function(
        self,
        functions: Optional[Callable[[float, float, float, float], Sequence[tuple[float, float]]]],
    ) -> Self: ...
    def set_bend_radius(self, *radii: Optional[float]) -> Self: ...
    def set_datatypes(self, *datatypes: int) -> Self: ...
    def set_ends(
        self,
        *ends: Literal["flush", "extended", "round", "smooth"]
        | tuple[float, float]
        | Callable[[float, float, float, float], Sequence[float]],
    ) -> Self: ...
    def set_gds_property(self, attr: int, value: str) -> Self: ...
    def set_joins(
        self,
        *joins: Literal["natural", "miter", "bevel", "round", "smooth"]
        | Callable[
            [float, float, float, float, float, float], Sequence[tuple[float, float] | complex]
        ],
    ) -> Self: ...
    def set_layers(self, *layers: int) -> Self: ...
    def set_property(
        self, name: str, value: str | bytes | float | Sequence[str | bytes | float]
    ) -> Self: ...
    def spine(self) -> numpy.ndarray[Any, numpy.dtype[numpy.float64]]: ...
    def to_polygons(self) -> list[Polygon]: ...
    def translate(
        self, dx: float | tuple[float, float] | complex, dy: Optional[float] = None
    ) -> Self: ...
    def turn(
        self,
        radius: float,
        angle: float,
        width: Optional[float] | Sequence[float] = None,
        offset: Optional[float] | Sequence[float] = None,
    ) -> Self: ...
    def vertical(
        self,
        y: float | Sequence[float],
        width: Optional[float] | Sequence[float] = None,
        offset: Optional[float] | Sequence[float] = None,
        relative: bool = False,
    ) -> Self: ...
    def widths(self) -> numpy.ndarray[Any, numpy.dtype[numpy.float64]]: ...

class GdsWriter:
    def __init__(
        self,
        outfile: str | pathlib.Path,
        name: str = "library",
        unit: float = 1e-6,
        precision: float = 1e-9,
        max_points: int = 199,
        timestamp: Optional[datetime.datetime] = None,
    ) -> None: ...
    def close(self) -> None: ...
    def write(self, *cells: Cell | RawCell) -> Self: ...

class Label:
    anchor: Literal["n", "s", "e", "w", "ne", "nw", "se", "sw", "o"]
    layer: int
    magnification: float
    origin: tuple[float, float]
    properties: list[list[str | bytes | float]]
    repetition: Repetition
    rotation: float
    text: str
    texttype: int
    x_reflection: bool
    def __init__(
        self,
        text: str,
        origin: tuple[float, float] | complex,
        anchor: Literal["n", "s", "e", "w", "ne", "nw", "se", "sw", "o"] = "o",
        rotation: float = 0,
        magnification: float = 1,
        x_reflection: bool = False,
        layer: int = 0,
        texttype: int = 0,
    ) -> None: ...
    def apply_repetition(self) -> list[Self]: ...
    def copy(self) -> Self: ...
    def delete_gds_property(self, attr: int) -> Self: ...
    def delete_property(self, name: str) -> Self: ...
    def get_gds_property(self, attr: int) -> Optional[str]: ...
    def get_property(self, name: str) -> Optional[list[list[str | bytes | float]]]: ...
    def set_gds_property(self, attr: int, value: str) -> Self: ...
    def set_property(
        self, name: str, value: str | bytes | float | Sequence[str | bytes | float]
    ) -> Self: ...

class Library:
    cells: list[Cell | RawCell]
    name: str
    precision: float
    properties: list[list[str | bytes | float]]
    unit: float
    def __init__(
        self, name: str = "library", unit: float = 1e-6, precision: float = 1e-9
    ) -> None: ...
    def add(self, *cells: Cell | RawCell) -> Self: ...
    def delete_property(self, name: str) -> Self: ...
    def get_property(self, name: str) -> Optional[list[list[str | bytes | float]]]: ...
    layer_names: dict[tuple[int, int], tuple[str, str]]
    def layers_and_datatypes(self) -> set[tuple[int, int]]: ...
    def layers_and_texttypes(self) -> set[tuple[int, int]]: ...
    def new_cell(self, name: str) -> Cell: ...
    def remove(self, *cells: Cell | RawCell) -> Self: ...
    def rename_cell(self, old_name: str, new_name: str) -> Self: ...
    def replace(self, *cells: Cell | RawCell) -> Self: ...
    def set_property(
        self, name: str, value: str | bytes | float | Sequence[str | bytes | float]
    ) -> Self: ...
    def top_level(self) -> list[Cell | RawCell]: ...
    def write_gds(
        self,
        outfile: str | pathlib.Path,
        max_points: int = 199,
        timestamp: Optional[datetime.datetime] = None,
    ) -> None: ...
    def write_oas(
        self,
        outfile: str | pathlib.Path,
        compression_level: int = 6,
        detect_rectangles: bool = True,
        detect_trapezoids: bool = True,
        circletolerance: float = 0,
        standard_properties: bool = False,
        validation: Optional[Literal["crc32", "checksum32"]] = None,
    ) -> None: ...

class Polygon:
    datatype: int
    layer: int
    points: list[tuple[float, float]]
    properties: list[list[str | bytes | float]]
    repetition: Repetition
    size: int
    def __init__(
        self, points: Sequence[tuple[float, float] | complex], layer: int = 0, datatype: int = 0
    )-> None: ...
    def apply_repetition(self) -> list[Self]: ...
    def area(self) -> float: ...
    def perimeter(self) -> float: ...
    def bounding_box(self) -> tuple[tuple[float, float], tuple[float, float]]: ...
    def contain(self, *points: tuple[float, float] | complex) -> bool | tuple[bool, ...]: ...
    def contain_all(self, *points: tuple[float, float] | complex) -> bool: ...
    def contain_any(self, *points: tuple[float, float] | complex) -> bool: ...
    def copy(self) -> Self: ...
    def delete_gds_property(self, attr: int) -> Self: ...
    def delete_property(self, name: str) -> Self: ...
    def fillet(self, radius: float | Sequence[float], tolerance: float = 0.01) -> Self: ...
    def fracture(self, max_points: int = 199, precision: float = 1e-3) -> list[Polygon]: ...
    def get_gds_property(self, attr: int) -> Optional[str]: ...
    def get_property(self, name: str) -> Optional[list[list[str | bytes | float]]]: ...
    def mirror(
        self, p1: tuple[float, float] | complex, p2: tuple[float, float] | complex = (0, 0)
    ) -> Self: ...
    def rotate(self, angle: float, center: tuple[float, float] | complex = (0, 0)) -> Self: ...
    def scale(
        self, sx: float, sy: float = 0, center: tuple[float, float] | complex = (0, 0)
    ) -> Self: ...
    def set_gds_property(self, attr: int, value: str) -> Self: ...
    def set_property(
        self, name: str, value: str | bytes | float | Sequence[str | bytes | float]
    ) -> Self: ...
    def transform(
        self,
        magnification: float = 1,
        x_reflection: bool = False,
        rotation: float = 0,
        translation: Optional[tuple[float, float] | complex] = None,
        matrix: Optional[ArrayLike] = None, # type: ignore
    ) -> Self: ...
    def translate(
        self, dx: float | tuple[float, float] | complex, dy: Optional[float] = None
    ) -> Self: ...

class RawCell:
    name: str
    size: int
    def __init__(self, name: str)-> None: ...
    def dependencies(self, recursive: bool = True) -> list[RawCell]: ...

class Reference:
    cell: Cell
    cell_name: str
    magnification: float
    origin: tuple[float, float]
    properties: list[list[str | bytes | float]]
    repetition: Repetition
    rotation: float
    x_reflection: bool
    def __init__(
        self,
        cell: Cell,
        origin: tuple[float, float] | complex = (0, 0),
        rotation: float = 0,
        magnification: float = 1,
        x_reflection: bool = False,
        columns: int = 1,
        rows: int = 1,
        spacing: Optional[Sequence[float]] = ...,
    )-> None: ...
    def apply_repetition(self) -> list[Self]: ...
    def bounding_box(self) -> tuple[tuple[float, float], tuple[float, float]]: ...
    def convex_hull(self) -> numpy.ndarray[Any, numpy.dtype[numpy.float64]]: ...
    def copy(self) -> Self: ...
    def delete_gds_property(self, attr: int) -> Self: ...
    def delete_property(self, name: str) -> Self: ...
    def get_gds_property(self, attr: int) -> Optional[str]: ...
    def get_labels(
        self,
        apply_repetitions: bool = True,
        depth: Optional[int] = None,
        layer: Optional[int] = None,
        texttype: Optional[int] = None,
    ) -> list[Label]: ...
    def get_paths(
        self,
        apply_repetitions: bool = True,
        depth: Optional[int] = None,
        layer: Optional[int] = None,
        datatype: Optional[int] = None,
    ) -> list[RobustPath | FlexPath]: ...
    def get_polygons(
        self,
        apply_repetitions: bool = True,
        include_paths: bool = True,
        depth: Optional[int] = None,
        layer: Optional[int] = None,
        datatype: Optional[int] = None,
    ) -> list[Polygon]: ...
    def get_property(self, name: str) -> Optional[list[list[str | bytes | float]]]: ...
    def set_gds_property(self, attr: int, value: str) -> Self: ...
    def set_property(
        self, name: str, value: str | bytes | float | Sequence[str | bytes | float]
    ) -> Self: ...

class Repetition:
    columns: Optional[int]
    offsets: Optional[numpy.ndarray[Any, numpy.dtype[numpy.float64]]]
    rows: Optional[int]
    size: int
    spacing: Optional[tuple[float, float]]
    v1: Optional[tuple[float, float]]
    v2: Optional[tuple[float, float]]
    x_offsets: Optional[numpy.ndarray[Any, numpy.dtype[numpy.float64]]]
    y_offsets: Optional[numpy.ndarray[Any, numpy.dtype[numpy.float64]]]
    def __init__(
        self,
        columns: Optional[int] = None,
        rows: Optional[int] = None,
        spacing: Optional[tuple[float, float] | complex] = None,
        v1: Optional[tuple[float, float] | complex] = None,
        v2: Optional[tuple[float, float] | complex] = None,
        offsets: Optional[Sequence[tuple[float, float] | complex]] = None,
        x_offsets: Optional[Sequence[float]] = None,
        y_offsets: Optional[Sequence[float]] = None,
    )-> None: ...
    def get_offsets(self) -> numpy.ndarray[Any, numpy.dtype[numpy.float64]]: ...

class RobustPath:
    datatypes: tuple[int, ...]
    ends: tuple[
        Literal["flush", "extended", "round", "smooth"]
        | tuple[float, float]
        | Callable[[float, float, float, float], Sequence[complex | tuple[float, float]]],
        ...,
    ]
    layers: tuple[int, ...]
    max_evals: int
    num_paths: int
    properties: list[list[str | bytes | float]]
    repetition: Repetition
    scale_width: bool
    simple_path: bool
    size: int
    tolerance: float
    def __init__(
        self,
        initial_point: tuple[float, float] | complex,
        width: float | Sequence[float],
        offset: float | Sequence[float] = 0,
        ends: Sequence[
            Literal["flush", "extended", "round", "smooth"]
            | tuple[float, float]
            | Callable[[float, float, float, float], Sequence[complex | tuple[float, float]]]
        ]
        | Literal["flush", "extended", "round", "smooth"]
        | tuple[float, float]
        | Callable[[float, float, float, float], Sequence[complex | tuple[float, float]]] = "flush",
        tolerance: float = 1e-2,
        max_evals: int = 1000,
        simple_path: bool = False,
        scale_width: bool = True,
        layer: int | list[int] = 0,
        datatype: int | list[int] = 0,
    )->None: ...
    def apply_repetition(self) -> list[Self]: ...
    def arc(
        self,
        radius: float | tuple[float, float],
        initial_angle: float,
        final_angle: float,
        rotation: float = 0,
        width: Optional[float]
        | tuple[float, Literal["constant", "linear", "smooth"]]
        | Callable[[float], float]
        | Sequence[
            float | tuple[float, Literal["constant", "linear", "smooth"]] | Callable[[float], float]
        ] = None,
        offset: Optional[float]
        | tuple[float, Literal["constant", "linear", "smooth"]]
        | Callable[[float], float]
        | Sequence[
            float | tuple[float, Literal["constant", "linear", "smooth"]] | Callable[[float], float]
        ] = None,
    ) -> Self: ...
    def bezier(
        self,
        xy: Sequence[tuple[float, float] | complex],
        width: Optional[float]
        | tuple[float, Literal["constant", "linear", "smooth"]]
        | Callable[[float], float]
        | Sequence[
            float | tuple[float, Literal["constant", "linear", "smooth"]] | Callable[[float], float]
        ] = None,
        offset: Optional[float]
        | tuple[float, Literal["constant", "linear", "smooth"]]
        | Callable[[float], float]
        | Sequence[
            float | tuple[float, Literal["constant", "linear", "smooth"]] | Callable[[float], float]
        ] = None,
        relative: bool = False,
    ) -> Self: ...
    def commands(self, *args: str | float) -> Self: ...
    def copy(self) -> Self: ...
    def cubic(
        self,
        xy: Sequence[tuple[float, float]],
        width: Optional[float]
        | tuple[float, Literal["constant", "linear", "smooth"]]
        | Callable[[float], float]
        | Sequence[
            float | tuple[float, Literal["constant", "linear", "smooth"]] | Callable[[float], float]
        ] = None,
        offset: Optional[float]
        | tuple[float, Literal["constant", "linear", "smooth"]]
        | Callable[[float], float]
        | Sequence[
            float | tuple[float, Literal["constant", "linear", "smooth"]] | Callable[[float], float]
        ] = None,
        relative: bool = False,
    ) -> Self: ...
    def cubic_smooth(
        self,
        xy: Sequence[tuple[float, float]],
        width: Optional[float]
        | tuple[float, Literal["constant", "linear", "smooth"]]
        | Callable[[float], float]
        | Sequence[
            float | tuple[float, Literal["constant", "linear", "smooth"]] | Callable[[float], float]
        ] = None,
        offset: Optional[float]
        | tuple[float, Literal["constant", "linear", "smooth"]]
        | Callable[[float], float]
        | Sequence[
            float | tuple[float, Literal["constant", "linear", "smooth"]] | Callable[[float], float]
        ] = None,
        relative: bool = False,
    ) -> Self: ...
    def delete_gds_property(self, attr: int) -> Self: ...
    def delete_property(self, name: str) -> Self: ...
    def get_gds_property(self, attr: int) -> Optional[str]: ...
    def get_property(self, name: str) -> Optional[list[list[str | bytes | float]]]: ...
    def gradient(self, u: float, from_below: bool = True) -> numpy.ndarray[Any, numpy.dtype[numpy.float64]]: ...
    def horizontal(
        self,
        x: float,
        width: Optional[float]
        | tuple[float, Literal["constant", "linear", "smooth"]]
        | Callable[[float], float]
        | Sequence[
            float | tuple[float, Literal["constant", "linear", "smooth"]] | Callable[[float], float]
        ] = None,
        offset: Optional[float]
        | tuple[float, Literal["constant", "linear", "smooth"]]
        | Callable[[float], float]
        | Sequence[
            float | tuple[float, Literal["constant", "linear", "smooth"]] | Callable[[float], float]
        ] = None,
        relative: bool = False,
    ) -> Self: ...
    def interpolation(
        self,
        points: Sequence[tuple[float, float] | complex],
        angles: Optional[Sequence[float]] = None,
        tension_in: float | Sequence[float] = 1,
        tension_out: float | Sequence[float] = 1,
        initial_curl: float = 1,
        final_curl: float = 1,
        cycle: bool = False,
        width: Optional[float]
        | tuple[float, Literal["constant", "linear", "smooth"]]
        | Callable[[float], float]
        | Sequence[
            float | tuple[float, Literal["constant", "linear", "smooth"]] | Callable[[float], float]
        ] = None,
        offset: Optional[float]
        | tuple[float, Literal["constant", "linear", "smooth"]]
        | Callable[[float], float]
        | Sequence[
            float | tuple[float, Literal["constant", "linear", "smooth"]] | Callable[[float], float]
        ] = None,
        relative: bool = True,
    ) -> Self: ...
    def mirror(
        self, p1: tuple[float, float] | complex, p2: tuple[float, float] | complex = (0, 0)
    ) -> Self: ...
    def offsets(self, u: float, from_below: bool = True) -> numpy.ndarray[Any, numpy.dtype[numpy.float64]]: ...
    def parametric(
        self,
        path_function: Callable[[float], tuple[float, float] | complex],
        path_gradient: Optional[Callable[[float], tuple[float, float] | complex]] = None,
        width: Optional[float]
        | tuple[float, Literal["constant", "linear", "smooth"]]
        | Callable[[float], float]
        | Sequence[
            float | tuple[float, Literal["constant", "linear", "smooth"]] | Callable[[float], float]
        ] = None,
        offset: Optional[float]
        | tuple[float, Literal["constant", "linear", "smooth"]]
        | Callable[[float], float]
        | Sequence[
            float | tuple[float, Literal["constant", "linear", "smooth"]] | Callable[[float], float]
        ] = None,
        relative: bool = True,
    ) -> Self: ...
    def path_spines(self) -> list[numpy.ndarray[Any, numpy.dtype[numpy.float64]]]: ...
    def position(self, u: float, from_below: bool = True) -> numpy.ndarray[Any, numpy.dtype[numpy.float64]]: ...
    def quadratic(
        self,
        xy: Sequence[tuple[float, float] | complex],
        width: Optional[float]
        | tuple[float, Literal["constant", "linear", "smooth"]]
        | Callable[[float], float]
        | Sequence[
            float | tuple[float, Literal["constant", "linear", "smooth"]] | Callable[[float], float]
        ] = None,
        offset: Optional[float]
        | tuple[float, Literal["constant", "linear", "smooth"]]
        | Callable[[float], float]
        | Sequence[
            float | tuple[float, Literal["constant", "linear", "smooth"]] | Callable[[float], float]
        ] = None,
        relative: bool = False,
    ) -> Self: ...
    def quadratic_smooth(
        self,
        xy: tuple[float, float] | complex,
        width: Optional[float]
        | tuple[float, Literal["constant", "linear", "smooth"]]
        | Callable[[float], float]
        | Sequence[
            float | tuple[float, Literal["constant", "linear", "smooth"]] | Callable[[float], float]
        ] = None,
        offset: Optional[float]
        | tuple[float, Literal["constant", "linear", "smooth"]]
        | Callable[[float], float]
        | Sequence[
            float | tuple[float, Literal["constant", "linear", "smooth"]] | Callable[[float], float]
        ] = None,
        relative: bool = False,
    ) -> Self: ...
    def rotate(self, angle: float, center: tuple[float, float] | complex = (0, 0)) -> Self: ...
    def scale(self, s: float, center: tuple[float, float] | complex = (0, 0)) -> Self: ...
    def segment(
        self,
        xy: tuple[float, float] | complex,
        width: Optional[float]
        | tuple[float, Literal["constant", "linear", "smooth"]]
        | Callable[[float], float]
        | Sequence[
            float | tuple[float, Literal["constant", "linear", "smooth"]] | Callable[[float], float]
        ] = None,
        offset: Optional[float]
        | tuple[float, Literal["constant", "linear", "smooth"]]
        | Callable[[float], float]
        | Sequence[
            float | tuple[float, Literal["constant", "linear", "smooth"]] | Callable[[float], float]
        ] = None,
        relative: bool = False,
    ) -> Self: ...
    def set_datatypes(self, *datatypes: int) -> Self: ...
    def set_ends(
        self,
        *ends: Literal["flush", "extended", "round", "smooth"]
        | tuple[float, float]
        | Callable[[float, float, float, float], float],
    ) -> Self: ...
    def set_gds_property(self, attr: int, value: str) -> Self: ...
    def set_layers(self, *layers: int) -> Self: ...
    def set_property(
        self, name: str, value: str | bytes | float | Sequence[str | bytes | float]
    ) -> Self: ...
    def spine(self) -> numpy.ndarray[Any, numpy.dtype[numpy.float64]]: ...
    def to_polygons(self) -> list[Polygon]: ...
    def translate(
        self, dx: float | tuple[float, float] | complex, dy: Optional[float] = None
    ) -> Self: ...
    def turn(
        self,
        radius: float,
        angle: float,
        width: Optional[float] | Sequence[float] = None,
        offset: Optional[float] | Sequence[float] = None,
    ) -> Self: ...
    def vertical(
        self,
        y: float,
        width: Optional[float]
        | tuple[float, Literal["constant", "linear", "smooth"]]
        | Callable[[float], float]
        | Sequence[
            float | tuple[float, Literal["constant", "linear", "smooth"]] | Callable[[float], float]
        ] = None,
        offset: Optional[float]
        | tuple[float, Literal["constant", "linear", "smooth"]]
        | Callable[[float], float]
        | Sequence[
            float | tuple[float, Literal["constant", "linear", "smooth"]] | Callable[[float], float]
        ] = None,
        relative: bool = False,
    ) -> Self: ...
    def widths(self, u: float, from_below: bool = True) -> numpy.ndarray[Any, numpy.dtype[numpy.float64]]: ...

def all_inside(
    points: Sequence[tuple[float, float] | complex],
    polygons: Polygon
    | FlexPath
    | RobustPath
    | Reference
    | Sequence[Polygon | FlexPath | RobustPath | Reference],
) -> bool: ...
def any_inside(
    points: Sequence[tuple[float, float] | complex],
    polygons: Polygon
    | FlexPath
    | RobustPath
    | Reference
    | Sequence[Polygon | FlexPath | RobustPath | Reference],
) -> bool: ...
def boolean(
    operand1: Polygon
    | FlexPath
    | RobustPath
    | Reference
    | Sequence[Polygon | FlexPath | RobustPath | Reference],
    operand2: Polygon
    | FlexPath
    | RobustPath
    | Reference
    | Sequence[Polygon | FlexPath | RobustPath | Reference],
    operation: Literal["or", "and", "xor", "not"],
    precision: float = 1e-3,
    layer: int = 0,
    datatype: int = 0,
) -> list[Polygon]: ...
def contour(
    data: ArrayLike, # type: ignore
    level: int = 0,
    length_scale: float = 1,
    precision: float = 0.01,
    layer: int = 0,
    datatype: int = 0,
) -> list[Polygon]: ...
def cross(
    center: tuple[float, float] | complex,
    full_size: float,
    arm_width: float,
    layer: int = 0,
    datatype: int = 0,
) -> Polygon: ...
def ellipse(
    center: tuple[float, float] | complex,
    radius: float | tuple[float, float],
    inner_radius: Optional[float] | tuple[float, float] = None,
    initial_angle: float = 0,
    final_angle: float = 0,
    tolerance: float = 0.01,
    layer: int = 0,
    datatype: int = 0,
) -> Polygon: ...
def gds_info(infile: str | pathlib.Path) -> dict[str, Any]: ...

def gds_timestamp(filename: str | pathlib.Path, timestamp:Optional[datetime.datetime]=None) -> datetime.datetime: ...
def gds_units(infile: str | pathlib.Path) -> tuple[float, float]: ...
def inside(
    points: Sequence[tuple[float, float] | complex],
    polygons: Polygon
    | FlexPath
    | RobustPath
    | Reference
    | Sequence[Polygon | FlexPath | RobustPath | Reference],
) -> tuple[bool, ...]: ...
def oas_precision(infile: str | pathlib.Path) -> float: ...
def oas_validate(infile: str | pathlib.Path) -> tuple[bool, int]: ...
def offset(
    polygons: Polygon
    | FlexPath
    | RobustPath
    | Reference
    | Sequence[Polygon | FlexPath | RobustPath | Reference],
    distance: float,
    join: Literal["miter", "bevel", "round"] = "miter",
    tolerance: int = 2,
    precision: float = 1e-3,
    use_union: bool = False,
    layer: int = 0,
    datatype: int = 0,
) -> list[Polygon]: ...
def racetrack(
    center: tuple[float, float] | complex,
    straight_length: float,
    radius: float,
    inner_radius: float = 0,
    vertical: bool = False,
    tolerance: float = 0.01,
    layer: int = 0,
    datatype: int = 0,
) -> Polygon: ...
def read_gds(
    infile: str | pathlib.Path,
    unit: float = 0,
    tolerance: float = 0,
    filter: Optional[Iterable[tuple[int, int]]] = None,
) -> Library: ...
def read_oas(infile: str | pathlib.Path, unit: float = 0, tolerance: float = 0) -> Library: ...
def read_rawcells(infile: str | pathlib.Path) -> dict[str, RawCell]: ...
def rectangle(
    corner1: tuple[float, float] | complex,
    corner2: tuple[float, float] | complex,
    layer: int = 0,
    datatype: int = 0,
) -> Polygon: ...
def regular_polygon(
    center: tuple[float, float] | complex,
    side_length: float,
    sides: int,
    rotation: float = 0,
    layer: int = 0,
    datatype: int = 0,
) -> Polygon: ...
def slice(
    polygons: Polygon
    | FlexPath
    | RobustPath
    | Reference
    | Sequence[Polygon | FlexPath | RobustPath | Reference],
    position: float | Sequence[float],
    axis: Literal["x", "y"],
    precision: float = 1e-3,
) -> list[list[Polygon]]: ...
def text(
    text: str,
    size: float,
    position: tuple[float, float] | complex,
    vertical: bool = False,
    layer: int = 0,
    datatype: int = 0,
) -> list[Polygon]: ...
