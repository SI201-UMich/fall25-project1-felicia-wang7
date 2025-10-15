# Name: John (Yohan) Park, Felicia Wang, Huy Pham
# ID: 15490838, 62645970, 34833492
# Email: yypark@umich.edu, wangfeli@umich.edu, huypham@umich.edu
# Collaborators: John Park Felicia Wang, Huy Pham
# AI usage: Used ChatGPT for decomposition and base test code; code verified manually. Also used ChatGPT to compile separate code files together and verify tests to function with matching format.

import csv
import os

# John's Functions

NUMERIC_FIELDS = {
    "bill_length_mm",
    "bill_depth_mm",
    "flipper_length_mm",
    "body_mass_g"
}

def read_penguins(csv_file):
    """Reads CSV -> list of dicts with cleaned values."""
    out = []
    with open(csv_file, newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            clean = {}
            for k, v in row.items():
                s = str(v).strip() if v else ""
                if not s:
                    clean[k] = None
                elif k in NUMERIC_FIELDS:
                    try:
                        clean[k] = float(s)
                    except:
                        clean[k] = None
                else:
                    clean[k] = s
            out.append(clean)
    return out


def write_results_to_csv(filename, header, rows):
    """Simple CSV writer used by all functions."""
    with open(filename, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        for row in rows:
            w.writerow(row)


def avg_flipper_length_gentoo_by_island(data):
    """Average flipper length for Gentoo penguins per island."""
    sums, counts = {}, {}
    for row in data:
        sp = (row.get("species") or "").strip().lower()
        isl = (row.get("island") or "").strip().lower()
        fl = row.get("flipper_length_mm")
        if sp != "gentoo" or not isl or fl is None:
            continue
        sums[isl] = sums.get(isl, 0) + fl
        counts[isl] = counts.get(isl, 0) + 1
    return {isl.title(): sums[isl]/counts[isl] for isl in sums if counts[isl] > 0}


def sex_ratio_by_species_on_dream(data):
    """% male vs female within each species on Dream Island."""
    dream = [r for r in data if (r.get("island") or "").strip().lower() == "dream"]
    counts, display = {}, {}
    for r in dream:
        sp = (r.get("species") or "").strip().lower()
        sx = (r.get("sex") or "").strip().lower()
        if sx not in ("male", "female") or not sp:
            continue
        if sp not in counts:
            counts[sp] = {"male": 0, "female": 0, "total": 0}
            display[sp] = sp.title()
        counts[sp][sx] += 1
        counts[sp]["total"] += 1
    out = {}
    for sp, c in counts.items():
        t = c["total"]
        if t > 0:
            out[display[sp]] = {"male_%": 100*c["male"]/t, "female_%": 100*c["female"]/t}
    return out

# Felicia's Functions

def percent_fem_bill_over_40_by_island(data):
    """% of FEMALE penguins with bill_length_mm > 40 per island."""
    counts = {}
    for row in data:
        sx = (row.get("sex") or "").strip().lower()
        isl = (row.get("island") or "").strip().lower()
        bl = row.get("bill_length_mm")
        if sx != "female" or not isl or bl is None:
            continue
        try:
            blv = float(bl)
        except:
            continue
        d = counts.setdefault(isl, {"pass": 0, "total": 0})
        d["total"] += 1
        if blv > 40.0:
            d["pass"] += 1
    return {isl.title(): 100*d["pass"]/d["total"] for isl, d in counts.items() if d["total"] > 0}


def percent_male_flip_under_180_by_species(data):
    """% of MALE penguins with flipper_length_mm < 180 per species."""
    counts = {}
    for row in data:
        sx = (row.get("sex") or "").strip().lower()
        sp = (row.get("species") or "").strip().lower()
        fl = row.get("flipper_length_mm")
        if sx != "male" or not sp or fl is None:
            continue
        try:
            flv = float(fl)
        except:
            continue
        d = counts.setdefault(sp, {"pass": 0, "total": 0})
        d["total"] += 1
        if flv < 180.0:
            d["pass"] += 1
    return {sp.title(): 100*d["pass"]/d["total"] for sp, d in counts.items() if d["total"] > 0}

# Huy's Functions

def calculate_percentage_of_male_penguins_over_threshold(data, threshold=4500.0):
    """% of MALE penguins heavier than threshold grams, by species."""
    counts = {}
    for row in data:
        sx = (row.get("sex") or "").strip().lower()
        sp = (row.get("species") or "").strip().lower()
        mass = row.get("body_mass_g")
        if sx != "male" or not sp or mass is None:
            continue
        try:
            mv = float(mass)
        except:
            continue
        d = counts.setdefault(sp, {"pass": 0, "total": 0})
        d["total"] += 1
        if mv > threshold:
            d["pass"] += 1
    return {sp.title(): 100*d["pass"]/d["total"] for sp, d in counts.items() if d["total"] > 0}


def calculate_avg_bill_depth_of_male_on_biscoe(data):
    """Average bill_depth_mm for MALE penguins on Biscoe Island."""
    vals = []
    for row in data:
        sx = (row.get("sex") or "").strip().lower()
        isl = (row.get("island") or "").strip().lower()
        bd = row.get("bill_depth_mm")
        if sx == "male" and isl == "biscoe" and bd is not None:
            try:
                vals.append(float(bd))
            except:
                continue
    avg = sum(vals)/len(vals) if vals else 0.0
    return {"Biscoe": avg}

# --------------- CSV OUTPUTS (main) ---------------

def _rows_from_dict(dct):
    """Helper: convert {key: value} to [[key, value], ...] with stable order."""
    return [[k, dct[k]] for k in sorted(dct.keys())]

def main():
    # Resolve penguins.csv relative to this file OR current working dir
    csv_name = "penguins.csv"
    if not os.path.exists(csv_name):
        here = os.path.dirname(__file__)
        candidate = os.path.join(here, csv_name)
        path = candidate if os.path.exists(candidate) else csv_name
    else:
        path = csv_name

    data = read_penguins(path)

    # John A
    j1 = avg_flipper_length_gentoo_by_island(data)
    write_results_to_csv(
        "avg_flipper_gentoo_by_island.csv",
        ["island", "avg_flipper_length_mm"],
        _rows_from_dict(j1),
    )

    # John B
    j2 = sex_ratio_by_species_on_dream(data)
    write_results_to_csv(
        "sex_ratio_by_species_on_dream.csv",
        ["species", "male_%", "female_%"],
        [[sp, vals["male_%"], vals["female_%"]] for sp, vals in sorted(j2.items())],
    )

    # Felicia A
    f1 = percent_fem_bill_over_40_by_island(data)
    write_results_to_csv(
        "percent_female_bill_gt40_by_island.csv",
        ["island", "percent_female_bill_gt_40"],
        _rows_from_dict(f1),
    )

    # Felicia B
    f2 = percent_male_flip_under_180_by_species(data)
    write_results_to_csv(
        "percent_male_flipper_lt180_by_species.csv",
        ["species", "percent_male_flipper_lt_180"],
        _rows_from_dict(f2),
    )

    # Huy A
    h1 = calculate_percentage_of_male_penguins_over_threshold(data, threshold=4500.0)
    write_results_to_csv(
        "percent_male_heavy_gt4500_by_species.csv",
        ["species", "percent_male_heavy_gt_4500"],
        _rows_from_dict(h1),
    )

    # Huy B
    h2 = calculate_avg_bill_depth_of_male_on_biscoe(data)  # {"Biscoe": avg}
    write_results_to_csv(
        "avg_bill_depth_male_biscoe.csv",
        ["island", "avg_bill_depth_mm_male"],
        _rows_from_dict(h2),
    )

if __name__ == "__main__":
    main()
