import time
import os
import sys
import matplotlib.pyplot as plt

def print_row(max_widths, row, header=False):
    """Prints a database table row with each cell the max_width size"""
    print("| ", end="")
    for index, arg in enumerate(row):
        if type(arg) != str:
            arg = str(arg)
        print(f"{arg:^{max_widths[index]}} | ", end="")
    print()
    if header:
        for _ in range(sum(max_widths.values()) + 3 * len(row) + 1):
            print("-", end="")
        print()

def get_max_widths(headers, result):
    """Get the length of the longest cell in a collumn and store it in max_widths"""
    max_widths = {}
    for index, header in enumerate(headers):
        if index not in max_widths.keys():
            max_widths[index] = 0
        max_widths[index] = max(max_widths[index], len(header))
    for row in result:
        for index, cell in enumerate(row):
            if type(cell) != str:
                cell = str(cell)
            max_widths[index] = max(max_widths[index], len(cell))
    return max_widths

def print_query(cnx, query):
    db_cursor = cnx.cursor()
    try:
        db_cursor.execute(query)
    except:
        os.system("cls" if os.name == "nt" else "clear")
        print("Invalid Query")
        time.sleep(1)
        return None

    # Get results and headers
    headers = [header[0] for header in db_cursor.description]
    result = db_cursor.fetchall()

    # Get the length of the longest cell in a collumn and store it in max_widths
    max_widths = get_max_widths(headers, result)
    
    # Format print the collumn headers
    print_row(max_widths, headers, header=True)

    # Format print each row
    for row in result:
        print_row(max_widths, row)

    db_cursor.close()
    return (headers, result)

def show_plot(x, y, x_label, y_label, title, chart_type):
    if chart_type == "bar":
        plt.bar(x, y, width=0.5, color='blue')
    elif chart_type == "barh":
        plt.barh(x, y, 0.5, color='blue')
        for index, value in enumerate(y):
            plt.text(value + 0.05, index, str(value), color='blue', fontweight='bold')
    elif chart_type == "scatter":
        plt.scatter(x, y, 0.5, 'blue')
    else:
        return None

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 7:
        print(sys.argv)
        print("USAGE: python3 sql_helper.py [x] [y] [x_label] [y_label] [title] [chart_type]")
        exit()
    x = []
    y = []
    for char in sys.argv[1].strip("[]").split(","):
        char = char.strip(" ")
        try:
            unit = float(char)
        except:
            char = char.strip("'")
            unit = str(char)
        if unit:
            x.append(unit)
    
    for char in sys.argv[2].strip("[]").split(","):
        char = char.strip(" ")
        try:
            unit = float(char)
        except:
            char = char.strip("'")
            unit = str(char)
        if unit:
            y.append(unit)

    show_plot(x, y, *sys.argv[3:])
