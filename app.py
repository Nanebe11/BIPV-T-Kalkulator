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
    def get_Erträge_view(self, params: Munch, **kwargs):

      JährlicherEnergieeintragBIPV = DataItem(
        label="jährlicher Energieertrag BIPV",
        value=0,
        #value= aus tabelle,
        suffix ="kWh/a",
        number_of_decimals=0
      )

      JährlicherEnergieeintragBIPVT = DataItem(
        label="jährlicher Energieertrag BIPVT",
        value= AnteilBIPVTthermisch + AnteilBIPVTelektrisch,
        suffix="kWh/a",
        number_of_decimals=0
      )

      AnteilBIPVTthermisch = DataItem(
        label="Anteil thermischer Energie (BIPVT)",
        value=710* (step_2.Area2 + step_2.Area4),
        suffix="kWh/a",
        number_of_decimals=0
      )

      AnteilBIPVTelektrisch = DataItem(
        label="Anteil elektrischer Energie (BIPVT)",
        value=0,
        #value= aus tabelle
        suffix="kWh/a", 
        number_of_decimals=0
      )
      return DataResult()

    @DataView('energiebezogene Kennzahlen', duration_guess=10) #for step 2
    def get_Energie_view(self, params, **kwargs):

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

      Jahresenergiebedarf = DataItem(
        label="Jahresenergiebedarf Gesamt",
        value = Heizwärmebedarf + BedarfTWW,
        suffix="kWh/a",
        number_of_decimals=0
      )

      #nutzbarer Anteil am elektrischen Ertrag bestimmen hier Annahme 30%

      jährlichNutzbarElek = DataItem(
        label="jährlich nutbare Energie elektrisch",
        value=(JährlicherEnergieeintragBIPV+AnteilBIPVTelektrisch)*0.3,
        suffix="kWh/a",
      )

      jährlichEinspeis = DataItem(
        label="jährlich eingespeiste Energie",
        value=(JährlicherEnergieeintragBIPV+AnteilBIPVTelektrisch)-jährlichNutzbarElek,
        suffix="kWh/a"
      )

      jährlichNutzbarTherm = DataItem(
        label="jährlich nutzbare Energie thermisch",
        value= AnteilBIPVTthermisch,
        suffix="kWh/a"
      )

      main_data_group = DataGroup(Heizwärmebedarf, BedarfTWW, Jahresenergiebedarf)
      return DataResult(main_data_group)
    
    @DataView('Data', duration_guess=10) #for step ?
    def get_data_view(self, params: Munch, **kwargs):
      return DataResult()



    @PlotlyAndDataView("ökologische Kennzahlen", duration_guess=10) #for step 3
    def get_plotlyÖko_view(self, params: Munch, **kwargs):
      #"""Shows the plot"""
      return PlotlyAndDataResult(fig)
    
    @PlotlyAndDataView('wirtschaftliche Kennzahlen', duration_guess=10) #for step 3
    def get_plotlyWirt_view(self, params: Munch, **kwargs):
      return PlotlyAndDataResult(fig)

