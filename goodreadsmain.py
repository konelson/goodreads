from flask import Flask, request, render_template
import book_flask.py
rec_func #Import python file that runs recommender function

# create a flask object
app = Flask(__name__)

# creates an association between the / page and the entry_page function (defaults to GET)
@app.route('/')
def entry_page():
    return render_template('index.html')

# creates an association between the /recommend_book page and the render_message function
# (includes POST requests which allow users to enter in data via form)
@app.route('/recommend_book/', methods=['GET', 'POST'])
def render_message():

	# user-input
    user_id = ['user_num']
    
    # error messages to ensure correct units of measure
    messages = ["Enter Valid User ID"]

    # hold all user number as a float
    user_number = []
    
    # takes user input and ensures it can be turned into a floats 
    # doing error check to make sure entered info is a float
    
    for i, num in enumerate(user_id):
        user_input = request.form[num]
        float_input = user_input
        try:
            #float_input = user_input
            user_number.append(float_input)
        except:
            return render_template('index.html', message=messages[i])
        print('amounts', amounts)
        #user_number.append(float_input)
    
    # show user final message

    recs = rec_func(user_number) #Returns a dictionary - use to lookup in index.html
    return render_template('index.html', message=recs)

if __name__ == '__main__':
    app.run(debug=True)