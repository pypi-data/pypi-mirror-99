# Copyright (c) 2020-2021, Manfred Moitzi
# License: MIT License
from typing import (
    TYPE_CHECKING, List, Iterable, Union, Tuple, Optional, Dict, Callable,
)
from functools import singledispatch
import enum
import math
from ezdxf.math import (
    Vec2, Vec3, Z_AXIS, NULLVEC, OCS, Bezier3P, Bezier4P,
    ConstructionEllipse, BSpline, have_bezier_curves_g1_continuity,
    global_bspline_interpolation, Vertex,
)
from ezdxf.lldxf import const
from ezdxf.entities import (
    LWPolyline, Polyline, Hatch, Line, Spline, Ellipse, Arc, Circle, Solid,
    Trace, Face3d, Viewport, Image, Helix, Wipeout,
)
from .path import Path
from .commands import Command
from . import tools
from .nesting import group_paths

if TYPE_CHECKING:
    from ezdxf.entities.hatch import PolylinePath, EdgePath, TPath

__all__ = [
    'make_path', 'to_lines', 'to_polylines3d', 'to_lwpolylines',
    'to_polylines2d', 'to_hatches', 'to_bsplines_and_vertices',
    'to_splines_and_polylines', 'from_hatch', 'from_hatch_boundary_path',
    'from_vertices', 'from_matplotlib_path', 'from_qpainter_path',
    'to_matplotlib_path', 'to_qpainter_path'
]

MAX_DISTANCE = 0.01
MIN_SEGMENTS = 4
G1_TOL = 1e-4


@singledispatch
def make_path(entity, segments: int = 1, level: int = 4) -> Path:
    """ Factory function to create a single :class:`Path` object from a DXF
    entity.

    Args:
        entity: DXF entity
        segments: minimal count of cubic Bézier-curves for elliptical arcs
        level: subdivide level for SPLINE approximation

    Raises:
        TypeError: for unsupported DXF types

    """
    # Complete documentation is path.rst, because Sphinx auto-function
    # renders for each overloaded function a signature, which is ugly
    # and wrong signatures for multiple overloaded function
    # e.g. 3 equal signatures for type Solid.
    raise TypeError(f'unsupported DXF type: {entity.dxftype()}')


@make_path.register(LWPolyline)
def _from_lwpolyline(lwpolyline: LWPolyline, **kwargs) -> 'Path':
    path = Path()
    tools.add_2d_polyline(
        path,
        lwpolyline.get_points('xyb'),
        close=lwpolyline.closed,
        ocs=lwpolyline.ocs(),
        elevation=lwpolyline.dxf.elevation,
    )
    return path


@make_path.register(Polyline)
def _from_polyline(polyline: Polyline, **kwargs) -> 'Path':
    if polyline.is_polygon_mesh or polyline.is_poly_face_mesh:
        raise TypeError('Unsupported DXF type PolyMesh or PolyFaceMesh')

    path = Path()
    if len(polyline.vertices) == 0:
        return path

    if polyline.is_3d_polyline:
        return from_vertices(polyline.points(), polyline.is_closed)

    points = [vertex.format('xyb') for vertex in polyline.vertices]
    ocs = polyline.ocs()
    if polyline.dxf.hasattr('elevation'):
        elevation = Vec3(polyline.dxf.elevation).z
    else:
        # Elevation attribute is mandatory, but you never know,
        # take elevation from first vertex.
        elevation = Vec3(polyline.vertices[0].dxf.location).z
    tools.add_2d_polyline(
        path,
        points,
        close=polyline.is_closed,
        ocs=ocs,
        elevation=elevation,
    )
    return path


@make_path.register(Helix)
@make_path.register(Spline)
def _from_spline(spline: Spline, **kwargs) -> 'Path':
    level = kwargs.get('level', 4)
    path = Path()
    tools.add_spline(path, spline.construction_tool(), level=level, reset=True)
    return path


