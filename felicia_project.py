# Name: Felicia Wang
# ID: 62645970
# Email: wangfeli@umich.edu
# Collaborators: Huy Pham, John (Yohan) Park
# Asked ChatGPT for hints and guidance on the structure

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
            # get numerator; may be absent
            if g in num_counts:
                n = num_counts[g]
            else:
                n = 0
            pct = (n * 100.0) / float(den)
        result[g] = pct
    return result
