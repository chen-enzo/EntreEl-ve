import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from matplotlib.widgets import Slider, Button

# Constante Globale : 1 pas = 1 million d'années
TIME_PER_STEP = 1e6  # années par pas
YDWARF_RFACTOR = 2
BGIANT_RFACTOR = 4
RGIANT_RFACTOR = 0.4
SRGIANT_RFACTOR = 0.1

YTHRESHOLD = 75
BTHRESHOLD = 250


class Star:
    def __init__(self, position, mass, radius, yellow_threshold, blue_threshold):
        self.position = position
        self.mass = mass
        self.initial_mass = mass

        # Type initial basé sur la masse
        if mass > blue_threshold:
            self.type = "blue_giant"
            base_lifetime = 1e10  # pour qu'une étoile de masse 15 vive ~100 pas
            self.initial_radius = radius * BGIANT_RFACTOR
            self.radius = radius * BGIANT_RFACTOR
        elif mass > yellow_threshold:
            self.type = "yellow_dwarf"
            base_lifetime = 1e9   # pour qu'une étoile de masse 1 vive ~700 pas
            self.initial_radius = radius * YDWARF_RFACTOR
            self.radius = radius * YDWARF_RFACTOR
        else:
            self.type = "red_dwarf"
            base_lifetime = 1e10   # supposée très longue
            self.initial_radius = radius
            self.radius = radius

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

        self.core_fraction = 0.25          # Pour naines blanches
        self.massive_core_fraction = 0.15  # Pour supernovae

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

    # Phases Naine Rouge / Jaune / Géante Bleue
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

            else:  # Naine rouge -> Naine blanche
                star.type = "white_dwarf"
                star.radius = star.white_dwarf_radius
                star.mass *= star.core_fraction
                star.alive = False

    # Phase Géante Rouge (expansion modérée)
    elif star.type == "red_giant":
        if star.giant_timer > 0:
            star.giant_timer -= 1
            growth = 1 - star.giant_timer / star.giant_lifetime
            star.radius = max(int(star.initial_radius *
                              (1 + 39 * growth)) * RGIANT_RFACTOR, star.initial_radius)
        else:
            # Fin : expulsion calme -> Naine Blanche
            core_mass = star.mass * star.core_fraction
            redistribute_envelope(sigma, star.position,
                                  star.radius, star.mass - core_mass)
            star.mass, star.radius, star.type, star.alive = core_mass, star.white_dwarf_radius, "white_dwarf", False

    # Phase Supergéante Rouge (expansion massive)
    elif star.type == "red_supergiant":
        if star.giant_timer > 0:
            star.giant_timer -= 1
            growth = 1 - star.giant_timer / star.giant_lifetime
            star.radius = max(int(star.initial_radius *
                              (1 + 99 * growth)) * SRGIANT_RFACTOR, star.initial_radius)
        else:
            # ÉVÉNEMENT SUPERNOVA
            core_mass = star.mass * star.massive_core_fraction
            redistribute_envelope(sigma, star.position,
                                  star.radius, star.mass - core_mass)

            star.mass = core_mass
            star.alive = False

            # Détermination du résidu selon la masse finale
            if star.mass > blue_threshold * 0.2:
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

        if star.type in ["yellow_dwarf", "blue_giant"]:
            r = star.radius * 10
        else:
            r = star.radius * 3

        mask = (X - y0)**2 + (Y - x0)**2 <= r**2
        occ |= mask

    return occ


def remove_star_region(sigma, star):
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
                        xn, yn = x + dx, y + dy
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
        yellow_threshold=YTHRESHOLD,
        blue_threshold=BTHRESHOLD):

    sigma = sigma_init.copy()
    nx, ny = sigma.shape

    for _ in range(steps):
        for star in stars:
            remove_star_region(sigma, star)

        diffusion = D * laplacian(sigma)
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
        sigma = np.nan_to_num(sigma, nan=0.0, posinf=0.0, neginf=0.0)

        occupied = star_occupancy_mask(sigma.shape, stars)
        mask = (sigma > density_threshold) & (~occupied)
        regions = find_connected_regions(mask)

        for region in regions:
            if len(region) < 10:
                continue

            mass = sum(sigma[i, j] for i, j in region)
            if np.isnan(mass) or mass <= 0:
                continue
            sum_i = sum(i * sigma[i, j] for i, j in region)
            sum_j = sum(j * sigma[i, j] for i, j in region)
            if np.isnan(sum_i) or np.isnan(sum_j):
                continue

            x_cm = int(sum_i / mass)
            y_cm = int(sum_j / mass)
            radius = int(np.sqrt(len(region) / np.pi))

            new_star = Star((x_cm, y_cm), mass, radius,
                            yellow_threshold, blue_threshold)
            stars.append(new_star)
            deposit_star_density(sigma, new_star)

        for star in stars:
            evolve_star(star, sigma, blue_threshold)
        for star in stars:
            if star.alive:
                deposit_star_density(sigma, star)

    return sigma, stars


