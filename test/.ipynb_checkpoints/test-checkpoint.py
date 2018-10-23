import seaborn
from pandas import ExcelFile
from matplotlib.pyplot import show
from matplotlib.pyplot import plot
from matplotlib.pyplot import figure
from matplotlib.pyplot import axes
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits


%matplotlib inline
%config InlineBackend.figure_format = 'svg'

file = ExcelFile('./work/survey.xlsx')
file.sheet_names
file.parse('Fields Explained')
file.parse('Points Binned')
file.parse('3D Vectors')

latitudes = []
longitudes = []
elevations = []
rows = file.parse('Points Binned').iterrows()
# rows = sample(list(rows), 10)
for index, row in rows:
    latitudes.append(row['surface_latitude'])
    longitudes.append(row['surface_longitude'])
    elevations.append(row['depth_top'])

len(latitudes)
len(longitudes)
len(elevations)

dots_figure = figure()
dots_axes = axes(projection='3d')
dots_axes.set_xlabel('latitude')
dots_axes.set_ylabel('longitude')
dots_axes.set_zlabel('elevation')
# dots_axes.scatter(xs=latitudes,
#                   ys=longitudes,
#                   zs=elevations)
dots_axes.plot_trisurf(latitudes,
                       longitudes,
                       elevations)
dots_figure.savefig('./work/surface.svg', format='svg')
