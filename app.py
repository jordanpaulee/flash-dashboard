from flask import Flask, render_template, request, jsonify
import pandas as pd
import folium 
import matplotlib
matplotlib.use('Agg')  # Ensure non-GUI mode for Matplotlib
import matplotlib.pyplot as plt

app = Flask(__name__)

def load_data():
    # Read CSV and handle missing values
    return pd.read_csv("./data/sample.csv").fillna("").sort_values(by = "nat_score", ascending = False)

@app.route('/', methods=["GET", "POST"])
def index():
    
    schools = load_data()
    print(schools.head())

    # Get a list of the unique regions in the schools dataframe
    unique_regions = list(schools["Region"].str.strip().unique())
    print(unique_regions)

    # Region Filter Logic
    selected_region = request.form.get("region", "All")
    print("selected_region: ", selected_region)

    # Subset the dataframe to the selected Region if it is not "All"
    if selected_region != "All":
        schools = schools[schools["Region"] == selected_region]

    # KPIs
    avg_teacher_ratio = round(schools["student_teacher_ratio"].mean(), 1)
    num_elec = schools["noelec"].sum()    
    avg_nat_score = round(schools["nat_score"].mean(), 1)
    avg_cct = round(schools["cct_percentage"].mean(), 1)

    # Map of Schools
    school_map = folium.Map(location=[12.8797, 121.7740], zoom_start=6)
    for _, row in schools.iterrows():
        folium.CircleMarker(
            location=[row["Lat"], row["Lon"]],
            popup=f"{row['school_name']}<br>NAT Score: {row['nat_score']}%",
            # icon=folium.Icon(color="blue" if row["original_internet_boolean"] else "red")
            radius=4,  # Circle size
            color="green",  # Border color
            fill=True,
            fill_color="green",
            fill_opacity=0.7,
        ).add_to(school_map)
    school_map.save("static/school_map.html")

    # Pie Chart: Male vs Female Students
    total_male = schools["total_male"].sum()  # Sum all male students
    total_female = schools["total_female"].sum()  # Sum all female students
    plt.figure(figsize=(4, 4))
    plt.pie(
        [total_male, total_female], 
        labels=["Male Students", "Female Students"], 
        autopct='%1.1f%%', 
        colors=["blue", "pink"]
    )
    plt.savefig("static/gender_pie.png")
    plt.close()

    return render_template("index.html",
        avg_teacher_ratio=avg_teacher_ratio,
        num_elec=num_elec,
        avg_nat_score=avg_nat_score,
        avg_cct=avg_cct,
        schools=schools.to_dict(orient="records"), # Convert DataFrame to list of dictionaries
        regions=unique_regions,
        selected_region=selected_region)  

if __name__ == "__main__":
    app.run(debug=True)