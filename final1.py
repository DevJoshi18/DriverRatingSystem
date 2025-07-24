import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkcalendar import DateEntry
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Driver:
    def rash_score(self, lanechange_perHR, speedtxt_perweek, accidents_per_month):
        return 100 - (((lanechange_perHR*0.1)/5) + (speedtxt_perweek * 3) + (accidents_per_month * 10))
 
    def driver_type(self, rash_score):
        if rash_score >= 90:
            return "Excellent 🌟"
        elif rash_score >= 85:
            return "Safe ✅"
        elif rash_score >= 70:
            return "Moderate 👍"
        elif rash_score >= 50:
            return "Rash ⚠️"
        else:
            return "Very Rash 🚨"

class DriverDashboard:
    def __init__(self, window):
        self.window = window
        self.window.title("Driver Information System")
        self.window.geometry("1000x800")
        self.load_drivers_data()
        self.create_login_screen()

    def load_drivers_data(self):
        self.drivers_data = []
        if os.path.exists("drivers_data.csv"):
            with open("drivers_data.csv", mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    self.drivers_data.append({
                        "car_number": row[0],
                        "driver_name": row[1],
                        "car_name": row[2],
                        "lanechange_perHR": int(row[3]),
                        "speedtxt_perweek": int(row[4]),
                        "accidents_per_month": int(row[5]),
                        "PUC_validity": row[6],
                        "insurance_validity": row[7],
                        "gender": row[8],
                    })
        else:
            self.create_csv_file()

    def create_csv_file(self):
        with open("drivers_data.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Car Number", "Driver Name", "Car Name", "Lane Changes per Hour", "Speeding Tickets per Week", "Accidents per Month", "Insurance Validity", "PUC Validity", "gender"])
            
    def save_drivers_data(self):
        with open("drivers_data.csv", mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Car Number", "Driver Name", "Car Name", "Lane Changes per Hour", "Speeding Tickets per Week", "Accidents per Month", "Insurance validity", "PUC validity", "gender"])
            for driver in self.drivers_data:
                writer.writerow([driver["car_number"], driver["driver_name"], driver["car_name"],
                                 driver["lanechange_perHR"], driver["speedtxt_perweek"], driver["accidents_per_month"],
                                 driver["PUC_validity"], driver["insurance_validity"], driver["gender"]])

    def clear_screen(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def create_login_screen(self):
        self.clear_screen()
        self.login_frame = tk.Frame(self.window)
        self.login_frame.pack(pady=50)

        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0, padx=10, pady=5)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)


        tk.Button(self.login_frame, text="Login", command=self.authenticate).grid(row=2, columnspan=2, pady=20)

    def authenticate(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        correct_username = "user1"
        correct_password = "dev"

        if username == correct_username and password == correct_password:
            self.create_main_screen()
        else:
            messagebox.showerror("Login Error", "Invalid username or password")

    def create_main_screen(self):
        self.clear_screen()
        self.main_frame = tk.Frame(self.window)
        self.main_frame.pack(pady=50)

        tk.Label(self.main_frame, text="Welcome to the Driver Information System", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.main_frame, text="View RTOS Dashboard", command=self.view_rtos_dashboard, width=25).pack(pady=10)
        tk.Button(self.main_frame, text="Add Driver", command=self.add_driver_screen, width=25).pack(pady=10)
        tk.Button(self.main_frame, text="Calculate Rash Score", command=self.calculate_rash_score_screen, width=25).pack(pady=10)
    
    def calculate_rash_score_screen(self):
        def r_score(lanechange_perHR, speedtxt_perweek, accidents_per_month):
            return 100 - (((lanechange_perHR*0.1)/5) + (speedtxt_perweek*3) + (accidents_per_month*10))
 
        def d_type(rash_score):
            if rash_score >= 90:
                return "Excellent 🌟"
            elif rash_score >= 85:
                return "Safe ✅"
            elif rash_score >= 70:
                return "Moderate 👍"
            elif rash_score >= 50:
                return "Rash ⚠️"
            else:
                return "Very Rash 🚨"
        self.clear_screen()
        self.rash_frame = tk.Frame(self.window)
        self.rash_frame.pack(pady=40)

        tk.Label(self.rash_frame, text="Rash Score Calculator", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.rash_frame, text="Lane Changes per Hour:").pack()
        lane_ = tk.Entry(self.rash_frame)
        lane_.pack()

        tk.Label(self.rash_frame, text="Speeding Tickets per Week:").pack()
        speed_ = tk.Entry(self.rash_frame)
        speed_.pack()

        tk.Label(self.rash_frame, text="Accidents per Month:").pack()
        accident_ = tk.Entry(self.rash_frame)
        accident_.pack()

        def submit():
            lane_imput = float(lane_.get())
            speed_imput = int(speed_.get())
            accident_imput = int(accident_.get())

            if lane_imput < 0 or speed_imput < 0 or accident_imput < 0:
                messagebox.showerror("Invalid Input", "Please enter positive values.")
                return

            rash_calc = r_score(lane_imput, speed_imput, accident_imput)
            driv_type = d_type(rash_calc)

            messagebox.showinfo("Rash Score Result", f"Rash Score: {rash_calc}\nDriver Type: {driv_type}")

        def go_back():
            self.create_main_screen()

        tk.Button(self.rash_frame , text="Submit", command=submit, width=12).pack()
        tk.Button(self.rash_frame, text="Back", command=go_back, width=12).pack()

    def view_rtos_dashboard(self):
        self.clear_screen()
        self.dashboard_frame = tk.Frame(self.window)
        self.dashboard_frame.pack(pady=40)

        tk.Label(self.dashboard_frame, text="RTOS Driver Dashboard", font=("Arial", 16)).pack(pady=10)

        self.tree = ttk.Treeview(self.dashboard_frame, columns=("Car Number", "Driver Name", "Rash Score", "Driver Type"), show="headings")
        self.tree.heading("Car Number", text="Car Number")
        self.tree.heading("Driver Name", text="Driver Name")
        self.tree.heading("Rash Score", text="Rash Score")
        self.tree.heading("Driver Type", text="Driver Type")
        self.tree.pack(fill="both", expand=True)

        driver_obj = Driver()

        for driver in self.drivers_data:
            rash_score = driver_obj.rash_score(driver["lanechange_perHR"], driver["speedtxt_perweek"], driver["accidents_per_month"])
            driver_type = driver_obj.driver_type(rash_score)
            self.tree.insert("", "end", values=(driver["car_number"], driver["driver_name"], rash_score, driver_type))

        tk.Button(self.dashboard_frame, text="Remove Driver", command=self.remove_driver, width=25).pack(pady=10)
        tk.Button(self.dashboard_frame, text="Update Info", command=self.update_driver_screen, width=25).pack(pady=10)
        tk.Button(self.dashboard_frame, text="View Statistics", command=self.view_statistics, width=25).pack(pady=10)
        tk.Button(self.dashboard_frame, text="Go Back", command=self.create_main_screen).pack(pady=10)
    
    def update_driver_screen(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a driver to update.")
            return

        car_number = self.tree.item(selected_item)["values"][0]
        driver = next((d for d in self.drivers_data if d["car_number"] == car_number), None)
        if not driver:
            messagebox.showerror("Error", "Driver not found.")
            return

        self.clear_screen()
        self.update_frame = tk.Frame(self.window)
        self.update_frame.pack(pady=20)

        tk.Label(self.update_frame, text="Update Driver Info", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.update_frame, text="Driver Gender:").pack()
        gender_entry = tk.Entry(self.update_frame)
        gender_entry = ttk.Combobox(self.update_frame, values=['Male', 'Female'])
        gender_entry.insert(0, driver["gender"])
        gender_entry.pack()

        tk.Label(self.update_frame, text="Car Name:").pack()
        car_entry = tk.Entry(self.update_frame)
        car_entry.insert(0, driver["car_name"])
        car_entry.pack()

        tk.Label(self.update_frame, text="Lane Changes per Hour:").pack()
        lane_entry = tk.Entry(self.update_frame)
        lane_entry.insert(0, driver["lanechange_perHR"])
        lane_entry.pack()

        tk.Label(self.update_frame, text="Speeding Tickets per Week:").pack()
        speed_entry = tk.Entry(self.update_frame)
        speed_entry.insert(0, driver["speedtxt_perweek"])
        speed_entry.pack()

        tk.Label(self.update_frame, text="Accidents per Month:").pack()
        accident_entry = tk.Entry(self.update_frame)
        accident_entry.insert(0, driver["accidents_per_month"])
        accident_entry.pack()

        tk.Label(self.update_frame, text="PUC Validity:").pack()
        puc_entry = DateEntry(self.update_frame, date_pattern='dd-mm-yyyy')
        puc_entry.set_date(datetime.strptime(driver["PUC_validity"], "%d-%m-%Y").date())
        puc_entry.pack()

        tk.Label(self.update_frame, text="Insurance Validity:").pack()
        ins_entry = DateEntry(self.update_frame, date_pattern='dd-mm-yyyy')
        ins_entry.set_date(datetime.strptime(driver["insurance_validity"], "%d-%m-%Y").date())
        ins_entry.pack()

        def save_updated_driver():
            driver["gender"] = gender_entry.get().strip()
            driver["car_name"] = car_entry.get().strip()
            driver["lanechange_perHR"] = int(lane_entry.get())
            driver["speedtxt_perweek"] = int(speed_entry.get())
            driver["accidents_per_month"] = int(accident_entry.get())
            driver["PUC_validity"] = puc_entry.get_date().strftime('%d-%m-%Y')
            driver["insurance_validity"] = ins_entry.get_date().strftime('%d-%m-%Y')

            self.save_drivers_data()
            messagebox.showinfo("Success", "Driver info updated.")
            self.view_rtos_dashboard()

        tk.Button(self.update_frame, text="Save Changes", command=save_updated_driver).pack(pady=10)
        tk.Button(self.update_frame, text="Go Back", command=self.view_rtos_dashboard).pack(pady=5)

    def pie_chart(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        driver_values = self.tree.item(selected_item[0])["values"]
        car_number = driver_values[0]
        
        driver = next((d for d in self.drivers_data if d["car_number"] == car_number), None)
        if not driver:
            return
        
        labels = ["Lane Changes/hr", "Speeding Tickets/wk", "Accidents/mo"]
        sizes = [driver["lanechange_perHR"], driver["speedtxt_perweek"], driver["accidents_per_month"]]
        
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.set_title(f"Driving Pattern for {driver['driver_name']}")
        
        chart_window = tk.Toplevel(self.window)
        chart_window.title("Driver Statistics Pie Chart")
        
        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def view_statistics(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        driver_values = self.tree.item(selected_item[0])["values"]
        car_number = driver_values[0]
        driver = next((d for d in self.drivers_data if d["car_number"] == car_number), None)
        if not driver:
            return

        
        driver_obj = Driver()
        rash_score = driver_obj.rash_score(
            driver["lanechange_perHR"],
            driver["speedtxt_perweek"],
            driver["accidents_per_month"]
        )
        driver_type = driver_obj.driver_type(rash_score)

        today = datetime.today().date()
        insurance_date = datetime.strptime(driver["insurance_validity"], "%d-%m-%Y").date()
        puc_date = datetime.strptime(driver["PUC_validity"], "%d-%m-%Y").date()
        one_month_from_now = today + relativedelta(months=1)

        if insurance_date < today:
            insurance_warning = "❌ Insurance expired ❌"
        elif today <= insurance_date <= one_month_from_now:
            insurance_warning = "⚠️ Insurance renewal within 1 month ⚠️"
        else:
            insurance_warning = ""

        if puc_date < today:
            puc_warning = "❌ PUC expired ❌"
        elif today <= puc_date <= one_month_from_now:
            puc_warning = "⚠️ PUC renewal within 1 month ⚠️"
        else:
            puc_warning = ""

        stats_window = tk.Toplevel(self.window)
        stats_window.title("Driver Statistics")
        stats_window.geometry("550x350")

        tk.Label(stats_window, text=f"Driver: {driver['driver_name']}", font=("Arial", 14)).pack(pady=10)
        tk.Label(stats_window, text=f"Gender: {driver['gender']}").pack()
        tk.Label(stats_window, text=f"Car Name: {driver['car_name']}").pack()
        tk.Label(stats_window, text=f"Lane Changes/hr: {driver['lanechange_perHR']}").pack()
        tk.Label(stats_window, text=f"Speeding Tickets/wk: {driver['speedtxt_perweek']}").pack()
        tk.Label(stats_window, text=f"Accidents/mo: {driver['accidents_per_month']}").pack()
        tk.Label(stats_window, text=f"PUC Validity: {driver['PUC_validity']}").pack()
        if puc_warning:
            tk.Label(stats_window, text=puc_warning, fg="red", font=("Arial", 12, "bold")).pack()
        tk.Label(stats_window, text=f"Insurance Validity: {driver['insurance_validity']}").pack()
        if insurance_warning:
            tk.Label(stats_window, text=insurance_warning, fg="red", font=("Arial", 12, "bold")).pack()
        tk.Label(stats_window, text=f"Rash Score: {rash_score:.2f}").pack()
        tk.Label(stats_window, text=f"Driver Type: {driver_type}").pack()
        tk.Button(stats_window, text="View pie chart", command=self.pie_chart, width=25).pack(pady=10)

    def remove_driver(self):
        selected_item = self.tree.selection()
        if selected_item:
            driver_car_number = self.tree.item(selected_item)["values"][0]  # Get car number of the selected driver

            # Find the driver in the drivers_data list
            driver_to_remove = None
            for driver in self.drivers_data:
                if driver["car_number"] == driver_car_number:
                    driver_to_remove = driver
                    break

            if driver_to_remove:
                self.drivers_data.remove(driver_to_remove)
                self.save_drivers_data()  # Save the updated data to the CSV file
                messagebox.showinfo("Success", f"Driver with car number {driver_car_number} removed successfully.")
                self.view_rtos_dashboard()  # Refresh the dashboard
            else:
                messagebox.showerror("Error", "Driver not found.")
        else:
            messagebox.showerror("Selection Error", "Please select a driver to remove.")

    def add_driver_screen(self):
        self.clear_screen()
        self.add_driver_frame = tk.Frame(self.window)
        self.add_driver_frame.pack(pady=20)

        tk.Label(self.add_driver_frame, text="Add New Driver", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.add_driver_frame, text="Driver Name:").pack()
        self.driver_name_entry = tk.Entry(self.add_driver_frame)
        self.driver_name_entry.pack(pady=5)

        tk.Label(self.add_driver_frame, text="Gender: ").pack()
        self.gender = ttk.Combobox(self.add_driver_frame, values=['Male', 'Female'])
        self.gender.pack(pady =5)
        self.gender.set('Select gender')

        tk.Label(self.add_driver_frame, text="Registration Number:").pack()
        self.car_number_entry = tk.Entry(self.add_driver_frame)
        self.car_number_entry.pack(pady=5)

        tk.Label(self.add_driver_frame, text="Car Name:").pack()
        self.car_name_entry = tk.Entry(self.add_driver_frame)
        self.car_name_entry.pack(pady=5)

        tk.Label(self.add_driver_frame, text="Insurance Validity Date:").pack()
        self.insurance_date_entry = DateEntry(
        self.add_driver_frame, width=12,
        background='darkgreen', foreground='white',
        borderwidth=4, date_pattern='dd-mm-yy'
        )
        self.insurance_date_entry.pack(pady=10)

        tk.Label(self.add_driver_frame, text="PUC Validity Date:").pack()
        self.PUC_date_entry = DateEntry(
        self.add_driver_frame, width=12,
        background='darkgreen', foreground='white',
        borderwidth=4, date_pattern='dd-mm-yy'
        )
        self.PUC_date_entry.pack(pady=10)

        tk.Label(self.add_driver_frame, text="Lane Changes per Hour:").pack()
        self.lanechange_perHR_entry = tk.Entry(self.add_driver_frame)
        self.lanechange_perHR_entry.pack(pady=5)

        tk.Label(self.add_driver_frame, text="Speeding Tickets per Week:").pack()
        self.speedtxt_perweek_entry = tk.Entry(self.add_driver_frame)
        self.speedtxt_perweek_entry.pack(pady=5)

        tk.Label(self.add_driver_frame, text="Accidents per Month:").pack()
        self.accidents_per_month_entry = tk.Entry(self.add_driver_frame)
        self.accidents_per_month_entry.pack(pady=5)

        tk.Button(self.add_driver_frame, text="Add Driver", command=self.add_driver_to_dashboard).pack(pady=10)
        tk.Button(self.add_driver_frame, text="Go Back", command=self.create_main_screen).pack(pady=5)

    def add_driver_to_dashboard(self):
        car_number = self.car_number_entry.get().strip()
        gender = self.gender.get().strip()
        driver_name = self.driver_name_entry.get().strip()
        car_name = self.car_name_entry.get().strip()
        lanechange_perHR = int(self.lanechange_perHR_entry.get())
        speedtxt_perweek = int(self.speedtxt_perweek_entry.get())
        accidents_per_month = int(self.accidents_per_month_entry.get())
        PUC_driver = self.PUC_date_entry.get_date().strftime('%d-%m-%Y')
        insurance_driver = self.insurance_date_entry.get_date().strftime('%d-%m-%Y')
        
        new_driver = {
            "car_number": car_number,
            "driver_name": driver_name,
            "car_name": car_name,
            "lanechange_perHR": lanechange_perHR,
            "speedtxt_perweek": speedtxt_perweek,
            "accidents_per_month": accidents_per_month,
            "PUC_validity": PUC_driver,
            "insurance_validity": insurance_driver,
            "gender": gender
        }
        self.drivers_data.append(new_driver)

        driver_obj = Driver()
        rash_score = driver_obj.rash_score(lanechange_perHR, speedtxt_perweek, accidents_per_month)
        driver_type = driver_obj.driver_type(rash_score)

        messagebox.showinfo("New Driver", f"Rash Score: {rash_score}\nDriver Type: {driver_type}")

        self.save_drivers_data()  # Save the updated data to CSV file immediately after adding
        messagebox.showinfo("Success", "New driver added successfully!")
        self.view_rtos_dashboard()

window = tk.Tk()
app = DriverDashboard(window)
window.mainloop()