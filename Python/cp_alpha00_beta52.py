import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# 1. Joukowski transformation: z = ζ + c^2 / ζ
# ------------------------------------------------------------
def joukowski_transform(zeta, c=1.0):
    return zeta + c**2 / zeta

def generate_circle(center, radius, n_points=500):
    theta = np.linspace(0, 2*np.pi, n_points, endpoint=True)
    return center + radius * np.exp(1j * theta)

# ------------------------------------------------------------
# 2. Geometry (from first code)
# ------------------------------------------------------------
c = 1.0
x0 = -0.1                     # horizontal shift (thickness)
y0 = 0.1                      # vertical shift (camber)
R_circle = np.sqrt((c - x0)**2 + y0**2)   # radius through ζ = c

# Generate circle points
n_points = 800
zeta_pts = generate_circle(complex(x0, y0), R_circle, n_points)
z_pts = joukowski_transform(zeta_pts, c)

# ------------------------------------------------------------
# 3. Physics: Kutta condition & circulation (from second code)
# ------------------------------------------------------------
U_inf = 1.0
alpha = 0.0                           # angle of attack
beta = np.arctan2(y0, c - x0)         # camber angle from geometry
Gamma = 4 * np.pi * R_circle * U_inf * np.sin(alpha + beta)

print(f"Geometry: x0={x0:.2f}, y0={y0:.2f}, R={R_circle:.4f}")
print(f"α={np.rad2deg(alpha):.1f}°, β={np.rad2deg(beta):.1f}°, Γ={Gamma:.4f}")

# ------------------------------------------------------------
# 4. Velocity on the airfoil (full shifted potential)
# ------------------------------------------------------------
zeta0 = complex(x0, y0)
zeta_rel = zeta_pts - zeta0

dV_dzeta = (U_inf * np.exp(-1j * alpha)
            - U_inf * np.exp(1j * alpha) * R_circle**2 / zeta_rel**2
            + 1j * Gamma / (2 * np.pi * zeta_rel))

dz_dzeta = 1 - c**2 / zeta_pts**2

V_z = dV_dzeta / dz_dzeta

# Mask trailing edge point (ζ = c) to avoid 0/0
idx_trail = np.argmin(np.abs(zeta_pts - c))
mask = np.ones(len(zeta_pts), dtype=bool)
mask[idx_trail] = False

z_masked = z_pts[mask]
x_masked = np.real(z_masked)
y_masked = np.imag(z_masked)
V_z_masked = V_z[mask]

speed = np.abs(V_z_masked)
Cp = 1 - (speed / U_inf)**2
Cp = np.clip(Cp, -10, 1)   # clip extreme values

# ------------------------------------------------------------
# 5. Plotting in the style of the second code (2 subplots)
# ------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Left: Airfoil colored by Cp
sc1 = ax1.scatter(x_masked, y_masked, c=Cp, cmap='coolwarm', 
                  s=10, edgecolor='none', alpha=0.9)
ax1.set_aspect('equal')
ax1.grid(True, linestyle='--', alpha=0.4)
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.set_title(f'Joukowski airfoil – $C_p$ distribution\n'
              f'x0={x0:.2f}, y0={y0:.2f},  α={np.rad2deg(alpha):.1f}°, β={np.rad2deg(beta):.1f}°')
fig.colorbar(sc1, ax=ax1, label='$C_p$', extend='both')

# Right: Cp vs chord position, colored by Cp
sc2 = ax2.scatter(x_masked, Cp, c=Cp, cmap='coolwarm', 
                  s=10, edgecolor='none', alpha=0.8)
ax2.invert_yaxis()                # negative Cp (suction) at top
ax2.grid(True, linestyle='--', alpha=0.4)
ax2.set_xlabel('x (chord position)')
ax2.set_ylabel('$C_p$')
ax2.set_title('Pressure coefficient along the chord\n(color = $C_p$ value)')
ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3, linewidth=0.8)
fig.colorbar(sc2, ax=ax2, label='$C_p$', extend='both')

plt.tight_layout()
plt.show()
