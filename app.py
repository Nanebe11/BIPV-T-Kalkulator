from viktor import ViktorController, File
from viktor.geometry import Point, Sphere
from viktor.external.spreadsheet import SpreadsheetCalculation, SpreadsheetCalculationInput
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

    @DataView('Erträge', duration_guess=5) #for step 2
    def get_Erträge_view(self, params: Munch, **kwargs: dict) ->DataResult:
      input_list = [
        SpreadsheetCalculationInput("Gebäudeart", params.step_1.GA),
        SpreadsheetCalculationInput("Anzahl WE", params.step_1.WE),
        SpreadsheetCalculationInput("Anzahl Personen", params.step_1.Pers),
        SpreadsheetCalculationInput("Wohnfläche", params.step_1.Wf),
        SpreadsheetCalculationInput("aktuelle Wärmeerzeugung", params.step_1.Wä),
      ]
      excel_file_path = Path(__file__).parent / "erträge.xlsx"
      workbook = File.from_path(excel_file_path)
      sheet = SpreadsheetCalculation(workbook, input_list)
      result = sheet.evaluate()
      data_groupe = DataGroup(
        DataItem(
          JährlicherEnergieeintragBIPV = DataItem(
          label="jährlicher Energieertrag BIPV",
          value=0,
          suffix ="kWh/a"),
        DataItem(
          label="jährlicher Energieertrag BIPVT",
          value= AnteilBIPVTthermisch + AnteilBIPVTelektrisch,
          suffix="kWh/a"),
        DataItem(
          label="Anteil thermischer Energie (BIPVT)",
         value=710* (step_2.Area2 + step_2.Area4),
          suffix="kWh/a"),
        DataItem(
          label="Anteil elektrischer Energie (BIPVT)",
          value=0,
          suffix="kWh/a")
      )
      return DataResult()

    @DataView('energiebezogene Kennzahlen', duration_guess=5) #for step 2
    def get_Energie_view(self, params: Munch, **kwargs: dict)-> DataResult:
      input_list = [
        SpreadsheetCalculationInput("Gebäudeart", params.step_1.GA),
        SpreadsheetCalculationInput("Anzahl WE", params.step_1.WE),
        SpreadsheetCalculationInput("Anzahl Personen", params.step_1.Pers),
        SpreadsheetCalculationInput("Wohnfläche", params.step_1.Wf),
        SpreadsheetCalculationInput("aktuelle Wärmeerzeugung", params.step_1.Wä),
      ]
      excel_file_path = Path(__file__).parent / "energie_bedarf.xlsx"
      workbook = File.from_path(excel_file_path)
      sheet = SpreadsheetCalculation(workbook, input_list)
      result = sheet.evaluate()
      data_group = DataGroup(
        DataItem(
          label="Jahresenergiebedarf Wärme",
          explanation_label="",
          value=result.values["Jahresenergiebedarf_Wärme"],
          suffix="kWh/a"),
        DataItem(
          label="Jahresenergiebedarf TWW",
          explanation_label="",
          value=result.values["Jahresenergiebedarf_TWW"],
          suffix="kWh/a"),
        DataItem(
          label="Jahresenergiebedarf Strom",
          explanation_label="",
          value=result.values["Jahresenergiebedarf_Strom"],
          suffix="kWh/a"),
        DataItem(
          label="Jahresenergiebedarf Gesamt",
          explanation_label="",
          value=result.values["Jahresenergiebedarf_Gesamt"],
          suffix="kWh/a")
        )
      return DataResult(data_group)

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


