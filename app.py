from viktor import ViktorController
from viktor.parametrization import ViktorParametrization, TextField, NumberField

class Parametrization (ViktorParametrization):
    input_1 = TextField('Enter your sentence')
    input_2 = NumberField('Number of trys failed')

class ExampeType(ViktorController):
    label = "Example Type"
    parametrization = Parametrization
