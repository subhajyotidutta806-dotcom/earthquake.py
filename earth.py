import tkinter as tk
from tkinter import messagebox
import folium
from geopy.geocoders import Nominatim
import webbrowser
import os

# Initialize geocoder
geolocator = Nominatim(user_agent="earthquake_app")

# Function to classify earthquake
def classify_earthquake(magnitude):
    if magnitude < 4.0:
        return "Minor", "No major damage expected."
    elif 4.0 <= magnitude < 6.0:
        return "Moderate", "Some damage possible."
    elif 6.0 <= magnitude < 7.5:
        return "Severe", "Serious damage possible!"
    else:
        return "Disaster", "Major destruction likely!"

# Safety instructions
def safety_instructions(level):
    if level == "Minor":
        return "Stay calm."
    elif level == "Moderate":
        return "Stay alert."
    elif level == "Severe":
        return "Drop, Cover, Hold."
    else:
        return "Evacuate immediately!"

# Main function
def analyze():
    try:
        magnitude = float(entry_mag.get())
        location_name = entry_loc.get()

        location = geolocator.geocode(location_name)

        if location is None:
            messagebox.showerror("Error", "Location not found!")
            return

        lat, lon = location.latitude, location.longitude

        level, message = classify_earthquake(magnitude)
        instructions = safety_instructions(level)

        result_text.set(
            f"Location: {location_name}\n"
            f"Coordinates: ({lat:.2f}, {lon:.2f})\n"
            f"Magnitude: {magnitude}\n"
            f"Level: {level}\n"
            f"Impact: {message}\n\n"
            f"Safety: {instructions}"
        )

        # Create map
        map_obj = folium.Map(location=[lat, lon], zoom_start=6)

        folium.Marker(
            [lat, lon],
            popup=f"{location_name}\nMagnitude: {magnitude}",
            tooltip="Earthquake Location",
            icon=folium.Icon(color="red")
        ).add_to(map_obj)

        # Save map
        map_file = "earthquake_map.html"
        map_obj.save(map_file)

        # Open in browser
        webbrowser.open('file://' + os.path.realpath(map_file))

    except ValueError:
        messagebox.showerror("Error", "Enter valid magnitude!")

# GUI setup
root = tk.Tk()
root.title("Earthquake Management System with Map")
root.geometry("500x400")

tk.Label(root, text="🌍 Earthquake System", font=("Arial", 16)).pack(pady=10)

tk.Label(root, text="Enter Location:").pack()
entry_loc = tk.Entry(root, width=30)
entry_loc.pack(pady=5)

tk.Label(root, text="Enter Magnitude:").pack()
entry_mag = tk.Entry(root, width=30)
entry_mag.pack(pady=5)

tk.Button(root, text="Analyze & Show Map", command=analyze, bg="blue", fg="white").pack(pady=15)

result_text = tk.StringVar()
tk.Label(root, textvariable=result_text, wraplength=400, justify="left").pack(pady=10)
root.mainloop()

