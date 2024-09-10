from openquake.hazardlib.gsim import get_available_gsims
from openquake.hazardlib.source import PointSource
from openquake.hazardlib.mfd import TruncatedGRMFD
from openquake.hazardlib.scalerel import WC1994
from openquake.hazardlib.geo import Point, NodalPlane, Line
from openquake.hazardlib.pmf import PMF
from openquake.hazardlib.tom import PoissonTOM
from openquake.hazardlib.site import Site, SiteCollection
from openquake.hazardlib.imt import PGA
from openquake.hazardlib.const import StdDev

import numpy

from matplotlib import pyplot, collections
from matplotlib.colorbar import cm
from collections import OrderedDict

# list available GMPEs
get_available_gsims().keys()

# for name, gmpe in get_available_gsims().items():
#     print(name)
#     print('supported tectonic region: %s' % gmpe.DEFINED_FOR_TECTONIC_REGION_TYPE)
#     print('supported intensity measure types: %s' % ', '.join([imt.__name__ for imt in gmpe.DEFINED_FOR_INTENSITY_MEASURE_TYPES]))
#     print('supported component: %s' % gmpe.DEFINED_FOR_INTENSITY_MEASURE_COMPONENT)
#     print('supported standard deviations: %s' % ', '.join(gmpe.DEFINED_FOR_STANDARD_DEVIATION_TYPES))
#     print('required site parameters: %s' % ', '.join(gmpe.REQUIRES_SITES_PARAMETERS))
#     print('required rupture parameters: %s' % ', '.join(gmpe.REQUIRES_RUPTURE_PARAMETERS))
#     print('required distance parameters: %s' % ', '.join(gmpe.REQUIRES_DISTANCES))
#     print()


# select a number of GMPEs for which we want to analyze the magnitude scaling
from openquake.hazardlib.gsim.abrahamson_silva_2008 import AbrahamsonSilva2008
from openquake.hazardlib.gsim.chiou_youngs_2008 import ChiouYoungs2008
from openquake.hazardlib.gsim.campbell_bozorgnia_2008 import CampbellBozorgnia2008
from openquake.hazardlib.gsim.base import CoeffsTable

gmpes = [AbrahamsonSilva2008(), ChiouYoungs2008(), CampbellBozorgnia2008()]

# explore magnitude scaling, by defining a Point source and calculating median ground shaking at the point
# source location
location = Point(9.1500, 45.1833)
src = PointSource(
    source_id='1',
    name='point',
    tectonic_region_type='Active Shallow Crust',
    mfd=TruncatedGRMFD(min_mag=5., max_mag=6.5, bin_width=0.1, a_val=0.01, b_val=0.98),
    rupture_mesh_spacing=2.,
    magnitude_scaling_relationship=WC1994(),
    rupture_aspect_ratio=1.,
    temporal_occurrence_model=PoissonTOM(50.),
    upper_seismogenic_depth=2.,
    lower_seismogenic_depth=12.,
    location=location,
    nodal_plane_distribution=PMF([(1., NodalPlane(strike=45, dip=50, rake=0))]),
    hypocenter_distribution=PMF([(1, 7.)])
)

# this is the site for which we compute the median ground shaking
site_collection = SiteCollection([Site(location=location, vs30=760., vs30measured=True, z1pt0=40., z2pt5=1.0)])

# this is the intensity measure type for which we compute the median ground shaking
imt = PGA()

# loop over ruptures. For each rupture extract magnitude and median value
means = []
mags = []
for rupture in src.iter_ruptures():
    mags.append(rupture.mag)

    values = []
    for gmpe in gmpes:
        mean, [std] = gmpe.get_mean_and_stddevs(site_collection, rupture, None, imt, [StdDev.TOTAL])
        values.append(numpy.exp(mean))

    means.append(values)

mags = numpy.array(mags)
means = numpy.array(means).T

# plot magnitude scaling
fig = pyplot.figure(figsize=(9,9))

for i, (values, gmpe) in enumerate(zip(means, gmpes)):
    pyplot.plot(mags, values, linewidth=2, label=gmpe.__class__.__name__, color=cm.jet(float(i) / len(gmpes)))

pyplot.xlabel('Magnitude', fontsize=20)
pyplot.ylabel('%s' % imt.__class__.__name__, fontsize=20)
pyplot.legend(loc="upper left", bbox_to_anchor=(1,1))

# define JB distance for which calculating mean ground shaking
jb_distances = numpy.arange(0, 210, 10)

# extract first rupture
ruptures = list(src.iter_ruptures())
rupture = ruptures[0]

# get coordinates of surface projection of bottom edge mid point
bottom_edge = Line([rupture.surface.bottom_left, rupture.surface.bottom_right])
bottom_edge = bottom_edge.resample_to_num_points(3)
mid_point = bottom_edge[1]
mid_point.depth = 0.

# compute coordinates of locations that are at jb_distances from bottom edge mid point
# along a direction that is perpendicular to the rupture strike
locs = [mid_point.point_at(horizontal_distance=d, vertical_increment=0, azimuth=rupture.surface.strike + 90.)
        for d in jb_distances]

# create corresponding site collection
site_collection = SiteCollection([Site(location=loc, vs30=760., vs30measured=True, z1pt0=40., z2pt5=1.) for loc in locs])

values = []
for gmpe in gmpes:

        sctx, rctx, dctx = gmpe.make_contexts(site_collection, rupture)
        mean, [std] = gmpe.get_mean_and_stddevs(sctx, rctx, dctx, PGA(), [StdDev.TOTAL])

        values.append(numpy.exp(mean))

# plot distance scaling
fig = pyplot.figure(figsize=(9,9))

for i, (means, gmpe) in enumerate(zip(values, gmpes)):
    pyplot.loglog(jb_distances, means, linewidth=2, label=gmpe.__class__.__name__, color=cm.jet(float(i) / len(gmpes)))

pyplot.xlabel('JB distance', fontsize=20)
pyplot.ylabel('%s' % imt.__class__.__name__, fontsize=20)
pyplot.title('Magnitude %s' % rupture.mag, fontsize=20)
pyplot.legend(loc="upper left", bbox_to_anchor=(1,1))