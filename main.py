import tkinter as tk
from sys import exit
from random import randint
from time import sleep


class Window:
    """
    Class for creating the main window
    """

    def __init__(self):
        """
        Initiates a class to create a window with the required objects
        """

        self.root = tk.Tk()
        self.root.configure(background="black")
        self.root.minsize(width=800, height=600)
        #self.root.maxsize(width=800, height=600)
        self.quit_button = tk.Button(self.root, text="Quit", command=self.quit_program)
        self.quit_button.pack(side="bottom")
        self.canvas = tk.Canvas(background="grey")
        self.canvas.pack(side="top", fill="x", padx=20, pady=20)
        self.dice_frame = WindowFrame(self.canvas, "grey")
        self.dice_labels = DiceLabelFormat(self.dice_frame)
        self.control_frame = ControlFrame(self.root, "grey")
        self.control_components = ControlComponents(self.control_frame, self.dice_labels, self.dice_frame)

    def remove_dice(self):
        self.dice_labels.remove_dice_labels()
        self.root.update_idletasks()

    def quit_program(self):
        print("Quitting program")
        exit()


class WindowFrame:

    def __init__(self, window: tk, colour: str):
        """
        Creates a frame.
        :param window: Which window that the frame is to sit in
        :param colour: Which colour it should be
        """
        super().__init__()
        self.frame = tk.Frame(window, background=colour, relief="raised", borderwidth=2)
        self.frame.pack(side="top", fill="x", padx=5, pady=5)


class DiceLabelFormat:
    def __init__(self, frame: WindowFrame):
        """
        Groups all dice labels into an object.
        :param frame: The frame that the labels for the dice are to be placed in
        """
        self.dice_list = [[tk.Label(frame.frame, text="Description", background="grey"),
                           tk.Label(frame.frame, text="Number of sides", background="grey"),
                           tk.Label(frame.frame, text="Number rolled", background="grey")],
                          [tk.Label(frame.frame, text="6 sided dice", background="grey"),
                           tk.Label(frame.frame, text="6", background="grey"),
                           tk.Label(frame.frame, text="Ready to roll", background="grey")]]
        self.place_labels()

    def place_labels(self) -> None:
        """
        Places the labels into the appropriate grid layout
        :return:
        """
        for i in range(len(self.dice_list)):
            # print(i)
            for ii in range(len(self.dice_list[i])):
                # print("-", ii)
                self.dice_list[i][ii].grid(row=i + 1, column=ii, padx=10, pady=10, sticky="NSEW")
                self.dice_list[i][ii].rowconfigure(i, weight=1)
                self.dice_list[i][ii].columnconfigure(ii, weight=1)

    def add_dice_label(self, frame: WindowFrame, sides: int) -> None:
        """
        Adds a die to the list of dice
        :param frame: The frame that the labels are set in
        :param sides: The number of sides that dice has
        :return: Nothing
        """
        print("adding dice", sides)
        self.dice_list.append([tk.Label(frame.frame, text=f"{sides} sided dice", background="grey"),
                               tk.Label(frame.frame, text=sides, background="grey"),
                               tk.Label(frame.frame, text="Ready to roll", background="grey")])
        self.place_labels()

    def remove_dice_labels(self) -> None:
        """
        Deletes the last set of labels as long as it is not the title block
        :return:
        """
        if len(self.dice_list) > 1:
            for label in self.dice_list[-1]:
                label.destroy()
            del self.dice_list[-1]

    def roll_dice(self,frame: WindowFrame)-> None:
        counter = 50
        while counter > 0:
            counter -= 1
            sleep(0.1)
            # print("rolling "*5)
            for i in range(1,len(self.dice_list)):
                roll = randint(1,int(self.dice_list[i][1].cget("text")))
                self.dice_list[i][2].configure(text=roll, background="grey")
                # print(self.dice_list[i][2].cget("text"))
                frame.frame.winfo_toplevel().update()

        for dice in self.dice_list[1:]:
            try:
                if dice[1].cget("text") == dice[2].cget("text"):
                    dice[2].configure(background="Yellow")
                if int(dice[2].cget("text")) == 1:
                    dice[2].configure(background="red")
            except ValueError as e:
                print(e)
            frame.frame.winfo_toplevel().update_idletasks()

class ControlFrame:

    def __init__(self, master: tk, colour: str):
        self.frame = tk.Frame(master, background=colour, relief="raised", borderwidth=2)
        self.frame.pack(side="bottom", fill="x", padx=5, pady=5)


class ControlComponents:

    def __init__(self, master: ControlFrame, dice_label_class: DiceLabelFormat, dice_frame: WindowFrame):
        """
        Creates the instance for the control components
        :param master: The frame that the control components sit are to sit in
        :param dice_label_class: The object that holds all the dice labels
        :param dice_frame: The frame that holds all of the labels,
        this is for to call methods in the DiceLabelFormat class
        """
        self.dice_label_class = dice_label_class
        self.dice_window = dice_frame
        self.components = [tk.Button(master.frame, text="Remove last dice",
                                     command=dice_label_class.remove_dice_labels,
                                     relief="raised", borderwidth=2),
                           tk.Text(master.frame, height=1, width=5, relief="raised", borderwidth=2),
                           tk.Button(master.frame, text="Add", command=self.add_dice, relief="raised",
                                     borderwidth=2),
                           tk.Button(master.frame, text="roll",
                                     command=self.roll_dice,
                                     relief="raised",borderwidth=5)]
        self.components[3].pack(side="top", fill="x", padx=2, pady=2)
        self.components[0].pack(side="left", padx=2, pady=2)
        self.components[1].pack(side="right", padx=2, pady=2)
        self.components[2].pack(side="right", padx=2, pady=2)


    def add_dice(self):
        """
        Adds a group of dice labels the the list and updates the screen
        :return:
        """
        try:
            dice = int(self.components[1].get("1.0", "end-1c"))
            self.dice_label_class.add_dice_label(self.dice_window, dice)

        except ValueError as err:
           print(err)

    def roll_dice(self)->None:
        self.dice_label_class.roll_dice(self.dice_window)


def main():
    main_window = Window()
    main_window.root.mainloop()


if __name__ == '__main__':
    main()
