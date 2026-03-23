import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle
from matplotlib.widgets import Slider, Button
from matplotlib.widgets import CheckButtons

# Constante Globale : 1 pas = 1 million d'années
STEP = 1
TIME_PER_STEP = 1e6

RDWARF_RFACTOR = 0.8
YDWARF_RFACTOR = 4
BGIANT_RFACTOR = 4
RGIANT_RFACTOR = 0.1
SRGIANT_RFACTOR = 0.05
RADIUS_FACTOR = 6

MASS_FACTOR = 20
TRHESHOLD_FACTOR = 20
DENSITY_THRESHOLD = 0.07 * TRHESHOLD_FACTOR
YTHRESHOLD = 0.8 * TRHESHOLD_FACTOR
BTHRESHOLD = 8 * TRHESHOLD_FACTOR

DISPERTION_COEF = 2
MAX_GRAD = 5


class Star:
    def __init__(self, position, mass, radius, yellow_threshold, blue_threshold):
        self.position = position
        self.mass = mass
        self.initial_mass = mass

        if mass > blue_threshold:
            self.type = "blue_giant"
            base_lifetime = 1e9
            self.initial_radius = max(
                (self.mass/MASS_FACTOR)**0.6 * BGIANT_RFACTOR, (blue_threshold/MASS_FACTOR) * YDWARF_RFACTOR)
        elif mass > yellow_threshold:
            self.type = "yellow_dwarf"
            base_lifetime = 1e8
            self.initial_radius = min(
                (self.mass/MASS_FACTOR) * YDWARF_RFACTOR, (blue_threshold/MASS_FACTOR)**0.6 * BGIANT_RFACTOR)
        else:
            self.type = "red_dwarf"
            base_lifetime = 1e10
            self.initial_radius = self.mass**0.5 * RDWARF_RFACTOR
        self.radius = self.initial_radius

        self.lifetime = 1e10 * ((mass*15)**-2.5 + 1e-8)
        self.timer = self.lifetime

        self.giant_timer = None
        self.giant_lifetime = None

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
    is_supernova = False

    if not star.alive:
        return shed_mass, is_supernova

    star.timer -= 1

    if star.type in ["red_dwarf", "yellow_dwarf", "blue_giant"]:
        if star.timer <= 0:
            if star.type == "blue_giant":
                star.type = "red_supergiant"
                star.giant_lifetime = np.random.uniform(15, 25)
                star.giant_timer = star.giant_lifetime
                star.timer = star.giant_lifetime
            elif star.type == "yellow_dwarf":
                star.type = "red_giant"
                star.giant_lifetime = np.random.uniform(40, 120)
                star.giant_timer = star.giant_lifetime
                star.timer = star.giant_lifetime
            else:  # Mort d'une naine rouge
                star.type = "white_dwarf"
                core_mass = star.mass * star.core_fraction
                shed_mass = star.mass - core_mass
                star.mass = core_mass
                star.radius = (star.mass/MASS_FACTOR)**(-1/3) * 7
                star.alive = False

    elif star.type == "red_giant":
        if star.giant_timer is None:
            star.giant_lifetime = np.random.uniform(35, 70)
            star.giant_timer = star.giant_lifetime
        if star.giant_timer > 0:
            star.giant_timer -= 1
            growth = 1 - star.giant_timer / star.giant_lifetime
            star.radius = max(int(star.initial_radius * (1 + 45 * growth))
                              * RGIANT_RFACTOR, star.initial_radius)
        else:
            core_mass = star.mass * star.core_fraction
            shed_mass = star.mass - core_mass
            star.mass = core_mass
            star.radius = (star.mass/MASS_FACTOR)**(-1/3) * 7
            star.type = "white_dwarf"
            star.alive = False

    elif star.type == "red_supergiant":
        if star.giant_timer is None:
            star.giant_lifetime = np.random.uniform(15, 25)
            star.giant_timer = star.giant_lifetime
        if star.giant_timer > 0:
            star.giant_timer -= 1
            growth = 1 - star.giant_timer / star.giant_lifetime
            star.radius = max(int(star.initial_radius * (1 + 70 * growth))
                              * SRGIANT_RFACTOR, star.initial_radius)
        else:
            core_mass = star.mass * star.massive_core_fraction
            shed_mass = star.mass - core_mass
            star.alive = False
            is_supernova = True

            if star.mass > 20 * MASS_FACTOR:
                star.type = "black_hole"
                star.mass = core_mass
                star.radius = max(11, star.mass / MASS_FACTOR * 3)

            else:
                star.type = "neutron_star"
                star.mass = core_mass
                star.radius = 3.5

    return shed_mass, is_supernova