@make_path.register(Ellipse)
def _from_ellipse(ellipse: Ellipse, **kwargs) -> 'Path':
    segments = kwargs.get('segments', 1)
    path = Path()
    tools.add_ellipse(path,
                      ellipse.construction_tool(),
                      segments=segments,
                      reset=True)
    return path


@make_path.register(Line)
def _from_line(line: Line, **kwargs) -> 'Path':
    path = Path(line.dxf.start)
    path.line_to(line.dxf.end)
    return path


@make_path.register(Arc)
def _from_arc(arc: Arc, **kwargs) -> 'Path':
    segments = kwargs.get('segments', 1)
    path = Path()
    radius = abs(arc.dxf.radius)
    if not math.isclose(radius, 0):
        ellipse = ConstructionEllipse.from_arc(
            center=arc.dxf.center,
            radius=radius,
            extrusion=arc.dxf.extrusion,
            start_angle=arc.dxf.start_angle,
            end_angle=arc.dxf.end_angle,
        )
        tools.add_ellipse(path, ellipse, segments=segments, reset=True)
    return path


@make_path.register(Circle)
def _from_circle(circle: Circle, **kwargs) -> 'Path':
    segments = kwargs.get('segments', 1)
    path = Path()
    radius = abs(circle.dxf.radius)
    if not math.isclose(radius, 0):
        ellipse = ConstructionEllipse.from_arc(
            center=circle.dxf.center,
            radius=radius,
            extrusion=circle.dxf.extrusion,
        )
        tools.add_ellipse(path, ellipse, segments=segments, reset=True)
    return path


@make_path.register(Face3d)
@make_path.register(Trace)
@make_path.register(Solid)
def _from_quadrilateral(solid: 'Solid', **kwargs) -> 'Path':
    vertices = solid.wcs_vertices()
    return from_vertices(vertices, close=True)


@make_path.register(Viewport)
def _from_viewport(vp: 'Viewport', **kwargs) -> Path:
    if vp.has_clipping_path():
        handle = vp.dxf.clipping_boundary_handle
        if handle != '0' and vp.doc:  # exist
            db = vp.doc.entitydb
            if db:  # exist
                # Many DXF entities can define a clipping path:
                clipping_entity = vp.doc.entitydb.get(handle)
                if clipping_entity:  # exist
                    return make_path(clipping_entity, **kwargs)
    # Return bounding box:
    return from_vertices(vp.boundary_path(), close=True)


@make_path.register(Wipeout)
@make_path.register(Image)
def _from_image(image: 'Image', **kwargs) -> Path:
    return from_vertices(image.boundary_path_wcs(), close=True)


def from_hatch(hatch: Hatch) -> Iterable[Path]:
    """ Yield all HATCH boundary paths as separated :class:`Path` objects.

    .. versionadded:: 0.16

    """
    ocs = hatch.ocs()
    elevation = hatch.dxf.elevation.z
    for boundary in hatch.paths:
        yield from_hatch_boundary_path(boundary, ocs, elevation)


def from_hatch_boundary_path(boundary: 'TPath', ocs: OCS = None,
                             elevation: float = 0) -> 'Path':
    """ Returns a :class:`Path` object from a :class:`~ezdxf.entities.Hatch`
    polyline- or edge path.
    """
    if boundary.PATH_TYPE == 'EdgePath':
        return from_hatch_edge_path(boundary, ocs, elevation)
    else:
        return from_hatch_polyline_path(boundary, ocs, elevation)


def from_hatch_polyline_path(polyline: 'PolylinePath', ocs: OCS = None,
                             elevation: float = 0) -> 'Path':
    """ Returns a :class:`Path` object from a :class:`~ezdxf.entities.Hatch`
    polyline path.
    """
    path = Path()
    tools.add_2d_polyline(
        path,
        polyline.vertices,  # List[(x, y, bulge)]
        close=polyline.is_closed,
        ocs=ocs or OCS(),
        elevation=elevation,
    )
    return path


