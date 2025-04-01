from tkinter import *
from pathlib import Path
import cv2

class GUI(object):
    def __init__(self, master):
        ##### LAYOUT CONSTANTS #####
        # Application settings
        master.title("Opticos")
        root.resizable(False, False)
        screenResolution = (1600, 900)
        master.geometry(str(screenResolution[0]) + 'x' + str(screenResolution[1]))

        # Sizing and padding
        buttonWidth = screenResolution[0] // 30
        buttonPadx = buttonWidth // 15
        buttonPady = screenResolution[0] // 100
        objectPackPady = buttonPady

        # Color and font
        frameColor = "Gray"
        buttonFont = ('TkDefaultFont', 15)
        pageFont = ('TkDefaultFont', 12)
        
        ##### MEMBER VARIABLES #####
        # Set the root Tk() object and parent directory
        self.parent = master
        self.directory = Path(__file__).parent

        # Instantiate dictionaries to map frame IDs to frame and their corresponding text
        self.chapterText = dict()
        self.frames = dict()

        # Store the ID of the current frame at all times
        self.currentFrameID = (0, 0)

        ##### HELPER FUNCTIONS #####
        # Create and configure new button object
        def newButton(parent, cmd, buttontext):
            button = Button(parent, command=cmd, text = buttontext, font=buttonFont)
            button.configure(width=buttonWidth, padx=buttonPadx, pady=buttonPady)
            return button

        # Create a new information frame for a topic
        def newPage(text, canInputFunction=False):
            # Main frame of this page
            rootFrame = Frame(master, bg=frameColor, relief=RAISED)

            # Create a sub-frame that holds the text box and scrollbar
            textFrame = Frame(rootFrame, bg=frameColor, relief=RAISED, width=screenResolution[0]//1.4, height=screenResolution[1]//2)
            textFrame.pack(pady=objectPackPady, side=TOP)

            # Create and connect textbox and scrollbar
            pageText = Text(textFrame, font=pageFont, width=150, height=20)
            pageText.insert(END, text)
            pageText.configure(state=DISABLED)
            scrollBar = Scrollbar(textFrame, orient='vertical')
            scrollBar.config(command=pageText.yview)
            pageText['yscrollcommand'] = scrollBar.set

            # Pack the scrollbar and text into the text frame
            scrollBar.pack(side=RIGHT, fill='y')
            pageText.pack(side=LEFT)

            # Create an entry box and corresponding sub-frame if needed
            if canInputFunction:
                # Sub-frame for the entry and its label
                entryFrame = Frame(rootFrame, bg=frameColor, relief=RAISED, width=200, height=50)
                entryFrame.pack(side=TOP, pady=(50, 0))

                # Label for the entry frame
                entryLabel = Label(entryFrame, text="Function: ", pady=2, bg=frameColor)
                entryLabel.pack(padx=10, side=LEFT)

                # Entry box for the user to input a function
                functionBox = Entry(entryFrame)
                functionBox.pack(padx=5, side=RIGHT)

            # Button to play the page's video
            videoButton = newButton(rootFrame, lambda: self.playVideo(str(self.directory/'stockmp4.mp4')), "Play")
            videoButton.pack(pady=objectPackPady, side=TOP)

            # Button to go back and return the new page
            backButton = newButton(rootFrame, lambda: self.switchFrame((self.currentFrameID[0], 0)), 'Back')
            backButton.pack(pady=objectPackPady, side=BOTTOM)
            return rootFrame





        ##### MAIN FRAME #####
        mainFrame = Frame(master, bg=frameColor, relief=GROOVE)
        self.frames[(0, 0)] = mainFrame

        # Button to terminate the program
        quitButton = newButton(mainFrame, self.terminate, 'Quit')
        quitButton.pack(pady=objectPackPady, side=BOTTOM)

        # Button to test playing a manim mp4
        testManimButton = newButton(mainFrame, self.playManim, 'Manim')
        testManimButton.pack(pady=objectPackPady, side=BOTTOM)

        ##### OTHER FRAMES #####
        # Read from text file, creating frames with buttons for each topic.
        subjects = open(self.directory/"exampleText.txt").read().split('-----\n')
        for i in range(len(subjects)):
            # Create the menu frame for each subject
            subject = subjects[i]
            frame = Frame(master, bg=frameColor, relief=GROOVE)
            self.frames[(i+1, 0)] = frame

            # Button on the main frame to go to the subject frame
            subjectTitle = subject[:subject.index('\n')].strip()
            subjectButton = newButton(mainFrame, lambda n=i+1: self.switchFrame((n, 0)), subjectTitle)
            subjectButton.pack(pady=objectPackPady, side=TOP)
            
            # Button on the subject frame to go back to the main frame
            backButton = newButton(frame, lambda: self.switchFrame((0, 0)), "Back")
            backButton.pack(pady=objectPackPady, side=BOTTOM)

            # Read every topic in the subject and make a new frame for each
            topics = subject.split('\n\n')[1:]
            for j in range(len(topics)):
                # Find the title of the topic and the corresponding text for the page
                topic = topics[j]
                topicTitle = topic[:topic.index('\n')].strip()
                text = topic[topic.index('\n'):].strip()

                # Add the new page to the list of frames and text to the list of chapter text
                self.frames[(i+1, j+1)] = newPage(text, True)
                self.chapterText[(i+1, j+1)] = text
                
                # Button on the subject frame to go to the topic frame
                topicButton = newButton(frame, lambda n=i+1, m=j+1: self.switchFrame((n, m)), topicTitle)
                topicButton.pack(pady=objectPackPady, side=TOP) 

        # Pack the main frame so that it is what appears first on startup
        mainFrame.pack(expand=True, fill=BOTH)





    # switchFrame takes the frame ID of the frame that is going to be loaded
    # Frame IDs work as follows:
    #     (0, 0) is the main frame
    #     (#, 0) is the #th subject frame (i.e. (1, 0) is the frame for precalculus topics)
    #     (#, #) is the page with the text of topic #.# (i.e (1, 1) is topic 1.1: precalc->discontinuities)
    def switchFrame(self, nextID):
        self.frames[self.currentFrameID].pack_forget()
        next = self.frames[nextID]
        next.pack(expand=True, fill=BOTH)
        self.currentFrameID = nextID

    # Currently only plays one video, will either use a dict or generate the video through manim on demand   
    def playVideo(self, videoFile):
        # Get the function in the entry if one exists (currently only prints, will be used to generate anim)
        slaves = self.frames[self.currentFrameID].pack_slaves()
        userFunction = None
        for slave in slaves:
            if type(slave) == Frame:
                slaves = slave.pack_slaves()
                for slave in slaves:
                    if type(slave) == Entry:
                        userFunction = slave.get()
                        break
                break
        if userFunction != None and userFunction != '':
            print("Function: " + userFunction)

        # Play the video
        cap = cv2.VideoCapture(videoFile)
        if (cap.isOpened()== False):
            print("Error opening video file")
            return

        cv2.namedWindow('Animation')
        cv2.moveWindow('Animation', 1, 1)
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



    # Test function to play a manimation through the GUI
    def playManim(self):
        self.playVideo(self.directory/'../media/videos/1080p60/hello.mp4')

    # Quit the program
    def terminate(self):
        self.parent.destroy()


if __name__ == '__main__':
    root = Tk()
    app = GUI(root)
    root.mainloop()