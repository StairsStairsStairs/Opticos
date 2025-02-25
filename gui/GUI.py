from tkinter import *
import cv2
'''
THINGS TO REDO:
Frame tuple system
Play buttons
Double window size and button size

THINGS TO REMEMBER:
git pull BEFORE trying to commit
Save backup of file in case you mess it up
DONT delete your local repo before checking that you didnt overwrite your files.
'''

class GUI(object):
    def __init__(self, master):

        def newButton(parent, cmd, buttontext):
            button = Button(parent, command=cmd, text = buttontext)
            button.configure(width=buttonWidth, padx=buttonPadx, pady=buttonPady )
            return button

        # Layout constants
        buttonWidth = 30
        buttonPadx = 2
        buttonPady = 10
        screenResolution = (900, 600)

        self.parent = master
        self.parent.geometry(str(screenResolution[0]) + 'x' + str(screenResolution[1]))

        self.chapterText = dict()
        self.frames = dict()
        self.currentFrameID = (0, 0)

        self.mainFrame = Frame(master, bg="Gray", relief=GROOVE)
        self.infoFrame = Frame(master, bg="Blue", relief=RAISED )

        # MAIN FRAME
        quitButton = newButton(self.mainFrame, self.terminate, 'Quit')
        quitButton.pack(pady=10, side=BOTTOM)

        self.frames[(0, 0)] = self.mainFrame
        subjects = open("gui/exampleText.txt").read().split('-----\n')

        # Read from text file, creating frames with buttons for each topic.
        for i in range(len(subjects)):
            subject = subjects[i]
            frame = Frame(master, bg="Gray", relief=GROOVE)
            self.frames[(i+1, 0)] = frame


            subjectTitle = subject[:subject.index('\n')].strip()
            subjectButton = newButton(self.mainFrame, lambda n=i+1: self.switchFrame((n, 0)), subjectTitle)
            subjectButton.pack(pady=10, side=TOP)
            backButton = newButton(frame, lambda: self.switchFrame((0, 0)), "Back")
            backButton.pack(pady=10, side=BOTTOM)

            topics = subject.split('\n\n')[1:]
            for j in range(len(topics)):
                topic = topics[j]
                topicTitle = topic[:topic.index('\n')].strip()
                text = topic[topic.index('\n'):].strip()
                self.frames[(i+1, j+1)] = self.infoFrame
                self.chapterText[(i+1, j+1)] = text
                

                topicButton = newButton(frame, lambda n=i+1, m=j+1: self.switchFrame((n, m)), topicTitle)
                topicButton.pack(pady=10, side=TOP)

        self.mainFrame.pack(expand=True, fill=BOTH)



        # INFORMATION FRAME

        self.text = StringVar()
        self.text.set("test")
        label = Label(self.infoFrame, textvariable=self.text, pady=2, 
                      wraplength=int(.7*screenResolution[0]))
        label.pack(pady=20, side=TOP)

        backButton = newButton(self.infoFrame, lambda: self.switchFrame((self.currentFrameID[0], 0)), 'Back')
        backButton.pack(pady=10, side=BOTTOM)

        videoButton = newButton(self.infoFrame, self.playVideo, "Play")
        videoButton.pack(pady=10, side=TOP)


    '''
    switchFrame takes the frame ID of the frame that is going to be loaded
    Frame IDs work as follows:
        (0, 0) is the main frame
        (#, 0) is the #th subject frame (i.e. (1, 0) is the frame for precalculus topics)
        (#, #) is the info frame with the text of topic #.# (i.e (1, 1) = topic 1.1: precalc.discontinuities)
    '''
    def switchFrame(self, nextID):
        self.frames[self.currentFrameID].pack_forget()
        next = self.frames[nextID]
        next.pack(expand=True, fill=BOTH)
        if nextID[1] != 0:
            self.text.set(self.chapterText[nextID])
        self.currentFrameID = nextID

    # Currently only plays one video, will either use a dict or generate the video through manim on demand   
    def playVideo(self):
        cap = cv2.VideoCapture('gui/stockmp4.mp4')
        if (cap.isOpened()== False):
            print("Error opening video file")
            return

        cv2.namedWindow('Animation')
        cv2.moveWindow('Animation', 40, 30)
        # Read video frame by frame
        while(cap.isOpened()):
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow('Animation', frame)
            
            # Press Q on keyboard to exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def terminate(self):
        self.parent.destroy()




if __name__ == '__main__':
    root = Tk()
    app = GUI(root)
    root.mainloop()