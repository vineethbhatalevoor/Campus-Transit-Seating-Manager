import os
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "smvitm_secret_transit_key"

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123", 
        database="campus_transit_db"
    )

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for(f"{session['role']}_dashboard"))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    user_id = request.form['user_id'].strip()
    role = request.form['role'].strip()
    password = request.form['password'].strip()
    
    # 1. DYNAMIC ADMIN LOGIN
    if role == 'admin' and user_id.lower() == 'admin' and password == 'admin123':
        session['user_id'] = 'Admin_Master'
        session['role'] = 'admin'
        return redirect(url_for('admin_dashboard'))
        
    # 2. DYNAMIC DRIVER LOGIN (Checks if the Bus ID exists in your database!)
    elif role == 'driver' and password == 'driver123':
        try:
            conn = get_db_connection()
            cursor = conn.get_db_connection().cursor() if hasattr(conn, 'get_db_connection') else conn.cursor()
            cursor.execute("SELECT Bus_ID FROM Bus WHERE Bus_ID = %s", (user_id,))
            bus_exists = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if bus_exists:
                session['user_id'] = user_id
                session['role'] = 'driver'
                return redirect(url_for('driver'))
        except Exception as e:
            print(f"Driver authentication database fault: {str(e)}")

    # 3. DYNAMIC STUDENT LOGIN (Checks if the USN exists in your database!)
    elif role == 'student' and password == 'student123':
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT USN FROM Student WHERE UPPER(USN) = %s", (user_id.upper(),))
            student_exists = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if student_exists:
                session['user_id'] = user_id.upper()
                session['role'] = 'student'
                return redirect(url_for('student'))
        except Exception as e:
            print(f"Student authentication database fault: {str(e)}")
        
    return "<script>alert('Invalid Credentials or User Not Found in Database!'); window.location='/';</script>"
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/admin')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/driver')
def driver():
    return driver_dashboard()

def driver_dashboard():
    if session.get('role') != 'driver': 
        return redirect(url_for('index'))
    
    bus_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT S.Name, S.Phone, St.Stop_Name, CAST(St.Pickup_Time AS CHAR) as Pickup_Time 
        FROM Student S 
        JOIN Registration R ON S.USN = R.USN 
        JOIN Stop St ON R.Stop_ID = St.Stop_ID AND R.Route_ID = St.Route_ID
        WHERE R.Bus_ID = %s 
        ORDER BY St.Pickup_Time ASC
    """
    cursor.execute(query, (bus_id,))
    manifest = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('driver_dashboard.html', manifest=manifest)

@app.route('/student')
def student():
    return student_dashboard()

def student_dashboard():
    if session.get('role') != 'student': 
        return redirect(url_for('index'))
        
    usn = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT S.Name, S.USN, B.Plate_Number, B.Driver_Name, St.Stop_Name, CAST(St.Pickup_Time AS CHAR) as Pickup_Time, R.Fee_Status
        FROM Student S
        JOIN Registration R ON S.USN = R.USN
        JOIN Bus B ON R.Bus_ID = B.Bus_ID
        JOIN Stop St ON R.Stop_ID = St.Stop_ID AND R.Route_ID = St.Route_ID
        WHERE S.USN = %s
    """
    cursor.execute(query, (usn,))
    profile = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('student_dashboard.html', p=profile, student=profile)


@app.route('/api/search_student/<string:usn>', methods=['GET'])
def search_student(usn):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT S.USN, S.Name, S.Department, S.Phone, B.Plate_Number, B.Driver_Name, St.Stop_Name, R.Fee_Status, R.Semester, R.Registration_ID
        FROM Student S
        JOIN Registration R ON S.USN = R.USN
        JOIN Bus B ON R.Bus_ID = B.Bus_ID
        JOIN Stop St ON R.Stop_ID = St.Stop_ID AND R.Route_ID = St.Route_ID
        WHERE S.USN = %s
    """
    cursor.execute(query, (usn.upper(),))
    student = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if student:
        return jsonify({"status": "success", "data": student})
    return jsonify({"status": "error", "message": "No active transit profile discovered for this USN ID."})

@app.route('/api/get_registrations')
def get_registrations():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT R.Registration_ID, S.Name, S.USN, B.Plate_Number, St.Stop_Name, R.Fee_Status
            FROM Registration R
            JOIN Student S ON R.USN = S.USN
            JOIN Bus B ON R.Bus_ID = B.Bus_ID
            JOIN Stop St ON R.Stop_ID = St.Stop_ID AND R.Route_ID = St.Route_ID
        """
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(data)
    except Exception as e:
        print(f"!!! MANIFEST ENGINE ERROR: {str(e)}")
        return jsonify([])
