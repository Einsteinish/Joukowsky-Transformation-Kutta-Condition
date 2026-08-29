import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# 1. Joukowski transformation: z = ζ + c^2 / ζ
# ------------------------------------------------------------
def joukowski_transform(zeta, c=1.0):
    return zeta + c**2 / zeta

# ------------------------------------------------------------
# 2. Parameters for the shifted circle (ζ-plane)
# ------------------------------------------------------------
c = 1.0                      # critical point (trailing edge)
x0 = -0.1                    # shift left → thickness
y0 = 0.1                     # shift up → camber
alpha = 0.0                  # angle of attack (in radians)

# Radius forced to pass through ζ = c (trailing edge)
R_circle = np.sqrt((c - x0)**2 + y0**2)

# ---- NEW: Compute circulation Γ from the Kutta condition ----
# The trailing edge point on the circle is at ζ = c.
# Vector from circle center (x0, y0) to trailing edge (c, 0):
#   (c - x0, 0 - y0) = (c - x0, -y0)
theta_TE = np.arctan2(-y0, c - x0)   # angle of the trailing edge point

# Kutta condition: v_theta must be zero at θ = θ_TE
# v_theta(θ_TE) = -2 U_inf sin(θ_TE - α) + Γ / (2π R) = 0
# => Γ = 4π R U_inf sin(θ_TE - α)
U_inf = 1.0
Gamma = 4 * np.pi * R_circle * U_inf * np.sin(theta_TE - alpha)

# Print the computed value for verification
print(f"Computed circulation from Kutta condition: Γ = {Gamma:.4f}")
print(f"Trailing edge angle θ_TE = {theta_TE:.4f} rad ({np.degrees(theta_TE):.2f}°)")
print(f"Radius R = {R_circle:.4f}")

# Generate points on the circle in ζ-plane
theta_geo = np.linspace(0, 2*np.pi, 500)
zeta = (x0 + R_circle * np.cos(theta_geo)) + 1j * (y0 + R_circle * np.sin(theta_geo))

# Map to z-plane (airfoil)
z = joukowski_transform(zeta, c)

# ------------------------------------------------------------
# 3. Velocity on the cylinder surface (using the Kutta-consistent Γ)
# ------------------------------------------------------------
theta_vel = np.linspace(0, 2*np.pi, 500)
# General formula: v_θ(θ) = -2 U_inf sin(θ - α) + Γ / (2π R)
v_theta = -2 * U_inf * np.sin(theta_vel - alpha) + Gamma / (2 * np.pi * R_circle)

# ------------------------------------------------------------
# 4. Plot: 3 subplots side by side
# ------------------------------------------------------------
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

# ---- Subplot 1: Circle in ζ-plane ----
ax1.plot(zeta.real, zeta.imag, 'b-', linewidth=2, label='Circle')
ax1.scatter([1, -1], [0, 0], color='red', s=40, zorder=5)   # ζ = 1 and ζ = -1
ax1.scatter(x0, y0, color='black', marker='x', s=60, zorder=5)  # center
ax1.set_aspect('equal')
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.set_xlabel(r'$\chi = \mathrm{Re}(\zeta)$')
ax1.set_ylabel(r'$\eta = \mathrm{Im}(\zeta)$')
ax1.set_title('Circle in $\zeta$-plane')
ax1.text(1.0, 0.1, r'$\zeta=1$', ha='center')
ax1.text(-1.0, 0.1, r'$\zeta=-1$', ha='center')
ax1.text(x0, y0-0.2, f'Center: ({x0:.2f}, {y0:.2f})', ha='center', fontsize=9)

# ---- Subplot 2: Joukowski airfoil in z-plane ----
ax2.plot(z.real, z.imag, 'r-', linewidth=2, label='Airfoil')
ax2.scatter([2, -2], [0, 0], color='blue', s=40, zorder=5)   # images of ζ = ±1
ax2.set_aspect('equal')
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.set_xlabel(r'$x = \mathrm{Re}(z)$')
ax2.set_ylabel(r'$y = \mathrm{Im}(z)$')
ax2.set_title('Joukowski Airfoil in $z$-plane')
ax2.text(2.0, 0.1, r'$z=2$', ha='center')
ax2.text(-2.0, 0.1, r'$z=-2$', ha='center')

# ---- Subplot 3: Tangential velocity on the cylinder ----
ax3.plot(theta_vel, v_theta, 'k-', linewidth=2, label=r'$v_\theta(\theta)$')
# Mark the trailing edge angle and zero velocity point
ax3.scatter(theta_TE, 0, color='red', s=60, zorder=5, label=f'Kutta point (θ_TE = {np.degrees(theta_TE):.1f}°)')
ax3.axhline(0, color='black', linewidth=0.8, linestyle='--')
ax3.set_xlabel(r'$\theta$ (radians)')
ax3.set_ylabel(r'$v_\theta$')
ax3.set_title(rf'$v_\theta$ on Cylinder Surface ($\alpha={np.degrees(alpha):.1f}^\circ$, $\Gamma={Gamma:.3f}$)')
ax3.grid(True, linestyle=':', alpha=0.7)
ax3.set_xlim(0, 2*np.pi)
ax3.set_xticks(np.arange(0, 2*np.pi + 0.1, np.pi/2))
ax3.set_xticklabels([r'$0$', r'$\pi/2$', r'$\pi$', r'$3\pi/2$', r'$2\pi$'])
ax3.legend(loc='best')

plt.tight_layout()
plt.show()
