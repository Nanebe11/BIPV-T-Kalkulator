from pathlib import Path
from munch import Munch

import numpy as np
import pandas as pd
import plotly.express as px
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
  WebView, 
  WebResult,
)

from parametrization import Parametrization

class ExampeType(ViktorController):
    viktor_enforce_field_constraints = True
    label = "Example Type"
    parametrization = Parametrization (width=40)

    @ImageView('', duration_guess=1) #for step 1
    def get_image_view(self, params, **kwargs):
     image_path = Path(__file__).parent / 'ubersicht.jpg'
     return ImageResult.from_path(image_path)

    @ImageView('Anlagentypen', duration_guess=1) #for step 2
    def get_image2_view(self, params, **kwargs):
     image_path = Path(__file__).parent / 'Darstellung.jpg'
     return ImageResult.from_path(image_path) 

    @DataView('Erträge', duration_guess=10) #for step 2
    def get_Erträge_view(self, params: Munch, **kwargs) -> DataResult:
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
      workbook = File.from_path(excel_file_path)
      sheet = SpreadsheetCalculation(workbook, input_list)
      result = sheet.evaluate()

      data_groupe = DataGroup(
        DataItem(
          label="jährlicher Energieertrag BIPV (elektrisch)",
          value=round(result.values["jährlicher Energieertrag BIPV (elektrisch)"], 0),
          suffix ="kWh/a"),
        DataItem(
          label="jährlicher Energieertrag BIPVT",
          value=round(result.values["jährlicher Energieertrag BIPVT"],0),
          suffix="kWh/a"),
        DataItem(
          label="Anteil elektrischer Energie (BIPVT)",
         value=round(result.values["Anteil elektrische Energie an BIPVT"],0),
          suffix="kWh/a"),
        DataItem(
          label="Anteil thermischer Energie (BIPVT)",
          value=round(result.values["Anteil thermische Energie an BIPVT"],0),
          suffix="kWh/a")
        )
      return DataResult(data_groupe)

    @DataView('energiebezogene Kennzahlen', duration_guess=5) #for step 2
    def get_Energie_view(self, params: Munch, **kwargs)-> DataResult:
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
          value=round(result.values["Jahresenergiebedarf_Wärme"],0),
          suffix="kWh/a"),
        DataItem(
          label="Jahresenergiebedarf TWW",
          explanation_label="",
          value=round(result.values["Jahresenergiebedarf_TWW"],0),
          suffix="kWh/a"),
        DataItem(
          label="Jahresenergiebedarf Strom",
          explanation_label="",
          value=round(result.values["Jahresenergiebedarf_Strom"],0),
          suffix="kWh/a"),
        DataItem(
          label="Jahresenergiebedarf Gesamt",
          explanation_label="",
          value=round(result.values["Jahresenergiebedarf_Gesamt"],0),
          suffix="kWh/a"),
        DataItem(
          label="Jährlich nutzbare Strommenge aus BIPV(T)",
          value=round(result.values["jährlich_nutzbar_elektrisch"],0),
          suffix="kWh/a"),
        DataItem(
          label="Jährlich eingespeiste Strommenge aus BIPV(T)",
          value=round(result.values["jährlich_einspeis_elektrisch"],0),
          suffix="kWh/a"),
        DataItem(
          label="Jährlich nutzbare Wärmemenge aus BIPVT",
          value=round(result.values["jährlich_nutzbar_thermisch"],0),
          suffix="kWh/a"),
        )
      return DataResult(data_group)


    @PlotlyAndDataView("Primärenergieverbrauch", duration_guess=1) #for step 3
    def get_plotlyÖko1_view(self, params: Munch, **kwargs) -> DataResult:
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
      workbook = File.from_path(excel_file_path)
      sheet = SpreadsheetCalculation(workbook, input_list)
      result = sheet.evaluate()

      fig_1 = go.Figure(
        data=[go.Bar(x=["ohne BIPV(T)","mit BIPV(T)"], 
        y=[result.values["Primärenergieverbrauch Vgl Ges"],result.values["Primärenergieverbrauch BIPV(T)"]])], 
        layout=go.Layout(title=go.layout.Title(text="Primärenergieverbrauch")),
      )
      
      summary = DataGroup(
        DataItem(
          label= "Vergleichssystem",
          value=result.values["Primärenergieverbrauch Vgl Ges"], 
          suffix="kWh/a"),
        DataItem(
          label="mit BIPV(T)-Anlage", 
          value=round(result.values["Primärenergieverbrauch BIPV(T)"], 0),
          suffix="kWh/a")
      )
      return PlotlyAndDataResult(fig_1.to_json(), summary)

    @PlotlyAndDataView("CO2-Äquivalent", duration_guess=1) #for step 3
    def get_plotlyÖko2_view(self, params: Munch, **kwargs) -> DataResult:
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
      workbook = File.from_path(excel_file_path)
      sheet = SpreadsheetCalculation(workbook, input_list)
      result = sheet.evaluate()

      fig_2 = go.Figure(
        data=[go.Bar(x=["ohne BIPV(T)", "mit BIPV(T)"],
        y=[result.values["CO2-Äquivalent Vgl Ges"], result.values["CO2-Äquivalent BIPV(T)"]])],
        layout=go.Layout(title=go.layout.Title(text="CO2-Äquivalent")),
      )
      summary = DataGroup(
        DataItem(
          label="Vergleichssystem",
          value=result.values["CO2-Äquivalent Vgl Ges"], 
          suffix="kg/a"),
        DataItem(
          label= "mit BIPV(T)", 
          value=round(result.values["CO2-Äquivalent BIPV(T)"], 0),
          suffix="kg/a")
      )

      return PlotlyAndDataResult(fig_2.to_json(), summary)
    
    @PlotlyAndDataView('wirtschaftliche Kennzahlen', duration_guess=10) #for step 3
    def get_plotlyWirt_view(self, params: Munch, **kwargs) -> DataResult:
      input_list = [
        SpreadsheetCalculationInput("GA", params.step_1.GA),
        SpreadsheetCalculationInput("WE", params.step_1.WE),
        SpreadsheetCalculationInput("Personen", params.step_1.Pers),
        SpreadsheetCalculationInput("Wohnfläche", params.step_1.Wf),
        SpreadsheetCalculationInput("aktuelle Wärmeerzeugung", params.step_1.Wä),
        SpreadsheetCalculationInput("Fläche1", params.step_2.Area1),
        SpreadsheetCalculationInput("Ausrichtung1", params.step_2.Azimut1),
        SpreadsheetCalculationInput("Neigung1", params.step_2.Neigung1),
        SpreadsheetCalculationInput("Fläche2", params.step_2.Area2),
        SpreadsheetCalculationInput("Ausrichtung2", params.step_2.Azimut2),
        SpreadsheetCalculationInput("Neigung2", params.step_2.Neigung2),
        SpreadsheetCalculationInput("Fläche3", params.step_2.Area3),
        SpreadsheetCalculationInput("Ausrichtung3", params.step_2.Azimut3),
        SpreadsheetCalculationInput("Fläche4", params.step_2.Area4),
        SpreadsheetCalculationInput("Ausrichtung4", params.step_2.Azimut4),
        SpreadsheetCalculationInput("Stromspeicher", params.step_2.Speicher),
        SpreadsheetCalculationInput("Inbetrieb", params.step_2.Inbetrieb),
        SpreadsheetCalculationInput("Elektroauto", params.step_2.Förder1),
        SpreadsheetCalculationInput("Ladesäule", params.step_2.Förder2)
      ]
      
      excel_file_path = Path(__file__).parent / "break_even2.xlsx"
      workbook = File.from_path(excel_file_path)
      sheet = SpreadsheetCalculation(workbook, input_list)
      result = sheet.evaluate()
      print(result.values)

      x_data = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
      y_data = [result.values["Barwert_0"],result.values["Barwert_1"],result.values["Barwert_2"],result.values["Barwert_3"],result.values["Barwert_4"],result.values["Barwert_5"],
      result.values["Barwert_6"],result.values["Barwert_7"],result.values["Barwert_8"],result.values["Barwert_9"],result.values["Barwert_10"],
      result.values["Barwert_11"], result.values["Barwert_12"], result.values["Barwert_13"],result.values["Barwert_14"],result.values["Barwert_15"],
      result.values["Barwert_16"],result.values["Barwert_17"],result.values["Barwert_18"],result.values["Barwert_19"],result.values["Barwert_20"],
      result.values["Barwert_21"],result.values["Barwert_22"],result.values["Barwert_23"],result.values["Barwert_24"],result.values["Barwert_25"],
      result.values["Barwert_26"],result.values["Barwert_27"],result.values["Barwert_28"],result.values["Barwert_29"],result.values["Barwert_30"],]

      fig_3 = {
       "data": [
         {"type": "line",
          "x": x_data, 
          "y": y_data }],
       "layout": {
          "title": {"text": f"Amortisationsdauer der BIPV(T)-Anlage"},
          "xaxis": {"title": {"text": "Lebensdauer in Jahren"}},
          "yaxis": {"title": {"text": "Kumulierter Barwert in €"}},
        },
      }
      

      summary = DataGroup(
        DataItem(
          label = "Investitionskosten",
          value = result.values["Barwert_0"],
          suffix="€"
        ),
        DataItem(
          label="Amortisationsdauer",
          value=result.values["Break-Even-Point"]
        )
        )
      return PlotlyAndDataResult(fig_3,summary)


    @WebView("What's next?", duration_guess=1)
    def whats_next(self, **kwargs):
      html_path = Path(__file__).parent / "final_step_text.html"
      with html_path.open() as f:
        html_string = f.read()
      return WebResult(html=html_string)   

