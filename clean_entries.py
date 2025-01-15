import pandas as pd


def find_duplicates(series):
    duplicates = []
    seen = set()
    for item in series:
        reversed_last_two = item[-2:][::-1]
        prefix = item[:-2]
        key = prefix + reversed_last_two
        if key in seen or item in seen:
            duplicates.append(item)
        else:
            seen.add(item)
            seen.add(key)
    return duplicates


def reverse(series):
    transformed = []
    for s in series:
        transformed.append(s[:-2] + s[-2:][::-1])
    return transformed


teams = pd.read_csv("teams_ip_NEW.csv")
dupes = find_duplicates(teams["Team"])
dupes2 = reverse(dupes)
df = pd.DataFrame({"1": dupes, "2": dupes2})

for i in range(len(df["1"])):
    print("df[col] = df[col].str.replace('" + df["2"][i] + "','" + df["1"][i] + "')")
