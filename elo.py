import pandas as pd
import numpy as np

def setup(teams, rd):
    aff = pd.merge(rd, teams, left_on='Aff', right_on='Team', suffixes=('', '_Aff'))
    neg = pd.merge(rd, teams, left_on='Neg', right_on='Team', suffixes=('', '_Neg'))
    return aff, neg

def compute_new_elo(aff, neg, weight):
    win_aff = aff['Win'] == 'Aff'
    win_neg = aff['Win'] == 'Neg'

    # Calculate expected scores
    expected_aff = 1 / (1 + 10 ** ((neg['ELO'] - aff['ELO']) / 400))
    expected_neg = 1 / (1 + 10 ** ((aff['ELO'] - neg['ELO']) / 400))
    expected_aff_aff = 1 / (1 + 10 ** ((neg['Neg_ELO'] - aff['Aff_ELO']) / 400))
    expected_neg_neg = 1 / (1 + 10 ** ((aff['Aff_ELO'] - neg['Neg_ELO']) / 400))

    # Update ELOs
    aff['New_ELO'] = aff['ELO'] + (weight * 16) * (win_aff - expected_aff)
    neg['New_ELO'] = neg['ELO'] + (weight * 16) * (win_neg - expected_neg)
    aff['New_Aff_ELO'] = aff['Aff_ELO'] + (weight * 16) * (win_aff - expected_aff_aff)
    neg['New_Neg_ELO'] = neg['Neg_ELO'] + (weight * 16) * (win_neg - expected_neg_neg)

    return aff[['Aff', 'New_ELO', 'New_Aff_ELO']], neg[['Neg', 'New_ELO', 'New_Neg_ELO']]

def elo_merge(teams, aff, neg):
    # Update aff data
    aff_updates = aff.dropna(subset=['New_ELO'])
    teams = teams.merge(aff_updates[['Aff', 'New_ELO', 'New_Aff_ELO']], 
                        left_on='Team', right_on='Aff', how='left')
    teams['ELO'] = teams['New_ELO'].combine_first(teams['ELO'])
    teams['Aff_ELO'] = teams['New_Aff_ELO'].combine_first(teams['Aff_ELO'])
    teams['Aff_Rounds'] = teams['Aff_Rounds'] + teams['New_Aff_ELO'].notna().astype(int)
    teams.drop(columns=['Aff', 'New_ELO', 'New_Aff_ELO'], inplace=True)

    # Update neg data
    neg_updates = neg.dropna(subset=['New_ELO'])
    teams = teams.merge(neg_updates[['Neg', 'New_ELO', 'New_Neg_ELO']], 
                        left_on='Team', right_on='Neg', how='left')
    teams['ELO'] = teams['New_ELO'].combine_first(teams['ELO'])
    teams['Neg_ELO'] = teams['New_Neg_ELO'].combine_first(teams['Neg_ELO'])
    teams['Neg_Rounds'] = teams['Neg_Rounds'] + teams['New_Neg_ELO'].notna().astype(int)
    teams.drop(columns=['Neg', 'New_ELO', 'New_Neg_ELO'], inplace=True)

    return teams[['Team', 'ELO', 'Aff_ELO', 'Neg_ELO', 'Aff_Rounds', 'Neg_Rounds']]

def elo_all(teams, rd, weight):
    # Prepare and compute new ELOs
    aff, neg = setup(teams, rd)
    aff, neg = compute_new_elo(aff, neg, weight)

    # Merge updates back into teams
    return elo_merge(teams, aff, neg)