def from_hatch_edge_path(edges: 'EdgePath', ocs: OCS = None,
                         elevation: float = 0) -> 'Path':
    """ Returns a :class:`Path` object from a :class:`~ezdxf.entities.Hatch`
    edge path.
    """

    def add_line_edge(edge):
        start = wcs(edge.start)
        end = wcs(edge.end)
        if len(path):
            if path.end.isclose(start):
                # path-end -> line-end
                path.line_to(end)
            elif path.end.isclose(end):
                # path-end (==line-end) -> line-start
                path.line_to(start)
            else:
                # path-end -> edge-start -> edge-end
                path.line_to(start)
                path.line_to(end)
        else:  # start path
            path.start = start
            path.line_to(end)

    def add_arc_edge(edge):
        x, y, *_ = edge.center
        # from_arc() requires OCS data:
        ellipse = ConstructionEllipse.from_arc(
            center=(x, y, elevation),
            radius=edge.radius,
            extrusion=extrusion,
            start_angle=edge.start_angle,
            end_angle=edge.end_angle,
        )
        tools.add_ellipse(path, ellipse, reset=not bool(path))

    def add_ellipse_edge(edge):
        ocs_ellipse = edge.construction_tool()
        # ConstructionEllipse has WCS representation:
        ellipse = ConstructionEllipse(
            center=wcs(ocs_ellipse.center.replace(z=elevation)),
            major_axis=wcs(ocs_ellipse.major_axis),
            ratio=ocs_ellipse.ratio,
            extrusion=extrusion,
            start_param=ocs_ellipse.start_param,
            end_param=ocs_ellipse.end_param,
        )
        tools.add_ellipse(path, ellipse, reset=not bool(path))

    def add_spline_edge(edge):
        control_points = [wcs(p) for p in edge.control_points]
        if len(control_points) == 0:
            fit_points = [wcs(p) for p in edge.fit_points]
            if len(fit_points):
                bspline = from_fit_points(edge, fit_points)
            else:
                # No control points and no fit points:
                # DXF structure error
                return
        else:
            bspline = from_control_points(edge, control_points)
        tools.add_spline(path, bspline, reset=not bool(path))

    def from_fit_points(edge, fit_points):
        tangents = None
        if edge.start_tangent and edge.end_tangent:
            tangents = (
                wcs(edge.start_tangent),
                wcs(edge.end_tangent)
            )
        return global_bspline_interpolation(
            fit_points,
            degree=edge.degree,
            tangents=tangents,
        )

    def from_control_points(edge, control_points):
        return BSpline(
            control_points=control_points,
            order=edge.degree + 1,
            knots=edge.knot_values,
            weights=edge.weights if edge.weights else None
        )

    def wcs(vertex):
        if ocs and ocs.transform:
            return ocs.to_wcs((vertex.x, vertex.y, elevation))
        else:
            return Vec3(vertex)

    extrusion = ocs.uz if ocs else Z_AXIS
    path = Path()
    for edge in edges:
        if edge.EDGE_TYPE == "LineEdge":
            add_line_edge(edge)
        elif edge.EDGE_TYPE == "ArcEdge":
            if not math.isclose(edge.radius, 0):
                add_arc_edge(edge)
        elif edge.EDGE_TYPE == "EllipseEdge":
            if not NULLVEC.isclose(edge.major_axis):
                add_ellipse_edge(edge)
        elif edge.EDGE_TYPE == "SplineEdge":
            add_spline_edge(edge)

    return path


def from_vertices(vertices: Iterable['Vertex'], close=False) -> Path:
    """ Returns a :class:`Path` object from the given `vertices`.  """
    vertices = Vec3.list(vertices)
    if len(vertices) < 2:
        return Path()
    path = Path(start=vertices[0])
    for vertex in vertices[1:]:
        path.line_to(vertex)
    if close:
        path.close()
    return path


