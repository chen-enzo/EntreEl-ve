import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from matplotlib.widgets import Slider, Button

# Constante Globale : 1 pas = 1 million d'années
TIME_PER_STEP = 1e6
RDWARF_RFACTOR = 2
YDWARF_RFACTOR = 3
BGIANT_RFACTOR = 4
RGIANT_RFACTOR = 0.4
SRGIANT_RFACTOR = 0.1

MASS_FACTOR = 20
TRHESHOLD_FACTOR = 20
DENSITY_THRESHOLD = 0.05 * TRHESHOLD_FACTOR
YTHRESHOLD = 0.8 * TRHESHOLD_FACTOR
BTHRESHOLD = 10 * TRHESHOLD_FACTOR

DISPERTION_COEF = 2


class Star:
    def __init__(self, position, mass, radius, yellow_threshold, blue_threshold):
        self.position = position
        self.mass = mass
        self.initial_mass = mass

        if mass > blue_threshold:
            self.type = "blue_giant"
            base_lifetime = 1e9
            self.initial_radius = radius * BGIANT_RFACTOR
            self.radius = radius * BGIANT_RFACTOR
        elif mass > yellow_threshold:
            self.type = "yellow_dwarf"
            base_lifetime = 1e9
            self.initial_radius = radius * YDWARF_RFACTOR
            self.radius = radius * YDWARF_RFACTOR
        else:
            self.type = "red_dwarf"
            base_lifetime = 1e10
            self.initial_radius = radius * RDWARF_RFACTOR
            self.radius = radius * RDWARF_RFACTOR

        self.lifetime = base_lifetime / (mass**3 + 1e-8)
        self.timer = self.lifetime

        self.giant_timer = None
        self.giant_lifetime = None

        self.white_dwarf_radius = max(1, int(self.initial_radius))
        self.neutron_star_radius = max(1, int(self.initial_radius))
        self.black_hole_radius = max(1, int(self.initial_radius))

        self.core_fraction = 0.25
        self.massive_core_fraction = 0.15

        self.alive = True


def redistribute_envelope(sigma, center, radius, mass):
    """ Redistribue la masse éjectée (supernova/géante rouge) largement pour éviter l'emballement """
    nx, ny = sigma.shape
    x0, y0 = center
    shell_inner = radius + 2
    shell_outer = shell_inner + 15

    Y, X = np.ogrid[:nx, :ny]
    dist2 = (X - y0)**2 + (Y - x0)**2
    mask = (dist2 > shell_inner**2) & (dist2 <= shell_outer**2)

    n = np.sum(mask)
    if n > 0:
        sigma[mask] += mass / n
    else:
        sigma += mass / (nx * ny)


def evolve_star_and_get_shed_mass(star, blue_threshold):
    """ Fait vieillir l'étoile et renvoie strictement la masse qu'elle perd pour la conserver """
    shed_mass = 0.0
    if not star.alive:
        return shed_mass

    star.timer -= 1

    if star.type in ["red_dwarf", "yellow_dwarf", "blue_giant"]:
        if star.timer <= 0:
            if star.type == "blue_giant":
                star.type = "red_supergiant"
                star.giant_lifetime = np.random.uniform(50, 150)
                star.giant_timer = star.giant_lifetime
                star.timer = star.giant_lifetime
            elif star.type == "yellow_dwarf":
                star.type = "red_giant"
                star.giant_lifetime = np.random.uniform(100, 400)
                star.giant_timer = star.giant_lifetime
                star.timer = star.giant_lifetime
            else:  # Mort d'une naine rouge
                star.type = "white_dwarf"
                star.radius = star.white_dwarf_radius
                core_mass = star.mass * star.core_fraction
                shed_mass = star.mass - core_mass
                star.mass = core_mass
                star.alive = False

    elif star.type == "red_giant":
        if star.giant_timer > 0:
            star.giant_timer -= 1
            growth = 1 - star.giant_timer / star.giant_lifetime
            star.radius = max(int(star.initial_radius * (1 + 39 * growth))
                              * RGIANT_RFACTOR, star.initial_radius)
        else:
            core_mass = star.mass * star.core_fraction
            shed_mass = star.mass - core_mass
            star.mass, star.radius, star.type, star.alive = core_mass, star.white_dwarf_radius, "white_dwarf", False

    elif star.type == "red_supergiant":
        if star.giant_timer > 0:
            star.giant_timer -= 1
            growth = 1 - star.giant_timer / star.giant_lifetime
            star.radius = max(int(star.initial_radius * (1 + 99 * growth))
                              * SRGIANT_RFACTOR, star.initial_radius)
        else:
            core_mass = star.mass * star.massive_core_fraction
            shed_mass = star.mass - core_mass
            star.mass = core_mass
            star.alive = False

            if star.mass > blue_threshold * 0.2:
                star.type = "black_hole"
                star.radius = star.black_hole_radius
            else:
                star.type = "neutron_star"
                star.radius = star.neutron_star_radius

    return shed_mass