rds = ['uk_1', 'uk_2', 'uk_3', 'uk_4', 'uk_5', 'uk_6', 'uk_octas', 'uk_quarters', 'uk_semis', 'uk_finals', \
        'niles_1', 'niles_2', 'niles_3', 'niles_4', 'niles_5', 'niles_6', 'niles_dubs', 'niles_octas', 'niles_quarters', 'niles_semis', 'niles_finals', \
        'grapevine_1', 'grapevine_2', 'grapevine_3', 'grapevine_4', 'grapevine_5', 'grapevine_6', \
            'grapevine_dubs', 'grapevine_octas', 'grapevine_quarters', 'grapevine_semis', 'grapevine_finals', \
        'waru_1', 'waru_2', 'waru_3', 'waru_4', 'waru_5', 'waru_6', 'waru_octas', 'waru_quarters', 'waru_semis', 'waru_finals', \
        'greenhill_1', 'greenhill_2', 'greenhill_3', 'greenhill_4', 'greenhill_5', 'greenhill_6', \
             'greenhill_dubs', 'greenhill_octas', 'greenhill_quarters', 'greenhill_semis', 'greenhill_finals', \
        'bvsw_1', 'bvsw_2', 'bvsw_3', 'bvsw_4', 'bvsw_5', 'bvsw_6', 'bvsw_octas', 'bvsw_quarters', 'bvsw_semis', 'bvsw_finals', \
        'lb_1', 'lb_2', 'lb_3', 'lb_4', 'lb_5', 'lb_6', 'lb_dubs', 'lb_octas', 'lb_quarters', 'lb_semis', \
        'gds_1', 'gds_2', 'gds_3', 'gds_4', 'gds_5', 'gds_6', 'gds_octas', 'gds_quarters', 'gds_finals', \
        'marist_1', 'marist_2', 'marist_3', 'marist_4', 'marist_5', 'marist_6', 'marist_octas', 'marist_quarters', 'marist_semis', 'marist_finals', \
        'mac_1', 'mac_2', 'mac_3', 'mac_4', 'mac_5', 'mac_6', 'mac_octas', 'mac_quarters', 'mac_semis', 'mac_finals', \
        'delores_1', 'delores_2', 'delores_3', 'delores_4', 'delores_5', 'delores_6', 'delores_octas', 'delores_quarters', 'delores_semis', 'delores_finals', \
        'tw_1', 'tw_2', 'tw_3', 'tw_4', 'tw_5', 'tw_quarters', 'tw_finals', \
        'jwp_1', 'jwp_2', 'jwp_3', 'jwp_4', 'jwp_5', 'jwp_6', 'jwp_octas', 'jwp_quarters', 'jwp_semis', 'jwp_finals', \
        'wm_1', 'wm_2', 'wm_3', 'wm_4', 'wm_5', 'wm_6', 'wm_octas', 'wm_quarters', 'wm_semis', 'wm_finals', \
        'nyc_1', 'nyc_2', 'nyc_3', 'nyc_4', 'nyc_5', 'nyc_6', 'nyc_dubs', 'nyc_octas', 'nyc_quarters', 'nyc_semis', \
        'nt_1', 'nt_2', 'nt_3', 'nt_4', 'nt_5', 'nt_6', 'nt_dubs', 'nt_octas', 'nt_quarters', 'nt_semis', 'nt_finals', \
        'meadows_1', 'meadows_2', 'meadows_3', 'meadows_4', 'meadows_5', 'meadows_6', \
            'meadows_octas', 'meadows_quarters', 'meadows_semis', 'meadows_finals', \
        'hot_1', 'hot_2', 'hot_3', 'hot_4', 'hot_5', 'hot_6', 'hot_dubs', 'hot_octas', 'hot_quarters', 'hot_semis', 'hot_finals', \
        'iowa_1', 'iowa_2', 'iowa_3', 'iowa_4', 'iowa_5', 'iowa_6', 'iowa_octas', 'iowa_quarters', 'iowa_semis', 'iowa_finals', \
        'kcc_1', 'kcc_2', 'kcc_3', 'kcc_4', 'kcc_5', 'kcc_6', 'kcc_dubs', 'kcc_octas', 'kcc_quarters', 'kcc_semis', 'kcc_finals', \
        'udd_1', 'udd_2', 'udd_3', 'udd_4', 'udd_5', 'udd_6', 'udd_octas', 'udd_quarters', 'udd_semis', 'udd_finals', \
        'damus_1', 'damus_2', 'damus_3', 'damus_4', 'damus_5', 'damus_6', 'damus_octas', 'damus_quarters', 'damus_semis', 'damus_finals', \
        'mich_1', 'mich_2', 'mich_3', 'mich_4', 'mich_5', 'mich_6', 'mich_dubs', 'mich_octas', 'mich_quarters', 'mich_semis', 'mich_finals', \
        'gbx_1', 'gbx_2', 'gbx_3', 'gbx_4', 'gbx_5', 'gbx_6', 'gbx_7', 'gbx_dubs', 'gbx_octas', 'gbx_quarters', 'gbx_semis', 'gbx_finals', \
        'alta_1', 'alta_2', 'alta_3', 'alta_4', 'alta_5', 'alta_6', 'alta_octas', 'alta_quarters', 'alta_semis', \
        'ut_1', 'ut_2', 'ut_3', 'ut_4', 'ut_5', 'ut_6', 'ut_dubs', 'ut_octas', 'ut_quarters', 'ut_semis', \
        'mamo_1', 'mamo_2', 'mamo_3', 'mamo_4', 'mamo_5', 'mamo_6', 'mamo_octas', 'mamo_quarters', 'mamo_semis', 'mamo_finals', \
        'ds1_1', 'ds1_2', 'ds1_3', 'ds1_4', 'ds1_5', 'ds1_6', 'ds1_dubs', 'ds1_octas', 'ds1_quarters', 'ds1_semis', 'ds1_finals', \
        'lcc_1', 'lcc_2', 'lcc_3', 'lcc_4', 'lcc_5', 'lcc_6', 'lcc_octas', 'lcc_quarters', 'lcc_semis', 'lcc_finals', \
        'in_1', 'in_2', 'in_3', 'in_4', 'in_5', 'in_6', 'in_quarters', 'in_semis', \
        'dowling_1', 'dowling_2', 'dowling_3', 'dowling_4', 'dowling_5', 'dowling_6', 'dowling_octas', 'dowling_quarters', 'dowling_semis', \
        'blake_1', 'blake_2', 'blake_3', 'blake_4', 'blake_5', 'blake_6', 'blake_7', 'blake_dubs', 'blake_octas', 'blake_quarters', 'blake_semis', \
        'mba_1', 'mba_2', 'mba_3', 'mba_4', 'mba_5', 'mba_6', 'mba_octas', 'mba_quarters', 'mba_semis', 'mba_finals', \
        'asu_1', 'asu_2', 'asu_3', 'asu_4', 'asu_5', 'asu_6', 'asu_octas', 'asu_quarters', 'asu_semis', \
        'gonzaga_1', 'gonzaga_2', 'gonzaga_3', 'gonzaga_4', 'gonzaga_5', 'gonzaga_6', 'gonzaga_octas', 'gonzaga_quarters', 'gonzaga_semis', 'gonzaga_finals', \
        'sunvite_1', 'sunvite_2', 'sunvite_3', 'sunvite_4', 'sunvite_5', 'sunvite_semis', 'sunvite_finals', \
        'pen_1', 'pen_2', 'pen_3', 'pen_4', 'pen_5', 'pen_6', 'pen_octas', 'pen_quarters', 'pen_semis', 'pen_finals', \
        'samford_1', 'samford_2', 'samford_3', 'samford_4', 'samford_5', 'samford_6', 'samford_octas', 'samford_quarters', 'samford_semis', \
        'uh_1', 'uh_2', 'uh_3', 'uh_4', 'uh_5', 'uh_6', 'uh_octas', 'uh_quarters', 'uh_semis', 'uh_finals', \
        'vernon_1', 'vernon_2', 'vernon_3', 'vernon_4', 'vernon_5', 'vernon_quarters', 'vernon_semis', \
        'jw_1', 'jw_2', 'jw_3', 'jw_4', 'jw_5', 'jw_quarters', 'jw_semis', \
        'lex_1', 'lex_2', 'lex_3', 'lex_4', 'lex_5', 'lex_dubs', 'lex_octas', 'lex_quarters', 'lex_semis', \
        'bfhs_1', 'bfhs_2', 'bfhs_3', 'bfhs_4', 'bfhs_5', 'bfhs_6', 'bfhs_dubs', 'bfhs_octas', 'bfhs_quarters', 'bfhs_semis', 'bfhs_finals', \
        'icc_1', 'icc_2', 'icc_3', 'icc_4', 'icc_5', 'icc_6', 'icc_quarters', 'icc_semis']
