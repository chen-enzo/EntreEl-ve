import numpy as np


class Star:
    def __init__(self, position, mass, radius, yellow_threshold, blue_threshold):
        self.position = position
        self.mass = mass
        self.initial_mass = mass
        self.initial_radius = radius

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
            base_lifetime = 80000 # 2000 * 40

        # Durée de vie inversement proportionnelle à la masse au cube
        self.lifetime = base_lifetime / (mass**3 + 1e-8)
        self.timer = self.lifetime

        # Paramètres pour les phases de géantes
        self.giant_timer = None
        self.giant_lifetime = None

        # Paramètres des résidus
        self.white_dwarf_radius = max(1, int(radius / 4))
        self.neutron_star_radius = 1
        self.black_hole_radius = 1

        self.core_fraction = 0.25  # Pour naines blanches
        self.massive_core_fraction = 0.15 # Pour supernovae (plus de gaz expulsé)

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

            else: # Naine rouge -> Naine blanche
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
            redistribute_envelope(sigma, star.position, star.radius, star.mass - core_mass)
            star.mass, star.radius, star.type, star.alive = core_mass, star.white_dwarf_radius, "white_dwarf", False

    # -------------------------
    # Phase Supergéante Rouge (Expansion massive)
    # -------------------------
    elif star.type == "red_supergiant":
        if star.giant_timer > 0:
            star.giant_timer -= 1
            growth = 1 - star.giant_timer / star.giant_lifetime
            star.radius = int(star.initial_radius * (1 + 99 * growth)) # Grossit bcp plus
        else:
            # ÉVÉNEMENT SUPERNOVA
            core_mass = star.mass * star.massive_core_fraction
            redistribute_envelope(sigma, star.position, star.radius, star.mass - core_mass)

            star.mass = core_mass
            star.alive = False

            # Détermination du résidu selon la masse finale
            if star.mass > blue_threshold * 0.2: # Seuil arbitraire pour trou noir
                star.type = "black_hole"
                star.radius = star.black_hole_radius
            else:
                star.type = "neutron_star"


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

    cells = []

    for i in range(nx):
        for j in range(ny):
            if (i - x0)**2 + (j - y0)**2 <= r**2:
                cells.append((i, j))

    if not cells:
        return

    density = star.mass / len(cells)

    for i, j in cells:
        sigma[i, j] = density


def star_occupancy_mask(sigma_shape, stars):
    nx, ny = sigma_shape
    occ = np.zeros((nx, ny), dtype=bool)

    for star in stars:
        x0, y0 = star.position
        r = star.radius

        for i in range(nx):
            for j in range(ny):
                if (i - x0)**2 + (j - y0)**2 <= r**2:
                    occ[i, j] = True

    return occ


def remove_star_region(sigma, star):
    # Rend nulle la densité de masse dans une zone précedement au sein d'une étoile mais qui n'y est plus à cause de son rétrécissement'
    nx, ny = sigma.shape
    x0, y0 = star.position
    r = star.radius

    for i in range(nx):
        for j in range(ny):
            if (i - x0)**2 + (j - y0)**2 <= r**2:
                sigma[i, j] = 0.0


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

    stars = []

    for step in range(steps):

        for star in stars:
            remove_star_region(sigma, star)

        # Evolution de la densité de masse

        diffusion = D * laplacian(sigma) # 2ème loi de Fick
                                         #Pour la gravité on part de l'eq de continuité et on approxime la vitesse comme proportionelle à la gravité et le flux par -G*sigma
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

            new_star = Star((x_cm, y_cm), mass, radius, yellow_threshold, blue_threshold)

            stars.append(new_star)

        # Réorganiser la densité interne
            deposit_star_density(sigma, new_star)

        # Evolution des étoiles

        for star in stars:
            evolve_star(star, sigma, blue_threshold)
        for star in stars:
            deposit_star_density(sigma, star)

        return sigma, stars
