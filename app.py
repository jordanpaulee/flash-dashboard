from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

def load_data():
    # Read CSV and handle missing values
    return pd.read_csv("./data/sample.csv").fillna("")

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