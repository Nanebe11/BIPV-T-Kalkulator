from viktor import ViktorController
from viktor.geometry import Point, Sphere
from viktor.parametrization import ViktorParametrization, NumberField, DownloadButton
from viktor.result import DownloadResult
from viktor.views import GeometryView, GeometryResult, DataView, DataResult, DataGroup, DataItem
from munch import Munch

class Parametrization (ViktorParametrization):
    x = NumberField('X')
    y = NumberField('Y')
    download = DownloadButton("Download file", method='download_file')

class ExampeType(ViktorController):
    viktor_enforce_field_constraints = True
    label = "Example Type"
    parametrization = Parametrization

    @GeometryView('3D Geo', duration_guess=1)
    def get_3d_view(self, params, **kwargs):
      geometry = Sphere(Point(0,0,0), radius=10)
      return GeometryResult(geometry)

    @DataView('Data', duration_guess=1)
    def get_data_view(self, params, **kwargs):
      addition = params.x+params.y
      multiplication = 5

      main_data_group = DataGroup(
        DataItem('Data item 1', addition),
        DataItem('Data item 2', multiplication),
      )
      return DataResult(main_data_group)