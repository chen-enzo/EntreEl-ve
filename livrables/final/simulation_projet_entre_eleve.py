import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle


class Star:
    def __init__(self, position, mass, radius, yellow_threshold, blue_threshold):
        self.position = position
        self.mass = mass
        self.initial_mass = mass
        self.initial_radius = radius
        self.radius = radius

        # -------------------------
        # Type initial basé sur la masse
        # -------------------------
        if mass > blue_threshold:
            self.type = "blue_giant"
            base_lifetime = 400  # Vie très courte
        elif mass > yellow_threshold:
            self.type = "yellow_dwarf"
            base_lifetime = 2000
        else:
            self.type = "red_dwarf"
            base_lifetime = 80000  # 2000 * 40

        # Durée de vie inversement proportionnelle à la masse au cube
        self.lifetime = base_lifetime / (mass**3 + 1e-8)
        self.timer = self.lifetime

        # Paramètres pour les phases de géantes
        self.giant_timer = None
        self.giant_lifetime = None

        # Paramètres des résidus
        self.white_dwarf_radius = max(1, int(self.initial_radius))
        self.neutron_star_radius = max(1, int(self.initial_radius))
        self.black_hole_radius = max(1, int(self.initial_radius))

        self.core_fraction = 0.25  # Pour naines blanches
        # Pour supernovae (plus de gaz expulsé)
        self.massive_core_fraction = 0.15

        self.alive = True


def redistribute_envelope(sigma, center, radius, mass):

    nx, ny = sigma.shape
    x0, y0 = center

    shell_inner = radius
    shell_outer = 10 * shell_inner

    cells = []

    for i in range(nx):
        for j in range(ny):
            d = np.sqrt((i - x0)**2 + (j - y0)**2)
            if shell_inner < d <= shell_outer:
                cells.append((i, j))

    if not cells:
        return

    mass_per_cell = mass / len(cells)

    for i, j in cells:
        sigma[i, j] += mass_per_cell


def evolve_star(star, sigma, blue_threshold):
    if not star.alive:
        return

    star.timer -= 1

    # -------------------------
    # Phase Naine Rouge / Jaune / Géante Bleue
    # -------------------------
    if star.type in ["red_dwarf", "yellow_dwarf", "blue_giant"]:
        if star.timer <= 0:
            if star.type == "blue_giant":
                # Transition vers Supergéante Rouge
                star.type = "red_supergiant"
                star.giant_lifetime = np.random.uniform(50, 150)
                star.giant_timer = star.giant_lifetime
                star.timer = star.giant_lifetime

            elif star.type == "yellow_dwarf":
                # Transition vers Géante Rouge
                star.type = "red_giant"
                star.giant_lifetime = np.random.uniform(100, 400)
                star.giant_timer = star.giant_lifetime
                star.timer = star.giant_lifetime

            else:  # Naine rouge -> Naine blanche
                star.type = "white_dwarf"
                star.radius = star.white_dwarf_radius
                star.mass *= star.core_fraction
                star.alive = False

    # -------------------------
    # Phase Géante Rouge (Expansion)
    # -------------------------
    elif star.type == "red_giant":
        if star.giant_timer > 0:
            star.giant_timer -= 1
            growth = 1 - star.giant_timer / star.giant_lifetime
            star.radius = int(star.initial_radius * (1 + 39 * growth))
        else:
            # Fin : Expulsion calme -> Naine Blanche
            core_mass = star.mass * star.core_fraction
            redistribute_envelope(sigma, star.position,
                                  star.radius, star.mass - core_mass)
            star.mass, star.radius, star.type, star.alive = core_mass, star.white_dwarf_radius, "white_dwarf", False

    # -------------------------
    # Phase Supergéante Rouge (Expansion massive)
    # -------------------------
    elif star.type == "red_supergiant":
        if star.giant_timer > 0:
            star.giant_timer -= 1
            growth = 1 - star.giant_timer / star.giant_lifetime
            star.radius = int(star.initial_radius *
                              (1 + 99 * growth))  # Grossit bcp plus
        else:
            # ÉVÉNEMENT SUPERNOVA
            core_mass = star.mass * star.massive_core_fraction
            redistribute_envelope(sigma, star.position,
                                  star.radius, star.mass - core_mass)

            star.mass = core_mass
            star.alive = False

            # Détermination du résidu selon la masse finale
            if star.mass > blue_threshold * 0.2:  # Seuil arbitraire pour trou noir
                star.type = "black_hole"
                star.radius = star.black_hole_radius
            else:
                star.type = "neutron_star"
                star.radius = star.neutron_star_radius


