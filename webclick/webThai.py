import pyautogui
import time
import math
from tkinter import Tk, Label, Entry, Button
import sys
import os

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def locate_image_with_retry(image_path, retries=10, confidence=0.8, delay=1):
    img_path_con = resource_path(image_path)
    for attempt in range(retries):
        try:
            position = pyautogui.locateCenterOnScreen(img_path_con, confidence=confidence)
            if position:
                return position
        except pyautogui.ImageNotFoundException:
            pass
        time.sleep(delay)
    return None

def start_process(rows, inputrowsEP, nextCal):
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

    while True:
        if endloop == rows:
            print(f'***********{endloop}*********')
            break
        
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

    position_singel_save_last = locate_image_with_retry('./img/singel_save.png', retries=1, confidence=0.8, delay=1)
    if position_singel_save_last:
        pyautogui.moveTo(position_singel_save_last)
        pyautogui.click()
        time.sleep(0.5)
    else:
        print('position_singel_save_last not found after retry')


def run_ui():
    window = Tk()
    window.title("Automation Tool")

    Label(window, text="Rows").grid(row=0, column=0)
    rows_entry = Entry(window)
    rows_entry.grid(row=0, column=1)

    Label(window, text="Input Rows Per Page").grid(row=1, column=0)
    inputrowsEP_entry = Entry(window)
    inputrowsEP_entry.grid(row=1, column=1)

    Label(window, text="Next Cal (comma-separated)").grid(row=2, column=0)
    nextCal_entry = Entry(window)
    nextCal_entry.grid(row=2, column=1)

    def on_submit():
        rows = rows_entry.get()
        inputrowsEP = inputrowsEP_entry.get()
        nextCal = nextCal_entry.get()
        start_process(rows, inputrowsEP, nextCal)

    Button(window, text="Start", command=on_submit).grid(row=3, column=1)

    window.mainloop()

if __name__ == "__main__":
    run_ui()