results = []
for i in rds:
    results.append(pd.DataFrame(pd.read_csv('data_ip/'+i+'.csv')))
weight_map = {
    **{key: 0.875 for key in range(0,10)},
    **{key: 0.75 for key in range(10,21)},
    **{key: 0.875 for key in range(21,32)},
    **{key: 0.75 for key in range(32,42)},
    **{key: 1 for key in range(42,53)},
    **{key: 0.625 for key in range(53,63)},
    **{key: 0.875 for key in range(63,73)},
    **{key: 0.75 for key in range(73,82)},
    **{key: 0.625 for key in range(82,92)},
    **{key: 0.75 for key in range(92,102)},
    **{key: 0.625 for key in range(102,119)},
    **{key: 0.75 for key in range(119,139)},
    **{key: 0.875 for key in range(139,170)},
    **{key: 1 for key in range(170,181)},
    **{key: 0.75 for key in range(181,212)},
    **{key: 0.875 for key in range(212,233)},
    **{key: 1 for key in range(233,245)},
    **{key: 0.875 for key in range(245,274)},
    **{key: 0.75 for key in range(274,285)},
    **{key: 0.625 for key in range(285,303)},
    **{key: 0.875 for key in range(303,312)},
    **{key: 1 for key in range(312,333)},
    **{key: 0.875 for key in range(333,342)},
    **{key: 0.75 for key in range(342,352)},
    **{key: 0.625 for key in range(352,359)},
    **{key: 0.875 for key in range(359,369)},
    **{key: 0.75 for key in range(369,388)},
    **{key: 0.625 for key in range(388,402)},
    **{key: 0.875 for key in range(402,411)},
    **{key: 1 for key in range(411,422)},
    **{key: 0.625 for key in range(422,430)}
}
decay_map = {
    **{key: np.exp(-0.1 * 4) for key in range(0,53)},
    **{key: np.exp(-0.1 * 3) for key in range(53,181)},
    **{key: np.exp(-0.1 * 2) for key in range(181,245)},
    **{key: np.exp(-0.1 * 1) for key in range(245,333)},
    **{key: np.exp(-0.1 * 0) for key in range(333,430)}
}

real_map = {
    **{key: decay_map.get(key) * weight_map.get(key) for key in range(0,430)}
}

teams = pd.read_csv('teams_ip_NEW.csv')
for i in range(100):
    for k in range(len(rds)):
        teams = elo_all(teams, results[k], real_map.get(k) * (1/(1 + np.exp(-0.5*(i-50)))))
teams[['ELO', 'Aff_ELO', 'Neg_ELO']] = round(teams[['ELO', 'Aff_ELO', 'Neg_ELO']], 3)
teams[['Aff_Rounds', 'Neg_Rounds']] /= 100
teams.to_csv('teams_emory.csv')