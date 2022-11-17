import time
import os

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