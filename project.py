# imports: 
#  * h_pct - external file, html-to-python character translator (original)
#  * random - python package
#  * curses - python package, allows windows to be created
#  * time - python package, timeit: timer extension
#  * textColor - external file, color data storage
#  * playsound - allows mp3 files to be played
#  * config - external file, json
#  * profanity - profanity filter

from utility.hctp import pct
import random
import curses
import time
from timeit import default_timer as timer
from utility.textColor import textColors
from playsound import playsound
import utility.config as config
from better_profanity import profanity

# data: dict, where all essential data to run the game is stored. Could potentially be separated into a .json file.

hs = config.CONFIG['leaderboard']
score = 0
timeElapsed = 0
q = 100

data = {
    # Correct sound effect random options 
    "cs": ["ding","nice","angrybirds"],
    # Wrong sound effect random options 
    "ws": ["boing","cry","grrrrr","heheheha"],
    # Dialogue line data, each object in list is by line
    "dialogue": [
        [f'''"{textColors.LightBlue}{textColors.Bold}I'm jumping off the diving board today{textColors.ResetAll}{textColors.White}," Jabari told his dad.''', '''"Really?" said his dad.'''],
        [f'''The diving board is a bit scary, but Jabari had finished his {textColors.LightBlue}{textColors.Bold}swimming lessons and passed his swim test{textColors.ResetAll}{textColors.White}, and now he was ready to jump.''','''"I'm a great jumper," said Jabari, "so I'm not scared at all."'''],
        [f'''Jabari watched the other kids climb the long ladder. They walked all the way out to the end of the board, as big as tiny bugs. Then they stood on the edge. They spread their arms and bent their knees. And sprang up! up! up! And then they dove down, down, down.''', '''SPLASH!''', '''"Looks easy," Jabari said.''', '''But when his dad squeezed his hand. Jabari squeezed back.'''],
        ['''Jabari stood at the bottom of the ladder.''', '''"You can go before me if you want," he told the kid behind him.''', '''"I need to think about what kind of special jump I'm going to do."''', '''Jabari thought and thought.'''],
        ['''Jabari started to climb. Up and up. This ladder is very tall, he thought.''', '''"Are you okay?" called his dad.''', '''"I'm just a little tired," said Jabari.''', '''"Maybe you should climb down and take a tiny rest," said his dad.''', '''A tiny rest sounded like a good idea.'''],
        [f'''When he got to the bottom, Jabari remembered something. "{textColors.LightBlue}{textColors.Bold}I forgot to do my stretches!{textColors.ResetAll}{textColors.White}" he said to his dad.''', '''"Stretching is very important," said his dad.''', '''"I think tomorrow might be a better day for jumping," Jabari said.''', '''They looked up at the diving board together.'''],
        ['''"It's okay to feel a little scared" said his dad. "Sometimes, if I feel a little scared, I take a deep breath and tell myself I am ready. And you know what? Sometimes it stops feeling scary and feels a little like a surprise."''', '''Jabari loved surprises.'''],
        ['''Jabari took a deep breath and felt it fill his body from the ends of his hair right down to the tips of his toes.''','''Jabari looked up. He began to climb.''', '''Up and up. And up and up.''', '''Until he got to the top. Jabari stood up straight.''', '''He walked all the way to the end of the board.'''],
        ['''His toes curled around the rough edge.'''],
        ['''Jabari looked out, as far as he could see. He felt like he was ready.''', '''"I love surprises," he whispered.'''],
        ['''He took a deep breath and spread his arms and bent his knees.''', '''Then he sprang up!''', '''Up off the board!''', '''Flying!'''],
        ['''Jabari hit the water with a SPLASH!'''],
        ['''Down,''','''down,''','''down he went.''','''And then back up!''','''WHOOSH'''],
        ['''"Jabari! You did it!" said his dad.''','''"I did it!" said Jabari. "I'm a great jumper! And you know what?"''', '''"What?" said his dad.'''],
        ['''"Surprise double backflip is next!"''']
    ],
    # Question part data
    "questions": [
        "Looking at the cover, who is the author of the book?", 
        "What is the setting of the story?", 
        "What will Jabari be doing?",
        "What does Jabari think about jumping down the diving board, and why was he confident?", 
        "Who is Jabari with?",
        "Just as Jabari was about to jump off the diving board, he forgets to do something. What did Jabari forget to do?",
        "Who encourages Jabari?",
        "What is the advice Jabari's dad give Jabari?",
        "In this book, what qualities does Jabari show?",
        "How does Jabari's perspective of jumping off the diving board change?",
        "Find at least 2 signs of Jabari being nervous.",
        """Here are the 17 UN goals. Which of the 17 UN goals connect most to this book?"""
        ],
    # Type data stored in format: [Question type (optional image), question value]
    "type": [
        ["Multiple Choice image_question_1.html",100], 
        ["Multiple Choice",100], 
        ["Multiple Choice",100],
        ["Short Answer",200],
        ["Multiple Choice",100],
        ["Multiple Choice",100],
        ["Multiple Choice",100],
        ["Multiple Choice,",200],
        ["Short Answer",400],
        ["Short Answer",400],
        ["Short Answer",200],
        ["UN", 1000]
        ],
    # If question type multiple choice, stored format [a,b,c]
    "answers": [
        ["Jabari","Gaia Cornwell","David Shannon"],
        ["A park", "Jabari's home", "A swimming pool"],
        ["Playing with his sister", "Swimming with his dad", "Jumping off a diving board"],
        [],
        ["His dad and his sister","His dad","His dad and his mother"],
        ["He forgets to strech","He forgets to hug his sister","He forgets how to jump"],
        ["His mother", "His dad", "His sister"],
        ['''"Sometimes, if I feel a little scared, I take a deep breath and tell myself I am ready. And you know what? Sometimes it stops feeling scary and feels a little like a surprise."''','''"Stretching is very important,"''','''"Are you okay?"'''],
        [],
        [],
        [],
        [],
        ],
    # Correct answer list
    "answer": ["b","c","c",["test", "swimming lesson"],"a","a","b","a",["bravery","courage","risk","confiden"],["nervous","confiden","encourage","dad"],["front"],["6","9"]],
    # Stored user input result 
    "result": []
}


