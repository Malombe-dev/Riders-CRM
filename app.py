from flask import*
import mysql.connector
import os
from werkzeug.utils import secure_filename
import json
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import re  # for password validation
from functools import wraps
from datetime import datetime, timedelta
from flask import make_response   

# from flask_cors import CORS

app = Flask(__name__)

# CORS(app)      
app.secret_key = os.urandom(24)

def validate_password(password):
    """
    Validates that a password meets the following criteria:
    - At least 8e characters long
    - Contains an uppercase letter
    - Contains a lowercase letter
    - Contains a number
    - Contains a special character
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number."
    if not re.search(r'[\W_]', password):
        return False, "Password must contain at least one special character."
    return True, ""

def validate_email(email):
    """
    Validates that the email format is correct.
    """
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

def validate_phone(phone):
    """
    Validates that the phone number format is correct.
    """
    phone_regex = r'^\+?[1-9]\d{1,14}$'  # E.164 format
    return re.match(phone_regex, phone)     


# Set folder to save uploaded product images
app.config['UPLOAD_FOLDER'] = 'static/images'

# Allowed extensions for image Fuploads
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Helper function to check if the file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Helper function to get a database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Add your password if set
        database="rider_db"
    )

# Fetch total riders
@app.route('/totalRiders')
def total_riders():
    db = get_db_connection()
    cursor = db.cursor()
  
    # Riders by 'submitted_by'
    cursor.execute("SELECT submitted_by, COUNT(rider_id) FROM riders GROUP BY submitted_by")
    submitted_by_data = cursor.fetchall()

    # Riders by 'lead_classification'
    cursor.execute("SELECT lead_classification, COUNT(rider_id) FROM riders GROUP BY lead_classification")
    lead_classification_data = cursor.fetchall()
    return render_template('totalRiders.html'
                           ,submitted_by_data= submitted_by_data,
                           lead_classification_data = lead_classification_data
                            )
# ridersAnalytics Route
@app.route('/ridersAnalytics')
def riders_analytics():
    db = get_db_connection()
    cursor = db.cursor()
     # 1. Total Riders (Banner)
    cursor.execute("SELECT COUNT(*) FROM riders")
    total_riders = cursor.fetchone()[0]
    
    
        # Riders by Location
    cursor.execute("SELECT work_location, COUNT(rider_id) FROM riders GROUP BY work_location")
    location_data = cursor.fetchall()

    # Riders by Loan Status
    cursor.execute("SELECT any_pending_loan, COUNT(rider_id) FROM riders GROUP BY any_pending_loan")
    loan_status_data = cursor.fetchall()
    loan_status_labels = ['No Loan', 'Has Loan']
    loan_status_data = [(loan_status_labels[status[0]], status[1]) for status in loan_status_data]
    # close cursor 
    cursor.close()
    db.close()
    return render_template('ridersAnalytics.html',
                           total_riders=total_riders, 
                            location_data=location_data, 
                            loan_status_data=loan_status_data,)

# Add Product route
@app.route('/addProduct', methods=['GET', 'POST'])
def addProduct():
    if request.method == 'POST':
        # Get form data
        product_name = request.form['product_name']
        product_description = request.form['product_description']
        product_image = request.files['product_image']

        # Check if the image file is valid
        if product_image and allowed_file(product_image.filename):
            filename = secure_filename(product_image.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            product_image.save(filepath)  # Save image to the static/images folder

            # Insert product details into the database
            db = get_db_connection()
            cursor = db.cursor()
            sql = """
                INSERT INTO products 
                (product_name, product_description, product_image, created_at)
                VALUES (%s, %s, %s, NOW())
            """
            values = (product_name, product_description, filename)
            cursor.execute(sql, values)
            db.commit()
            cursor.close()
            db.close()

            return redirect(url_for('addProduct'))  # Redirect after successful submission

    return render_template('addProduct.html')

@app.route('/get_add_product_link')
def get_add_product_link():
    # Return the HTML fragment for the "Add Product" link
    link_html = '<li><a class="dropdown-item text-white" href="#" onclick="loadContent(\'addProduct\')">Add Product</a></li>'
    print("Returning Add Product link: ", link_html)  # Log the link
    return jsonify(html=link_html)

# All Customers route
@app.route('/allcustomers', methods=['GET', 'GET'])
def allcustomers():
    page = request.args.get('page', 1, type=int)  # Get the page number (default is 1)
    limit = 10  # Number of riders to show per page
    offset = (page - 1) * limit  # Offset for pagination
    
    # Get the search query from the URL
    search_query = request.args.get('search', '')  # Default is empty if no search
    
    db = get_db_connection()
    cursor = db.cursor()

    if search_query:
        # If there is a search query, filter riders by name, phone number, or location
        query = """
            SELECT * FROM riders
            WHERE customername LIKE %s OR phone_number LIKE %s OR work_location LIKE %s
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, ('%' + search_query + '%', '%' + search_query + '%', '%' + search_query + '%', limit, offset))
    else:
        # If no search query, fetch all riders
        cursor.execute("SELECT * FROM riders ORDER BY created_at DESC LIMIT %s OFFSET %s", (limit, offset))
    
    riders = cursor.fetchall()
    
    cursor.close()
    db.close()

    # Pass the search query and the results to the template
    return render_template('allcustomers.html', riders=riders, page=page, search_query=search_query, no_results=len(riders) == 0)