def laplacian(Z):
    return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) + np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4 * Z)


def compute_gravitational_potential(sigma, G=0.5):
    nx, ny = sigma.shape
    sigma_hat = np.fft.fft2(sigma)
    kx = np.fft.fftfreq(nx).reshape(nx, 1) * 2 * np.pi
    ky = np.fft.fftfreq(ny).reshape(1, ny) * 2 * np.pi
    k2 = kx**2 + ky**2
    k2[0, 0] = 1.0
    phi_hat = -4 * np.pi * G * sigma_hat / k2
    phi_hat[0, 0] = 0.0
    return np.real(np.fft.ifft2(phi_hat))


def star_occupancy_mask(sigma_shape, stars):
    nx, ny = sigma_shape
    occ = np.zeros((nx, ny), dtype=bool)
    Y, X = np.ogrid[:nx, :ny]

    for star in stars:
        if star.type in ["yellow_dwarf", "blue_giant"]:
            r = max(1, star.radius * 7)
        elif star.type in ["red_giant", "red_supergiant"]:
            r = max(1, star.radius)
        else:
            r = max(1, star.radius * 2)

        mask = (X - star.position[1])**2 + (Y - star.position[0])**2 <= r**2
        occ |= mask
    return occ


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
                        xn, yn = x + dx, y + dy
                        if 0 <= xn < nx and 0 <= yn < ny:
                            if mask[xn, yn] and not visited[xn, yn]:
                                visited[xn, yn] = True
                                stack.append((xn, yn))

                regions.append(region)
    return regions


