import pyautogui
import time
import math
from tkinter import Tk, Label, Entry, Button, StringVar
import sys
import os

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def locate_image_with_retry(image_path, retries=10, confidence=0.8, delay=1):
    img_path_con = resource_path(image_path)
    for attempt in range(retries + 5):
        try:
            position = pyautogui.locateCenterOnScreen(img_path_con, confidence=confidence)
            if position:
                return position
        except pyautogui.ImageNotFoundException:
            pyautogui.moveTo(x=150, y=150)
            pyautogui.click()
            pass
        time.sleep(delay)
    return None

def start_process(rows, inputrowsEP, nextCal, label_var, inputJump):
    rows = int(rows)
    inputrowsEP = int(inputrowsEP)
    nextCal = [int(x) for x in nextCal.split(',')]
    
    average = sum(nextCal) / len(nextCal)
    rowsEP = inputrowsEP + 1
    endloop = 1
    nextRow = round(average)
    page = math.ceil(rows / rowsEP)
    currentPage = 1
    i = 1

    # Adjust starting point if jump is specified
    jump = int(inputJump) - 1
    if jump > 0:
        currentPage = math.ceil(jump / inputrowsEP)
        i = jump % inputrowsEP
        if i == 0:
            i = inputrowsEP
        endloop = jump

    while True:
        label_var.set(f'{endloop} / {rows}')
        
        if endloop == rows + 1:
            print(f'***********{endloop}*********')
            break
        
        if jump < 1:
            if i == rowsEP:
                time.sleep(0.5)
                i = 1
                currentPage += 1
                time.sleep(0.5)
                print(f'{currentPage}>>>>>>>>changedPage<<<<<<<<')
            else:
                time.sleep(0.5)

                position = locate_image_with_retry('./img/store.png', retries=1, confidence=0.8, delay=1)
                if position:
                    pyautogui.moveTo(position.x, position.y + (i * nextRow))
                    pyautogui.click()
                    time.sleep(1)

                    position_singel_save = locate_image_with_retry('./img/singel_save.png', retries=1, confidence=0.8, delay=1)
                    if position_singel_save:
                        pyautogui.moveTo(position_singel_save)
                        pyautogui.click()
                        time.sleep(0.5)

                        position_cat = locate_image_with_retry('./img/cat.png', retries=1, confidence=0.8, delay=1)
                        if position_cat:
                            pyautogui.moveTo(position_cat)
                            pyautogui.click()
                            time.sleep(0.2)
                            pyautogui.click()
                            time.sleep(0.1)

                            pyautogui.moveTo(x=25, y=76)
                            pyautogui.click()

                            print(f'////finish//// {currentPage}.{i}<<<easy {i} at --> {endloop}')
                            i += 1
                            endloop += 1
                            time.sleep(3)
                        else:
                            print('cat not found after retry')
                            break
                    else:
                        print('singel_save not found after retry')
                        break
                else:
                    print('store not found after retry')
                    break

        if currentPage > 1 and i != rowsEP:
            time.sleep(0.5)
            print(f' CHANGED PAGE >>>{currentPage}.{i}<<<')

            click_count = currentPage - 1
            for _ in range(click_count):
                pyautogui.moveTo(x=1802, y=1041)
                pyautogui.click()
                time.sleep(0.1)
        
        jump = 0

    position_singel_save_last = locate_image_with_retry('./img/singel_save.png', retries=1, confidence=0.8, delay=1)
    if position_singel_save_last:
        pyautogui.moveTo(position_singel_save_last)
        pyautogui.click()
        time.sleep(0.5)
    else:
        print('position_singel_save_last not found after retry')

def find_distance(label_var, nextCal_entry):
    label_var.set("Click on rows 1, 2, 3... in sequence")

    y_positions = []

    for i in range(5):  
        pyautogui.alert(f"press OK and then hover on row {i+1} ")
        time.sleep(2)  
        y_positions.append(pyautogui.position().y)

    # Calculate distances between each pair of y positions
    distances = [y_positions[i+1] - y_positions[i] for i in range(len(y_positions)-1)]
    
    nextCal_entry.set(",".join(map(str, distances)))
    label_var.set("Distances calculated and set")

def run_ui():
    window = Tk()
    window.title("Automation Tool")

    Label(window, text="Rows").grid(row=0, column=0)
    input_rows_entry = StringVar(value="85")
    rows_entry = Entry(window, textvariable=input_rows_entry)
    rows_entry.grid(row=0, column=1)

    Label(window, text="Rows Per Page").grid(row=1, column=0)
    inputrowsEP_var = StringVar(value="15")
    inputrowsEP_entry = Entry(window, textvariable=inputrowsEP_var)
    inputrowsEP_entry.grid(row=1, column=1)

    Label(window, text=" ").grid(row=2, column=1)

    Label(window, text="Next Cal").grid(row=3, column=0)
    Label(window, text="(comma-separated)").grid(row=4, column=0)
    input_nextCal_entry = StringVar(value="42")
    nextCal_entry = Entry(window, textvariable=input_nextCal_entry)
    nextCal_entry.grid(row=3, column=1)

    def on_submit():
        rows = rows_entry.get()
        inputrowsEP = inputrowsEP_entry.get()
        nextCal = nextCal_entry.get()
        start_process(rows, inputrowsEP, nextCal, label_var, 0)
        
    def on_Jump():
        rows = rows_entry.get()
        inputrowsEP = inputrowsEP_entry.get()
        nextCal = nextCal_entry.get()
        inputJump = inputJump_entry.get()
        start_process(rows, inputrowsEP, nextCal, label_var, inputJump)

    def on_find_distance():
        find_distance(label_var, input_nextCal_entry)

    Button(window, text="Start", command=on_submit).grid(row=6, column=1)
    Label(window, text=" ").grid(row=7, column=0)
    Button(window, text="Jump", command=on_Jump).grid(row=8, column=1)
    Button(window, text="Find Distance", command=on_find_distance).grid(row=2, column=0)
    
    # StringVar to hold the text for the label
    label_var = StringVar()
    label_var.set("endloop / inputrowsEP")
    
    Label(window, textvariable=label_var).grid(row=9, column=0)
    inputJump_entry = Entry(window)
    inputJump_entry.grid(row=8, column=0)
    Label(window, text=" ").grid(row=10, column=0)

    window.mainloop()
if __name__ == "__main__":
    run_ui()
