from wtforms import Form, FloatField, IntegerField, FileField, validators, \
                    RadioField, BooleanField, SelectField, SelectMultipleField

class InputForm(Form):
    user_file = FileField(
        label = "Data File", 
        validators = [validators.InputRequired(message = "Please select a file for analysis.")])
    som_shape = RadioField(
        label = "Grid Shape",
        choices = ["Hex", "Rectangle"],
        default= "Hex")
    iters = IntegerField(
        default = 20,
        label = "Iterations",
        render_kw = {"placeholder":"Default: 50"}, 
        validators = [validators.InputRequired(message = "Please enter any integer greater than 0."),
                      validators.NumberRange(min = 1, 
                      message = "Please enter any integer greater than 0.")])
    test_split = FloatField(
        label = 'Test Split',
        default = 0.25,
        render_kw = {'placeholder':'Default: 0.2'},
        validators = [validators.InputRequired(message = "Please enter a number between 0 and 1."),
                validators.NumberRange(min = 0, max = 1, 
                message = "Please enter a number between 0 and 1.")])
    classifiers = SelectMultipleField(
        label = "Classifiers",
        default = "LVQ",
        render_kw = {'style': 'overflow: hidden; height: 102px'},
        choices = [('LVQ', 'Learning Vector Quantization'), ('SVM', 'Support Vector Machine'),
                   ('DT', 'Decision Tree'), ('RF', 'Random Forest'),
                   ('6NN', '6 Nearest Neighbors'), ('NB', 'Naive Bayes')])

def get_err_messages(form):
    output = ""
    for field,errors in form.errors.items():
        label = getattr(form,field).label.text
        for error in errors:
            output += "Error in {} field. {}\n".format(label,error)
    return output