import numpy as np


class Star:

    def __init__(self, position, mass, radius, yellow_threshold):

        self.position = position
        self.mass = mass
        self.initial_mass = mass
        self.initial_radius = radius
        self.radius = radius

        # -------------------------
        # Type initial
        # -------------------------
        if mass > yellow_threshold:
            self.type = "yellow_dwarf"
            base_lifetime = 2000
        else:
            self.type = "red_dwarf"
            base_lifetime = 2000 * 40  # rouges vivent ~40x plus longtemps

        # Durée dépendant de la masse : 1 / m^3
        self.lifetime = base_lifetime / (mass**3 + 1e-8)
        self.timer = self.lifetime

        # Paramètres évolution
        self.giant_timer = None
        self.giant_lifetime = None

        self.white_dwarf_radius = max(1, int(radius / 4))
        self.core_fraction = 0.25

        self.alive = True

    def update():
        evolve_mass_distribution(sigma,)


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


def evolve_star(star, sigma):

    if not star.alive:
        return

    star.timer -= 1

    # -------------------------
    # Phase naine rouge / jaune
    # -------------------------
    if star.type in ["red_dwarf", "yellow_dwarf"]:

        if star.timer <= 0:

            if star.type == "yellow_dwarf":

                # Devient géante rouge
                star.type = "red_giant"

                # durée géante rouge aléatoire
                star.giant_lifetime = np.random.uniform(100, 400)
                star.giant_timer = star.giant_lifetime
                star.timer = star.giant_lifetime

            else:
                # Naine rouge → naine blanche directe
                star.type = "white_dwarf"
                star.radius = star.white_dwarf_radius
                star.mass *= star.core_fraction
                star.alive = False

    # -------------------------
    # Phase géante rouge
    # -------------------------
    elif star.type == "red_giant":

        if star.giant_timer > 0:

            star.giant_timer -= 1

            growth_ratio = 1 - star.giant_timer / star.giant_lifetime
            star.radius = int(
                star.initial_radius * (1 + 39 * growth_ratio)
            )

        else:
            # Fin → expulsion enveloppe

            core_mass = star.mass * star.core_fraction
            envelope_mass = star.mass - core_mass

            redistribute_envelope(
                sigma,
                star.position,
                star.radius,
                envelope_mass
            )

            star.mass = core_mass
            star.radius = star.white_dwarf_radius
            star.type = "white_dwarf"
            star.alive = False


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
        steps=500,
        dt=0.05,
        D=0.1,
        G=0.5,
        density_threshold=5.0,
        freeze_radius=4):

    sigma = sigma_init.copy()
    nx, ny = sigma.shape

    stars = []

    for step in range(steps):

        for star in stars:
            remove_star_region(sigma, star)

        # Dynamique de la densité de masse (diffusion + gravité simplifiée)

        diffusion = D * laplacian(sigma)

        phi = -G * sigma
        gradx = (np.roll(phi, -1, 0) - np.roll(phi, 1, 0)) * 0.5
        grady = (np.roll(phi, -1, 1) - np.roll(phi, 1, 1)) * 0.5

        gravity = -(sigma * gradx + sigma * grady)

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

        new_star = Star((x_cm, y_cm), mass, radius, lifetime)

        stars.append(new_star)

        # Réorganiser la densité interne
        deposit_star_density(sigma, new_star)

        # Evolution des étoiles

    for star in stars:
        star.update(dt)
    for star in stars:
        deposit_star_density(sigma, star)

    return sigma, stars
