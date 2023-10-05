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
      workbook = File.from_path(excel_file_path)
      sheet = SpreadsheetCalculation(workbook, input_list)
      result = sheet.evaluate(include_filled_file=True)

      sheet2 = SpreadsheetCalculation(File.from_path(Path(__file__).parent / 'energie_bedarf.xlsx'), input_list)
      result = sheet2.evaluate()

      FlächeGes = params.step_2.Area1 + params.step_2.Area2 + params.step_2.Area3 + params.step_2.Area4

      A3=100+200
      A4=100+ FlächeGes*2
      A5=100
      A6=100+ FlächeGes*2 +200
      A7=100
      A8=100+ FlächeGes*2
      A9=100+200
      A10=100+ FlächeGes*2
      A11=100
      A12=100+ FlächeGes*2+200
      A13=100 + result.values["Inv_Wechselrichter"]
      A14=100+ FlächeGes*2 
      A15=100 +200
      A16=100+ FlächeGes*2
      A17=100
      A18=100+ FlächeGes*2+200
      A19=100
      A20=100+ FlächeGes*2

      if params.step_1.Wä == "Heizöl": 
        E1= result.values["Einspeisevergütung_1-20"] * result.values["jährlich_einspeis_elektrisch"] + result.values["jährlich_nutzbar_elektrisch"] * 0.3496 + result.values["jährlich_nutzbar_thermisch"] * 0.09833
      else: E1= result.values["Einspeisevergütung_1-20"] * result.values["jährlich_einspeis_elektrisch"] + result.values["jährlich_nutzbar_elektrisch"] * 0.3496 + result.values["jährlich_nutzbar_thermisch"] * 0.0934

      R0 = 0-result.values["Investitionskosten"]
      R1 = (E1 - result.values["Investitionskosten"])/(1.05^1)
      R2 = (E1 * (100-0.4*(2-1))/100 -100)/(1.05^2)
      R3 = (E1 * (100-0.4*(3-1))/100 -100 + FlächeGes * 2)/(1.05^3)
      R4 = (E1 * (100-0.4*(4-1))/100 -A4)/(1.05^4)
      R5 = (E1 * (100-0.4*(5-1))/100 -A5)/(1.05^5)
      R6 = (E1 * (100-0.4*(6-1))/100 -A6)/(1.05^6)
      R7 = (E1 * (100-0.4*(7-1))/100 -A7)/(1.05^7)
      R8 = (E1 * (100-0.4*(8-1))/100 -A8)/(1.05^8)
      R9 = (E1 * (100-0.4*(9-1))/100 -A9)/(1.05^9)
      R10 = (E1 * (100-0.4*(10-1))/100 -A10)/(1.05^10)
      R11 = (E1 * (100-0.4*(11-1))/100 -A11)/(1.05^11)
      R12 = (E1 * (100-0.4*(12-1))/100 -A12)/(1.05^12)
      R13 = (E1 * (100-0.4*(13-1))/100 -A13)/(1.05^13)
      R14 = (E1 * (100-0.4*(14-1))/100 -A14)/(1.05^14)
      R15 = (E1 * (100-0.4*(15-1))/100 -A15)/(1.05^15)
      R16 = (E1 * (100-0.4*(16-1))/100 -A16)/(1.05^16)
      R17 = (E1 * (100-0.4*(17-1))/100 -A17)/(1.05^17)
      R18 = (E1 * (100-0.4*(18-1))/100 -A18)/(1.05^18)
      R19 = (E1 * (100-0.4*(19-1))/100 -A19)/(1.05^19)
      R20 = (E1 * (100-0.4*(20-1))/100 -A20)/(1.05^20)

      
      

      x_data = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
      y_data = [R0, R0+R1,R0+R1+R2, R0+R1+R2+R3, R0+R1+R2+R3+R4, R0+R1+R2+R3+R4+R5, R0+R1+R2+R3+R4+R5+R6, R0+R1+R2+R3+R4+R5+R6+R7,
        R0+R1+R2+R3+R4+R5+R6+R7+R8, R0+R1+R2+R3+R4+R5+R6+R7+R8+R9]

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
          value = round(result.values["Investitionskosten"],2),
          suffix="€"
        )
        )
      return PlotlyAndDataResult(fig_3,summary)


    @WebView("What's next?", duration_guess=1)
    def whats_next(self, **kwargs):
      html_path = Path(__file__).parent / "final_step_text.html"
      with html_path.open() as f:
        html_string = f.read()
      return WebResult(html=html_string)   