def evolve_mass_distribution(sigma_gas, stars, steps=1, dt=0.05, D=DISPERTION_COEF, G=0.5, density_threshold=DENSITY_THRESHOLD, yellow_threshold=YTHRESHOLD, blue_threshold=BTHRESHOLD):
    nx, ny = sigma_gas.shape

    # Bilan strict de la masse pour éviter toute création accidentelle
    target_mass = np.sum(sigma_gas)

    for _ in range(steps):
        # 1. Gravité : Seul le gaz attire le gaz. Empêche les singularités autour des étoiles.
        phi = compute_gravitational_potential(sigma_gas, G)

        gradx = (np.roll(phi, -1, 0) - np.roll(phi, 1, 0)) * 0.5
        grady = (np.roll(phi, -1, 1) - np.roll(phi, 1, 1)) * 0.5

        # Limiteur pour éviter l'explosion numérique
        max_grad = 5.0
        gradx = np.clip(gradx, -max_grad, max_grad)
        grady = np.clip(grady, -max_grad, max_grad)

        flux_x = sigma_gas * gradx
        flux_y = sigma_gas * grady

        div_flux = (np.roll(flux_x, -1, 0) - np.roll(flux_x, 1, 0)) * 0.5 + \
                   (np.roll(flux_y, -1, 1) - np.roll(flux_y, 1, 1)) * 0.5

        gravity = div_flux
        diffusion = D * laplacian(sigma_gas)

        sigma_gas = sigma_gas + dt * (diffusion + gravity)

        # 2. Correction stricte pour préserver la masse
        sigma_gas = np.maximum(sigma_gas, 0.0)
        sigma_gas = np.nan_to_num(sigma_gas, nan=0.0, posinf=0.0, neginf=0.0)

        current_mass = np.sum(sigma_gas)
        if current_mass > 0 and target_mass > 0:
            sigma_gas *= (target_mass / current_mass)
        elif target_mass == 0:
            sigma_gas[:] = 0.0

        # 3. Formation stellaire
        occupied = star_occupancy_mask(sigma_gas.shape, stars)
        mask_formation = (sigma_gas > density_threshold) & (~occupied)
        regions = find_connected_regions(mask_formation)

        for region in regions:
            if len(region) < 10:
                continue

            mass = sum(sigma_gas[i, j] for i, j in region)
            if mass <= 0:
                continue

            sum_i = sum(i * sigma_gas[i, j] for i, j in region)
            sum_j = sum(j * sigma_gas[i, j] for i, j in region)

            x_cm = int(sum_i / mass)
            y_cm = int(sum_j / mass)
            radius = max(1, int(np.sqrt(len(region) / np.pi)))

            new_star = Star((x_cm, y_cm), mass, radius,
                            yellow_threshold, blue_threshold)
            stars.append(new_star)

            # L'étoile "consomme" le gaz
            for i, j in region:
                sigma_gas[i, j] = 0.0
            target_mass -= mass

        # 4. Évolution stellaire (Supernovas, naines blanches...)
        for star in stars:
            shed_mass = evolve_star_and_get_shed_mass(star, blue_threshold)
            if shed_mass > 0:
                redistribute_envelope(
                    sigma_gas, star.position, star.radius, shed_mass)
                target_mass += shed_mass  # On rajoute la masse rejetée au bilan du gaz

    # 5. Préparation de l'image (optionnel : superpose visuellement les étoiles sans altérer la physique)
    sigma_display = sigma_gas.copy()
    for star in stars:
        x0, y0 = star.position
        r = max(1, star.radius)
        Y, X = np.ogrid[:nx, :ny]
        mask = (X - y0)**2 + (Y - x0)**2 <= r**2
        n = np.sum(mask)
        if n > 0:
            sigma_display[mask] += np.clip(star.mass / n, 0, 15)

    return sigma_gas, sigma_display, stars