@app.route('/delete_rider/<int:rider_id>', methods=['POST'])
def delete_rider(rider_id):
    # Connect to the database
    db = get_db_connection()
    cursor = db.cursor()

    try:
        # Execute the delete query
        cursor.execute("DELETE FROM riders WHERE rider_id = %s", (rider_id,))
        db.commit()
        flash('Rider deleted successfully!', 'success')
    except Exception as e:
        db.rollback()
        flash(f'Error deleting rider: {str(e)}', 'danger')
    finally:
        cursor.close()
        db.close()
    
    return redirect(url_for('allCustomers'))  # Redirect back to the all customers page



# Create Rider route
@app.route('/createRider', methods=['GET', 'POST'])
def createRider():
    if request.method == 'POST':
        # Retrieve form data
        customername = request.form['customername']
        phone_number = request.form['phone_number']
        work_location = request.form['work_location']
        current_motorbike = request.form['current_motorbike']
        fuel_consumption_per_day = request.form['fuel_consumption_per_day']
        
        # Check the value of any_pending_loan (dropdown) and convert to 1 or 0
        any_pending_loan = request.form.get('any_pending_loan')
        any_pending_loan = 1 if any_pending_loan == "yes" else 0

        lead_classification = request.form['lead_classification']
        any_comments = request.form['any_comments']
        submitted_by = request.form['submitted_by']

        # Insert into database
        db = get_db_connection()
        cursor = db.cursor()
        sql = """
            INSERT INTO riders 
            (customername, phone_number, work_location, current_motorbike, fuel_consumption_per_day, any_pending_loan, lead_classification, any_comments, submitted_by, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """
        values = (customername, phone_number, work_location, current_motorbike, fuel_consumption_per_day, any_pending_loan, lead_classification, any_comments, submitted_by)
        cursor.execute(sql, values)
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('createRider'))

    return render_template('createRider.html')


# Create Deal route
@app.route('/createDeal', methods=['GET', 'POST'])
def createDeal():
    error_message = None

    if request.method == 'POST':
        rider_id = request.form['rider_id']
        product_id = request.form['product_id']

        # Check if the deal already exists
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM deals WHERE rider_id = %s AND product_id = %s', (rider_id, product_id))
        existing_deal = cursor.fetchall()  # Fetch all results to avoid unread result error

        if existing_deal:
            # Deal already exists, set the error message
            error_message = "This deal already exists."
        else:
            # Insert deal into the deals table
            sql = 'INSERT INTO deals (rider_id, product_id) VALUES (%s, %s)'
            values = (rider_id, product_id)
            cursor.execute(sql, values)
            db.commit()

        cursor.close()
        db.close()

        if not error_message:
            return redirect(url_for('totalDeals'))  # Redirect to total deals page after saving     

    # Fetch riders and products for the suggestion functionality
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute('SELECT rider_id, customername FROM riders')
    riders = cursor.fetchall()
    cursor.execute('SELECT product_id, product_name FROM products')
    products = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('createDeal.html', riders=riders, products=products, error_message=error_message)
