from oauth2client.service_account import ServiceAccountCredentials
import gspread
import tkinter
import csv


def authorise():
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
        ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/lauraturnbull/Documents/personal/griddle-earth/configs/sheets-credentials.json', scope)
    client = gspread.authorize(creds)
    return client


# def add_textbox(root):
#
#     ent = tkinter.Text(root)
#     ent.pack()
#
#     all_entries.append(ent)


def visualise_map():
    client = authorise()

    root = tkinter.Tk()

    sheet = client.open("griddle earth map").sheet1
    values = sheet.get_all_values()
    values = values[1:]
    for row in values:
        if row[0] and row[1]:
            x = int(row[0])
            y = int(row[1])

            label = tkinter.Label(root, wraplength=150, text=row[3], relief=tkinter.RIDGE)
            label.grid(column=x, row=y*2 -1)

            # description textbox
            box = tkinter.Text(root, height=10, width=22, wrap="word", font=("Helvetica", 12))
            # *2 to height so we can add labels in between
            box.grid(column=x, row=y*2)
            box.insert("1.0", row[4])

    # cols, rows = root.grid_size()
    #
    # bottom_row_button = tkinter.Button(root, text="+")
    # bottom_row_button.grid(column=0, row=0, sticky="sw")
    #
    # # button = tkinter.Button(root, text="%s,%s" % (y * 2, x), command=lambda r=y * 2, c=x: add_textbox(root, r, c))

    root.mainloop()


if __name__ == "__main__":
    visualise_map()
