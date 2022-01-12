import functions as fx
import csv
import numpy as np

def redundant_overview():
    """makes a file (dataframe) overview of all materials currently in the course"""
    missions_df = fx.csv_to_df('export_missions.csv')
    chapters_df = fx.csv_to_df('export_chapters.csv')
    levels_df = fx.csv_to_df('export_levels.csv')
    blocks_df = fx.csv_to_df('export_blocks.csv')

    with open('overview_blocks (redundant).csv', 'w', newline='') as f:
        print('making a new redundant overview')
        writer = csv.writer(f, delimiter=';')
        writer.writerow(('block_id', 'block_type', 'block_number', 'block_page', 'level_id', 'level_name', 'level_type',
                         'chapter_id', 'chapter_name', 'mission_id', 'mission_name'))
        for mission in missions_df.iterrows():
            mission_name = mission[1].iloc[2]
            mission_id = mission[1].iloc[0]
            print(mission_name)

            for chapter in chapters_df.iterrows():
                chapter_id = chapter[1].iloc[0]
                chapter_name = chapter[1].iloc[2]
                # print("      ", chapter_name)

                if chapter[1].iloc[1] == mission_id:  # if mission IDs convenant

                    for level in levels_df.iterrows():
                        level_id = level[1].iloc[0]
                        level_name = level[1].iloc[3]
                        level_type = level[1].iloc[7]

                        for block in blocks_df.iterrows():
                            block_id = block[1].iloc[0]
                            block_type = block[1].iloc[2]
                            block_number = block[1].iloc[3]
                            block_page = block[1].iloc[5]
                            if block[1].iloc[1] == level_id:
                                #                                 print(3*"      ", block_id)
                                writer.writerow((block_id, block_type, block_number, block_page, level_id, level_name,
                                                 level_type, chapter_id, chapter_name, mission_id, mission_name))

        # Hieronder nog Primm-Hints
        print('now primm')
        levels_df  = levels_df[levels_df['type'].isin(set(['primm_predict', 'primm_modify', 'primm_quiz', 'primm_create', 'primm_use']))]

        block_id = np.nan
        block_type = np.nan
        block_number = np.nan
        block_page = np.nan
        level_id = np.nan
        level_name = np.nan
        level_type = np.nan
        chapter_id = np.nan
        chapter_name = np.nan
        mission_id = np.nan
        mission_name = np.nan

        for level in levels_df.iterrows():
            #     print(level[:])
            level_id = level[1][0]
            level_name = level[1][3]
            level_type = level[1][7]
            chapter_id = level[1][1]
            if chapters_df[chapters_df['id'] == chapter_id]['name'].values.tolist():
                chapter_name = chapters_df[chapters_df['id'] == chapter_id]['name'].values.tolist()[0]
                mission_id = chapters_df[chapters_df['id'] == chapter_id]['mission_id'].values.tolist()[0]
                mission_name = missions_df[missions_df['id'] == mission_id]['name'].values.tolist()[0]
            else:
                chapter_name = 'xxx'
                mission_id = 'xxx'
                mission_name = 'xxx'

            writer.writerow((block_id, block_type, block_number, block_page, level_id, level_name, level_type,
                             chapter_id, chapter_name, mission_id, mission_name))
        print('done!')

redundant_overview()