@app.route('/api/update_fee', methods=['POST'])
def update_fee():
    reg_id = request.form['registration_id']
    new_status = request.form['fee_status']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Registration SET Fee_Status = %s WHERE Registration_ID = %s", (new_status, reg_id))
        conn.commit()
        return jsonify({"status": "success", "message": "Student statement balance updated!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route('/api/update_bus_capacity', methods=['POST'])
def update_bus_capacity():
    bus_id = request.form['bus_id']
    new_capacity = request.form['capacity']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE Bus SET Capacity = %s WHERE Bus_ID = %s", (new_capacity, bus_id))
        conn.commit()
        return jsonify({"status": "success", "message": f"Bus {bus_id} configuration ceiling updated to {new_capacity} seats."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/api/add_student', methods=['POST'])
def add_student():
    usn = request.form['usn']
    name = request.form['name']
    dept = request.form['dept']
    phone = request.form['phone']
    bus_id = request.form['bus_id']
    stop_id = request.form['stop_id']
    route_id = request.form['route_id']
    sem = request.form['semester']
    fee = request.form['fee_status']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT Capacity FROM Bus WHERE Bus_ID = %s", (bus_id,))
        capacity = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM Registration WHERE Bus_ID = %s", (bus_id,))
        allocated = cursor.fetchone()[0]
        
        if allocated >= capacity:
            return jsonify({"status": "error", "message": "Allocation Failed: Bus Capacity Exceeded!"})

        cursor.execute("INSERT INTO Student VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE Name=%s", (usn, name, dept, phone, name))
        reg_id = int(usn[-3:]) + 6000
        cursor.execute("INSERT INTO Registration VALUES (%s, %s, %s, %s, %s, %s, %s, CURDATE())", 
                       (reg_id, usn, bus_id, stop_id, route_id, sem, fee))
        conn.commit()
        return jsonify({"status": "success", "message": "Transit allocation processed successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route('/api/remove_registration/<int:reg_id>', methods=['DELETE'])
def remove_registration(reg_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Registration WHERE Registration_ID = %s", (reg_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"status": "success", "message": "Allocation dropped successfully."})
@app.route('/api/get_fleet_details')
def get_fleet_details():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Pull bus details with both lowercase and uppercase properties for safety
        query_buses = """
            SELECT 
                B.Bus_ID as bus_id, B.Bus_ID as Bus_ID,
                B.Plate_Number as plate_number, B.Plate_Number as Plate_Number,
                B.Capacity as capacity, B.Capacity as Capacity,
                B.Driver_Name as driver_name, B.Driver_Name as Driver_Name,
                Ro.Route_Name as route_name, Ro.Route_Name as Route_Name,
                (SELECT COUNT(*) FROM Registration WHERE Bus_ID = B.Bus_ID) as current_occupancy,
                (SELECT COUNT(*) FROM Registration WHERE Bus_ID = B.Bus_ID) as Current_Occupancy
            FROM Bus B
            LEFT JOIN Route Ro ON B.Route_ID = Ro.Route_ID
        """
        cursor.execute(query_buses)
        buses = cursor.fetchall()
        
        # Pull stops details with both lowercase and uppercase properties for safety
        query_stops = """
            SELECT 
                Route_ID as route_id, Route_ID as Route_ID,
                Stop_ID as stop_id, Stop_ID as Stop_ID,
                Stop_Name as stop_name, Stop_Name as Stop_Name,
                CAST(Pickup_Time AS CHAR) as pickup_time, CAST(Pickup_Time AS CHAR) as Pickup_Time
            FROM Stop 
            ORDER BY Route_ID, Pickup_Time ASC
        """
        cursor.execute(query_stops)
        stops = cursor.fetchall()
        
        cursor.close()
        conn.close()
        return jsonify({"buses": buses, "stops": stops})
    except Exception as e:
        print(f"!!! FLEET API ERROR: {str(e)}")
        return jsonify({"buses": [], "stops": [], "error": str(e)})
if __name__ == '__main__':
    app.run(port=5000, debug=True)