# delete fuction for deals
@app.route('/delete_deal/<int:deal_id>', methods=['POST'])
def delete_deal(deal_id):
    try:
        db = get_db_connection()
        cursor = db.cursor()

        # Delete the deal from the database
        sql = "DELETE FROM deals WHERE deal_id = %s"
        cursor.execute(sql, (deal_id,))
        db.commit()

        cursor.close()
        db.close()

        flash("Deal deleted successfully!", "success")
    except Exception as e:
        flash("An error occurred while trying to delete the deal.", "danger")
        print(f"Error: {e}")
    return redirect(url_for('totalDeals'))   


# Suggestion route for rider names
@app.route('/suggest_riders', methods=['GET'])
def suggest_riders():
    query = request.args.get('query', '')
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT rider_id, customername FROM riders WHERE customername LIKE %s", (f'%{query}%',))
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(results)

# Suggestion route for product names
@app.route('/suggest_products', methods=['GET'])
def suggest_products():
    query = request.args.get('query', '')
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT product_id, product_name FROM products WHERE product_name LIKE %s", (f'%{query}%',))
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(results)

# Total Deals route
@app.route('/totalDeals')
def totalDeals():
    db = get_db_connection()
    cursor = db.cursor()

    # Select deal_id, rider_id, customername, product_name, and created_at
    cursor.execute('SELECT d.deal_id, d.rider_id, r.customername, p.product_name, d.created_at '
                   'FROM deals d '
                   'JOIN riders r ON d.rider_id = r.rider_id '
                   'JOIN products p ON d.product_id = p.product_id')
    deals = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template('totalDeals.html', deals=deals)

@app.route('/rider_details/<int:rider_id>')
def rider_details(rider_id):
    # Fetch the rider details from the database
    db = get_db_connection()
    cursor = db.cursor()

    # Fetch rider information
    cursor.execute("SELECT rider_id, customername, phone_number, work_location, current_motorbike, "
                   "fuel_consumption_per_day, any_pending_loan, lead_classification, any_comments, "
                   "submitted_by, created_at FROM riders WHERE rider_id = %s", (rider_id,))
    rider = cursor.fetchone()

    # Check if the rider was found
    if not rider:
        return "Rider not found", 404

    # Convert rider tuple to a dictionary for easier access in the template
    rider_columns = [column[0] for column in cursor.description]  # Get column names
    rider_dict = dict(zip(rider_columns, rider))  # Combine into a dictionary

    # Fetch the deals related to the rider, including product name
    cursor.execute("SELECT d.deal_id, p.product_name, d.created_at FROM deals d "
                   "JOIN products p ON d.product_id = p.product_id "
                   "WHERE d.rider_id = %s", (rider_id,))
    deals = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template('rider_details.html', rider=rider, deals=deals)

# pipeline 
@app.route('/pipelineAnalytics', methods=['GET'])
def pipeline_analytics():
    db = get_db_connection()
    cursor = db.cursor()

    # Query to count total deals
    cursor.execute("SELECT COUNT(*) FROM deals")  # Ensure the 'deals' table is correct
    total_deals = cursor.fetchone()[0]  # Get the total count of deals

    # Riders by 'lead_classification'
    cursor.execute("SELECT lead_classification, COUNT(rider_id) FROM riders GROUP BY lead_classification")
    lead_classification_data = cursor.fetchall()

    cursor.close()
    db.close()

    # Lead Classification for Pie and Funnel Chart
    lead_classification_labels = [item[0] for item in lead_classification_data]
    lead_classification_counts = [item[1] for item in lead_classification_data]
    
    funnel_data = {
        "hot": next((count for label, count in lead_classification_data if label == "hot"), 0),
        "warm": next((count for label, count in lead_classification_data if label == "warm"), 0),
        "cold": next((count for label, count in lead_classification_data if label == "cold"), 0),
    }

    funnel_labels = list(funnel_data.keys())
    funnel_counts = list(funnel_data.values())

    # Sending data to the template
    return render_template(
        'pipelineAnalytics.html',
        total_deals=total_deals,
        lead_classification_labels=lead_classification_labels,
        lead_classification_counts=lead_classification_counts,
        funnel_labels=funnel_labels,
        funnel_counts=funnel_counts
    )



