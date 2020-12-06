import csv


def csv_to_list(csv_name):
    with open(csv_name) as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        csv_list = [row for row in reader]

        return csv_list


def create_header(header):
    return header[0:1][0] + ["postal_code", "coordinates"]


def create_zip_coordinates(dbn_list):
    list_no_header = dbn_list[1:]
    header = create_header(dbn_list)

    for li in list_no_header:
        location = li[1]
        location_split = location.split(" ")
        length = len(location_split)
        [right, _] = location_split[length - 1].split(")")
        left = location_split[length - 2]
        [post_code, lat] = left.split("(")
        coordinates = f"{lat}{right}"

        li.append(post_code)
        li.append(coordinates)

    return [header] + list_no_header


def write_to_csv(file_name, data_list):
    file = open(file_name, "a+", newline="")

    with file:
        write = csv.writer(file)
        write.writerows(data_list)


def main():
    dbn_list = csv_to_list("./ORIGINAL-CSV/2018_DBN_HS.csv")
    zip_cord_fields = create_zip_coordinates(dbn_list)
    write_to_csv("./OUTPUT-CSV/2018-DBN-ZIP-COORDINATES.csv", zip_cord_fields)


if __name__ == "__main__":
    main()