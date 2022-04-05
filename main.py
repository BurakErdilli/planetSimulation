import pygame
import math

# git remote add origin https://github.com/BurakErdilli/planetSimulation.git

# git branch -M main
#
# git push -u origin main
pygame.init()

WIDTH, HEIGHT = 1920, 1080
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
BROWN = (200, 102, 0)
DARK_BLUE = (0, 0, 255)
LIGHT_YELLOW = (255, 255, 102)
LIGHT_BLUE = (0, 204, 204)

FONT = pygame.font.SysFont("comicsans", 16)


class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 200 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600 * 24 / 5  # 1 day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun / 1000, 1)}km", True, WHITE)
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 5, YELLOW, 1.98892 * 10 ** 30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 12, BLUE, 5.9742 * 10 ** 24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 6, RED, 6.39 * 10 ** 23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 4, DARK_GREY, 3.30 * 10 ** 23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 12, WHITE, 4.8685 * 10 ** 24)
    venus.y_vel = -35.02 * 1000

    jupiter = Planet(5.2 * Planet.AU, 0, 40, BROWN, 1.9 * 10 ** 27)
    jupiter.y_vel = -13.1 * 1000

    uranus = Planet(19.2 * Planet.AU, 0, 20, DARK_BLUE, 8.68 * 10 ** 25)
    uranus.y_vel = -6.8 * 1000

    saturn = Planet(9.5 * Planet.AU, 0, 35, LIGHT_YELLOW, 5.68 * 10 ** 26)
    saturn.y_vel = -9.7 * 1000

    neptun = Planet(30 * Planet.AU, 0, 20, LIGHT_BLUE, 1.024 * 10 ** 26)
    neptun.y_vel = -5.4 * 1000

    moon_dist = Planet.AU + 3844000
    moon_test = Planet(-1 * moon_dist, 0, 10, DARK_GREY, 7.34 * 10 ** 22)
    moon_test.y_vel = earth.y_vel + 1022

    planets = [sun, mercury, venus, earth, moon_test, mars, jupiter, saturn, uranus, neptun]
    # planets = [sun, venus , earth, mars, moon_test]
    # planets = [moon_test]

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()


main()