def to_lwpolylines(
        paths: Iterable[Path], *,
        distance: float = MAX_DISTANCE,
        segments: int = MIN_SEGMENTS,
        extrusion: 'Vertex' = Z_AXIS,
        dxfattribs: Optional[Dict] = None) -> Iterable[LWPolyline]:
    """ Convert the given `paths` into :class:`~ezdxf.entities.LWPolyline`
    entities.
    The `extrusion` vector is applied to all paths, all vertices are projected
    onto the plane normal to this extrusion vector. The default extrusion vector
    is the WCS z-axis. The plane elevation is the distance from the WCS origin
    to the start point of the first path.

    Args:
        paths: iterable of :class:`Path` objects
        distance:  maximum distance, see :meth:`Path.flattening`
        segments: minimum segment count per Bézier curve
        extrusion: extrusion vector for all paths
        dxfattribs: additional DXF attribs

    Returns:
        iterable of :class:`~ezdxf.entities.LWPolyline` objects

    .. versionadded:: 0.16

    """
    if isinstance(paths, Path):
        paths = [paths]
    else:
        paths = list(paths)
    if len(paths) == 0:
        return []

    extrusion = Vec3(extrusion)
    reference_point = paths[0].start
    dxfattribs = dxfattribs or dict()
    if not extrusion.isclose(Z_AXIS):
        ocs, elevation = _get_ocs(extrusion, reference_point)
        paths = tools.transform_paths_to_ocs(paths, ocs)
        dxfattribs['elevation'] = elevation
        dxfattribs['extrusion'] = extrusion
    elif reference_point.z != 0:
        dxfattribs['elevation'] = reference_point.z

    for path in paths:
        p = LWPolyline.new(dxfattribs=dxfattribs)
        p.append_points(path.flattening(distance, segments), format='xy')
        yield p


def _get_ocs(extrusion: Vec3, referenc_point: Vec3) -> Tuple[OCS, float]:
    ocs = OCS(extrusion)
    elevation = ocs.from_wcs(referenc_point).z
    return ocs, elevation


def to_polylines2d(
        paths: Iterable[Path],
        *,
        distance: float = MAX_DISTANCE,
        segments: int = MIN_SEGMENTS,
        extrusion: 'Vertex' = Z_AXIS,
        dxfattribs: Optional[Dict] = None) -> Iterable[Polyline]:
    """ Convert the given `paths` into 2D :class:`~ezdxf.entities.Polyline`
    entities.
    The `extrusion` vector is applied to all paths, all vertices are projected
    onto the plane normal to this extrusion vector. The default extrusion vector
    is the WCS z-axis. The plane elevation is the distance from the WCS origin
    to the start point of the first path.

    Args:
        paths: iterable of :class:`Path` objects
        distance:  maximum distance, see :meth:`Path.flattening`
        segments: minimum segment count per Bézier curve
        extrusion: extrusion vector for all paths
        dxfattribs: additional DXF attribs

    Returns:
        iterable of 2D :class:`~ezdxf.entities.Polyline` objects

    .. versionadded:: 0.16

    """
    if isinstance(paths, Path):
        paths = [paths]
    else:
        paths = list(paths)
    if len(paths) == 0:
        return []

    extrusion = Vec3(extrusion)
    reference_point = paths[0].start
    dxfattribs = dxfattribs or dict()
    if not extrusion.isclose(Z_AXIS):
        ocs, elevation = _get_ocs(extrusion, reference_point)
        paths = tools.transform_paths_to_ocs(paths, ocs)
        dxfattribs['elevation'] = Vec3(0, 0, elevation)
        dxfattribs['extrusion'] = extrusion
    elif reference_point.z != 0:
        dxfattribs['elevation'] = Vec3(0, 0, reference_point.z)

    for path in paths:
        p = Polyline.new(dxfattribs=dxfattribs)
        p.append_vertices(path.flattening(distance, segments))
        yield p


