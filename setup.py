import pandas as pd

df = pd.read_csv("teams_ip.csv")
df2 = pd.read_csv("TOURNAMENT_entries.csv")
new = pd.concat([df["Team"], df2["Code"]]).drop_duplicates()
df3 = pd.DataFrame(
    {
        "Team": new,
        "ELO": 1600,
        "Aff_ELO": 1600,
        "Neg_ELO": 1600,
        "Aff_Rounds": 0,
        "Neg_Rounds": 0,
    }
)
df3.to_csv("teams_ip_NEW.csv")
