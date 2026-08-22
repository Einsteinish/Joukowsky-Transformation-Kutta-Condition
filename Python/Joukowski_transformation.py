import numpy as np
import matplotlib.pyplot as plt

def joukowski_transform(zeta):
    """
    Apply the Joukowski mapping:
        z = ζ + 1/ζ
    where ζ is a complex number in the circle plane.
    """
    return zeta + 1.0 / zeta

def generate_circle(center, radius, n_points=500):
    """
    Return complex points on a circle in the ζ-plane.
    ζ = χ + iη
    """
    theta = np.linspace(0, 2*np.pi, n_points, endpoint=True)
    chi = center.real + radius * np.cos(theta)
    eta = center.imag + radius * np.sin(theta)
    return chi + 1j * eta

# --- Parameters for a cambered airfoil ---
# Circle must pass through ζ = 1 (trailing edge at z = 2)
# and enclose ζ = -1 (to keep the profile closed).
chi0 = -0.2          # centre real part (negative → camber)
eta0 = 0.1           # centre imaginary part (non‑zero → camber)
# Radius forced by passing through ζ = 1
R = np.sqrt((1 - chi0)**2 + eta0**2)

# Generate points on the circle in the ζ-plane
zeta_points = generate_circle(complex(chi0, eta0), R)

# Map to the z-plane (airfoil) using Joukowski
z_points = joukowski_transform(zeta_points)

# ---- Plotting ----
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# ============== Left: ζ-plane (circle) ==============
ax1.plot(zeta_points.real, zeta_points.imag, 'b-', linewidth=1.5)

# Mark the critical points ζ = 1 and ζ = -1
ax1.scatter([1, -1], [0, 0], color='red', s=30, zorder=5)

# Mark the center with a large 'X'
ax1.plot(chi0, eta0, 'kx', markersize=10)

# Add a text box with the exact parameters (no radial line)
info_text = f'Center: (χ₀={chi0:.2f}, η₀={eta0:.2f})\nRadius R = {R:.3f}'
ax1.text(chi0, eta0 - 0.3, info_text, ha='center', va='top',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7),
         fontsize=10)

ax1.set_aspect('equal')
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.set_xlabel(r'$\chi = \mathrm{Re}(\zeta)$')
ax1.set_ylabel(r'$\eta = \mathrm{Im}(\zeta)$')
ax1.set_title('Circle in $\zeta$-plane ($\zeta = \chi + i\eta$)')
ax1.text(1, 0.1, r'$\zeta=1$', ha='center')
ax1.text(-1, 0.1, r'$\zeta=-1$', ha='center')

# ============== Right: z-plane (airfoil) ==============
ax2.plot(z_points.real, z_points.imag, 'r-', linewidth=1.5)

# Mark the images of ζ = 1 and ζ = -1 in the z-plane
ax2.scatter([2, -2], [0, 0], color='blue', s=30, zorder=5)

ax2.set_aspect('equal')
ax2.grid(True, linestyle='--', alpha=0.5)
ax2.set_xlabel(r'$x = \mathrm{Re}(z)$')
ax2.set_ylabel(r'$y = \mathrm{Im}(z)$')
ax2.set_title('Airfoil in $z$-plane ($z = \zeta + 1/\zeta$)')
ax2.text(2, 0.1, r'$z=2$', ha='center')
ax2.text(-2, 0.1, r'$z=-2$', ha='center')

plt.tight_layout()
plt.show()
