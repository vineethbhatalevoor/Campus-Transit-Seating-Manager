# Campus Transit & Seating Manager 🚍

A robust, centralized digital operational control hub designed to streamline institutional transportation networks, track available seating counts dynamically, and eliminate logistical tracking blind spots.

---

## 📺 Project Video Demonstration

Click the thumbnail image below to watch the complete end-to-end operational software walkthrough, covering system transactions, database validations, and role-based portal navigations:

[![Watch the Demo Video](https://img.shields.io/badge/YouTube-Video_Walkthrough-red?style=for-the-badge&logo=youtube)](https://youtu.be/mNqyutUeEwM)

---

## 👥 Team - Core Collaborators
*4th Sem (Academic Year 2026) Department of Computer Science and Engineering, Shri Madhwa Vadiraja Institute of Technology and Management (SMVITM)*

* **Vineeth** 
* **Sarthak** 
* **Shreyas Bhat** 
* **Swasthik Acharya** 


---

## 🛠️ Technical Architecture & Technology Stack

* **Frontend Presentation Layer:** Responsive HTML5 templates styled via structural CSS3 Grids and non-blocking asynchronous **Vanilla JavaScript (`fetch` / AJAX API routing)**.
* **Backend Application Layer:** Python-based **Flask Micro-framework** managing business rules and data transfer loops.
* **Database Persistence Layer:** **MySQL Relational Engine** utilizing the transactional **InnoDB Storage Engine** for automated referential integrity constraint tracking and ACID compliance.
* **Database Normalization:** Fully normalized up to **Third Normal Form (3NF)** to eliminate data redundancy, modification anomalies, and orphan tracking entries.

---

## 🏗️ Database Schema & Relational Mappings

The data architecture is structured around **four strong entities** and **one weak entity**:

1. **Student:** `USN (PK)`, Name, Department, Phone.
2. **Registration:** `Registration_ID (PK)`, Semester, Fee_Status, Registration_Date, `USN (FK)`, `Bus_ID (FK)`, `(Stop_ID, Route_ID) (FK)`.
3. **Bus:** `Bus_ID (PK)`, Plate_Number, Capacity, Driver_Name, `Route_ID (FK)`.
4. **Route:** `Route_ID (PK)`, Route_Name, Start_Point, End_Point.
5. **Stop (Weak Entity):** `(Stop_ID, Route_ID) (Composite PK)`, Stop_Name, Pickup_Time.

### Entity Relationships:
* **Student ➔ Registration (`1:N`):** A student can hold distinct historic transit allocations across semesters.
* **Registration ➔ Stop (`N:1`):** Secured via a **Composite Foreign Key** constraint to ensure a student is only assigned to a boarding stop explicitly associated with their chosen route path.
* **Registration ➔ Bus (`N:1`):** Governed by an `ON DELETE SET NULL` referential action to prevent orphaned profiles if a vehicle is decommissioned.
* **Bus ➔ Route (`1:1`):** Each fleet vehicle is strictly bound to a single route path to optimize resource tracking.

---

## ⚡ Key System Modules

* **Administrative Control Portal:** Provides full CRUD privileges to search student records asynchronously, update billing/fee statuses via background endpoints, adjust vehicle maximum capacities, and process commuter lines.
* **Capacity Validation Engine:** Operates at the transaction level. Before executing an `INSERT` block, an aggregate query calculations check (`allocated >= capacity`) runs; if the vehicle is full, the transaction safely rolls back to prevent overbooking.
* **Fleet Operator (Driver) Manifest Module:** Restricts unauthorized viewing and pulls live data sorted chronologically by pickup times to render boarding manifests for specific drivers.
* **Commuter (Student) Digital Pass Module:** Provides students with a secure view of their vehicle assignments, driver contacts, and accounting payment approvals.

---

## 🚀 Local Deployment Instructions

### 1. Clone the Workspace
```bash
git clone [https://github.com/vineethbhatalevoor/Campus-Transit-Seating-Manager.git](https://github.com/vineethbhatalevoor/Campus-Transit-Seating-Manager.git)
cd Campus-Transit-Seating-Manager
```

### 2. Set Up the Database Environment
* Open **MySQL Workbench**.
* Open and run the clean schema generation backup file `bus_db.sql` located inside the repository root.
* Update the database connection credentials at the top of your `app.py` script:

```python
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_MYSQL_PASSWORD",
        database="bus_db"
    )
```
### 3. Launch the Server Pipeline
```python app.py```
Open your web browser and navigate to http://127.0.0.1:5000/ to test out the login interfaces.

### 📖 Key References
* VTU BCS403: Database Management Systems Laboratory Framework (2022 Scheme).

* Silberschatz, A., Korth, H. F., & Sudarshan, S., Database System Concepts, McGraw-Hill.
