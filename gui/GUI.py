from tkinter import *



class GUI(object):
    def __init__(self, master):

        def newButton(parent, cmd, buttontext):
            button = Button(parent, command=cmd, text = buttontext)
            button.configure(width=buttonWidth, padx=buttonPadx, pady=buttonPady )
            return button

        # Layout constants
        buttonWidth = 30
        buttonPadx = 2
        buttonPady = 1


        self.parent = master
        self.chapterText = dict()

        self.mainFrame = Frame(master, bg="Gray", relief=GROOVE)
        self.infoFrame = Frame(master, bg="Blue", relief=RAISED )

        # MAIN FRAME
        quitButton = newButton(self.mainFrame, self.terminate, 'Quit')
        quitButton.pack(pady=20, side=BOTTOM)

        self.subjectFrames = []
        subjects = open("gui/exampleText.txt").read().split('-----\n')
        topicCount = 0

        # Read from text file, creating frames with buttons for each topic.
        for subject in subjects:
            frame = Frame(master, bg="Gray", relief=GROOVE)
            subjectTitle = subject[:subject.index('\n')].strip()
            button = newButton(self.mainFrame, lambda c=self.mainFrame, n=frame: self.switchFrame(c,n), subjectTitle)
            button.pack(pady=10, side=TOP)


            topics = subject.split('\n\n')[1:]
            for topic in topics:
                topicTitle = topic[:topic.index('\n')].strip()
                text = topic[topic.index('\n'):].strip()
                self.chapterText[topicCount] = text

                button = newButton(frame, lambda c=frame, n=self.infoFrame, t=topicCount: self.switchFrame(c,n,t), topicTitle)
                button.pack(pady=10, side=TOP)

                topicCount += 1



            self.subjectFrames.append(frame)

        self.mainFrame.pack(expand=True, fill=BOTH)



        # INFORMATION FRAME

        self.text = StringVar()
        self.text.set("test")
        label = Label(self.infoFrame, textvariable=self.text, pady=2)
        label.pack(pady=20, side=TOP)

        quitButton = newButton(self.infoFrame, self.terminate, 'Quit')
        quitButton.pack(pady=20, side=BOTTOM)

        backButton = newButton(self.infoFrame, lambda: self.switchFrame(self.infoFrame, self.mainFrame), 'Back')
        backButton.pack(side=BOTTOM)


    def switchFrame(self, current, next, topic=-1):
        current.pack_forget()
        next.pack(expand=True, fill=BOTH)
        if topic != -1:
            self.lastFrame = current    
            self.text.set(self.chapterText[topic])
        

    def terminate(self):
        self.parent.destroy()




if __name__ == '__main__':
    root = Tk()
    root.geometry("450x300")
    app = GUI(root)
    root.mainloop()