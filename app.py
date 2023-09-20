from viktor import ViktorController
from viktor.geometry import Point, Sphere
from viktor.parametrization import ViktorParametrization, NumberField, OptionField, Text, Step
from viktor.views import (
  GeometryView, 
  GeometryResult, 
  DataView, 
  DataResult, 
  DataGroup, 
  DataItem,
  PlotlyView, 
  PlotlyResult,
)
from munch import Munch

def validate_step_1(params, **kwargs):
  """Validates step 1."""
  if not params.step_1.point:
    raise UserError("Select something")
  if params.step_1.surface == 0:
    raise UserError("Bigger area needed")

class Parametrization(ViktorParametrization):

  step_1 = Step("Starting off",
    views="get_geometry_view", 
  )

  step_1.text1 = Text (
    """ Welcome to this app, that I'm trying to build!

    I hope we can get along
    
    ##User Information

    XXXX
    
    ##Choose input
    """
  )
    
  step_1.x = NumberField(
    "BIPV(T) surface area", 
    suffix="m2",
    default=20,
    min=1,
    max=200,
    description="Use decimal point instead of comma",
    )
  
  step_1.z = OptionField(
    "Anlagentyp",
    options=["BIPV Dachintegriert", "BIPVT Dachintegriert"],
    default="BIPV Dachintegriert",
    autoselect_single_option=True,
    )
  
  step_2 = Step("More Input", views="get_data_view")

  step_2.text2 = Text (
    """ Here are going to be more Inputs necessary"""
  )

  step_3 = Step("Outputs",views="get_plotly_view")

  step_3.text3 = Text ("Hi")



class ExampeType(ViktorController):
    viktor_enforce_field_constraints = True
    label = "Example Type"
    parametrization = Parametrization

    @GeometryView('3D Geo', duration_guess=1) #for step 1
    def get_geometry_view(self, params, **kwargs):
      geometry = Sphere(Point(0,0,0), radius=10)
      return GeometryResult(geometry)

    @DataView('Data', duration_guess=1) #for step 2
    def get_data_view(self, params, **kwargs):
      Ertrag = params.step_1.x * 1000
      Fantasie = params.step_1.z

      main_data_group = DataGroup(
        DataItem('jährlicher solarer Ertrag', Ertrag),
        DataItem('Anlagenkonfiguration', Fantasie),
      )
      return DataResult(main_data_group)

    @PlotlyView("Plot", duration_guess=10) #for step 3
    def get_plotly_view(self, params: Munch, **kwargs):
      """Shows the plot"""
      return PlotlyResult(fig)
