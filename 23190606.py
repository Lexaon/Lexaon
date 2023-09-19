def load_csv(filename):
    # Load CSV file into a list of dictionaries.
    data = []
    with open(filename, 'r') as file:
        # Extract the headers
        headers = file.readline().strip().split(',')
        
        # Read each line and convert it into a dictionary
        for line in file:
            values = line.strip().split(',')
            record = {headers[i]: values[i] for i in range(len(headers))}
            data.append(record)
    
    return data

def max_min_employees(data, country):
    # Find organizations with the highest and lowest number of employees for a specific country founded between 1981 and 2000.
    max_employee_org = None
    min_employee_org = None
    max_employees = float('-inf')
    min_employees = float('inf')
    
    for record in data:
        if record['Country'] == country and 1981 <= int(record['Founded']) <= 2000:
            num_employees = int(record['Number of employees'])
            if num_employees > max_employees:
                max_employees = num_employees
                max_employee_org = record['Name']
            if num_employees < min_employees:
                min_employees = num_employees
                min_employee_org = record['Name']
    
    return [max_employee_org, min_employee_org]

def calculate_std_dev(data, country):
    # Compute the standard deviations for the median salary for organizations of a specific country and for all organizations.
    salaries_country = [int(record['Median Salary']) for record in data if record['Country'] == country]
    salaries_all = [int(record['Median Salary']) for record in data]
    
    def std_dev(values):
        n = len(values)
        if n == 0:
            return 0  # Return 0 if there are no values
        mean = sum(values) / n
        variance = sum((x - mean) ** 2 for x in values) / (n - 1)  # Using n-1 for sample standard deviation
        return variance ** 0.5 if variance > 0 else 0  # Return 0 if variance is 0
    
    return [round(std_dev(salaries_country), 4), round(std_dev(salaries_all), 4)]

def calculate_ratio(data, country):
    # Determine the ratio of profit increases to profit decreases between 2020 and 2021 for a specific country.
    profit_changes = [(int(record['Profits in 2021(Million)']) - int(record['Profits in 2020(Million)'])) for record in data if record['Country'] == country]
    
    positive_changes = sum(change for change in profit_changes if change > 0)
    negative_changes = abs(sum(change for change in profit_changes if change < 0))
    
    if negative_changes == 0:
        return 'Division by zero is not defined'
    
    ratio = positive_changes / negative_changes
    
    return round(ratio, 4)

def calculate_correlation(data, country):
    # Compute the correlation between the median salary and profits in 2021 for organizations in a specific country that show a profit increase from 2020 to 2021.
    salaries = []
    profits_2021 = []
    
    for record in data:
        if record['Country'] == country and int(record['Profits in 2021(Million)']) > int(record['Profits in 2020(Million)']):
            salaries.append(int(record['Median Salary']))
            profits_2021.append(int(record['Profits in 2021(Million)']))
    
    if not salaries or not profits_2021:
        return 0  # Return 0 if there are no data points
    
    mean_salary = sum(salaries) / len(salaries)
    mean_profit = sum(profits_2021) / len(profits_2021)
    
    numerator = sum((salaries[i] - mean_salary) * (profits_2021[i] - mean_profit) for i in range(len(salaries)))
    
    sum_x_squared = sum((x - mean_salary) ** 2 for x in salaries)
    sum_y_squared = sum((y - mean_profit) ** 2 for y in profits_2021)
    
    if sum_x_squared == 0 or sum_y_squared == 0:
        return 0  # Return 0 if the denominators are zero
    
    denominator = (sum_x_squared * sum_y_squared) ** 0.5
    
    correlation = numerator / denominator
    
    return round(correlation, 4)

def main(csvfile, country):
    data = load_csv(csvfile)
    
    max_min = max_min_employees(data, country)
    stdv = calculate_std_dev(data, country)
    ratio = calculate_ratio(data, country)
    corr = calculate_correlation(data, country)
    
    return max_min, stdv, ratio, corr

