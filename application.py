from flask import Flask, render_template, request

from src.pipeline.predict_pipeline import CustomData, PredictPipeline

application = Flask(__name__)
app = application


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    prediction = None
    error = None
    submitted = request.form.to_dict()
    if request.method == 'POST':
        try:
            data = CustomData(
                gender=request.form['gender'], race_ethnicity=request.form['race_ethnicity'],
                parental_level_of_education=request.form['parental_level_of_education'],
                lunch=request.form['lunch'], test_preparation_course=request.form['test_preparation_course'],
                reading_score=float(request.form['reading_score']), writing_score=float(request.form['writing_score']),
            )
            prediction = round(float(PredictPipeline().predict(data.get_data_as_data_frame())[0]), 1)
        except (KeyError, ValueError):
            error = 'Please complete every field with valid score values.'
        except Exception:
            app.logger.exception('Prediction failed')
            error = 'We could not create a prediction just now. Please try again.'
    return render_template('home.html', prediction=prediction, error=error, form_data=submitted)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
