import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# Configure matplotlib for publication-quality output
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['DejaVu Serif', 'Times New Roman', 'Times']
rcParams['mathtext.fontset'] = 'cm'  # Computer Modern for LaTeX-like math
rcParams['axes.linewidth'] = 0.8
rcParams['xtick.major.width'] = 0.8
rcParams['ytick.major.width'] = 0.8
rcParams['xtick.direction'] = 'in'
rcParams['ytick.direction'] = 'in'
rcParams['xtick.top'] = True
rcParams['ytick.right'] = True

# Define the function
def A3_hat(p):
    numerator = -0.616647881739505 * np.exp(-0.552605335919693 * np.exp(p))
    denominator = np.sin(np.cos(p)) - np.abs(p)
    return numerator / denominator + 0.921964323679771

# Generate data for the curve
p = np.linspace(0, 0.5, 1000)
y = A3_hat(p)

# Scatter data points
scatter_data = """0.00,0.5
0.01,0.49744950892200523
0.02,0.4947961454086841
0.03,0.49203568028781275
0.04,0.4891655063931692
0.05,0.4861804681386442
0.06,0.4830774611793251
0.07,0.4798516728499167
0.08,0.4764965649930478
0.09,0.4730092271000399
0.1,0.46938333702446194
0.11,0.46561045412689755
0.12,0.46168780095224604
0.13,0.45760728178648097
0.14,0.45335797129833433
0.15,0.44893751974883506
0.16,0.44433208243911365
0.17,0.43953758533578097
0.18,0.43454255921952245
0.19,0.4293311822253738
0.2,0.42390081850381817
0.21,0.4182300784035889
0.22,0.4123108180947064
0.23,0.40613172436516815
0.24,0.399669551694508
0.25,0.3929162754078347
0.26,0.38584326351619247
0.27,0.3784359299789587
0.28,0.370672189995087
0.29,0.3625279290473855
0.3,0.35397672110443756
0.31,0.3449895164077589
0.32,0.33553428875892377
0.33,0.3255756349223103
0.34,0.31506734776888573
0.35,0.3039779337611788
0.36,0.2922446697896221
0.37,0.2798182518473617
0.38,0.2666353397344354
0.39,0.252615526498267
0.4,0.23768332022995975
0.41,0.22173411227463893
0.42,0.20466312830238828
0.43,0.1863198446038385
0.44,0.16655284045247842
0.45,0.1451501913600998
0.46,0.1218716445414851
0.47,0.09638121630669728
0.48,0.06824513327478827
0.49,0.03687714681581637
0.5,0.00"""

# Parse scatter data
p_scatter = []
y_scatter = []
for line in scatter_data.strip().split('\n'):
    px, py = line.split(',')
    p_scatter.append(float(px))
    y_scatter.append(float(py))
p_scatter = np.array(p_scatter)
y_scatter = np.array(y_scatter)

# Create figure with square aspect ratio
fig, ax = plt.subplots(figsize=(4.5, 4.5), dpi=300)

# Plot the curve
ax.plot(p, y, color='#1a1a1a', linewidth=1.2, label=r'$\hat{A}_3(p)$', zorder=2)

# Plot scatter points
ax.scatter(p_scatter, y_scatter, s=20, facecolors='none', edgecolors='#c41e3a', 
           linewidths=0.8, label='Data', zorder=3)

# Labels with LaTeX formatting
ax.set_xlabel(r'$p$', fontsize=11, labelpad=8)
ax.set_ylabel(r'$\hat{A}_3(p)$', fontsize=11, labelpad=8)

# Set axis limits
ax.set_xlim(0, 0.5)

# Determine y-limits for square data aspect (include scatter data)
all_y = np.concatenate([y, y_scatter])
y_min, y_max = all_y.min(), all_y.max()
y_range = y_max - y_min
x_range = 0.5

# Add small padding to y-axis, ensure 0 is included
padding = 0.05 * y_range
ax.set_ylim(y_min - padding, y_max + padding)

# Move x-axis (spine) to y=0
ax.spines['bottom'].set_position('zero')

# Set equal aspect ratio for the data
ax.set_aspect('equal', adjustable='box')

# Customize ticks
ax.tick_params(axis='both', which='major', labelsize=10, length=4)
ax.tick_params(axis='x', which='major', direction='out')  # x-ticks point down from y=0

# Light grid (optional, comment out if not wanted)
ax.grid(True, linestyle='-', alpha=0.15, linewidth=0.5)

# Add legend
ax.legend(loc='upper right', frameon=True, framealpha=0.95, edgecolor='none', fontsize=9)

# Remove top and right spines for cleaner look (optional)
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)

# Tight layout
plt.tight_layout()

# Save as PDF (vector format, ideal for papers)
plt.savefig('/mnt/user-data/outputs/A3_hat_plot.pdf', format='pdf', bbox_inches='tight', dpi=300)

# Also save as PNG for preview
plt.savefig('/mnt/user-data/outputs/A3_hat_plot.png', format='png', bbox_inches='tight', dpi=300)

print("Plot saved successfully!")
print(f"y range: [{y_min:.6f}, {y_max:.6f}]")