def to_hatches(
        paths: Iterable[Path],
        *,
        edge_path: bool = True,
        distance: float = MAX_DISTANCE,
        segments: int = MIN_SEGMENTS,
        g1_tol: float = G1_TOL,
        extrusion: 'Vertex' = Z_AXIS,
        dxfattribs: Optional[Dict] = None) -> Iterable[Hatch]:
    """ Convert the given `paths` into :class:`~ezdxf.entities.Hatch` entities.
    Uses LWPOLYLINE paths for boundaries without curves and edge paths, build
    of LINE and SPLINE edges, as boundary paths for boundaries including curves.
    The `extrusion` vector is applied to all paths, all vertices are projected
    onto the plane normal to this extrusion vector. The default extrusion vector
    is the WCS z-axis. The plane elevation is the distance from the WCS origin
    to the start point of the first path.

    Args:
        paths: iterable of :class:`Path` objects
        edge_path: ``True`` for edge paths build of LINE and SPLINE edges,
            ``False`` for only LWPOLYLINE paths as boundary paths
        distance:  maximum distance, see :meth:`Path.flattening`
        segments: minimum segment count per Bézier curve to flatten LWPOLYLINE paths
        g1_tol: tolerance for G1 continuity check to separate SPLINE edges
        extrusion: extrusion vector to all paths
        dxfattribs: additional DXF attribs

    Returns:
        iterable of :class:`~ezdxf.entities.Hatch` objects

    .. versionadded:: 0.16

    """

    def build_edge_path(hatch: Hatch, path: Path, flags: int):
        if path.has_curves:  # Edge path with LINE and SPLINE edges
            edge_path = hatch.paths.add_edge_path(flags)
            for edge in to_bsplines_and_vertices(
                    path, g1_tol=g1_tol):
                if isinstance(edge, BSpline):
                    edge_path.add_spline(
                        control_points=edge.control_points,
                        degree=edge.degree,
                        knot_values=edge.knots(),
                    )
                else:  # add LINE edges
                    prev = edge[0]
                    for p in edge[1:]:
                        edge_path.add_line(prev, p)
                        prev = p
        else:  # Polyline boundary path
            hatch.paths.add_polyline_path(
                Vec2.generate(path.flattening(distance, segments)), flags=flags)

    def build_poly_path(hatch: Hatch, path: Path, flags: int):
        hatch.paths.add_polyline_path(
            # Vec2 removes the z-axis, which would be interpreted as bulge value!
            Vec2.generate(path.flattening(distance, segments)), flags=flags)

    if edge_path:
        boundary_factory = build_edge_path
    else:
        boundary_factory = build_poly_path

    yield from _hatch_converter(paths, boundary_factory, extrusion, dxfattribs)


def _hatch_converter(
        paths: Iterable[Path],
        add_boundary: Callable[[Hatch, Path, int], None],
        extrusion: 'Vertex' = Z_AXIS,
        dxfattribs: Optional[Dict] = None) -> Iterable[Hatch]:
    if isinstance(paths, Path):
        paths = [paths]
    else:
        paths = list(paths)
    if len(paths) == 0:
        return []

    extrusion = Vec3(extrusion)
    reference_point = paths[0].start
    dxfattribs = dxfattribs or dict()
    if not extrusion.isclose(Z_AXIS):
        ocs, elevation = _get_ocs(extrusion, reference_point)
        paths = tools.transform_paths_to_ocs(paths, ocs)
        dxfattribs['elevation'] = Vec3(0, 0, elevation)
        dxfattribs['extrusion'] = extrusion
    elif reference_point.z != 0:
        dxfattribs['elevation'] = Vec3(0, 0, reference_point.z)
    dxfattribs.setdefault('solid_fill', 1)
    dxfattribs.setdefault('pattern_name', 'SOLID')
    dxfattribs.setdefault('color', const.BYLAYER)

    for group in group_paths(paths):
        if len(group) == 0:
            continue
        hatch = Hatch.new(dxfattribs=dxfattribs)
        external = group[0]
        external.close()
        add_boundary(hatch, external, 1)
        for hole in group[1:]:
            hole.close()
            add_boundary(hatch, hole, 0)
        yield hatch


