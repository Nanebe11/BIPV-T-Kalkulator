from viktor.parametrization import (
    ViktorParametrization,
    NumberField, 
    IntegerField,
    OptionField,
    Text,
    Step
)

class Parametrization(ViktorParametrization):

  step_1 = Step("Start", views="get_image_view")

  step_1.textü = Text (
    """# Willkommen zur Break-Even-Point-Kalkulation von BIPV(T)-Anlagen!

  In dieser App können verschiedene Konfigurationen von BIPV(T)-Anlagen
  auf ihre Wirtschaftlichkeit hin geprüft werden.
  Es soll dabei helfen eine erste Einschätzung zu erhalten, ob eine Investition
  in eine solche Anlage für einen bestimmten Anwendungsfall sinnvoll ist.

  Auf der rechten Seite können Sie zwei Beispiele für bereits durchgeführte BIPV-Anlagen sehen.

  Diese App wurde im Rahmen der Masterarbeit: 
  "Wirtschaftlichkeitsanalyse von BIPV(T)-Anlagen unter Berücksichtigung der Kosten und Nutzen" entwickelt. 
  Alle verwendeten Abschätzungen und Eingrenzungen sind im schriftlichen Teil
  dieser Arbeit ausführlich aufgeführt.

  ## Generelle Informationen

  Die Daten, die Sie im ersten Schritt angeben, 
  sind generelle Informationen des zu betrachtenden Gebäudes. 
  Weiterführende Informationen zu den einzelnen Eingaben sind unter dem Infobutton zu finden. 
    """
  )

  step_1.GA = OptionField(
    "Gebäudeart", 
    options=['Neubau', 'Sanierung', 'Bestand'], 
    default="Neubau",
    variant='radio-inline'
  ) 

  step_1.texta = Text( 
    """  """
  )

  step_1.WE = IntegerField(
    "Anzahl Wohneinheiten", 
    default=1,
    min=1,
    max=10,
    description="Anzahl der getrennt lebenden Haushalte in einem Gebäude mit gemeinsamer Warmwassererzeugung und Heizungsanlage",
    )

  step_1.Pers = IntegerField( #dieses Feld ist nur erforderlich für WE>2 
     "Anzahl Personen", 
     default=1,
     min=1,
     max=50,
     description="Anzahl der Personen, die in dem Gebäude leben; Nur erforderlich wenn es mehr als 2 Wohneinheiten gibt",
    )
  
  step_1.Wf = NumberField(
    "Wohnfläche", 
    suffix="m^2", 
    default=50,
    min=5,
    description="Zusammengerechnete beheizte Wohnfläche aller Wohneinheiten"
  )
  step_1.textx = Text("""
  Sollten Ihnen die genauen Jahresbedarfswerte für Wärme und Trinkwarmwasser, 
  sowie für Strom bekannt sein, können Sie diese hier eintragen. 
  Ansonsten belassen Sie die Eintragung "0" und die Jahresbedarfswerte werden 
  über Durchschnittswerte aus den vorherigen Eingaben berechnet.
  """)

  step_1.jebw = NumberField(
    "Jahresenergiebedarf Wärme und Trinkwarmwasser", 
    suffix="kWh", 
    default=0
  )  
  step_1.jebs = NumberField(
    "Jahresenergiebedarf Strom", 
    suffix="kWh", 
    default=0
  )

  step_1.text2 = Text("""
  Bitte geben Sie im folgenden die Art der aktuellen Wärmeerzeugung an. 
  Sollten Sie keine aktuelle Wärmererzeugung (Neubauten) haben, können Sie eine alternative als Vergleichswert wählen.
  Diese Information wird berücksichtigt, um die ökologischen Kennzahlen zu berechnen. 
  Dabei werden die Auswirkungen eines Gebäudes mit BIPV(T)-Anlage mit denen eines Vergleichsgebäudes verglichen.
  Im Rahmen dieser Berechnung sind nur Erdgas und Heizöl berücksichtigt, 
  sollte Ihr Gebäude über eine andere Wärmeerzeugung verfügen, können Sie hier einen Vergleichwert frei wählen. 
  """)

  step_1.Wä = OptionField(
    "aktuelle Wärmeerzeugung",
    options=["Erdgas", "Heizöl"],
    default="Erdgas",
    variant='radio-inline',
    description="Bei Neubauten bitte Alternative zur Wärmeerzeugung wählen (Vergleichswert)",
  )
  
  step_2 = Step("Anlagenkonfiguration", views=["get_image2_view","get_Erträge_view", "get_Energie_view"])

  step_2.text3 = Text (
    """# Anlagenkonfiguration

  Im Folgenden müssen Sie einige Informationen zu der geplanten BIPV(T)-Anlage treffen. 
  Auf der rechten Seite werden die solaren Erträge und die energiebezogenen Kennzahlen für die konfigurierte Anlage ausgegeben. 

  Die Berechnung der Ergebnisse kann im Allgemeinen einen kleinen Moment dauern.
    
  Dabei wird für den Solarertrag vereinfacht eine Einstrahlung von 1.000 kWh je kWpeak für ganz Deutschland angenommen. 
  Die Ausrichtung und Neigung der Fläche wird gemäß der Angaben berücksichtigt. 
  Für eine detaillierte Betrachtung der individuellen Erträge können die Solarkataster der einzelnen Bundesländer verwendet werden. 
    """
  )
  
  step_2.textA1 = Text ("""## BIPV-Anlage Dachintegriert
  Diese Anlage wird in die Dachfläche eines Gebäudes integriert, 
  die Photovoltaikmodule erzeugen dabei elektrische Energie, die im Gebäude genutzt oder eingespeist werden kann.
    """
  )

  step_2.Area1 = NumberField(
    "Fläche der PV-Anlage", 
    suffix="m^2", 
    default=0,
    min=0,
    max=500,
  )

  step_2.Azimut1 = OptionField(
    "Ausrichtung der Fläche", 
    options=["Nord", "Nord-Ost", "Ost", "Süd-Ost", "Süd", "Süd-West", "West", "Nord-West"], 
    default="Süd", 
  )

  step_2.Neigung1 = OptionField(
    "Neigung der Fläche",
    options=["5°","25°","35°","45°","55°","70°","90°"], 
    default="35°",
    description="Die nächstmögliche Neigung wählen, für Flachdächer 5°", 
  )

  step_2.textA2 = Text ("""## BIPVT-Anlage Dachintegriert
  Diese Anlage wird ebenfalls in die Dachfläche eines Gebäudes integriert, 
  die Photovoltaikmodule erzeugen dabei elektrische Energie, die im Gebäude genutzt oder eingespeist werden kann.
  Zusätzlich wird über darunter liegende Kollektoren thermische Energie erzeugt.
    """
  )

  step_2.Area2 = NumberField(
    "Fläche der PVT-Anlage", 
    suffix="m^2",
    default=0, 
    min=0,
    max=500,
  )

  step_2.Azimut2 = OptionField(
    "Ausrichtung der Fläche", 
    options=["Nord", "Nord-Ost", "Ost", "Süd-Ost", "Süd", "Süd-West", "West", "Nord-West"], 
    default="Süd", 
  )

  step_2.Neigung2 = OptionField(
    "Neigung der Fläche",
    options=["5°","25°","35°","45°","55°","70°","90°"], 
    default="35°",
    description="Die nächstmögliche Neigung wählen, für Flachdächer 5°", 
  )

  step_2.textA3 = Text ("""## BIPV-Anlage Fassadenintegriert
  Diese Anlage wird in die Fassade/ Wandfläche eines Gebäudes integriert, 
  die Photovoltaikmodule erzeugen dabei elektrische Energie, die im Gebäude genutzt oder eingespeist werden kann.
    """
  )

  step_2.Area3 = NumberField(
    "Fläche der PV-Anlage", 
    suffix="m^2", 
    default=0,
    min=0,
    max=500,
  )

  step_2.Azimut3 = OptionField(
    "Ausrichtung der Fläche", 
    options=["Nord", "Nord-Ost", "Ost", "Süd-Ost", "Süd", "Süd-West", "West", "Nord-West"], 
    default="Süd", 
  )

  step_2.textA4 = Text ("""## BIPVT-Anlage Fassadenintegriert
  Diese Anlage wird in die Fassade/ Wandfläche eines Gebäudes integriert, 
  die Photovoltaikmodule erzeugen dabei elektrische Energie, die im Gebäude genutzt oder eingespeist werden kann.
  Zusätzlich wird über innenliegende Kollektoren thermische Energie erzeugt.
    """
  )

  step_2.Area4 = NumberField(
    "Fläche der PV-Anlage", 
    suffix="m^2", 
    default=0,
    min=0,
    max=500,
  )

  step_2.Azimut4 = OptionField(
    "Ausrichtung der Fläche", 
    options=["Nord", "Nord-Ost", "Ost", "Süd-Ost", "Süd", "Süd-West", "West", "Nord-West"], 
    default="Süd", 
  )

  step_2.textb = Text ("""
  Neben den Angaben zu den Flächen, Ausrichtungen und Neigungen ist die Bestimmung des Inbetriebenahmezeitpunktes der Anlage relevant.

  Durch die Auswahl eines Stromspeichers kann der nutzbare Anteil an der elektrischen Energie gesteigert werden. 
  """)
  
  step_2.Inbetrieb = OptionField(
    "Inbetriebnahme-Zeitpunkt der Anlage", 
    options=["bis 31.01.2024", "ab 01.02.2024", "ab 01.08.2024", "ab 01.02.2025", "ab 01.08.2025", "ab 01.02.2026"], 
    default="bis 31.01.2024",
  )
  step_2.Speicher = OptionField(
    "Anlage mit Stromspeicher",
    options=["ja","nein"], 
    default="nein",
    variant='radio-inline',
    description="Soll ein Stromspeicher für Ihre Anlage eingeplant werde? Durch einen Stromspeicher kann ein höherer Anteil des produzierten Stroms verwendet werden (vgl. Lastmanagement)",
  )

  step_3 = Step("Ergebnisse",views=["get_plotlyÖko1_view", "get_plotlyÖko2_view", "get_plotlyWirt_view"])

  step_3.text4 = Text ("""# Ergebnisse

  In diesem Schritt werden die Ergebnisse aus allen zuvor getätigen Angaben berechnet. 
  Durch die auf der rechten Seite dargestellten Kennzahlen soll Ihnen die Entscheidung für oder gegen die eingestellte Anlage auf Basis wissenschaftlicher Kennzahlen erleichtert werden. 

  Es ist jederzeit möglich über 'Previous step' zurück zur Anlagenkonfiguration zu gelangen und die Eingangswerte zu ändern. 
  Dadurch können Sie verschiedene Konfigurationen vergleichen. 
    
  ## Ökologische Kennzahlen
  In den ökologischen Kennzahlen, dem Primärenergieverbrauch und dem CO2-Äquivalent,
  finden Sie Vergleichswerte darüber, wie viel Primärenergie und CO2-Äquivalent während der Nutzungsphase durch eine BIPV(T)-Anlage eingespart werden können. 
  Dadurch soll verdeutlicht werden, dass bei einer Investitionsentscheidung nicht nur wirtschaftliche Faktoren relevant sind, 
  sondern auch die ökologischen Auswirkungen berücksichtigt werden sollten. 
  """
  )
  step_3.texty =Text (""" ## Wirtschaftliche Kennzahlen
  In den wirtschaftlichen Kennzahlen finden Sie die Ergebnisse der Amortisationsrechnung.
  Der Break-Even-Point wird sowohl in einer graphischen Darstellung als auch als Wert ausgegeben. 
  Dieser gibt an nach wie vielen Jahre die Investitionskosten durch Erträge wieder eingenommen wurden und
  sich die Anlage somit amortisiert hat.
    
  Bei der Berechnung der Wirtschaftlichkeit wurden Einsparungen berücksichtigt, die den Vergleich zu einem Gebäude ohne solarthermische oder PV-Anlage herstellen.
  Dabei wurden in den Investitionskosten für Neubauten und Sanierungen die Einsparungen aus nicht erforderlichen Dacheindeckungen und Fassadenverkleidungen einbezogen. 
  Ebenfalls ist in den Investitionskosten die BEG Förderung berücksichtigt, sofern die Vorraussetzungen für diese erfüllt sind. 
  Bei den laufenden Kosten wurden darüber hinaus die Einsparungen aus nicht erforderlichen Energien aus dem Netz berücksichtigt. 
  """)
  step_4 = Step("Abschluss",views=["whats_next"])
  
  step_4.text5 = Text("""
  ## Vielen Dank
  für Ihr Interesse an BIPV(T)-Anlagen 
  und viel Erfolg bei der Konfiguration der richtigen Anlage für Ihren speziellen Nutzen. 
    """
  )