def welcome():
    print(f"""{textColors.Magenta}\n\n██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗███████╗    ████████╗ ██████╗     ████████╗██╗  ██╗███████╗     ██████╗  █████╗ ███╗   ███╗███████╗
██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║██╔════╝    ╚══██╔══╝██╔═══██╗    ╚══██╔══╝██║  ██║██╔════╝    ██╔════╝ ██╔══██╗████╗ ████║██╔════╝
██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║█████╗         ██║   ██║   ██║       ██║   ███████║█████╗      ██║  ███╗███████║██╔████╔██║█████╗  
██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║██╔══╝         ██║   ██║   ██║       ██║   ██╔══██║██╔══╝      ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝  
╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║███████╗       ██║   ╚██████╔╝       ██║   ██║  ██║███████╗    ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗
 ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝       ╚═╝    ╚═════╝        ╚═╝   ╚═╝  ╚═╝╚══════╝     ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝
       """)
    skip = input(f"{textColors.Bold}            Press s to skip walkthrough | Press anything else to start the story walkthrough{textColors.ResetAll}     ")
    if skip == "s":
        questions()
    else:
       walkthrough()


def walkthrough():
    def dialogue():
        for lines in range(len(data["dialogue"])):
            print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            for line in data["dialogue"][lines]:
                print(line)
                time.sleep(2)
            try:
                print("\n\n")
                print(pct(f"hctp_images/walkthrough/{lines+1}.html"))
                for _ in range(2):
                    time.sleep(0.5)
                    print("\n")
                time.sleep(5)
            except:
                pass

    print(f"{textColors.White}\n\n\n\n\nHere is a brief walkthrough of Jabari Jumps! (Tip: Pay attention to the {textColors.LightBlue}{textColors.Bold}BLUE{textColors.ResetAll}{textColors.White} text!)")
    time.sleep(2)
    print(pct("hctp_images/walkthrough/cover.html"))
    for _ in range(10):
        time.sleep(0.1)
        print("\n")
    time.sleep(5)
    dialogue()
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print(""" ██████╗ ██╗   ██╗███████╗███████╗████████╗██╗ ██████╗ ███╗   ██╗███████╗
██╔═══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝
██║   ██║██║   ██║█████╗  ███████╗   ██║   ██║██║   ██║██╔██╗ ██║███████╗
██║▄▄ ██║██║   ██║██╔══╝  ╚════██║   ██║   ██║██║   ██║██║╚██╗██║╚════██║
╚██████╔╝╚██████╔╝███████╗███████║   ██║   ██║╚██████╔╝██║ ╚████║███████║
 ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
                       """)
    time.sleep(5)
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print(pct("hctp_images/q1.html"))
    time.sleep(5)
    questions()
    


