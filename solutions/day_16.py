from math import prod


def part_one():
    def parse_packet(packet, idx=0):
        version = int(packet[idx:idx + 3], 2)
        idx += 3
        type_id = int(packet[idx:idx + 3], 2)
        idx += 3
        if type_id != 4:
            if packet[idx] == "0":
                maximum_bits = int(packet[idx + 1:idx + 16], 2)
                idx += 16
                orig_idx = idx
                while idx - orig_idx != maximum_bits:
                    pack_version, idx = parse_packet(packet, idx)
                    version += pack_version
            elif packet[idx] == "1":
                total_packets = int(packet[idx + 1:idx + 12], 2)
                idx += 12
                for _ in range(total_packets):
                    pack_version, idx = parse_packet(packet, idx)
                    version += pack_version
        else:
            while True:
                sequence = packet[idx:idx + 5]
                if sequence.startswith("0"):
                    idx += 5
                    break
                else:
                    idx += 5

            return version, idx

        return version, idx

    with open("input.txt") as file:
        packet = file.read()
        new_packet = ""
        for char in packet:
            new_packet += bin(int(char, 16))[2:].zfill(4)

        packet = new_packet
        while len(packet) % 4 != 0:
            packet += "0"

        version, _ = parse_packet(packet)
        print(version)


def part_two():
    def parse_packet(packet, idx=0):
        version = int(packet[idx:idx + 3], 2)
        idx += 3
        type_id = int(packet[idx:idx + 3], 2)
        idx += 3
        if type_id != 4:
            all_vals = []
            if packet[idx] == "0":
                maximum_bits = int(packet[idx + 1:idx + 16], 2)
                idx += 16
                orig_idx = idx
                while idx - orig_idx != maximum_bits:
                    res, idx = parse_packet(packet, idx)
                    all_vals.append(res)
            elif packet[idx] == "1":
                total_packets = int(packet[idx + 1:idx + 12], 2)
                idx += 12
                for _ in range(total_packets):
                    res, idx = parse_packet(packet, idx)
                    all_vals.append(res)

            if type_id == 0:
                return sum(all_vals), idx
            elif type_id == 1:
                return prod(all_vals), idx
            elif type_id == 2:
                return min(all_vals), idx
            elif type_id == 3:
                return max(all_vals), idx
            elif type_id == 5:
                return int(all_vals[0] > all_vals[1]), idx
            elif type_id == 6:
                return int(all_vals[0] < all_vals[1]), idx
            elif type_id == 7:
                return int(all_vals[0] == all_vals[1]), idx

        else:
            total = ""
            while True:
                sequence = packet[idx:idx + 5]
                total += sequence[1:]
                if sequence.startswith("0"):
                    idx += 5
                    break
                else:
                    idx += 5

            return int(total, 2), idx

    with open("input.txt") as file:
        packet = file.read()
        new_packet = ""
        for char in packet:
            new_packet += bin(int(char, 16))[2:].zfill(4)

        packet = new_packet
        while len(packet) % 4 != 0:
            packet += "0"

        total, _ = parse_packet(packet)
        print(total)


part_two()