def merge_stars(stars, yellow_threshold, blue_threshold):
    """ fusion d'étoiles """
    used = set()
    result = []

    for i, s1 in enumerate(stars):
        if i in used:
            continue

        for j in range(i+1, len(stars)):
            if j in used:
                continue

            s2 = stars[j]
            dx = s1.position[0] - s2.position[0]
            dy = s1.position[1] - s2.position[1]
            dist = np.hypot(dx, dy)

            if dist < (s1.radius + s2.radius):
                
                # --- MODIFICATION ICI : Priorité absolue au trou noir pour le centre ---
                if s1.type == "black_hole":
                    big, small, small_index = s1, s2, j
                elif s2.type == "black_hole":
                    big, small, small_index = s2, s1, i
                elif s1.mass >= s2.mass:
                    big, small, small_index = s1, s2, j
                else:
                    big, small, small_index = s2, s1, i
                # ----------------------------------------------------------------------

                big.mass += small.mass
                big.radius = np.sqrt(big.mass)

                if big.type == "black_hole" or s1.type == "black_hole" or s2.type == "black_hole":
                    new_type = "black_hole"
                elif "red_supergiant" in (s1.type, s2.type):
                    new_type = "red_supergiant"
                elif big.type == "red_giant":
                    if big.mass > blue_threshold:
                        new_type = "red_supergiant"
                    else:
                        new_type = "red_giant"
                else:
                    if big.mass > blue_threshold:
                        new_type = "blue_giant"
                    elif big.mass > yellow_threshold:
                        new_type = "yellow_dwarf"
                    else:
                        new_type = "red_dwarf"

                big.type = new_type
                used.add(small_index)

        if i not in used:
            result.append(s1)

    return result


def laplacian(Z):
    return (np.roll(Z, 1, 0) + np.roll(Z, -1, 0) + np.roll(Z, 1, 1) + np.roll(Z, -1, 1) - 4 * Z)


def compute_gravitational_potential(sigma, G=0.5):
    """ calcul du potentiel gravitationnel"""
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
    """ délimite les zones occupées par des étoiles """
    nx, ny = sigma_shape
    occ = np.zeros((nx, ny), dtype=bool)
    Y, X = np.ogrid[:nx, :ny]

    for star in stars:
        if star.type in ["yellow_dwarf", "red_dwarf"]:
            r = max(5, star.radius * 7)
        elif star.type == "blue_giant" :
            r = max(5, star.radius * 2.5)    
        elif star.type in ["red_giant", "red_supergiant"]:
            r = max(5, star.radius * 1.5)
        else:
            r = max(5, star.radius * 2)

        mask = (X - star.position[1])**2 + (Y - star.position[0])**2 <= r**2
        occ |= mask
    return occ