def to_polylines3d(
        paths: Iterable[Path],
        *,
        distance: float = MAX_DISTANCE,
        segments: int = MIN_SEGMENTS,
        dxfattribs: Optional[Dict] = None) -> Iterable[Polyline]:
    """ Convert the given `paths` into 3D :class:`~ezdxf.entities.Polyline`
    entities.

    Args:
        paths: iterable of :class:`Path` objects
        distance:  maximum distance, see :meth:`Path.flattening`
        segments: minimum segment count per Bézier curve
        dxfattribs: additional DXF attribs

    Returns:
        iterable of 3D :class:`~ezdxf.entities.Polyline` objects

    .. versionadded:: 0.16

    """
    if isinstance(paths, Path):
        paths = [paths]

    dxfattribs = dxfattribs or {}
    dxfattribs['flags'] = const.POLYLINE_3D_POLYLINE
    for path in paths:
        p = Polyline.new(dxfattribs=dxfattribs)
        p.append_vertices(path.flattening(distance, segments))
        yield p


def to_lines(
        paths: Iterable[Path],
        *,
        distance: float = MAX_DISTANCE,
        segments: int = MIN_SEGMENTS,
        dxfattribs: Optional[Dict] = None) -> Iterable[Line]:
    """ Convert the given `paths` into :class:`~ezdxf.entities.Line` entities.

    Args:
        paths: iterable of :class:`Path` objects
        distance:  maximum distance, see :meth:`Path.flattening`
        segments: minimum segment count per Bézier curve
        dxfattribs: additional DXF attribs

    Returns:
        iterable of :class:`~ezdxf.entities.Line` objects

    .. versionadded:: 0.16

    """
    if isinstance(paths, Path):
        paths = [paths]
    dxfattribs = dxfattribs or {}
    prev_vertex = None
    for path in paths:
        for vertex in path.flattening(distance, segments):
            if prev_vertex is None:
                prev_vertex = vertex
                continue
            dxfattribs['start'] = prev_vertex
            dxfattribs['end'] = vertex
            yield Line.new(dxfattribs=dxfattribs)
            prev_vertex = vertex
        prev_vertex = None


PathParts = Union[BSpline, List[Vec3]]


def to_bsplines_and_vertices(path: Path,
                             g1_tol: float = G1_TOL) -> Iterable[PathParts]:
    """ Convert a :class:`Path` object into multiple cubic B-splines and
    polylines as lists of vertices. Breaks adjacent Bèzier without G1
    continuity into separated B-splines.

    Args:
        path: :class:`Path` objects
        g1_tol: tolerance for G1 continuity check

    Returns:
        :class:`~ezdxf.math.BSpline` and lists of :class:`~ezdxf.math.Vec3`

    .. versionadded:: 0.16

    """
    from ezdxf.math import bezier_to_bspline

    def to_vertices():
        points = [polyline[0][0]]
        for line in polyline:
            points.append(line[1])
        return points

    def to_bspline():
        b1 = bezier[0]
        _g1_continuity_curves = [b1]
        for b2 in bezier[1:]:
            if have_bezier_curves_g1_continuity(b1, b2, g1_tol):
                _g1_continuity_curves.append(b2)
            else:
                yield bezier_to_bspline(_g1_continuity_curves)
                _g1_continuity_curves = [b2]
            b1 = b2

        if _g1_continuity_curves:
            yield bezier_to_bspline(_g1_continuity_curves)

    prev = path.start
    curves = []
    for cmd in path:
        if cmd.type == Command.CURVE3_TO:
            curve = Bezier3P([prev, cmd.ctrl, cmd.end])
        elif cmd.type == Command.CURVE4_TO:
            curve = Bezier4P([prev, cmd.ctrl1, cmd.ctrl2, cmd.end])
        elif cmd.type == Command.LINE_TO:
            curve = (prev, cmd.end)
        else:
            raise ValueError
        curves.append(curve)
        prev = cmd.end

    bezier = []
    polyline = []
    for curve in curves:
        if isinstance(curve, tuple):
            if bezier:
                yield from to_bspline()
                bezier.clear()
            polyline.append(curve)
        else:
            if polyline:
                yield to_vertices()
                polyline.clear()
            bezier.append(curve)

    if bezier:
        yield from to_bspline()
    if polyline:
        yield to_vertices()