def laplacian(Z):
    return (
        np.roll(Z, 1, 0) +
        np.roll(Z, -1, 0) +
        np.roll(Z, 1, 1) +
        np.roll(Z, -1, 1) -
        4 * Z
    )


def deposit_star_density(sigma, star):
    """
    Actualise la densité interne d'une étoile dans sigma
    en conservant exactement la masse.
    """
    nx, ny = sigma.shape
    x0, y0 = star.position
    r = star.radius

    Y, X = np.ogrid[:nx, :ny]
    mask = (X - y0)**2 + (Y - x0)**2 <= r**2

    n = np.sum(mask)
    if n == 0:
        return

    sigma[mask] = star.mass / n


def star_occupancy_mask(sigma_shape, stars):

    nx, ny = sigma_shape
    occ = np.zeros((nx, ny), dtype=bool)

    Y, X = np.ogrid[:nx, :ny]

    for star in stars:
        x0, y0 = star.position
        r = star.radius*10000

        mask = (X - y0)**2 + (Y - x0)**2 <= r**2
        occ |= mask

    return occ


def remove_star_region(sigma, star):
    # Rend nulle la densité de masse dans une zone précedement au sein d'une étoile mais qui n'y est plus à cause de son rétrécissement'
    nx, ny = sigma.shape
    x0, y0 = star.position
    r = star.radius

    Y, X = np.ogrid[:nx, :ny]
    mask = (X - y0)**2 + (Y - x0)**2 <= r**2

    sigma[mask] = 0.0


def find_connected_regions(mask):
    nx, ny = mask.shape
    visited = np.zeros_like(mask, dtype=bool)
    regions = []

    for i in range(nx):
        for j in range(ny):

            if mask[i, j] and not visited[i, j]:

                stack = [(i, j)]
                region = []
                visited[i, j] = True

                while stack:
                    x, y = stack.pop()
                    region.append((x, y))

                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        xn, yn = x+dx, y+dy
                        if 0 <= xn < nx and 0 <= yn < ny:
                            if mask[xn, yn] and not visited[xn, yn]:
                                visited[xn, yn] = True
                                stack.append((xn, yn))

                regions.append(region)

    return regions


def evolve_mass_distribution(
        sigma_init,
        stars,
        steps=1,
        dt=0.05,
        D=0.1,
        G=0.5,
        density_threshold=5.0,
        freeze_radius=4,
        yellow_threshold=50.0,
        blue_threshold=150.0):

    sigma = sigma_init.copy()
    nx, ny = sigma.shape

    for step in range(steps):

        for star in stars:
            remove_star_region(sigma, star)

        # Evolution de la densité de masse

        diffusion = D * laplacian(sigma)  # 2ème loi de Fick
        # Pour la gravité on part de l'eq de continuité et on approxime la vitesse comme proportionelle à la gravité et le flux par -G*sigma
        phi = -G * sigma
        gradx = (np.roll(phi, -1, 0) - np.roll(phi, 1, 0)) * 0.5
        grady = (np.roll(phi, -1, 1) - np.roll(phi, 1, 1)) * 0.5
        flux_x = sigma * gradx
        flux_y = sigma * grady
        div_flux = (np.roll(flux_x, -1, 0) - np.roll(flux_x, 1, 0)) * 0.5 + \
                   (np.roll(flux_y, -1, 1) - np.roll(flux_y, 1, 1)) * 0.5
        gravity = -div_flux

        sigma = sigma + dt * (diffusion + gravity)
        sigma = np.maximum(sigma, 0.0)

        # Formation des étoiles

        occupied = star_occupancy_mask(sigma.shape, stars)

        mask = (sigma > density_threshold) & (~occupied)

        regions = find_connected_regions(mask)

        for region in regions:

            if len(region) < 10:
                continue

            mass = sum(sigma[i, j] for i, j in region)

            x_cm = int(sum(i * sigma[i, j] for i, j in region) / mass)
            y_cm = int(sum(j * sigma[i, j] for i, j in region) / mass)

            radius = int(np.sqrt(len(region) / np.pi))

            lifetime = 100 + 50*np.random.rand()

            new_star = Star((x_cm, y_cm), mass, radius,
                            yellow_threshold, blue_threshold)

            stars.append(new_star)

        # Réorganiser la densité interne
            deposit_star_density(sigma, new_star)

        # Evolution des étoiles

        for star in stars:
            evolve_star(star, sigma, blue_threshold)
        for star in stars:
            if star.alive:
                deposit_star_density(sigma, star)

    return sigma, stars