@app.route('/dealsAnalytics', methods=['GET', 'POST'])
def dealsAnalytics():
    db = get_db_connection()
    cursor = db.cursor()
    
        # Deals Analytics
    cursor.execute("SELECT COUNT(deal_id) AS total_deals FROM deals")
    total_deals_count = cursor.fetchone()[0]
    cursor.execute("""
        SELECT r.submitted_by, COUNT(d.deal_id) AS deal_count
        FROM deals AS d
        JOIN riders AS r ON d.rider_id = r.rider_id
        GROUP BY r.submitted_by
    """)
    submitted_by_data = cursor.fetchall()
    submitted_by_labels = [data[0] for data in submitted_by_data]
    submitted_by_counts = [data[1] for data in submitted_by_data]
    cursor.execute("""
        SELECT p.product_name, COUNT(d.product_id) AS deal_count
        FROM products AS p
        LEFT JOIN deals AS d ON p.product_id = d.product_id
        GROUP BY p.product_name
    """)
    products_data = cursor.fetchall()
    products = [data[0] for data in products_data]
    product_counts = [data[1] for data in products_data]
    
       # Query to count total deals
    cursor.execute("SELECT COUNT(*) FROM deals")  # Ensure the 'deals' table is correct
    total_deals_count1 = cursor.fetchone()[0]  # Get the total count of deals 

    cursor.close()
    db.close()
    # Sending data to the template
    return render_template(
        'dealsAnalytics.html',total_deals_count=total_deals_count,                            
                                submitted_by_labels=submitted_by_labels, 
                                submitted_by_counts=submitted_by_counts, 
                                products=products, 
                                product_counts=product_counts)

 
   # byproductAnalysis
@app.route('/byProductAnalytics', methods=['GET'])
def byProductAnalytics():
    db = get_db_connection()
    cursor = db.cursor()

    # Query to count total products by product name
    cursor.execute("""
        SELECT product_name, COUNT(*) AS total_count
        FROM products
        GROUP BY product_name
    """)
    product_counts = cursor.fetchall()

    products = []
    
    # Analyze the stock status and determine the message and color
    for product_name, total_count in product_counts:
        if total_count < 10:
            status = "Almost out of stock"
            color = "red"
        elif 10 <= total_count <= 50:
            status = "Low stock"
            color = "orange"
        else:
            status = "In stock"
            color = "green"
        
        products.append({
            'product_name': product_name,
            'total_count': total_count,
            'status': status,
            'color': color
        })

    cursor.close()
    db.close()

    # Sending data to the template
    return render_template('byProductAnalytics.html',products=products)

@app.route('/register', methods=['GET'])
def register1():
    return render_template('register.html')




