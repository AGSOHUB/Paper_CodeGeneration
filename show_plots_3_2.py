import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the CSV file into a DataFrame
csv_file_path = 'results/iteration_results_3_2.csv'
data = pd.read_csv(csv_file_path)

# Convert 'Compilation Success' to a numeric binary column if it's not already
data['Compilation Success'] = data['Compilation Success'].apply(lambda x: 1 if x else 0)

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

# Plot 2: Line Graph of Total Time with Compilation Success Overlay
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
plt.title('Total Time vs. Compilation Success')
plt.show()
