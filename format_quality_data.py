import csv

def csv_dbn_to_set(file_name):
    hs_dbn_set = set()

    with open(file_name) as csvfile:
        blah = csv.reader(
            csvfile,
            delimiter=",",
        )
        for index, row in enumerate(blah):
            if index != 0:
                hs_dbn_set.add(row[0])

    return hs_dbn_set


def csv_to_list(csv_name):
    with open(csv_name) as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        csv_list = [row for row in reader]

        return csv_list


def flatten(hs_list):
    return [sub_row for row in hs_list for sub_row in row]


def create_dict(key_list, val_list):
    return dict(zip(key_list, val_list))


def filter_attrs(csv_list):
    file_dict = {}
    header = csv_list.pop(0)

    for row in csv_list:
        dict_key = row[0]
        year_key = row[3]
        grade_type = row[2]

        if (
            dict_key in file_dict
            and (year_key == "2016-17" or year_key == "2017-18")
            and grade_type == "All Grades"
        ):
            file_dict[dict_key].append(create_dict(header, row))

        elif (
            dict_key not in file_dict
            and (year_key == "2016-17" or year_key == "2017-18")
            and grade_type == "All Grades"
        ):
            file_dict[dict_key] = []
            file_dict[dict_key].append(create_dict(header, row))

    return file_dict


def map_values(hs_set, file_dict):
    hs_results = []

    for val in hs_set:
        if val in file_dict:
            list_val = file_dict[val]
            hs_results.append(list_val)

    return flatten(hs_results)


def write_to_csv(file_name, data_list):
    data_file = open(file_name, "w")
    csv_writer = csv.writer(data_file)

    for index, row in enumerate(data_list):
        if index == 0:
            header = row.keys()
            csv_writer.writerow(header)
        else:
            values = row.values()
            csv_writer.writerow(values)


def main():
    hs_set = csv_dbn_to_set("./ORIGINAL-CSV/2017_QUALITY_HS.csv")
    hs_t_set = csv_dbn_to_set("./ORIGINAL-CSV/2017_QUALITY_HST.csv")
    hs_list = csv_to_list("./ORIGINAL-CSV/2013-2019_ATTENDANCE.csv")
    hs_full_set = hs_set.union(hs_t_set)
    filtered_list = filter_attrs(hs_list)
    result = map_values(hs_full_set, filtered_list)
    write_to_csv("./OUTPUT-CSV/2017-DATA.csv", result)


if __name__ == "__main__":
    main()