def to_splines_and_polylines(
        paths: Iterable[Path],
        *,
        g1_tol: float = G1_TOL,
        dxfattribs: Optional[Dict] = None) -> Iterable[Union[Spline, Polyline]]:
    """ Convert the given `paths` into :class:`~ezdxf.entities.Spline` and 3D
    :class:`~ezdxf.entities.Polyline` entities.

    Args:
        paths: iterable of :class:`Path` objects
        g1_tol: tolerance for G1 continuity check
        dxfattribs: additional DXF attribs

    Returns:
        iterable of :class:`~ezdxf.entities.Line` objects

    .. versionadded:: 0.16

    """
    if isinstance(paths, Path):
        paths = [paths]
    dxfattribs = dxfattribs or {}

    for path in paths:
        for data in to_bsplines_and_vertices(path, g1_tol):
            if isinstance(data, BSpline):
                spline = Spline.new(dxfattribs=dxfattribs)
                spline.apply_construction_tool(data)
                yield spline
            else:
                attribs = dict(dxfattribs)
                attribs['flags'] = const.POLYLINE_3D_POLYLINE
                polyline = Polyline.new(dxfattribs=dxfattribs)
                polyline.append_vertices(data)
                yield polyline


# Interface to Matplotlib.path.Path

@enum.unique
class MplCmd(enum.IntEnum):
    CLOSEPOLY = 79
    CURVE3 = 3
    CURVE4 = 4
    LINETO = 2
    MOVETO = 1
    STOP = 0


def from_matplotlib_path(mpath, curves=True) -> Iterable[Path]:
    """ Yields multiple :class:`Path` objects from a Matplotlib `Path`_
    (`TextPath`_)  object. (requires Matplotlib)

    .. versionadded:: 0.16

    .. _TextPath: https://matplotlib.org/3.1.1/api/textpath_api.html
    .. _Path: https://matplotlib.org/3.1.1/api/path_api.html#matplotlib.path.Path

    """
    path = None
    for vertices, cmd in mpath.iter_segments(curves=curves):
        cmd = MplCmd(cmd)
        if cmd == MplCmd.MOVETO:  # each "moveto" creates new path
            if path is not None:
                yield path
            path = Path(vertices)
        elif cmd == MplCmd.LINETO:
            # vertices = [x0, y0]
            path.line_to(vertices)
        elif cmd == MplCmd.CURVE3:
            # vertices = [x0, y0, x1, y1]
            path.curve3_to(vertices[2:], vertices[0:2])
        elif cmd == MplCmd.CURVE4:
            # vertices = [x0, y0, x1, y1, x2, y2]
            path.curve4_to(vertices[4:], vertices[0:2], vertices[2:4])
        elif cmd == MplCmd.CLOSEPOLY:
            # vertices = [0, 0]
            if not path.is_closed:
                path.line_to(path.start)
            yield path
            path = None
        elif cmd == MplCmd.STOP:  # not used
            break

    if path is not None:
        yield path


