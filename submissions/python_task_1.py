import pandas as pd
import numpy as np

def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Question 1 
    
    car_df = df.pivot(index='id_1', index='id_2' values='car')
    car_df = car_df.fillna(0)
    np.fill_diagonal(car_df.values, 0)

    return car_df

# df_task1_q1 = pd.read_csv('dataset-1.csv')
# car_df = generate_car_matrix(df_task1_q1)
# print("Task 1 Question 1 - Car Matrix:")
# print(car_df)



def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Question 2

    df.loc[df['car'] <= 15, 'car_type'] = 'low'
    df.loc[(df['car'] > 15) & (df['car'] <= 25), 'car_type'] = 'medium'
    df.loc[df['car'] > 25, 'car_type'] = 'high'

    car_type_count = df['car_type'].value_counts().sort_index().to_dict()

    return car_type_count

# df_task1_q2 = pd.read_csv('dataset-1.csv')
# car_type_counts = get_type_count(df_task1_q2)
# print("\nTask 1 Question 2 - Car Type Counts:")
# print(car_type_counts)


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Question 3

    bus_mean = df['bus'].mean()
    bus_exc = df[df['bus'] > 2 * bus_mean].index.tolist()

    return bus_exc

# df_task1_q3 = pd.read_csv('dataset-1.csv')
# bus_exc = get_bus_indexes(df_task1_q3)
# print("\nTask 1 Question 3 - Bus Indexes:")
# print(bus_exc)


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Question 4

    route = df.groupby('route')['truck'].mean()
    routes7 = route.index[route > 7].tolist()
    sorted7 = sorted(routes7)

    return sorted7

# df_task1_q4 = pd.read_csv('dataset-1.csv')
# routes7 = filter_routes(df_task1_q4)
# print("\nTask 1 Question 4 - Filtered Routes:")
# print(routes7)



def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Question 5

    modi_matrix = (matrix > 20) * 0.75 + (matrix <= 20) * 1.25
    modi_matrix = modi_matrix.round(1)

    return modi_matrix

# df_task1_q5 = pd.read_csv('dataset-1.csv')
# car_matrix_task1_q5 = generate_car_matrix(df_task1_q5)
# modi_matrix = multiply_matrix(car_matrix_task1_q5)
# print("\nTask 1 Question 5 - Modified Matrix:")
# print(modi_matrix)



def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Question 6

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    group = df.groupby(['id', 'id_2'])
    diff = group['timestamp'].max() - group['timestamp'].min()
    complete = group['timestamp'].max().apply(lambda x: x.time() == pd.Timestamp('23:59:59').time())
    result_df = pd.DataFrame({'start_end_diff': diff, 'complete': complete})
    
    return result_df

# df_task1_q6 = pd.read_csv('dataset-2.csv')
# time_completeness = time_check(df_task1_q6)
# print("\nTask 1 Question 6 - Time Completeness:")
# print(time_completeness)