class Simulation:
    def __init__(self, sigma_init, step):
        self.sigma_init = sigma_init.copy()
        self.sigma = sigma_init.copy()
        self.nx, self.ny = self.sigma.shape
        self.stars = []
        self.totalmass = np.sum(sigma_init)

        self.step_count = 0
        self.step = step
        self.nbstars = 0

        # Configuration de la figure
        self.fig, self.ax = plt.subplots(
            figsize=(12, 10), facecolor="black")
        plt.subplots_adjust(bottom=0.2)
        # Encadrement
        self.ax.tick_params(axis='both', which='both',
                            length=0, labelbottom=False, labelleft=False)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        for spine in self.ax.spines.values():
            spine.set_color('darkgray')
            spine.set_linewidth(2)

        # Nebuleuse
        self.im = self.ax.imshow(
            self.sigma, cmap='bone', origin='lower', animated=True, vmin=0, vmax=20)
        # plt.colorbar(self.im, ax=self.ax, label='Densité de masse')

        self.title = self.ax.set_title(
            "", color="white", fontname="monospace", fontsize=10, pad=10)
        self.title.set_animated(True)
        self.title.set_bbox(
            dict(facecolor='black', alpha=0.8, edgecolor='none'))

        # Sliders
        ax_slider_mass = plt.axes([0.3, 0.15, 0.4, 0.01])
        self.slider_mass = Slider(
            ax=ax_slider_mass, label='Masse ajoutée',
            valmin=0.1, valmax=20.0, valinit=5.0, valstep=0.1)
        self.slider_mass.label.set_color('white')
        self.click_amount = self.slider_mass.val
        self.slider_mass.on_changed(self.update_click_amount)

        ax_slider_radius = plt.axes([0.3, 0.10, 0.4, 0.01])
        self.slider_radius = Slider(
            ax=ax_slider_radius, label='Rayon (pixels)',
            valmin=1, valmax=30, valinit=10, valstep=1)
        self.click_radius = self.slider_radius.val
        self.slider_radius.label.set_color('white')
        self.slider_radius.on_changed(self.update_click_radius)

        # Boutons
        ax_button_pause = plt.axes([0.33, 0.03, 0.1, 0.04])
        self.button_pause = Button(
            ax_button_pause, 'Pause', hovercolor='lightblue')
        self.button_pause.on_clicked(self.toggle_pause)
        self.paused = False

        ax_button_reset = plt.axes([0.5, 0.03, 0.1, 0.04])
        self.button_reset = Button(
            ax_button_reset, 'Reset', hovercolor='lightblue')
        self.button_reset.on_clicked(self.reset_simulation)

        self.star_circles = {}
        self.colors = {
            'red_dwarf': (1.0, 0.5, 0.5),
            'yellow_dwarf': (1.0, 1.0, 0.6),
            'blue_giant': (0.5, 0.8, 1.0, 0.9),
            'red_giant': (0.8, 0, 0, 0.6),
            'red_supergiant': (1, 0.2, 0.2, 0.7),
            'white_dwarf': (1.0, 1.0, 1.0, 0.9),
            'neutron_star': (0.7, 0.9, 1.0, 0.7),
            'black_hole': (0, 0, 0, 1)


        }
        self.names = {
            'red_dwarf': "Naine rouge",
            'yellow_dwarf': "Naine jaune",
            'blue_giant': "Géante bleu",
            'red_giant': "Géante rouge ",
            'red_supergiant': "Super Géante rouge",
            'white_dwarf': "Naine Blanche",
            'neutron_star': "Etoile à Neutron",
            'black_hole': "Trou noir"


        }

        # Connexions
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('motion_notify_event', self.info_hover)

        # Infobulle
        self.tooltip = self.ax.annotate(
            "", xy=(0, 0), xytext=(10, 10), textcoords='offset points',
            bbox=dict(boxstyle='round,pad=0.5', fc='lightgray', alpha=0.5),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0')
        )
        self.tooltip.set_visible(False)
        self.tooltip.set_animated(True)   # crucial pour blit
        self.current_star = None

    def update_click_amount(self, val):
        self.click_amount = val

    def update_click_radius(self, val):
        self.click_radius = int(val)

    def toggle_pause(self, event):
        self.paused = not self.paused
        self.button_pause.label.set_text('Start' if self.paused else 'Pause')

    def reset_simulation(self, event):
        self.sigma = self.sigma_init.copy()
        self.stars = []
        self.step_count = 0
        self.nbstars = 0
        self.im.set_array(self.sigma)
        for sid in list(self.star_circles.keys()):
            self.star_circles[sid].remove()
            del self.star_circles[sid]
        self.title.set_text(
            f"Simulation stellaire\nÂge : 0.00 millions d'années | 0 étoiles")
        self.tooltip.set_visible(False)
        self.current_star = None
        self.fig.canvas.draw_idle()

    def on_click(self, event):
        if event.inaxes != self.ax:
            return
        i = int(event.ydata)
        j = int(event.xdata)
        if i < 0 or i >= self.nx or j < 0 or j >= self.ny:
            return

        rayon = self.click_radius
        amount = self.click_amount

        for di in range(-rayon, rayon + 1):
            for dj in range(-rayon, rayon + 1):
                ni = i + di
                nj = j + dj
                if 0 <= ni < self.nx and 0 <= nj < self.ny:
                    dist = np.sqrt(di*di + dj*dj)
                    if dist <= rayon:
                        # à modifier (masse trop concentrée au centre)
                        factor = np.exp(-dist**2 / (2 * (rayon/3)**2))
                        self.sigma[ni, nj] += amount * factor

        self.im.set_array(self.sigma)
        self.fig.canvas.draw_idle()

    def info_hover(self, event):
        # si aucune etoile est selectionnée
        if event.inaxes != self.ax:
            if self.current_star is not None:
                self.tooltip.set_visible(False)
                self.current_star = None
            return

        # selection de l'etoile la plus proche dans un rayon max
        x, y = event.xdata, event.ydata
        min_dist = float('inf')
        selected_star = None
        for star in self.stars:
            sx, sy = star.position[1], star.position[0]
            dist = np.hypot(x - sx, y - sy)
            if dist < star.radius + 5 and dist < min_dist:
                min_dist = dist
                selected_star = star

        # affichage
        if selected_star is not None:
            self.current_star = selected_star
            self.tooltip.set_visible(True)
        elif self.current_star is not None:
            self.tooltip.set_visible(False)
            self.current_star = None

    def update(self, frame):
        if not self.paused:  # gestion pause
            self.sigma, self.stars = evolve_mass_distribution(
                self.sigma, self.stars, steps=self.step)
            self.step_count += self.step
            self.nbstars = len(self.stars)
            self.totalmass = np.sum(self.sigma)

        # Maj titre
        age_myr = self.step_count * TIME_PER_STEP / 1e6
        self.title.set_text(
            f"Simulation stellaire\nÂge : {age_myr:.2f} millions d'années | {self.nbstars} étoiles | masse totale = {self.totalmass:.1f}")

        self.im.set_array(self.sigma)

        # Maj infobulle
        if self.current_star is not None:
            if self.current_star in self.stars:
                remaining_myr = self.current_star.timer * TIME_PER_STEP / 1e6
                if self.current_star.type in ["black_hole", "white_dwarf", "neutron_star"]:
                    timetext = "« infini »"
                else:
                    timetext = f"{remaining_myr:.1f} millions d'années"
                text = (f"Type: {self.names[self.current_star.type]}\n"
                        f"Masse: {self.current_star.mass:.2f} M☉\n"
                        f"Rayon: {self.current_star.radius:.1f} px\n"
                        f"Temps restant: {timetext}")
                self.tooltip.set_text(text)
                self.tooltip.set_visible(True)
            else:
                self.tooltip.set_visible(False)
                self.current_star = None

        current_ids = set(id(star) for star in self.stars)
        for sid in list(self.star_circles.keys()):
            if sid not in current_ids:
                self.star_circles[sid].remove()
                del self.star_circles[sid]

        for star in self.stars:
            sid = id(star)

            if sid not in self.star_circles:
                if star.type == "black_hole":
                    circ = Circle(
                        (star.position[1], star.position[0]),
                        max(star.radius, 3),
                        facecolor='black', edgecolor='white',
                        linewidth=1, fill=True
                    )
                else:
                    color = self.colors.get(star.type, (0.5, 0.5, 0.5, 0.5))
                    circ = Circle(
                        (star.position[1], star.position[0]),
                        star.radius,
                        color=color, fill=True, linewidth=0
                    )
                self.ax.add_patch(circ)
                self.star_circles[sid] = circ
            else:
                circ = self.star_circles[sid]
                circ.center = (star.position[1], star.position[0])
                circ.radius = max(
                    star.radius, 3) if star.type == "black_hole" else star.radius
                if star.type == "black_hole":
                    circ.set_facecolor('black')
                    circ.set_edgecolor('white')
                    circ.set_linewidth(1)
                else:
                    color = self.colors.get(star.type, (0.5, 0.5, 0.5, 0.5))
                    circ.set_color(color)
                    circ.set_edgecolor('none')
                    circ.set_linewidth(0)
                circ.set_visible(True)

        return [self.im, self.title, self.tooltip] + list(self.star_circles.values())

    def animate(self, frames=500, interval=50):
        ani = FuncAnimation(
            self.fig, self.update, frames=frames,
            interval=interval, blit=True, repeat=False
        )
        plt.show()
        return ani


if __name__ == "__main__":
    nx, ny = 500, 500
    sigma = 4*np.random.rand(nx, ny)   # nébuleuse aléatoire
    sim = Simulation(sigma, step=1)
    sim.animate(frames=5000, interval=40)
