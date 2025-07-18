from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)
         
import os
os.chdir(os.path.dirname(os.path.abspath(__file__))) # Change to the directory of this script
print("Current working directory:", os.getcwd())

# Load the DataFrame once, globally
dfg = pd.read_csv('data/exercises.csv', encoding='latin1')
dfg['primaryMuscles'] = dfg['primaryMuscles'].str.lower()
dfg['level'] = dfg['level'].str.lower()

@app.route('/')
# route to home page
def home():
    return render_template('home.html')

@app.route('/search')
# search function to handle requests for specific muscle types and difficulty levels
def search():
    muscle = request.args.get('muscle', '').lower()
    level = request.args.get('level', '').lower()

    # Use a copy to avoid modifying the global DataFrame
    df = dfg.copy()

    df['primaryMuscles'] = df['primaryMuscles'].str.lower()
    df['level'] = df['level'].str.lower()

    # filter by muscle
    if muscle:
        df = df[df['primaryMuscles'].str.contains(muscle, na=False)] # Allows for matches that are not exact
        
    # filter by level
    if level != 'all':
        df = df[df['level'] == level]

    # return the results page with filtered exercises
    results = df.to_dict(orient='records')
    return render_template('results.html', results=results, muscle=muscle, level=level) 

plan = [] # will store temporary exercise plan

@app.route('/add_to_plan', methods=['POST'])
# add exercises to "my exercise plan"
def add_to_plan():
    exercise = {
        'name': request.form['name'],
        'muscle': request.form['muscle'],
        'level': request.form['level'],
        'instructions': request.form['video_url']
    }

    if exercise not in plan:
        plan.append(exercise)
    return redirect(request.referrer)

@app.route('/my_exercise_plan')
# view "my exercise plan" page
def view_plan():
    return render_template('my_exercise_plan.html', plan=plan)



if __name__ == '__main__':
    app.run(debug=False)