# Name: Felicia Wang
# ID: 62645970
# Email: wangfeli@umich.edu
# Collaborators: Huy Pham, John (Yohan) Park
# Asked ChatGPT for guidance and comments on how to structure each function

import csv
import os

def read_penguins(csv_file):
    """
    Read CSV -> list of dict rows (simple methods only).
    - Trims whitespace on strings.
    - Attempts to cast numeric fields to float where appropriate.
    - Leaves missing numerics as None.
    """
    data = []
    
    with open(csv_file, "r", newline="") as fh:
        reader = csv.reader(fh)
        rows = list(reader)
        if len(rows) == 0:
            return data
        headers = rows[0]
        # standardize headers by stripping spaces
        clean_headers = []
        for h in headers:
            if h is None:
                clean_headers.append("")
            else:
                clean_headers.append(h.strip())
        # known numeric columns in Palmer Penguins
        numeric_cols = set([
            "bill_length_mm",
            "bill_depth_mm",
            "flipper_length_mm",
            "body_mass_g"
        ])
        # build dict per row
        for row in rows[1:]:
            if len(row) == 0:
                continue
            record = {}
            i = 0
            while i < len(clean_headers) and i < len(row):
                key = clean_headers[i]
                val = row[i].strip()
                # try numeric cast for known numeric columns
                if key in numeric_cols:
                    if val == "" or val.lower() == "na" or val.lower() == "nan":
                        record[key] = None
                    else:
                        try:
                            # body_mass_g can be float but typically int; keep float for simplicity
                            record[key] = float(val)
                        except:
                            record[key] = None
                else:
                    # normalize sex to uppercase if key == "sex"
                    if key == "sex":
                        record[key] = val.upper()
                    else:
                        record[key] = val
                i += 1
            data.append(record)
    return data

def filter_rows(data, key, value):
    """ Keep rows where row.get(key) == value """
    out = []
    for row in data:
        if key in row:
            if row[key] == value:
                out.append(row)
    return out

def group_conditional_counts(rows, group_key, cond_key, op, threshold):
    """
    Count denominators and numerators per group.
    - Denominator: rows with non-missing group and valid numeric cond_key
    - Numerator: among denominator rows, those satisfying condition
    """
    den = {}
    num = {}
    for row in rows:
        if group_key not in row:
            continue
        group = row[group_key]
        if group is None or group == "":
            continue
        # fetch value for condition
        if cond_key not in row:
            continue
        value = row[cond_key]
        if value is None:
            continue
        # ensure group keys exist
        if group not in den:
            den[group] = 0
        if group not in num:
            num[group] = 0
        # denominator
        den[group] = den[group] + 1
        # operator check
        cond_true = False
        if op == ">":
            if value > threshold:
                cond_true = True
        elif op == "<":
            if value < threshold:
                cond_true = True
        else:
            # unsupported op; treat as false
            cond_true = False
        if cond_true:
            num[group] = num[group] + 1
    return den, num

def compute_percentages(num_counts, den_counts):
    """ Convert counts to percentages per group. If denominator is 0, percent = 0.0 """
    result = {}
    for g in den_counts:
        den = den_counts[g]
        if den == 0:
            pct = 0.0
        else:
            # get numerator (may be absent)
            if g in num_counts:
                n = num_counts[g]
            else:
                n = 0
            pct = (n * 100.0) / float(den)
        result[g] = pct
    return result

def write_dict_to_csv(d, out_path):
    """ Write a two-column CSV: group, percent (rounded to 2 decimals in file) """
    # stable order by key (alphabetical)
    keys = sorted(d.keys())
    with open(out_path, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["group", "percent"])
        for k in keys:
            # keep file values with two decimal places for readability
            pct = d[k]
            try:
                pct_str = "{:.2f}".format(float(pct))
            except:
                pct_str = "0.00"
            writer.writerow([k, pct_str])

def percent_fem_bill_over_40_by_island(penguin_data):
    """
    Compute {island: % FEMALE with bill_length_mm > 40}
    Uses columns: sex, bill_length_mm, island
    """
    females = filter_rows(penguin_data, "sex", "FEMALE")
    den, num = group_conditional_counts(
        females, group_key="island", cond_key="bill_length_mm", op=">", threshold=40.0
    )
    return compute_percentages(num, den)


def percent_male_flip_under_180_by_species(penguin_data):
    """
    Compute {species: % MALE with flipper_length_mm < 180}
    Uses columns: sex, flipper_length_mm, species
    """
    males = filter_rows(penguin_data, "sex", "MALE")
    den, num = group_conditional_counts(
        males, group_key="species", cond_key="flipper_length_mm", op="<", threshold=180.0
    )
    return compute_percentages(num, den)

def main():
    # Determine input file path from environment or default
    csv_file = os.environ.get("PENGUINS_CSV_PATH", "penguins.csv")
    if not os.path.isabs(csv_file):
        # resolve relative to script directory
        base = os.path.abspath(os.path.dirname(__file__))
        csv_file = os.path.join(base, csv_file)

    data = read_penguins(csv_file)

    # Problem A
    fem_by_island = percent_fem_bill_over_40_by_island(data)
    out_a = os.environ.get("OUT_A", "percent_fem_bill_over_40_by_island.csv")
    if not os.path.isabs(out_a):
        out_a = os.path.join(os.path.abspath(os.path.dirname(__file__)), out_a)
    write_dict_to_csv(fem_by_island, out_a)

    # Problem B
    male_by_species = percent_male_flip_under_180_by_species(data)
    out_b = os.environ.get("OUT_B", "percent_male_flip_under_180_by_species.csv")
    if not os.path.isabs(out_b):
        out_b = os.path.join(os.path.abspath(os.path.dirname(__file__)), out_b)
    write_dict_to_csv(male_by_species, out_b)

    # Print to console
    print("=== Percent_fem_bill_over_40_by_island ===")
    for k in sorted(fem_by_island.keys()):
        print(k + ":", "{:.2f}".format(fem_by_island[k]))
    print("=== Percent_male_flip_under_180_by_species ===")
    for k in sorted(male_by_species.keys()):
        print(k + ":", "{:.2f}".format(male_by_species[k]))

if __name__ == "__main__":
    main()