from flask import flash, redirect, render_template, request, session, url_for
from models import TripInputs, User, db
from utils import pwd_context, COUNTRY_FLAGS
from passlib.context import CryptContext
from datetime import datetime

import joblib
import pandas as pd
import numpy as np
import openai
from flask_mail import Message
import os
OPENAI_API_KEY = 'sk-proj-cd5ibzBiZgdoFzPUpWfLT3BlbkFJDfWkW2qUJsrpcOINYfVu'
def register_routes(app):
 if not OPENAI_API_KEY:
  raise ValueError("OPENAI_API_KEY is not set in the environment variables")
 @app.route('/Login_page', methods=['GET', 'POST'])
 def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(Email=email).first()

        if user and pwd_context.verify(password, user.PasswordHash):
            session['user_id'] = user.UserID
            session['user_name'] = user.Name 
            return redirect(url_for('trip_inputs'))  
        else:
            return 'Invalid email or password'

    return render_template('Login.html')


 @app.route('/register', methods=['GET', 'POST'])
 def register():
    from app import mail
    if request.method == 'POST':
        name = request.form.get('Name')
        email = request.form.get('Email')
        password = request.form.get('Password')

        if not password:
            return "Password is required", 400

        existing_user = User.query.filter((User.Name == name) | (User.Email == email)).first()
        if existing_user:
            return "A user with the same name or email already exists", 400

        password_hash = pwd_context.hash(password)
        new_user = User(Name=name, Email=email, PasswordHash=password_hash)

        db.session.add(new_user)
        db.session.commit()
        
        
        msg = Message("Welcome to Travelia!!",
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[email])
        msg.body = f"Hello {name}, We are happy to welcome you to our team of travelers. Enjoy your journey with Travelia!!, Where you will get the best recommendations for your next trip. best regards, Travelia Team."
        mail.send(msg)

        return render_template('Login.html')

    return render_template('register.html')

 @app.route('/trip_inputs1', methods=['GET', 'POST'])
 def trip_inputs1():
    if request.method == 'POST':
        if 'user_id' in session:
            user_id = session['user_id']
            
            
            age = request.form.get('Age')
            gender = request.form.get('Gender')
            budget = request.form.get('Budget')
            days = request.form.get('Days')
            reason = request.form.get('Reason')
            weather = request.form.get('Weather')
            food = request.form.get('Food')
            location = request.form.get('Continent')

            
            activities = {
                'beaches_and_relaxation': request.form.get('beaches_and_relaxation'),
                'food_and_culinary_experiences': request.form.get('food_and_culinary_experiences'),
                'sports_and_events': request.form.get('sports_and_events'),
                'museums_and_historical_sites': request.form.get('museums_and_historical_sites'),
                'hiking_and_outdoor_adventures': request.form.get('hiking_and_outdoor_adventures'),
                'nature_and_wildlife': request.form.get('nature_and_wildlife'),
                'shopping': request.form.get('shopping'),
                'nightlife_and_entertainment': request.form.get('nightlife_and_entertainment')
            }

           
            selected_activities_count = sum(1 for activity in activities.values() if activity)

            
            if selected_activities_count > 3:
                flash('You can only select up to 3 activities.', 'error')
               
                return render_template('TripInputs.html', **locals())
            
            
            new_trip_input = TripInputs(
                UserID=user_id,
                Age=age,
                Gender=gender,
                Budget=budget,
                Days=days,
                Reason=reason,
                Weather=weather,
                Food=food,
                Continent=location,
                **{key: bool(value) for key, value in activities.items()}
            )

            
            db.session.add(new_trip_input)
            db.session.commit()

            return redirect(url_for('new_recommendations'))
        else:
            return redirect(url_for('Login_page'))

    return render_template('TripInputs.html', user_id=session.get('user_id', None), user_name=session.get('user_name', 'Guest'))


 def generate_travel_plan(user_input, country):
    # Set your OpenAI API key
    openai_api_key = os.getenv('OPENAI_API_KEY')
    openai.api_key = openai_api_key

    # Prepare the prompt using a chat format
    messages = [
        {"role": "system", "content": "You are a helpful travel assistant named Globie. Your job is to plan trips for users according to their inputs and give them tips and notes about the country they are traveling to. Your job is to provide detailed travel plans without introductory phrases or remarks."},
        {"role": "user", "content": f"Generate a detailed travel plan for a trip to {country} with preferences: {user_input}. Provide a small introduction to the country, followed by daily itineraries with headers like 'Day 1-2: ...' or 'Tips and Notes,' and give tips and notes about the destination at the end of the trip. Start each headline with a * but dont end it with it."}
    ]

    # Generate the travel plan using OpenAI ChatCompletion
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1000
    )

    # Extract the response content
    travel_plan = response['choices'][0]['message']['content']

    # Format the travel plan with HTML tags
    formatted_plan = travel_plan.replace('\n\n', '</p><p>').replace('\n', '<br>')

    # Split the travel plan by '*' and process each section
    split_text = [section.strip() for section in travel_plan.split('*') if section.strip()]

    # Create a dictionary for each section, with formatted content
    sections_dict = {}
    for idx, section in enumerate(split_text, start=1):
        formatted_section = section.replace('\n\n', '</p><p>').replace('\n', '<br>')
        sections_dict[f'{idx}'] = f"<p>{formatted_section}</p>"

    # Return both the full formatted plan and the sections
    return {
        'formatted_plan': f"<h2>Travel Plan for {country}</h2><p>{formatted_plan}</p>",
        **sections_dict
    }


 @app.route('/new_recommendations', methods=['GET', 'POST'])
 def new_recommendations():
    if 'user_id' not in session:
        return redirect(url_for('Login_page'))

    # Load the machine learning model and user data
    grid_search = joblib.load('RecommendMe.joblib')
    user_id = session['user_id']
    user_trip_inputs = TripInputs.query.filter_by(UserID=user_id).order_by(TripInputs.TripID.desc()).first()

    if not user_trip_inputs:
        return "No trip preferences found for the user", 404

    # Load column order used during training
    column_order = joblib.load('column_order.joblib')

    # Prepare the DataFrame for prediction
    input_df = pd.DataFrame([{
        'Age': user_trip_inputs.Age,
        'Gender': user_trip_inputs.Gender,
        'Budget': user_trip_inputs.Budget,
        'Days': user_trip_inputs.Days,
        'Reason': user_trip_inputs.Reason,
        'Weather': user_trip_inputs.Weather,
        'Food': user_trip_inputs.Food,
        'Continent': user_trip_inputs.Continent,
        'Beaches and relaxation': int(user_trip_inputs.beaches_and_relaxation),
        'Food and culinary experiences': int(user_trip_inputs.food_and_culinary_experiences),
        'Sports and events': int(user_trip_inputs.sports_and_events),
        'Museums and historical sites': int(user_trip_inputs.museums_and_historical_sites),
        'Hiking and outdoor adventures': int(user_trip_inputs.hiking_and_outdoor_adventures),
        'Nature and wildlife': int(user_trip_inputs.nature_and_wildlife),
        'Shopping': int(user_trip_inputs.shopping),
        'Nightlife and entertainment': int(user_trip_inputs.nightlife_and_entertainment)
    }])
    input_df = pd.get_dummies(input_df)
    input_df = input_df.reindex(columns=column_order, fill_value=0)

    # Predict the best country
    prediction = grid_search.predict(input_df)
    predicted_country = prediction[0]
    if isinstance(predicted_country, np.ndarray):
        predicted_country = predicted_country.item()

    # Update the user's trip data with the predicted country
    user_trip_inputs.Country = predicted_country
    db.session.commit()

    # Generate a detailed travel plan using GPT
    user_input_description = f"{user_trip_inputs.Reason}, {user_trip_inputs.Weather}, {user_trip_inputs.Food}, budget: {user_trip_inputs.Budget}, for {user_trip_inputs.Days} days"
    detailed_plan = generate_travel_plan(user_input_description, predicted_country)

    # Extract and format the plan sections into a dictionary
    var_list = {k: v for k, v in detailed_plan.items() if k != 'formatted_plan'}

    # Store the recommendation in the session
    session['recommendation'] = prediction.tolist()


    return render_template(
        'Recommendation.html',
        recommendation=predicted_country,
        detailed_plan=detailed_plan['formatted_plan'],
        var_list=var_list
    )

 @app.route('/MyTrips', methods=['GET', 'POST'])
 def MyTrips():
     if 'user_id' not in session:
         return redirect(url_for('Login_page'))
     if 'user_id' in session:
        user_id = session['user_id']
       
        trips = TripInputs.query.filter_by(UserID=user_id).all()
        print("Trips found:", trips)

        
        countries = [trip.Country for trip in trips] 
       
        
        return render_template('MyTrips.html', countries=countries)
     else:
        
        return redirect(url_for('login'))



 @app.route('/')
 def index():
    return render_template('main.html')

 @app.route('/trip_inputs')
 def trip_inputs():
    return render_template('TripInputs.html')

 @app.route('/Login_page')
 def Login_page():
    return render_template('Login.html')
 
 @app.route('/aboutus')
 def aboutus():
    return render_template('aboutus.html')
 
 @app.route('/TripRoute')
 def  TripRoute():
    countries = session.get('countries', [])
    return render_template('MyTrips.html', countries=countries)

 @app.route('/Recommend')
 def Recommend():
    
    recommendation = session.get('recommendation', [])
    
    return render_template('Recommendation.html', recommendation=recommendation)