import sqlite3
import matplotlib.pyplot as plt
# We are making a database

# Campus Menus
# we will make a database in sql and connect it to python.
def initialize_db():
    conn = sqlite3.connect('vit_campus_ai.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS mess_logs 
                     (caterer TEXT, hour_pm INTEGER, food_item TEXT, is_popular INTEGER, wait_time INTEGER)''')
    
    # Data for each mess
    sample_data = [
        ('Mayuri', 1, 'Veg Biryani', 1, 35), ('Mayuri', 1, 'Dal Tadka', 0, 15),
        ('Mayuri', 8, 'Paneer Butter Masala', 1, 40), ('Mayuri', 8, 'Aloo Gobi', 0, 12),
        ('Safal', 1, 'Rajma Chawal', 1, 28), ('Safal', 1, 'Khichdi', 0, 8),
        ('Safal', 8, 'Pav Bhaji', 1, 30), ('Safal', 8, 'Mix Veg', 0, 10),
        ('JB', 1, 'Veg Manchurian', 1, 25), ('JB', 1, 'Lemon Rice', 0, 5),
        ('JB', 8, 'Matar Paneer', 1, 35), ('JB', 8, 'Sev Tamatar', 0, 15),
        ('AB Catering', 1, 'Masala Dosa', 1, 30), ('AB Catering', 1, 'Curd Rice', 0, 5),
        ('AB Catering', 8, 'Egg Curry', 1, 25), ('AB Catering', 8, 'Idli Sambar', 0, 10)
    ]
    
    cursor.execute("SELECT COUNT(*) FROM mess_logs")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO mess_logs VALUES (?,?,?,?,?)", sample_data)
        conn.commit()
    return conn

# Menu for selected mess
def get_mess_details(conn, caterer):
    cursor = conn.cursor()
    # Get only food items available for the selected mess
    cursor.execute("SELECT DISTINCT food_item FROM mess_logs WHERE caterer = ?", (caterer,))
    items = [row[0] for row in cursor.fetchall()]
    
    # Get available hours for that specific mess
    cursor.execute("SELECT DISTINCT hour_pm FROM mess_logs WHERE caterer = ?", (caterer,))
    hours = [row[0] for row in cursor.fetchall()]
    
    return items, hours

# Prediction
# In this block we will predict Base average time.
def predict_wait(conn, caterer, hour, food):
    cursor = conn.cursor()
    # 1. Base average for this mess at this time
    cursor.execute("SELECT wait_time FROM mess_logs WHERE caterer = ? AND hour_pm = ?", (caterer, hour))
    history = [r[0] for r in cursor.fetchall()]
    base_avg = sum(history) / len(history)
    
    # 2. Check if the selected food is favourite
    cursor.execute("SELECT is_popular FROM mess_logs WHERE food_item = ?", (food,))
    is_pop = cursor.fetchone()[0]
    
    # Weighted Logic: Adding the 'Popularity Coefficient'
    prediction = base_avg + (15 if is_pop == 1 else -5)
    return max(2, prediction), base_avg

# Printing layout
conn = initialize_db()
messes = ['Mayuri', 'Safal', 'JB', 'AB Catering']

print("--- VIT Bhopal AI Mess Assistant ---")
print(f"Registered Messes: {', '.join(messes)}")

c_choice = input("\nSelect Mess: ").strip()

if c_choice in messes:
    menu, timings = get_mess_details(conn, c_choice)
    
    print(f"\nAvailable timings for {c_choice}: {timings} PM")
    h_choice = int(input("Enter Hour: "))
    
    if h_choice in timings:
        print(f"\nToday's Menu for {c_choice}: {menu}")
        f_choice = input("Select Dish from list: ").strip()
        
        if f_choice in menu:
            final_pred, b_avg = predict_wait(conn, c_choice, h_choice, f_choice)
            
            print(f"\n[AI PREDICTION]")
            print(f"The predicted wait for {f_choice} is {final_pred:.1f} minutes.")
            
            # Graph to show the difference
            plt.bar(['Base Average', f'Prediction ({f_choice})'], [b_avg, final_pred], color=['lightgrey', 'orange'])
            plt.ylabel("Minutes")
            plt.title(f"Crowd Impact Analysis: {c_choice}")
            plt.show()
        else:
            print("Item not in the list!")
    else:
        print("Not a mess timing for this caterer.")
else:
    print("Invalid Mess Name.")

conn.close()