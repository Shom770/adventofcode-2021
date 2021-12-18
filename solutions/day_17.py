def part_one():
    with open("input.txt") as file:
        target_x, target_y = file.read().replace("target area: ", "").replace("x=", "").replace("y=", "").replace(",",
                                                                                                                  "").split()
        target_x = range(int(target_x.split("..")[0]), int(target_x.split("..")[1]))
        target_y = range(int(target_y.split("..")[0]), int(target_y.split("..")[1]))

        def working_velocity():
            coordinates = (0, 0)
            working_velocities = []

            for y in range(-301, 301):
                for x in range(0, 301):
                    if 0 + y < target_y.start or 0 + x > target_x.stop:
                        break
                    changed_velocity_x = x
                    changed_velocity_y = y
                    coords_on_run = [coordinates]

                    while True:
                        coordinates = (coordinates[0] + changed_velocity_x, coordinates[1] + changed_velocity_y)
                        coords_on_run.append(coordinates)

                        changed_velocity_x += 1 if changed_velocity_x < 0 else (-1 if changed_velocity_x > 0 else 0)
                        changed_velocity_y -= 1

                        if coordinates[0] in target_x and coordinates[1] in target_y:
                            working_velocities.append(coords_on_run)
                            break

                        if coordinates[-1] < target_y.start or coordinates[0] > target_x.stop:
                            break

                    coordinates = (0, 0)

            return working_velocities

        all_coords = working_velocity()
        return max([max(coords, key=lambda x: x[-1]) for coords in all_coords])[-1]


def part_two():
    with open("input.txt") as file:
        target_x, target_y = file.read().replace("target area: ", "").replace("x=", "").replace("y=", "").replace(",",
                                                                                                                  "").split()
        target_x = range(int(target_x.split("..")[0]), int(target_x.split("..")[1]) + 1)
        target_y = range(int(target_y.split("..")[0]), int(target_y.split("..")[1]) + 1)

        def working_velocity():
            coordinates = (0, 0)
            working_velocities = []

            for y in range(-301, 301):
                for x in range(0, 301):
                    if 0 + y < target_y.start or 0 + x > target_x.stop:
                        break
                    changed_velocity_x = x
                    changed_velocity_y = y

                    while True:
                        coordinates = (coordinates[0] + changed_velocity_x, coordinates[1] + changed_velocity_y)

                        changed_velocity_x += 1 if changed_velocity_x < 0 else (-1 if changed_velocity_x > 0 else 0)
                        changed_velocity_y -= 1

                        if coordinates[0] in target_x and coordinates[1] in target_y:
                            working_velocities.append((x, y))
                            break

                        if coordinates[-1] < target_y.start or coordinates[0] > target_x.stop:
                            break

                    coordinates = (0, 0)

            return working_velocities

        all_coords = working_velocity()
        return len(all_coords)