# Dashboard route and all graphs
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# Monthly Analytics Route
@app.route('/monthlyAnalytics')
def monthly_analytics():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # Query to get rider count by 'submitted_by'
    query = """
    SELECT submitted_by, COUNT(*) AS rider_count
    FROM riders
    GROUP BY submitted_by;
    """
    cursor.execute(query)
    rider_counts = cursor.fetchall()
    
    # Fetch daily rider counts for the current month (current and previous dates only)
    query = """
    SELECT DATE(created_at) AS day, COUNT(*) AS total_riders
    FROM riders
    WHERE MONTH(created_at) = MONTH(CURRENT_DATE) AND YEAR(created_at) = YEAR(CURRENT_DATE)
      AND DATE(created_at) <= CURRENT_DATE
    GROUP BY day
    ORDER BY day;
    """
    
    try:
        cursor.execute(query)
        daily_data = cursor.fetchall()

        # Prepare data for the total riders chart
        days = [row['day'].strftime('%Y-%m-%d') for row in daily_data]  # Format dates
        counts = [row['total_riders'] for row in daily_data]  # Extract counts

        # Generate all dates from the 1st of the month to the current date
        today = datetime.today()
        first_day = today.replace(day=1)
        
        # Stop generating days if they are in the future
        all_days = []
        for i in range((today - first_day).days + 1):  # Only up to today
            day = (first_day + timedelta(days=i)).strftime('%Y-%m-%d')
            all_days.append(day)

        # Fill missing days with zero counts
        all_counts = [0] * len(all_days)
        for i, day in enumerate(all_days):
            if day in days:
                all_counts[i] = counts[days.index(day)]
        
    except Exception as e:
        print(f"Error fetching monthly analytics: {e}")
        all_days, all_counts = [], []  # In case of error, return empty lists

    # Fetch daily deals count for the current month (current and previous dates only)
    query = """
    SELECT DATE(created_at) AS deal_date, COUNT(*) AS total_deals
    FROM deals
    WHERE MONTH(created_at) = MONTH(CURRENT_DATE) AND YEAR(created_at) = YEAR(CURRENT_DATE)
      AND DATE(created_at) <= CURRENT_DATE
    GROUP BY deal_date
    ORDER BY deal_date;
    """
    
    try:
        cursor.execute(query)
        daily_deals_data = cursor.fetchall()

        # Prepare data for the daily deals chart
        deal_dates = [row['deal_date'].strftime('%Y-%m-%d') for row in daily_deals_data]
        deal_counts = [row['total_deals'] for row in daily_deals_data]

        # Fill missing days with zero deals
        all_deals_counts = [0] * len(all_days)
        for i, day in enumerate(all_days):
            if day in deal_dates:
                all_deals_counts[i] = deal_counts[deal_dates.index(day)]
    except Exception as e:
        print(f"Error fetching daily deals analytics: {e}")
        deal_dates, deal_counts = [], []  # In case of error, return empty lists
    finally:
        cursor.close()
        db.close()
    return render_template('monthlyAnalytics.html', rider_counts=rider_counts,
                           days=all_days, counts=all_counts,
                           deal_dates=all_days, deal_counts=all_deals_counts)

