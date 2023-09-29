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


    @PlotlyAndDataView("Primärenergieverbrauch", duration_guess=1) #for step 3
    def get_plotlyÖko1_view(self, params: Munch, **kwargs: dict) -> DataResult:
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
      excel_file_path = Path(__file__).parent / "oekologische.xlsx"
      workbook2 = File.from_path(excel_file_path)
      sheet = SpreadsheetCalculation(workbook2, input_list)
      result = sheet.evaluate()

      fig_1 = go.Figure(
        data=[go.Bar(x=["ohne BIPV(T)","mit BIPV(T)"], 
        y=[result.values["Primärenergieverbrauch Vgl Ges"],result.values["Primärenergieverbrauch BIPV(T)"]])], 
        layout=go.Layout(title=go.layout.Title(text="Primärenergieverbrauch")),
      )
      
      summary = DataGroup(
        DataItem("Amount a",value=3),
        DataItem("Amount b", value=5)
      )
      return PlotlyAndDataResult(fig_1.to_json(), summary)

    @PlotlyAndDataView("CO2-Äquivalent", duration_guess=1) #for step 3
    def get_plotlyÖko2_view(self, params: Munch, **kwargs: dict) -> DataResult:
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
      excel_file_path = Path(__file__).parent / "oekologische.xlsx"
      workbook2 = File.from_path(excel_file_path)
      sheet = SpreadsheetCalculation(workbook2, input_list)
      result = sheet.evaluate()

      fig_2 = go.Figure(
        data=[go.Bar(x=["ohne BIPV(T)", "mit BIPV(T)"],
        y=[result.values["CO2-Äquivalent Vgl Ges"], result.values["CO2-Äquivalent BIPV(T)"]])],
        layout=go.Layout(title=go.layout.Title(text="CO2-Äquivalent")),
      )
      summary = DataGroup()

      return PlotlyAndDataResult(fig_2.to_json(), summary)
    
    @PlotlyAndDataView('wirtschaftliche Kennzahlen', duration_guess=10) #for step 3
    def get_plotlyWirt_view(self, params: Munch, **kwargs: dict) -> DataResult:
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
        SpreadsheetCalculationInput("Inbetriebnahme-Zeitpunkt", params.step_2.Inbetrieb),
        SpreadsheetCalculationInput("Elektroauto", params.step_2.Förder1),
        SpreadsheetCalculationInput("Ladesäule", params.step_2.Förder2)
      ]
      excel_file_path = Path(__file__).parent / "wirtschaftlich.xlsx"
      workbook3 = File.from_path(excel_file_path)
      sheet = SpreadsheetCalculation(workbook3, input_list)
      result = sheet.evaluate()

      fig_3 = go.Figure(
        data= [go.Line(x=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
        y=[result.values["kumulierter Barwert_0"],result.values["kumulierter Barwert_1"],result.values["kumulierter Barwert_2"],result.values["kumulierter Barwert_3"],result.values["kumulierter Barwert_4"],result.values["kumulierter Barwert_5"],
        result.values["kumulierter Barwert_6"],result.values["kumulierter Barwert_7"],result.values["kumulierter Barwert_8"],result.values["kumulierter Barwert_9"],result.values["kumulierter Barwert_10"],
        result.values["kumulierter Barwert_11"],result.values["kumulierter Barwert_12"],result.values["kumulierter Barwert_13"],result.values["kumulierter Barwert_14"],result.values["kumulierter Barwert_15"],
        result.values["kumulierter Barwert_16"],result.values["kumulierter Barwert_17"],result.values["kumulierter Barwert_18"],result.values["kumulierter Barwert_19"],result.values["kumulierter Barwert_20"],
        result.values["kumulierter Barwert_21"],result.values["kumulierter Barwert_22"],result.values["kumulierter Barwert_23"],result.values["kumulierter Barwert_24"],result.values["kumulierter Barwert_25"],
        result.values["kumulierter Barwert_26"],result.values["kumulierter Barwert_27"],result.values["kumulierter Barwert_28"],result.values["kumulierter Barwert_29"],result.values["kumulierter Barwert_30"]])],
      )

      summary = DataGroup(
        DataItem(
          label = "Investitionskosten",
          value = 100,
          suffix="€"
        )
      )

      return PlotlyAndDataResult(fig_3.to_json(), summary)