def questions():
    start = timer()
    global q
    global score
    global timeElapsed
    firstTry = True
    wrongCounter = 0
    stdscr = curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    stdscr.bkgd(' ', curses.color_pair(1))
    q = 0
    title_win = curses.newwin(25 if "UN" in data['type'][q][0] else 12, 260, 2, 5)
    while q < len(data["questions"]):
        output_win = curses.newwin(3, 20, 10, 5)
        input_win = curses.newwin(3 if "Multiple Choice" in data['type'][q][0] or "UN" in data['type'][q][0] else 5, 18 if "Multiple Choice" in data['type'][q][0] or "UN" in data['type'][q][0] else 60, 20 if "UN" in data['type'][q][0] else 10, 3)
        def incorrectFlash():
            global firstTry
            firstTry = False
            try_again = """████████╗██████╗ ██╗   ██╗     █████╗  ██████╗  █████╗ ██╗███╗   ██╗██╗
╚══██╔══╝██╔══██╗╚██╗ ██╔╝    ██╔══██╗██╔════╝ ██╔══██╗██║████╗  ██║██║
   ██║   ██████╔╝ ╚████╔╝     ███████║██║  ███╗███████║██║██╔██╗ ██║██║
   ██║   ██╔══██╗  ╚██╔╝      ██╔══██║██║   ██║██╔══██║██║██║╚██╗██║╚═╝
   ██║   ██║  ██║   ██║       ██║  ██║╚██████╔╝██║  ██║██║██║ ╚████║██╗
   ╚═╝   ╚═╝  ╚═╝   ╚═╝       ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚═╝"""
            title_win.addstr(0,0, try_again, curses.color_pair(3))
            title_win.refresh()
            time.sleep(0.1)
            title_win.addstr(0,0, try_again, curses.color_pair(4))
            title_win.refresh()
            time.sleep(0.1)
            title_win.addstr(0,0, try_again, curses.A_BLINK)
            title_win.refresh()
            time.sleep(0.1)
            title_win.addstr(0,0, try_again, curses.color_pair(3))
            title_win.refresh()
            time.sleep(0.1)
            title_win.addstr(0,0, try_again, curses.color_pair(4))
            title_win.refresh()
            time.sleep(0.1)
            title_win.addstr(0,0, try_again, curses.color_pair(3))
            title_win.refresh()
            if q != 100:
                playsound(f'mp3/Wrong Sounds/{random.choice(data["ws"])}.mp3')
            

        def correctFlash():
            title_win.addstr(0, 0, """████████╗██╗  ██╗ █████╗ ████████╗███████╗    ██████╗ ██╗ ██████╗ ██╗  ██╗████████╗██╗
╚══██╔══╝██║  ██║██╔══██╗╚══██╔══╝██╔════╝    ██╔══██╗██║██╔════╝ ██║  ██║╚══██╔══╝██║
   ██║   ███████║███████║   ██║   ███████╗    ██████╔╝██║██║  ███╗███████║   ██║   ██║
   ██║   ██╔══██║██╔══██║   ██║   ╚════██║    ██╔══██╗██║██║   ██║██╔══██║   ██║   ╚═╝
   ██║   ██║  ██║██║  ██║   ██║   ███████║    ██║  ██║██║╚██████╔╝██║  ██║   ██║   ██╗
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝    ╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝""", curses.color_pair(2))
            title_win.refresh()
            playsound(f'mp3/Correct Sounds/{random.choice(data["cs"])}.mp3')

        stdscr.border()
        input_win.border()
        output_win.border()

        # ternary operator 
        pointGrammar = "point" if data['type'][q][1] == 1 else "points"
        title_win.addstr(1, 0, f"{q+1}. {data['questions'][q]} ({data['type'][q][1]} {pointGrammar})", curses.A_BOLD)
        if "Multiple Choice" in data['type'][q][0]:
            title_win.addstr(3, 0, f"A. {data['answers'][q][0]}\nB. {data['answers'][q][1]}\nC. {data['answers'][q][2]}")
        elif "Short Answer" in data['type'][q][0]:
            title_win.addstr(3, 0, f"\nPress any key to start answering", curses.A_BOLD)
        elif "UN" in data['type'][q][0]:    
            title_win.addstr(3, 0, f"GOAL 1: No Poverty\nGOAL 3: Good Health and Well-being\nGOAL 5: Gender Equality\nGOAL 7: Affordable and Clean Energy\nGOAL 9: Industry, Innovation and Infrastructure\nGOAL 11: Sustainable Cities and Communities\nGOAL 13: Climate Action\nGOAL 15: Life on Land\nGOAL 17: Partnerships to achieve the Goal")
            array = ["GOAL 2: Zero Hunger","GOAL 4: Quality Education","GOAL 6: Clean Water and Sanitation","GOAL 8: Decent Work and Economic Growth","GOAL 10: Reduced Inequality","GOAL 12: Responsible Consumption and Production","GOAL 14: Life Below Water","GOAL 16: Peace and Justice Strong Institutions"]
            for i in range(8):
                title_win.addstr(i+3, 50, array[i])
        stdscr.refresh()
        title_win.refresh()

        if "Multiple Choice" in data['type'][q][0]:
            input_win.addstr(1, 1, "Your answer: ", curses.A_BOLD)
            answer = input_win.getkey()
            input_win.addstr(1, 17, answer)
            while not answer.lower() in ["a","b","c"]: 
                input_win.clear()
                input_win.border()
                input_win.addstr(1, 1, "Your answer: ", curses.A_BOLD)
                answer = input_win.getkey()
                input_win.refresh()
            stdscr.clear()
            stdscr.refresh()
            if answer.lower() != data['answer'][q]:
                incorrectFlash()
                wrongCounter += 1
            elif answer.lower() == data['answer'][q]:
                correctFlash()
                if firstTry == True and wrongCounter == 0:
                    data["result"].append("1!")
                else: 
                    data["result"].append(f"{wrongCounter}")
                firstTry = True
                wrongCounter = 0
                q += 1
        elif "Short Answer" in data['type'][q][0]:
            goodCounter = 0
            c = stdscr.getch()
            input_win.addstr(1, 1, "Your answer: ", curses.A_BOLD)
            while c != "ENTER":
                answer = input_win.getstr(1, 14, 175)
                break
            stdscr.clear()
            stdscr.refresh()
            for each in range(len(data['answer'][q])):
                if data['answer'][q][each] in str(answer.lower().decode("utf-8")):
                    goodCounter += 1
            if goodCounter >= 1:
                correctFlash()
                if firstTry == True and wrongCounter == 0:
                    data["result"].append(f"1!,{goodCounter}")
                else: 
                    data["result"].append(f"{wrongCounter},{goodCounter}")
                firstTry = True
                wrongCounter = 0
                q += 1
            elif goodCounter == 0:
                incorrectFlash()
                wrongCounter += 1
                time.sleep(1)
        elif "UN" in data['type'][q][0]:
            c = stdscr.getch()
            input_win.addstr(1, 1, "Your answer: ", curses.A_BOLD)
            while c != "ENTER":
                answer = input_win.getstr(1, 14, 175)
                break
            stdscr.clear()
            stdscr.refresh()
            if str(answer.lower().decode("utf-8")) in ["6","9"]:
                correctFlash()
                if firstTry == True and wrongCounter == 0:
                    data["result"].append(f"1!")
                else: 
                    data["result"].append(f"{wrongCounter}")
                firstTry = True
                wrongCounter = 0
                q += 1
            else:
                incorrectFlash()
                wrongCounter += 1
                time.sleep(1)
    if q == len(data["questions"]):
        end = timer()
        timeElapsed = round(end-start,2)
        stdscr.clear()
        stdscr.refresh()
        title_win.addstr(0,0, "Your results:", curses.A_BOLD)
        title_win.refresh()
        playsound("mp3/Other/drumroll.mp3") 
        maxscore = 0
        for i in data["type"]:
            maxscore += float(i[1])
        for i in range(len(data["result"])):
            if "1!" in data["result"][i]:
                if "," in data["result"][i]:
                    score += float(100 * int(data["result"][i].split(",")[1]))
                else:
                    score += data["type"][i][1]
            else: 
                if "," in data["result"][i]:
                    score += round(float(data["type"][i][1]/(float(int(data["type"][i].split(",")[0])+1))) * int(data["type"][i].split(",")[1]), 2)
                else:
                    score += round(float(data["type"][i][1]/float((int(data["type"][i].split(",")[0])+1))), 2)

        score = round(score,2)
        title_win.addstr(2,0, f"{score} / {maxscore} ({round((score/maxscore) * 100, 2)}%!) in {timeElapsed} seconds! 👑\n\n")
        title_win.refresh()
        q = 100
        playsound("mp3/Other/clap.mp3")
        curses.endwin()

def highscoreSystem():
    print(f"{textColors.White}{textColors.Bold}\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    name = profanity.censor(input("What is your name?\n"))
    print(f"Hi {name}!")
    time.sleep(1)
    print("Your high score will be recorded, as long as the json file does not get deleted!\n\n")
    hs.append([name,score,timeElapsed])
    config.CONFIG['leaderboard'] = hs 
    config.save_config()
    time.sleep(1)
    print("Current Leaderboards:")
    time.sleep(0.5)
    def sort_key1(h):
        return h[2]
    def sort_key2(h):
        return h[1]
    hs.sort(key=sort_key1, reverse=False)
    hs.sort(key=sort_key2, reverse=True)
    for s in range(len(hs)):
        color = textColors.Yellow if s == 0 else textColors.LightGreen if s == 1 else textColors.LightBlue if s == 2 else textColors.White
        print(f"{color}{s+1}. {hs[s][0]}: {hs[s][1]} points (⏱ {hs[s][2]}s)")
        time.sleep(0.25)
    time.sleep(3)
    print(f"{textColors.White}{textColors.Bold}\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")


welcome()
highscoreSystem()

print(pct('hctp_images/thanks.html'))