class Simulation:
    def __init__(self, sigma_init, step):
        self.sigma = sigma_init.copy()
        self.nx, self.ny = self.sigma.shape
        self.stars = []

        self.step_count = 0
        self.step = step

        # Pour l'affichage dans une fenêtre séparée
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.im = self.ax.imshow(
            self.sigma, cmap='bone', origin='lower', animated=True, vmin=0)
        plt.colorbar(self.im, ax=self.ax, label='Densité de masse')
        # self.ax.set_title(f'Simulation stellaire \n Age {self.step_count}')
        self.title = self.ax.set_title(
            "", color="black", fontname="monospace", fontsize=10, pad=10)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')

        self.star_circles = {}
        self.colors = {
            # 'brown_dwarf': (0.5, 0.25, 0, 0.6),
            'red_dwarf': (1, 0, 0, 0.5),  # bouge pas
            'yellow_dwarf': (1, 1, 0, 0.5),  # bouge pas
            'massive_star': (1, 0.5, 0, 0.5),
            'very_massive_star': (1, 0.5, 0, 0.5),
            'red_giant': (0.8, 0, 0, 0.6),
            'white_dwarf': (1, 1, 1, 0.7),
            'neutron_star': (0, 1, 0, 0.7),
            'black_hole': (0, 0, 1, 0.8),
            'blue_giant': (0.4, 0.6, 1, 0.6),
            'red_supergiant': (1, 0.2, 0.2, 0.7)
        }

    def update(self, frame):
        self.sigma, self.stars = evolve_mass_distribution(
            self.sigma, self.stars, steps=self.step)
        self.step_count += self.step
        self.title.set_text(f'Simulation stellaire \n Age {self.step_count}')

        # Mise à jour carte de densité
        self.im.set_array(self.sigma)

        # Supprimer les cercles d'étoiles qui n'existent plus
        current_ids = set(id(star) for star in self.stars)
        for sid in list(self.star_circles.keys()):
            if sid not in current_ids:
                self.star_circles[sid].remove()
                del self.star_circles[sid]

        # Mise à jour / création des cercles
        for star in self.stars:
            sid = id(star)

            # on ignore seulement les étoiles mortes
            # if not star.alive:
            #    continue

            # selection couleur
            color = self.colors.get(star.type, (0.5, 0.5, 0.5, 0.5))
            # création du cercle si nouvelle étoile
            if sid not in self.star_circles:
                circ = Circle(
                    (star.position[1], star.position[0]),
                    star.radius,
                    color=color,
                    fill=True,
                    linewidth=0
                )
                self.ax.add_patch(circ)
                self.star_circles[sid] = circ

            # sinon mise à jour du disque
            else:
                circ = self.star_circles[sid]
                circ.center = (star.position[1], star.position[0])
                circ.radius = star.radius
                circ.set_color(color)
                circ.set_visible(True)

        return [self.im] + list(self.star_circles.values())

    def animate(self, frames=500, interval=50):
        ani = FuncAnimation(
            self.fig, self.update, frames=frames,
            interval=interval, blit=True, repeat=False
        )
        plt.show()
        return ani


if __name__ == "__main__":

    # Taille de la grille
    nx, ny = 500, 500

    # Création d'une nébuleuse initiale
    sigma = np.random.rand(nx, ny)

    # Ajout de zones plus denses pour former des étoiles
    for _ in range(1):
        x = np.random.randint(20, nx-20)
        y = np.random.randint(20, ny-20)

        for i in range(-24, 25):
            for j in range(-24, 25):
                if 0 <= x+i < nx and 0 <= y+j < ny:
                    # parametre a modifier pour le test (la masse)
                    sigma[x+i, y+j] += 5*np.exp(-(i*i+j*j)/20) + 1

    # Lancer la simulation
    sim = Simulation(sigma, 1)

    sim.animate(frames=5000, interval=40)
