import numpy as np

class Star:
    def __init__(self, position, mass, radius, lifetime):
        self.position = position      # (i,j)
        self.mass = mass              # masse conservée
        self.initial_radius = radius
        self.radius = radius
        self.lifetime = lifetime
        self.age = 0.0
        self.phase = "main_sequence"

    def update(self, dt):
        self.age += dt

        # transition vers naine blanche
        if self.phase == "main_sequence" and self.age >= self.lifetime:
            self.phase = "white_dwarf"

        if self.phase == "white_dwarf":
            target_radius = self.initial_radius / 2.0
            shrink_time = 50.0
            shrink_rate = (self.initial_radius - target_radius) / shrink_time

            if self.radius > target_radius:
                self.radius -= shrink_rate * dt
                if self.radius < target_radius:
                    self.radius = target_radius


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


def remove_star_region(sigma, star):
    #Rend nulle la densité de masse dans une zone précedement au sein d'une étoile mais qui n'y est plus à cause de son rétrécissement'
    nx, ny = sigma.shape
    x0, y0 = star.position
    r = star.radius

    for i in range(nx):
        for j in range(ny):
            if (i - x0)**2 + (j - y0)**2 <= r**2:
                sigma[i, j] = 0.0



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


        for i in range(nx):
            for j in range(ny):

                if sigma[i, j] <= density_threshold:
                    continue

                xmin = max(0, i - freeze_radius)
                xmax = min(nx, i + freeze_radius + 1)
                ymin = max(0, j - freeze_radius)
                ymax = min(ny, j + freeze_radius + 1)

                region = sigma[xmin:xmax, ymin:ymax]

                if np.all(region > density_threshold):

                    # masse totale région
                    mass = np.sum(region)

                    # retirer masse du gaz
                    sigma[xmin:xmax, ymin:ymax] = 0.0

                    lifetime = 100 + 50 * np.random.rand()

                    stars.append(
                        Star((i, j), mass, freeze_radius, lifetime)
                    )

        #Evolution des étoiles

        for star in stars:
            star.update(dt)
        for star in stars:
            deposit_star_density(sigma, star)

    return sigma, stars