import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data from CSV
data = pd.read_csv('results/iteration_results_3_1.csv')

# Convert 'Compilation Success' to a numeric binary column
data['Compilation Success'] = data['Compilation Success'].apply(lambda x: 1 if x else 0)

# Use similarity metrics directly, no conversion needed
data['Similarity with Previous'] = data['Similarity with Previous']
data['Similarity with Original'] = data['Similarity with Original']

# Plot 1: Line Graph of Total Time vs. Iteration with Average Line
plt.figure(figsize=(10, 6))
plt.plot(data['Iteration'], data['Total Time (seconds)'], marker='o', color='blue', label='Total Time')
plt.axhline(y=data['Total Time (seconds)'].mean(), color='red', linestyle='--', label=f'Average Time = {data["Total Time (seconds)"].mean():.2f}')
plt.title('Total Time vs. Iteration')
plt.xlabel('Iteration')
plt.ylabel('Total Time (seconds)')
plt.legend()
plt.grid(True)
plt.show()

# Assuming 'Iteration' starts at 0 or 1, and you want to exclude the first one (0 or 1)
filtered_data = data[data['Iteration'] > data['Iteration'].min()]  # Exclude the first iteration

# Plot 2: Similarity with Previous vs. Iteration with Average Line
plt.figure(figsize=(10, 6))
plt.plot(filtered_data['Iteration'], filtered_data['Similarity with Previous'], marker='o', color='orange', label='Similarity with Previous')
plt.axhline(y=filtered_data['Similarity with Previous'].mean(), color='blue', linestyle='--', label=f'Average Similarity = {filtered_data["Similarity with Previous"].mean():.2f}%')
plt.title('Similarity with Previous vs. Iteration')
plt.xlabel('Iteration')
plt.ylabel('Similarity with Previous (%)')
plt.legend()
plt.grid(True)
plt.show()


# Plot 3: Similarity with Original vs. Iteration with Polynomial Trendline
plt.figure(figsize=(10, 6))
plt.plot(data['Iteration'], data['Similarity with Original'], marker='o', color='green', label='Similarity with Original')

# Fit a polynomial (e.g., cubic) to the data
polynomial_fit = np.polyfit(data['Iteration'], data['Similarity with Original'], 5)  # Cubic fit
polynomial_trend = np.poly1d(polynomial_fit)

plt.plot(data['Iteration'], polynomial_trend(data['Iteration']), linestyle='--', color='red', label='Polynomial Trendline')
plt.title('Similarity with Original vs. Iteration')
plt.xlabel('Iteration')
plt.ylabel('Similarity with Original (%)')
plt.legend()
plt.grid(True)
plt.show()

# Plot 4: Scatter Plot of Total Time vs. Similarity with Original
plt.figure(figsize=(10, 6))
plt.scatter(data['Total Time (seconds)'], data['Similarity with Original'], color='red')
plt.title('Total Time vs. Similarity with Original')
plt.xlabel('Total Time (seconds)')
plt.ylabel('Similarity with Original (%)')
plt.grid(True)
plt.show()

# Plot 8: Comparison of Compilation Success vs. Total Time
fig, ax1 = plt.subplots(figsize=(10, 6))

color = 'tab:blue'
ax1.set_xlabel('Iteration')
ax1.set_ylabel('Total Time (seconds)', color=color)
ax1.plot(data['Iteration'], data['Total Time (seconds)'], marker='o', color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Compilation Success', color=color)
ax2.plot(data['Iteration'], data['Compilation Success'], marker='x', color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
plt.title('Comparison of Compilation Success vs. Total Time')
plt.show()