# register Route 
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        try:
            user_name = request.form['user_name']
            email = request.form['email']
            phone = request.form['phone']
            subject = request.form['subject']
            message = request.form['message']
            
            # Validate email format
            if not validate_email(email):
                return jsonify({"status": "error", "error_email": "Invalid email format."}), 400
            
            # Validate phone format
            if not validate_phone(phone):
                return jsonify({"status": "error", "error_phone": "Invalid phone number format."}), 400

            # Check if the username or email is already taken
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM contact_form WHERE user_name = %s OR email = %s", (user_name, email))
            if cursor.fetchone():
                return jsonify({"status": "error", "error_all": "Username or email already taken."}), 409

            # Insert data into the contact_form table
            cursor.execute("""
                INSERT INTO contact_form (user_name, email, phone, subject, message)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_name, email, phone, subject, message))

            # Commit changes
            conn.commit()
            cursor.close()
            conn.close()

            # Return success message
            return jsonify({"status": "success", "message": "Registration successful."}), 201
        
        except Exception as e:
            # Rollback in case of any error
            conn.rollback()
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            
            # Log the error (optional)
            print(f"Error during registration: {e}")
            
            # Return a JSON error response
            return jsonify({"status": "error", "message": "An internal error occurred. Please try again later."}), 500

# Validate email format
def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

# Registration route
@app.route('/user_register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        # Validate email
        if not validate_email(email):
            flash("Invalid email format", "danger")
            return redirect(url_for('user_register'))

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Connect to database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the email is already in use
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            flash("Email already in use, please choose another.", "danger")
            cursor.close()
            conn.close()
            return redirect(url_for('user_register'))

        # Insert new user into the database
        cursor.execute("""
            INSERT INTO users (username, email, password, role)
            VALUES (%s, %s, %s, %s)
        """, (username, email, hashed_password, role))
        conn.commit()

        # Close the database connection
        cursor.close()
        conn.close()

        # Flash success message and redirect to login page
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('user_register.html') 

# Login route with role-based redirection
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check user in the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user['password'], password):
            # Save user info in session
            session['user_id'] = user['user_id']
            session['role'] = user['role']
            flash('Login successful!')

            # Role-based redirection
            if user['role'] == 'admin':
                return redirect('/admin/dashboard') # Redirect to the admin dashboard route
            elif user['role'] == 'user':
                return redirect('/user/dashboard') # Redirect to the user dashboard route
            else:
                flash("No dashboard assigned for this role.")
                return redirect(url_for('login'))
        else:
            flash('Invalid email or password.')

    return render_template('login.html')

# User Dashboard Route
@app.route('/user/dashboard')
def user_dashboard():
    
    db = get_db_connection()
    cursor = db.cursor()

    # Riders by 'submitted_by'
    cursor.execute("SELECT submitted_by, COUNT(rider_id) FROM riders GROUP BY submitted_by")
    submitted_by_data = cursor.fetchall()

    # Riders by 'lead_classification'
    cursor.execute("SELECT lead_classification, COUNT(rider_id) FROM riders GROUP BY lead_classification")
    lead_classification_data = cursor.fetchall()

    # Total Riders (Banner)
    cursor.execute("SELECT COUNT(*) FROM riders")
    total_riders = cursor.fetchone()[0]

    # Riders by Location
    cursor.execute("SELECT work_location, COUNT(rider_id) FROM riders GROUP BY work_location")
    location_data = cursor.fetchall()

    # Riders by Loan Status
    cursor.execute("SELECT any_pending_loan, COUNT(rider_id) FROM riders GROUP BY any_pending_loan")
    loan_status_data = cursor.fetchall()
    loan_status_labels = ['No Loan', 'Has Loan']
    loan_status_data = [(loan_status_labels[status[0]], status[1]) for status in loan_status_data]

    # Lead Classification for Pie and Funnel Chart
    lead_classification_labels = [item[0] for item in lead_classification_data]
    lead_classification_counts = [item[1] for item in lead_classification_data]
    funnel_data = {
        "hot": next((count for label, count in lead_classification_data if label == "hot"), 0),
        "warm": next((count for label, count in lead_classification_data if label == "warm"), 0),
        "cold": next((count for label, count in lead_classification_data if label == "cold"), 0),
    }
    funnel_labels = list(funnel_data.keys())
    funnel_counts = list(funnel_data.values())

    # Deals Analytics
    cursor.execute("SELECT COUNT(deal_id) AS total_deals FROM deals")
    total_deals_count = cursor.fetchone()[0]
    cursor.execute("""
        SELECT r.submitted_by, COUNT(d.deal_id) AS deal_count
        FROM deals AS d
        JOIN riders AS r ON d.rider_id = r.rider_id
        GROUP BY r.submitted_by
    """)
    submitted_by_data = cursor.fetchall()
    submitted_by_labels = [data[0] for data in submitted_by_data]
    submitted_by_counts = [data[1] for data in submitted_by_data]
    cursor.execute("""
        SELECT p.product_name, COUNT(d.product_id) AS deal_count
        FROM products AS p
        LEFT JOIN deals AS d ON p.product_id = d.product_id
        GROUP BY p.product_name
    """)
    products_data = cursor.fetchall()
    products = [data[0] for data in products_data]
    product_counts = [data[1] for data in products_data]

    # Monthly Riders - Fetch daily rider counts for the current month
    query = """
    SELECT DATE(created_at) AS day, COUNT(*) AS total_riders
    FROM riders
    WHERE MONTH(created_at) = MONTH(CURRENT_DATE) AND YEAR(created_at) = YEAR(CURRENT_DATE)
    GROUP BY day
    ORDER BY day;
    """
    
    try:
        cursor.execute(query)
        daily_data = cursor.fetchall()  # Fetch all results from the executed query

        # Prepare data for the chart
        days = [row[0].strftime('%Y-%m-%d') for row in daily_data]  # Extract and format days
        counts = [row[1] for row in daily_data]  # Extract counts
    except Exception as e:
        print(f"Error fetching monthly analytics: {e}")
        days, counts = [], []  # In case of error, return empty lists

    # Daily Deals - Query to fetch daily deals count for the current month
    query = """
    SELECT DATE(created_at) AS deal_date, COUNT(*) AS total_deals
    FROM deals
    WHERE MONTH(created_at) = MONTH(CURRENT_DATE) AND YEAR(created_at) = YEAR(CURRENT_DATE)
    GROUP BY deal_date
    ORDER BY deal_date;
    """
    
    try:
        cursor.execute(query)
        daily_deals_data = cursor.fetchall()  # Fetch all results from the executed query

        # Prepare data for the daily deals chart
        deal_dates = [row[0].strftime('%Y-%m-%d') for row in daily_deals_data]  # Format dates as 'YYYY-MM-DD'
        deal_counts = [row[1] for row in daily_deals_data]  # Extract counts
    except Exception as e:
        print(f"Error fetching daily deals analytics: {e}")
        deal_dates, deal_counts = [], []  # In case of error, return empty lists

    finally:
        cursor.close()  # Ensure cursor is closed
        db.close()  # Ensure database connection is closed
    
    if 'user_id' in session and session['role'] == 'user':
        
        
        # Render user dashboard from the user folder
        return render_template('user/dashboard2.html'                             , 
        submitted_by_data=submitted_by_data, 
        lead_classification_data=lead_classification_data,
        total_riders=total_riders, 
        location_data=location_data, 
        loan_status_data=loan_status_data,
        lead_classification_labels=lead_classification_labels,
        lead_classification_counts=lead_classification_counts,
        funnel_labels=funnel_labels,
        funnel_counts=funnel_counts, 
        total_deals_count=total_deals_count,
        submitted_by_labels=submitted_by_labels, 
        submitted_by_counts=submitted_by_counts, 
        products=products, 
        product_counts=product_counts,
        # total riders graph
        days=days, counts=counts,
        # daily deals 
        deal_dates=deal_dates, 
        deal_counts=deal_counts)  # Path to user dashboard
    else:
        flash("Unauthorized access.")
        return redirect(url_for('login'))

# Admin Dashboard Route
@app.route('/admin/dashboard')
def admin_dashboard():
    
    db = get_db_connection()
    cursor = db.cursor()

    # Riders by 'submitted_by'
    cursor.execute("SELECT submitted_by, COUNT(rider_id) FROM riders GROUP BY submitted_by")
    submitted_by_data = cursor.fetchall()

    # Riders by 'lead_classification'
    cursor.execute("SELECT lead_classification, COUNT(rider_id) FROM riders GROUP BY lead_classification")
    lead_classification_data = cursor.fetchall()

    # Total Riders (Banner)
    cursor.execute("SELECT COUNT(*) FROM riders")
    total_riders = cursor.fetchone()[0]

    # Riders by Location
    cursor.execute("SELECT work_location, COUNT(rider_id) FROM riders GROUP BY work_location")
    location_data = cursor.fetchall()

    # Riders by Loan Status
    cursor.execute("SELECT any_pending_loan, COUNT(rider_id) FROM riders GROUP BY any_pending_loan")
    loan_status_data = cursor.fetchall()
    loan_status_labels = ['No Loan', 'Has Loan']
    loan_status_data = [(loan_status_labels[status[0]], status[1]) for status in loan_status_data]

    # Lead Classification for Pie and Funnel Chart
    lead_classification_labels = [item[0] for item in lead_classification_data]
    lead_classification_counts = [item[1] for item in lead_classification_data]
    funnel_data = {
        "hot": next((count for label, count in lead_classification_data if label == "hot"), 0),
        "warm": next((count for label, count in lead_classification_data if label == "warm"), 0),
        "cold": next((count for label, count in lead_classification_data if label == "cold"), 0),
    }
    funnel_labels = list(funnel_data.keys())
    funnel_counts = list(funnel_data.values())

    # Deals Analytics
    cursor.execute("SELECT COUNT(deal_id) AS total_deals FROM deals")
    total_deals_count = cursor.fetchone()[0]
    cursor.execute("""
        SELECT r.submitted_by, COUNT(d.deal_id) AS deal_count
        FROM deals AS d
        JOIN riders AS r ON d.rider_id = r.rider_id
        GROUP BY r.submitted_by
    """)
    submitted_by_data = cursor.fetchall()
    submitted_by_labels = [data[0] for data in submitted_by_data]
    submitted_by_counts = [data[1] for data in submitted_by_data]
    cursor.execute("""
        SELECT p.product_name, COUNT(d.product_id) AS deal_count
        FROM products AS p
        LEFT JOIN deals AS d ON p.product_id = d.product_id
        GROUP BY p.product_name
    """)
    products_data = cursor.fetchall()
    products = [data[0] for data in products_data]
    product_counts = [data[1] for data in products_data]

    # Monthly Riders - Fetch daily rider counts for the current month
    query = """
    SELECT DATE(created_at) AS day, COUNT(*) AS total_riders
    FROM riders
    WHERE MONTH(created_at) = MONTH(CURRENT_DATE) AND YEAR(created_at) = YEAR(CURRENT_DATE)
    GROUP BY day
    ORDER BY day;
    """
    
    try:
        cursor.execute(query)
        daily_data = cursor.fetchall()  # Fetch all results from the executed query

        # Prepare data for the chart
        days = [row[0].strftime('%Y-%m-%d') for row in daily_data]  # Extract and format days
        counts = [row[1] for row in daily_data]  # Extract counts
    except Exception as e:
        print(f"Error fetching monthly analytics: {e}")
        days, counts = [], []  # In case of error, return empty lists

    # Daily Deals - Query to fetch daily deals count for the current month
    query = """
    SELECT DATE(created_at) AS deal_date, COUNT(*) AS total_deals
    FROM deals
    WHERE MONTH(created_at) = MONTH(CURRENT_DATE) AND YEAR(created_at) = YEAR(CURRENT_DATE)
    GROUP BY deal_date
    ORDER BY deal_date;
    """ 
    try:
        cursor.execute(query)
        daily_deals_data = cursor.fetchall()  # Fetch all results from the executed query

        # Prepare data for the daily deals chart
        deal_dates = [row[0].strftime('%Y-%m-%d') for row in daily_deals_data]  # Format dates as 'YYYY-MM-DD'
        deal_counts = [row[1] for row in daily_deals_data]  # Extract counts
    except Exception as e:
        print(f"Error fetching daily deals analytics: {e}")
        deal_dates, deal_counts = [], []  # In case of error, return empty lists

    finally:
        cursor.close()  # Ensure cursor is closed
        db.close()  # Ensure database connection is closed
        
    if 'user_id' in session and session['role'] == 'admin':       
        # Render admin dashboard from the admin folder
        return render_template('admin/dashboard1.html', 
        submitted_by_data=submitted_by_data, 
        lead_classification_data=lead_classification_data,
        total_riders=total_riders, 
        location_data=location_data, 
        loan_status_data=loan_status_data,
        lead_classification_labels=lead_classification_labels,
        lead_classification_counts=lead_classification_counts,
        funnel_labels=funnel_labels,
        funnel_counts=funnel_counts, 
        total_deals_count=total_deals_count,
        submitted_by_labels=submitted_by_labels, 
        submitted_by_counts=submitted_by_counts, 
        products=products, 
        product_counts=product_counts,
        # total riders graph
        days=days, counts=counts,
        # daily deals 
        deal_dates=deal_dates, 
        deal_counts=deal_counts)  # Path to admin dashboard
    else:
        flash("Unauthorized access.")
        return redirect(url_for('login'))

# log out route 
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.')
    return redirect(url_for('login'))


#settings 
@app.route('/settings')
def settings():
    return render_template('/settings.html')

#admin requests 
@app.route('/admin/requests')
def requests():
    try:
        # Use your existing database connection function
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Query to fetch all data from contact_form table
        query = "SELECT * FROM contact_form"
        cursor.execute(query)
        contact_forms = cursor.fetchall()

        # Close the connection
        cursor.close()
        connection.close()

        return render_template('requests.html', contact_forms=contact_forms)
    except mysql.connector.Error as e:
        return f"Error connecting to MySQL: {e}"
   
if __name__ == '__main__':
    app.run(debug=True, port=4001)