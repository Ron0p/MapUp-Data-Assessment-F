import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Question 1

    dfx = df.pivot(index='id_1', columns='id_2', values='distance').fillna(0)
    dfx = dfx + dfx.T
    dfx.values[[range(len(dfx))]*2] = 0

    return dfx

# df_task2_q1 = pd.read_csv('dataset-3.csv')
# distance_matrix = calculate_distance_matrix(df_task2_q1)
# print("Task 2 Question 1 - Distance Matrix:")
# print(distance_matrix)


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Question 2

    df_unrolled = df.unstack().reset_index()
    df_unrolled.columns = ['id_start', 'id_end', 'distance']
    df_unrolled = df_unrolled[df_unrolled['id_start'] != df_unrolled['id_end']].reset_index(drop=True)
    
    return df_unrolled

# df_task2_q2 = distance_matrix 
# unrolled_distances = unroll_distance_matrix(df_task2_q2)
# print("\nTask 2 Question 2 - Unrolled Distances:")
# print(unrolled_distances)



def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Question 3

    ref_avg_dist = df[df['id_start'] == reference_id]['distance'].mean()
    threshold_min = ref_avg_dist - 0.1 * ref_avg_dist
    threshold_max = ref_avg_dist + 0.1 * ref_avg_dist
    result_df = df.groupby('id_start')['distance'].mean().reset_index()
    result_df = result_df[(result_df['distance'] >= threshold_min) & (result_df['distance'] <= threshold_max)].sort_values(by='id_start')
    
    return result_df

# df_task2_q3 = unrolled_distances  
# reference_id_q3 = 123  # Replace desired reference ID
# ids_within_threshold = find_ids_within_ten_percentage_threshold(df_task2_q3, reference_id_q3)
# print("\nTask 2 Question 3 - IDs within 10% Threshold:")
# print(ids_within_threshold)




def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Question 4

    df['moto'] = df['distance'] * 0.8
    df['car'] = df['distance'] * 1.2
    df['rv'] = df['distance'] * 1.5
    df['bus'] = df['distance'] * 2.2
    df['truck'] = df['distance'] * 3.6

    return df

# df_task2_q4 = unrolled_distances 
# toll_rates = calculate_toll_rate(df_task2_q4)
# print("\nTask 2 Question 4 - Toll Rates:")
# print(toll_rates)


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Question 5

    df['start_time'] = pd.to_datetime(df['start_time']).dt.time
    df['end_time'] = pd.to_datetime(df['end_time']).dt.time

    weekday_ranges = [('00:00:00', '10:00:00', 0.8), ('10:00:00', '18:00:00', 1.2), ('18:00:00', '23:59:59', 0.8)]
    weekend_range = ('00:00:00', '23:59:59', 0.7)

    def apply_discount(row):
        time_range = weekday_ranges if row['start_day'] in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'] else [weekend_range]
        for start, end, discount in time_range:
            mask = (start <= str(row['start_time'])) & (str(row['start_time']) <= end) & (start <= str(row['end_time'])) & (str(row['end_time']) <= end)
            row['moto':'truck'] *= discount * mask
        return row

    df = df.apply(apply_discount, axis=1)

    return df

# df_task2_q5 = unrolled_distances  
# time_based_toll_rates = calculate_time_based_toll_rates(df_task2_q5)
# print("\nTask 2 Question 5 - Time-Based Toll Rates:")
# print(time_based_toll_rates)
    