def to_matplotlib_path(paths: Iterable[Path], extrusion: 'Vertex' = Z_AXIS):
    """ Convert the given `paths` into a single :class:`matplotlib.path.Path`
    object.
    The `extrusion` vector is applied to all paths, all vertices are projected
    onto the plane normal to this extrusion vector.The default extrusion vector
    is the WCS z-axis. The Matplotlib :class:`Path` is a 2D object with
    :ref:`OCS` coordinates and the z-elevation is lost. (requires Matplotlib)

    Args:
        paths: iterable of :class:`Path` objects
        extrusion: extrusion vector for all paths

    Returns:
        matplotlib `Path`_ in OCS!

    .. versionadded:: 0.16

    """
    from matplotlib.path import Path as MatplotlibPath
    if not extrusion.isclose(Z_AXIS):
        paths = tools.transform_paths_to_ocs(paths, OCS(extrusion))
    else:
        paths = list(paths)
    if len(paths) == 0:
        raise ValueError('one or more paths required')

    def add_command(code: MplCmd, point: Vec3):
        codes.append(code)
        vertices.append((point.x, point.y))

    vertices = []
    codes = []
    for path in paths:
        add_command(MplCmd.MOVETO, path.start)
        for cmd in path:
            if cmd.type == Command.LINE_TO:
                add_command(MplCmd.LINETO, cmd.end)
            elif cmd.type == Command.CURVE3_TO:
                add_command(MplCmd.CURVE3, cmd.ctrl)
                add_command(MplCmd.CURVE3, cmd.end)
            elif cmd.type == Command.CURVE4_TO:
                add_command(MplCmd.CURVE4, cmd.ctrl1)
                add_command(MplCmd.CURVE4, cmd.ctrl2)
                add_command(MplCmd.CURVE4, cmd.end)

    # STOP command is currently not required
    assert len(vertices) == len(codes)
    return MatplotlibPath(vertices, codes)


# Interface to PyQt5.QtGui.QPainterPath


def from_qpainter_path(qpath) -> Iterable[Path]:
    """ Yields multiple :class:`Path` objects from a `QPainterPath`_.
    (requires PyQt5)

    .. versionadded:: 0.16

    .. _QPainterPath: https://doc.qt.io/qt-5/qpainterpath.html

    """
    # QPainterPath stores only cubic Bèzier curves
    path = None
    vertices = list()
    for index in range(qpath.elementCount()):
        element = qpath.elementAt(index)
        cmd = element.type
        v = Vec3(element.x, element.y)

        if cmd == 0:  # MoveTo, each "moveto" creates new path
            if path is not None:
                yield path
            assert len(vertices) == 0
            path = Path(v)
        elif cmd == 1:  # LineTo
            assert len(vertices) == 0
            path.line_to(v)
        elif cmd == 2:  # CurveTo
            assert len(vertices) == 0
            vertices.append(v)
        elif cmd == 3:  # CurveToDataElement
            if len(vertices) == 2:
                path.curve4_to(v, vertices[0], vertices[1])
                vertices.clear()
            else:
                vertices.append(v)

    if path is not None:
        yield path


def to_qpainter_path(paths: Iterable[Path], extrusion: 'Vertex' = Z_AXIS):
    """ Convert the given `paths` into a :class:`PyQt5.QtGui.QPainterPath`
    object.
    The `extrusion` vector is applied to all paths, all vertices are projected
    onto the plane normal to this extrusion vector. The default extrusion vector
    is the WCS z-axis. The :class:`QPainterPath` is a 2D object with :ref:`OCS`
    coordinates and the z-elevation is lost. (requires PyQt5)

    Args:
        paths: iterable of :class:`Path` objects
        extrusion: extrusion vector for all paths

    Returns:
        `QPainterPath`_ in OCS!

    .. versionadded:: 0.16

    """
    from PyQt5.QtGui import QPainterPath
    from PyQt5.QtCore import QPointF
    if not extrusion.isclose(Z_AXIS):
        paths = tools.transform_paths_to_ocs(paths, OCS(extrusion))
    else:
        paths = list(paths)
    if len(paths) == 0:
        raise ValueError('one or more paths required')

    def qpnt(v: Vec3):
        return QPointF(v.x, v.y)

    qpath = QPainterPath()
    for path in paths:
        qpath.moveTo(qpnt(path.start))
        for cmd in path:
            if cmd.type == Command.LINE_TO:
                qpath.lineTo(qpnt(cmd.end))
            elif cmd.type == Command.CURVE3_TO:
                qpath.quadTo(qpnt(cmd.ctrl), qpnt(cmd.end))
            elif cmd.type == Command.CURVE4_TO:
                qpath.cubicTo(qpnt(cmd.ctrl1), qpnt(cmd.ctrl2), qpnt(cmd.end))
    return qpath
