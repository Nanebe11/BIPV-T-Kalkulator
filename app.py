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
  PlotlyAndDataView,
  PlotlyAndDataResult,
  ImageView, 
  ImageResult,
)
from pathlib import Path
from munch import Munch
from parametrization import Parametrization

class ExampeType(ViktorController):
    viktor_enforce_field_constraints = True
    label = "Example Type"
    parametrization = Parametrization

    @ImageView('', duration_guess=1) #for step 1
    def get_image_view(self, params, **kwargs):
     image_path = Path(__file__).parent / 'try_first.jpg'
     return ImageResult.from_path(image_path)

    @ImageView('Anlagentypen', duration_guess=1) #for step 2
    def get_image2_view(self, params, **kwargs):
     image_path = Path(__file__).parent / 'try_first.jpg'
     return ImageResult.from_path(image_path) 

    @DataView('Erträge', duration_guess=10) #for step 2
    def get_Erträge_view(self, params, **kwargs):
      return DataResult()
    
    @DataView('energiebezogene Kennzahlen', duration_guess=10) #for step 2
    def get_Energie_view(self, params, **kwargs):
      return DataResult()
    
    @DataView('Data', duration_guess=10) #for step ?
    def get_data_view(self, params: Munch, **kwargs):

      if params.step_1.GA == "Neubau" or "Sanierung" :
        GA = 45
      if params.step_1.GA == "Bestandsgebäude" :
        GA = 100
      
      Heizwärmebedarf = DataItem (
        label="Jahresenergiebedarf Wärme", 
        value = GA * params.step_1.Wf,
        suffix = "kWh",
        number_of_decimals=0,
      )
      
      if params.step_1.WE<3:
        BedarfTWW = 500 * params.step_1.Pers
      if params.step_1.WE>2:   
        BedarfTWW = 1000 * params.step_1.WE

      BedarfTWW = DataItem(
        label="Jahresenergiebedarf Trinkwarmwasser", 
        value = BedarfTWW, 
        suffix="kWh", 
        number_of_decimals=0,
      )

      # Strombedarf = aus Tabelle ablesen 

      main_data_group = DataGroup(Heizwärmebedarf, BedarfTWW)
      return DataResult(main_data_group)

     

    @PlotlyAndDataView("ökologische Kennzahlen", duration_guess=10) #for step 3
    def get_plotlyÖko_view(self, params: Munch, **kwargs):
      """Shows the plot"""
      return PlotlyAndDataResult(fig)
    
    @PlotlyAndDataView('wirtschaftliche Kennzahlen', duration_guess=10) #for step 3
    def get_plotlyWirt_view(self, params: Munch, **kwargs):
      return PlotlyAndDataResult(fig)