class Simulation:
    def __init__(self, sigma_init, step):
        self.sigma_init = sigma_init.copy()
        self.sigma = sigma_init.copy()  # Gaz uniquement
        self.sigma_display = sigma_init.copy()
        self.nx, self.ny = self.sigma.shape
        self.stars = []

        self.step_count = 0
        self.step = step
        self.nbstars = 0
        self.totalmass = np.sum(self.sigma)

        # Image

        self.fig, self.ax = plt.subplots(figsize=(16, 10), facecolor="black")
        plt.subplots_adjust(bottom=0.1, right=0.6, left=0.0)

        self.ax.tick_params(axis='both', which='both',
                            length=0, labelbottom=False, labelleft=False)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        for spine in self.ax.spines.values():
            spine.set_color('darkgray')
            spine.set_linewidth(2)

        self.im = self.ax.imshow(
            self.sigma_display, cmap='bone', origin='lower', animated=True, vmin=0, vmax=1)

        # Titre
        self.title = self.ax.set_title(
            "", color="white", fontname="monospace", fontsize=10, pad=10)
        self.title.set_animated(True)
        self.title.set_bbox(
            dict(facecolor='black', alpha=0.8, edgecolor='none'))

        # Sliders
        ax_slider_mass = plt.axes([0.12, 0.065, 0.4, 0.01])
        self.slider_mass = Slider(ax=ax_slider_mass, label='Masse ajoutée',
                                  valmin=0.1, valmax=20.0, valinit=5.0, valstep=0.1)
        self.slider_mass.label.set_color('white')
        self.slider_mass.valtext.set_color('white')
        self.slider_mass.on_changed(
            lambda val: setattr(self, 'click_amount', val))
        self.click_amount = self.slider_mass.val

        ax_slider_radius = plt.axes([0.12, 0.04, 0.4, 0.01])
        self.slider_radius = Slider(
            ax=ax_slider_radius, label='Rayon (pixels)', valmin=1, valmax=30, valinit=10, valstep=1)
        self.slider_radius.label.set_color('white')
        self.slider_radius.valtext.set_color('white')
        self.slider_radius.on_changed(
            lambda val: setattr(self, 'click_radius', int(val)))
        self.click_radius = int(self.slider_radius.val)

        # Boutons
        ax_button_pause = plt.axes([0.675, 0.03, 0.1, 0.04])
        self.button_pause = Button(
            ax_button_pause, 'Pause', hovercolor='lightblue')
        self.button_pause.on_clicked(self.toggle_pause)
        self.paused = False

        ax_button_reset = plt.axes([0.825, 0.03, 0.1, 0.04])
        self.button_reset = Button(
            ax_button_reset, 'Reset', hovercolor='lightblue')
        self.button_reset.on_clicked(self.reset_simulation)

        # Affichage
        self.star_circles = {}
        self.colors = {
            'red_dwarf': (1.0, 0.5, 0.5), 'yellow_dwarf': (1.0, 1.0, 0.6),
            'blue_giant': (0.5, 0.8, 1.0, 0.9), 'red_giant': (0.8, 0, 0, 0.6),
            'red_supergiant': (1, 0.2, 0.2, 0.7), 'white_dwarf': (1.0, 1.0, 1.0, 0.9),
            'neutron_star': (0.7, 0.9, 1.0, 0.7), 'black_hole': (0, 0, 0, 1)
        }
        self.names = {
            'red_dwarf': "Naine rouge", 'yellow_dwarf': "Naine jaune",
            'blue_giant': "Géante bleu", 'red_giant': "Géante rouge",
            'red_supergiant': "Super Géante rouge", 'white_dwarf': "Naine Blanche",
            'neutron_star': "Étoile à Neutrons", 'black_hole': "Trou noir"
        }

        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('motion_notify_event', self.info_hover)

        # Infobulle
        self.tooltip = self.ax.annotate("", xy=(0, 0), xytext=(10, 10), textcoords='offset points',
                                        bbox=dict(boxstyle='round,pad=0.5',
                                                  fc='lightgray', alpha=0.5))
        self.tooltip.set_visible(False)
        self.tooltip.set_animated(True)
        self.current_star = None

        # infotable
        self.ax_table = self.fig.add_axes([0.6, 0.1, 0.35, 0.75])
        # self.ax_table.axis('off')
        self.ax_table.set_facecolor('white')
        self.ax_table.set_visible(True)
        self.table = None  # sera mis à jour dans update
        self.checklist = {}

    def toggle_pause(self, event):
        self.paused = not self.paused
        self.button_pause.label.set_text('Start' if self.paused else 'Pause')

    def reset_simulation(self, event):
        self.sigma = self.sigma_init.copy()
        self.sigma_display = self.sigma_init.copy()
        self.stars = []
        self.step_count = 0
        self.nbstars = 0
        self.im.set_array(self.sigma_display)
        for circ in self.star_circles.values():
            circ.remove()
        self.star_circles.clear()
        self.tooltip.set_visible(False)
        self.current_star = None
        self.fig.canvas.draw_idle()

    def on_click(self, event):
        if event.inaxes != self.ax:
            return
        i, j = int(event.ydata), int(event.xdata)
        r = self.click_radius
        for di in range(-r, r + 1):
            for dj in range(-r, r + 1):
                ni, nj = i + di, j + dj
                if 0 <= ni < self.nx and 0 <= nj < self.ny:
                    dist = np.sqrt(di*di + dj*dj)
                    if dist <= r:
                        factor = np.exp(-dist**2 / (2 * (r/3)**2))
                        self.sigma[ni, nj] += self.click_amount * factor

        self.im.set_array(self.sigma)
        self.fig.canvas.draw_idle()

    def info_hover(self, event):
        if event.inaxes != self.ax:
            if self.current_star:
                self.tooltip.set_visible(False)
                self.current_star = None
            return

        min_dist, selected_star = float('inf'), None
        for star in self.stars:
            dist = np.hypot(
                event.xdata - star.position[1], event.ydata - star.position[0])
            if dist < star.radius + 5 and dist < min_dist:
                min_dist, selected_star = dist, star

        if selected_star:
            self.current_star = selected_star
            self.tooltip.set_visible(True)
        elif self.current_star:
            self.tooltip.set_visible(False)
            self.current_star = None

    def update(self, frame):
        if not self.paused:
            self.sigma, self.sigma_display, self.stars = evolve_mass_distribution(
                self.sigma, self.stars, steps=self.step)
            self.step_count += self.step
            self.nbstars = len(self.stars)
            self.totalmass = np.sum(self.sigma) + \
                sum(s.mass for s in self.stars)

        age_myr = self.step_count * TIME_PER_STEP / 1e6
        self.title.set_text(
            f"Simulation stellaire\nÂge : {age_myr:.2f} millions d'années | {self.nbstars} étoiles | masse totale = {self.totalmass:.1f}")
        self.im.set_array(self.sigma_display)

        if self.current_star and self.current_star in self.stars:
            rem = self.current_star.timer * TIME_PER_STEP / 1e6
            timetext = "« infini »" if self.current_star.type in [
                "black_hole", "white_dwarf", "neutron_star"] else f"{rem:.1f} M d'années"
            self.tooltip.set_text((f"Type: {self.names[self.current_star.type]}\n"
                                   f"Masse: {self.current_star.mass/MASS_FACTOR:.2f} M☉\n"
                                   f"Rayon: {self.current_star.radius:1f} px\n"
                                   f"Temps restant: {timetext}"))
        else:
            self.tooltip.set_visible(False)
            self.current_star = None

        current_ids = set(id(s) for s in self.stars)
        for sid in list(self.star_circles.keys()):
            if sid not in current_ids:
                self.star_circles[sid].remove()
                del self.star_circles[sid]

        for star in self.stars:
            sid = id(star)
            r = max(star.radius, 3) if star.type == "black_hole" else star.radius
            if sid not in self.star_circles:
                circ = Circle((star.position[1], star.position[0]), r,
                              facecolor='black' if star.type == "black_hole" else self.colors.get(
                                  star.type, 'gray'),
                              fill=True, linewidth=1 if star.type == "black_hole" else 0,
                              edgecolor='white' if star.type == "black_hole" else 'none')
                self.ax.add_patch(circ)
                self.star_circles[sid] = circ
            else:
                circ = self.star_circles[sid]
                circ.center = (star.position[1], star.position[0])
                circ.radius = r
                if star.type == "black_hole":
                    circ.set(facecolor='black', edgecolor='white', linewidth=1)
                else:
                    circ.set(color=self.colors.get(star.type, 'gray'),
                             edgecolor='none', linewidth=0)

        return [self.im, self.title, self.tooltip] + list(self.star_circles.values())

    def animate(self, frames=500, interval=50):
        ani = FuncAnimation(self.fig, self.update, frames=frames,
                            interval=interval, blit=True, repeat=False)
        plt.show()
        return ani


if __name__ == "__main__":
    nx, ny = 500, 500
    sigma = 0.1 * np.random.rand(nx, ny)
    sim = Simulation(sigma, step=1)
    sim.animate(frames=None, interval=40)