def find_connected_regions(mask):
    """ trouve des régions où une étoile peut se former"""
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
    """ renvoie l'étape suivante de la répartition de masse et des étoiles """
    nx, ny = sigma_gas.shape
    new_supernovae = []

    # Bilan strict de la masse pour éviter toute création accidentelle
    target_mass = np.sum(sigma_gas)

    for _ in range(steps):
        phi = compute_gravitational_potential(sigma_gas, G)

        gradx = (np.roll(phi, -1, 0) - np.roll(phi, 1, 0)) * 0.5
        grady = (np.roll(phi, -1, 1) - np.roll(phi, 1, 1)) * 0.5

        # Limiteur pour éviter l'explosion numérique
        max_grad = MAX_GRAD
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

        stars = merge_stars(stars, yellow_threshold, blue_threshold)

        # 4. Évolution stellaire (Supernovas, naines blanches...)
        for star in stars:
            shed_mass, is_sn = evolve_star_and_get_shed_mass(
                star, blue_threshold)
            if shed_mass > 0:
                redistribute_envelope(
                    sigma_gas, star.position, star.radius, shed_mass)
                target_mass += shed_mass  # On rajoute la masse rejetée au bilan du gaz
            if is_sn:
                new_supernovae.append(star.position)

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

    return sigma_gas, sigma_display, stars, new_supernovae


