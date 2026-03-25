# Vityarthi-Project-Mess-Crowd-prediction
## Campus Mess Crowd Predictor
A data-driven Python application designed to solve the real-world problem of unpredictable waiting times at communal dining facilities. This project uses Weighted Regression Logic and SQL Database Management to predict how long a user will wait in line based on the specific caterer, the hour of the day, and the popularity of the menu item.

## Project Features
  1. Multi-Caterer Data set: Dedicated data tracking for various independent mess providers (Mayuri, Safal, JB, AB Catering).

  2. Menu based on specific mess: Dynamically retrieves specific food items and operational timings for each mess.

  3. Predictive AI Logic: Moves beyond simple averages by using "Popularity Coefficients" to adjust wait times based on menu demand.

  4. Visual Data Analysis: Generates real-time bar charts comparing the general trend (Base Average) vs. the specific AI prediction.

  5. Input Validation: Prevents processing errors by cross-referencing user inputs with historical schedules.

## Technical Block Explanation
### 1. The Persistence Layer (SQL Database)
Function: initialize_db()

How it works: This block initializes a local SQLite database. It creates a structured table to store "Historical Observations" such as the caterer name, time, and recorded wait times.

Why needed: This acts as the AI's Memory. In predictive modeling, the system needs a baseline of past truths to calculate future estimates.

### 2. Menu Details
Function: get_mess_details()

How it works: This block uses specific SQL queries to filter the database. It ensures the user only sees the hours and dishes that actually belong to their chosen caterer.

Why needed : This is a Data Cleaning step. It prevents the system from showing irrelevant options, ensuring the user provides "Clean Input" for the prediction engine.

### 3. The Prediction Engine 
Function: predict_wait()

How it works: 1. It calculates the Base Average (the mathematical mean) for that specific time.
2. It checks if the dish is a "Popular" item (a crowd-puller).
3. It applies a Weighted Coefficient (+15 minutes for popular items, -5 for standard ones).

Why needed : This mimics Heuristic Regression. It recognizes that "Time" isn't the only factor; the "Quality of Food" is a high-weight feature that significantly changes the outcome.

### 4. Interactive Interface & Validation
Logic: Main Execution Block

How it works: This is the "Control Room" of the script. It manages user inputs and uses strict if/else guardrails to catch errors.

Why needed : This represents Error Handling. If a user enters a time when a mess is closed, the system identifies it as "Not a mess timing" rather than giving a false or "hallucinated" prediction.

### 5. Data Visualization (Explainable AI)
Logic: plt.bar(...)

How it works: Using the matplotlib library, the code produces a visual comparison between the general average and today’s specific prediction.

Why needed : This provides Explainability (XAI). It proves to the user why the wait time is higher than usual, making the AI's logic transparent and easy to trust.

## How to use
### Install Requirements:

pip install matplotlib

### Run the Script:

python MessPrediction.py

### Follow the Steps: 

Select a caterer, choose a valid timing, and pick a dish to see the visual crowd analysis.
