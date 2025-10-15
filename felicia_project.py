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