class Simulation:
    def __init__(self, sigma_init, step):
        self.sigma_init = sigma_init.copy()
        self.sigma = sigma_init.copy()  # Gaz uniquement
        self.sigma_display = sigma_init.copy()
        self.nx, self.ny = self.sigma.shape
        self.stars = []
        self.supernovae_anim = []
        self.sn_circles = []

        self.step_count = 0
        self.step = step
        self.nbstars = 0
        self.totalmass = np.sum(self.sigma)

        # Image ---

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
        self.slider_mass = Slider(ax=ax_slider_mass, label='Masse solaire',
                                  valmin=0.1, valmax=2, valinit=0.2, valstep=0.1)
        self.slider_mass.label.set_color('white')
        self.slider_mass.valtext.set_color('white')
        self.slider_mass.on_changed(
            lambda val: setattr(self, 'click_amount', val))
        self.click_amount = self.slider_mass.val

        ax_slider_radius = plt.axes([0.12, 0.04, 0.4, 0.01])
        self.slider_radius = Slider(
            ax=ax_slider_radius, label='Rayon ', valmin=1, valmax=40, valinit=10, valstep=1)
        self.slider_radius.label.set_color('white')
        self.slider_radius.valtext.set_color('white')
        self.slider_radius.on_changed(
            lambda val: setattr(self, 'click_radius', int(val)))
        self.click_radius = int(self.slider_radius.val)

        # Boutons
        ax_button_pause = plt.axes([0.65, 0.03, 0.1, 0.04])
        self.button_pause = Button(
            ax_button_pause, 'Pause', hovercolor='lightblue')
        self.button_pause.on_clicked(self.toggle_pause)
        self.paused = False

        ax_button_reset = plt.axes([0.8, 0.03, 0.1, 0.04])
        self.button_reset = Button(
            ax_button_reset, 'Reset', hovercolor='lightblue')
        self.button_reset.on_clicked(self.reset_simulation)

        ax_button_reset_to_zero = plt.axes([0.8, 0.08, 0.1, 0.04])
        self.button_reset_to_zero = Button(
            ax_button_reset_to_zero, 'Reset to zero', hovercolor='lightblue')
        self.button_reset_to_zero.on_clicked(self.reset_simulation_to_zero)

        # Affichage
        self.star_circles = {}
        self.colors = {
            'red_dwarf': (1.0, 0.5, 0.5), 'yellow_dwarf': (1.0, 1.0, 0.6),
            'blue_giant': (0.5, 0.8, 1.0, 0.9), 'red_giant': (0.8, 0, 0, 0.6),
            'red_supergiant': (1, 0.2, 0.2, 0.7), 'white_dwarf': (1.0, 1.0, 1.0),
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

        # Checklist
        self.types_ordre = ['red_dwarf', 'yellow_dwarf', 'blue_giant',
                            'red_giant', 'red_supergiant', 'white_dwarf',
                            'neutron_star', 'black_hole']
        self.discovered_stars = {t: None for t in self.types_ordre}
        self.ds_nb = 0

        self.ax_table = self.fig.add_axes([0.57, 0.3, 0.4, 0.5])
        self.ax_table.set_facecolor('black')
        self.ax_table.set_title(
            f"Mission : Découvre les étoiles ! ({self.ds_nb}/8 trouvées)", color="white", fontname="monospace", fontsize=12, pad=15)

        self.head = ['Trouvé', 'Type', 'Apparence',
                     'Nombre', "Temps de vie \n en million d'années "]

        lignes_init = []
        for t in self.types_ordre:
            lignes_init.append(["✗", self.names[t], "●", "0", "—"])
        lignes_init[len(lignes_init)-1][2] = "◯"
        data_init = [self.head] + lignes_init

        self.col_widths = [0.1, 0.25, 0.13, 0.12, 0.3]
        self.table = self.ax_table.table(
            cellText=data_init, loc='center', cellLoc='center', colWidths=self.col_widths)
        self.table.auto_set_font_size(False)
        self.table.set_fontsize(10)
        self.table.scale(1, 3)

        for (i, j), cell in self.table.get_celld().items():
            cell.set_facecolor('black')
            cell.set_text_props(color='white')
            cell.set_edgecolor('darkgray')
            if i == 0:
                cell.set_facecolor('darkgray')
                cell.set_text_props(weight='bold', color='white')
            else:
                if j == 0:
                    cell.get_text().set_color('salmon')
                elif j == 2:
                    t = self.types_ordre[i-1]
                    if t == 'black_hole':
                        cell.get_text().set_color('white')
                    else:
                        color = self.colors.get(t, (1, 1, 1))
                        if len(color) == 4:
                            color = color[:3]
                        cell.get_text().set_color(color)

    def update_info_table(self):
        """Mise à jour de la checklist"""
        counts = {t: 0 for t in self.types_ordre}
        for star in self.stars:
            if star.type in counts:
                counts[star.type] += 1

            t = star.type
            if self.discovered_stars[t] is None:
                self.discovered_stars[t] = {
                    'timer': star.timer
                }
                self.ds_nb += 1

        self.ax_table.set_title(
            f"Mission : Découvre les étoiles ! ({self.ds_nb}/8 trouvées)", color="white", fontname="monospace", fontsize=12, pad=15)

        for idx, t in enumerate(self.types_ordre):
            ligne = idx + 1
            data = self.discovered_stars[t]

            # Colonne 0
            cell = self.table.get_celld().get((ligne, 0))
            if cell:
                cell.get_text().set_text("✓" if data else "✗")
                cell.get_text().set_color('lightgreen' if data else 'salmon')

            # Colonne 3
            cell = self.table.get_celld().get((ligne, 3))
            if cell:
                if data:
                    cell.get_text().set_text(f"{counts[t]:.0f}")
                else:
                    cell.get_text().set_text("0")

            # Colonne 4
            cell = self.table.get_celld().get((ligne, 4))
            if cell:
                if data:
                    rem_myr = data['timer'] * TIME_PER_STEP / 1e6
                    if t in ['black_hole', 'white_dwarf', 'neutron_star']:
                        cell.get_text().set_text("∞")
                    else:
                        cell.get_text().set_text(
                            f"{rem_myr:.1f}")
                else:
                    cell.get_text().set_text("-")

    def toggle_pause(self, event):
        """ Bonton pause """
        self.paused = not self.paused
        self.button_pause.label.set_text('Start' if self.paused else 'Pause')

    def reset_simulation(self, event):
        """ Bouton resest """
        self.sigma = 0.1 * np.random.rand(nx, ny)
        self.sigma_display = self.sigma.copy()
        self.stars = []
        self.step_count = 0
        self.nbstars = 0
        self.im.set_array(self.sigma_display)
        for circ in self.star_circles.values():
            circ.remove()
        self.star_circles.clear()
        self.tooltip.set_visible(False)
        self.current_star = None

        self.supernovae_anim = []
        for circ in self.sn_circles:
            circ.remove()
        self.sn_circles.clear()

        self.fig.canvas.draw_idle()

    def reset_simulation_to_zero(self, event):
        """ Bouton resest """
        self.sigma = 0 * np.random.rand(nx, ny)
        self.sigma_display = self.sigma.copy()
        self.stars = []
        self.step_count = 0
        self.nbstars = 0
        self.im.set_array(self.sigma_display)
        for circ in self.star_circles.values():
            circ.remove()
        self.star_circles.clear()
        self.tooltip.set_visible(False)
        self.current_star = None

        self.supernovae_anim = []
        for circ in self.sn_circles:
            circ.remove()
        self.sn_circles.clear()

        self.fig.canvas.draw_idle()

    def on_click(self, event):
        """ fonctionnalité ajout de masse """
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
                        self.sigma_display[ni,
                                           nj] += self.click_amount * factor

        self.im.set_array(self.sigma_display)
        self.fig.canvas.draw_idle()

    def info_hover(self, event):
        """ affichage de l'infobulle """
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
        """ mise à jour globale """
        if not self.paused:
            self.sigma, self.sigma_display, self.stars, new_sn = evolve_mass_distribution(
                self.sigma, self.stars, steps=self.step)
            self.step_count += self.step
            self.nbstars = len(self.stars)
            self.totalmass = np.sum(self.sigma) + \
                sum(s.mass for s in self.stars)

            for pos in new_sn:
                self.supernovae_anim.append({'pos': pos, 'r': 5, 'alpha': 1.0})
            for sn in self.supernovae_anim:
                sn['r'] += 20
                sn['alpha'] -= 0.08
            self.supernovae_anim = [
                sn for sn in self.supernovae_anim if sn['alpha'] > 0]

            self.update_info_table()

        age = self.step_count * TIME_PER_STEP / 1e6
        self.title.set_text(
            f"Simulation stellaire\nÂge : {age:.2f} millions d'années | {self.nbstars} étoiles | masse totale = {self.totalmass:.1f}")
        self.im.set_array(self.sigma_display)

        if self.current_star and self.current_star in self.stars:
            lifetime = self.current_star.giant_lifetime if self.current_star.type in [
                "red_giant", "red_supergiant"] else self.current_star.lifetime
            lftext = "« infini »" if self.current_star.type in [
                "black_hole", "white_dwarf", "neutron_star"] else f"{lifetime:1f} M d'années"
            rem = self.current_star.timer * TIME_PER_STEP / 1e6
            timetext = "« infini »" if self.current_star.type in [
                "black_hole", "white_dwarf", "neutron_star"] else f"{rem:.1f} M d'années"
            self.tooltip.set_text((f"Type: {self.names[self.current_star.type]}\n"
                                   f"Masse: {self.current_star.mass/MASS_FACTOR:.2f} M☉\n"
                                   f"Temps de vie: {lftext}\n"
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

        for c in self.sn_circles:
            c.remove()
        self.sn_circles.clear()

        for sn in self.supernovae_anim:
            c1 = Circle((sn['pos'][1], sn['pos'][0]), sn['r'], fill=False, edgecolor=(
                0.0, 1.0, 1.0, sn['alpha']), linewidth=4)
            c2 = Circle((sn['pos'][1], sn['pos'][0]), sn['r']*0.6, fill=False,
                        edgecolor=(1.0, 0.4, 0.0, sn['alpha']), linewidth=3)
            self.ax.add_patch(c1)
            self.ax.add_patch(c2)
            self.sn_circles.extend([c1, c2])
        return [self.im, self.title, self.tooltip, self.table] + list(self.star_circles.values()) + self.sn_circles

    def animate(self, frames=500, interval=50):
        """ lance l'animation """
        ani = FuncAnimation(self.fig, self.update, frames=frames,
                            interval=interval, blit=True, repeat=False)
        plt.show()
        return ani


if __name__ == "__main__":
    nx, ny = 500, 500
    sigma = 0.1 * np.random.rand(nx, ny)
    sim = Simulation(sigma, step=STEP)
    sim.animate(frames=None, interval=40)
