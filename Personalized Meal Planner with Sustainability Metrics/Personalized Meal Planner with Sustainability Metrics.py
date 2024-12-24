import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Function to collect meal data from the user
def get_meal_data():
    meals = []
    print("Enter meal details (type 'done' when finished):")
    while True:
        meal_name = input("Meal name (or 'done' to finish): ").strip()
        if meal_name.lower() == 'done':
            break
        try:
            calories_grams = float(input(f"Calories in {meal_name} (in grams, will be converted to kcal): "))
            calories_kcal = calories_grams * 4  # Conversion: 1 gram = 4 kcal
            protein = float(input(f"Protein in {meal_name} (g): "))
            carbs = float(input(f"Carbs in {meal_name} (g): "))
            fat = float(input(f"Fat in {meal_name} (g): "))
            print(f"Details for '{meal_name}' have been recorded.\n")  # Confirmation message
            meals.append([meal_name, calories_kcal, protein, carbs, fat])
        except ValueError:
            print("Invalid input. Please enter numeric values for calories, protein, carbs, and fat.")
    return meals

# Collect user data
meal_data = get_meal_data()

# Create a DataFrame
columns = ["Meal", "Calories (kcal)", "Protein (g)", "Carbs (g)", "Fat (g)"]
df = pd.DataFrame(meal_data, columns=columns)

# Display the dataset
print("\nYour meal data:")
print(df)

# Plot 1: Matplotlib Bar Chart of Calories
plt.figure(figsize=(10, 5))
plt.bar(df["Meal"], df["Calories (kcal)"], color='skyblue')
plt.title("Calories in Each Meal", fontsize=16)
plt.xlabel("Meal", fontsize=12)
plt.ylabel("Calories (kcal)", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plot 2: Seaborn Heatmap for Nutritional Content
plt.figure(figsize=(10, 6))
sns.heatmap(df.iloc[:, 1:].set_index(df["Meal"]).T, annot=True, cmap="coolwarm", fmt=".1f")
plt.title("Nutritional Content per Meal", fontsize=16)
plt.show()

# Plot 3: Plotly Scatter Plot for Fat vs Protein
fig = px.scatter(
    df,
    x="Fat (g)",
    y="Protein (g)",
    text="Meal",
    size="Calories (kcal)",
    color="Fat (g)",
    title="Protein vs Fat Content by Meal",
    labels={"Fat (g)": "Fat Content (g)", "Protein (g)": "Protein (g)"},
    hover_data=["Meal"]
)
fig.update_traces(textposition='top center')
fig.show()