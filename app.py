from pathlib import Path
from munch import Munch

import pandas as pd
import plotly.graph_objects as go

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
    def get_Erträge_view(self, params: Munch, **kwargs: dict) -> DataResult:
      input_list = [
        SpreadsheetCalculationInput("Fläche der PV-Anlage (1)", params.step_2.Area1),
        SpreadsheetCalculationInput("Ausrichtung der Fläche (1)", params.step_2.Azimut1),
        SpreadsheetCalculationInput("Neigung der Fläche (1)", params.step_2.Neigung1),
        SpreadsheetCalculationInput("Fläche der PVT-Anlage (2)", params.step_2.Area2),
        SpreadsheetCalculationInput("Ausrichtung der Fläche (2)", params.step_2.Azimut2),
        SpreadsheetCalculationInput("Neigung der Fläche (2)", params.step_2.Neigung2),
        SpreadsheetCalculationInput("Fläche der PV-Anlage (3)", params.step_2.Area3),
        SpreadsheetCalculationInput("Ausrichtung der Fläche (3)", params.step_2.Azimut3),
        SpreadsheetCalculationInput("Fläche der PVT-Anlage (4)", params.step_2.Area4),
        SpreadsheetCalculationInput("Ausrichtung der Fläche (4)", params.step_2.Azimut4),
      ]
      excel_file_path = Path(__file__).parent / "ertraege.xlsx"
      workbook1 = File.from_path(excel_file_path)
      sheet = SpreadsheetCalculation(workbook1, input_list)
      result = sheet.evaluate()
      data_groupe = DataGroup(
        DataItem(
          label="jährlicher Energieertrag BIPV (elektrisch)",
          value=result.values["jährlicher Energieertrag BIPV (elektrisch)"],
          suffix ="kWh/a"),
        DataItem(
          label="jährlicher Energieertrag BIPVT",
          value=result.values["jährlicher Energieertrag BIPVT"],
          suffix="kWh/a"),
        DataItem(
          label="Anteil elektrischer Energie (BIPVT)",
         value=result.values["Anteil elektrische Energie an BIPVT"],
          suffix="kWh/a"),
        DataItem(
          label="Anteil thermischer Energie (BIPVT)",
          value=result.values["Anteil thermische Energie an BIPVT"],
          suffix="kWh/a")
        )
      return DataResult(data_groupe)

    @DataView('energiebezogene Kennzahlen', duration_guess=5) #for step 2
    def get_Energie_view(self, params: Munch, **kwargs: dict)-> DataResult:
      input_list = [
        SpreadsheetCalculationInput("Gebäudeart", params.step_1.GA),
        SpreadsheetCalculationInput("Anzahl WE", params.step_1.WE),
        SpreadsheetCalculationInput("Anzahl Personen", params.step_1.Pers),
        SpreadsheetCalculationInput("Wohnfläche", params.step_1.Wf),
        SpreadsheetCalculationInput("aktuelle Wärmeerzeugung", params.step_1.Wä),
        SpreadsheetCalculationInput("Fläche der PV-Anlage (1)", params.step_2.Area1),
        SpreadsheetCalculationInput("Ausrichtung der Fläche (1)", params.step_2.Azimut1),
        SpreadsheetCalculationInput("Neigung der Fläche (1)", params.step_2.Neigung1),
        SpreadsheetCalculationInput("Fläche der PVT-Anlage (2)", params.step_2.Area2),
        SpreadsheetCalculationInput("Ausrichtung der Fläche (2)", params.step_2.Azimut2),
        SpreadsheetCalculationInput("Neigung der Fläche (2)", params.step_2.Neigung2),
        SpreadsheetCalculationInput("Fläche der PV-Anlage (3)", params.step_2.Area3),
        SpreadsheetCalculationInput("Ausrichtung der Fläche (3)", params.step_2.Azimut3),
        SpreadsheetCalculationInput("Fläche der PVT-Anlage (4)", params.step_2.Area4),
        SpreadsheetCalculationInput("Ausrichtung der Fläche (4)", params.step_2.Azimut4),
        SpreadsheetCalculationInput("Stromspeicher", params.step_2.Speicher),
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
          suffix="kWh/a"),
        DataItem(
          label="Jährlich nutzbare Strommenge aus BIPV(T)",
          value=result.values["jährlich_nutzbar_elektrisch"],
          suffix="kWh/a"),
        DataItem(
          label="Jährlich eingespeiste Strommenge aus BIPV(T)",
          value=result.values["jährlich_einspeis_elektrisch"],
          suffix="kWh/a"),
        DataItem(
          label="Jährlich nutzbare Wärmemenge aus BIPVT",
          value=result.values["jährlich_nutzbar_thermisch"],
          suffix="kWh/a"),
        )
      return DataResult(data_group)


    @PlotlyAndDataView("ökologische Kennzahlen", duration_guess=1) #for step 3
    def get_plotlyÖko_view(self, params: Munch, **kwargs):
      fig = go.Figure(
        data=[go.Bar(x=["ohne BIPV(T)","mit BIPV(T)"], 
        y=[1,3,2])], 
        layout=go.Layout(title=go.layout.Title(text="a figure")),
      )
      summary = DataGroup(
        DataItem("Amount a",value=3),
        DataItem("Amount b", value=5)
      )
      return PlotlyAndDataResult(fig.to_json(), summary)
    
    @PlotlyAndDataView('wirtschaftliche Kennzahlen', duration_guess=10) #for step 3
    def get_plotlyWirt_view(self, params: Munch, **kwargs):
      return PlotlyAndDataResult(fig)


