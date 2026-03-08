""" Author EAHT, use for educational purposes ONLY.
Always credit owner """

from camoufox.sync_api import Camoufox
from csvreader import read_csv, write_csv

CSV_PATH = "questions.csv"
QUESTIONS = 100

# Small csv reader utility (csvreader.py)
questions = read_csv(CSV_PATH)

with Camoufox(
    os="windows",
    fonts=["Arial", "Helvetica", "Times New Roman"],
    humanize=True,
    window=(1280, 1000)
) as browser:
    
    page = browser.new_page()
    page.goto("https://smartrevise.online")
    
    input("Sign in manually then press enter") # Wait for input (user has signed in)
    
    """ In the question page """    
    for i in range(QUESTIONS):
        
        # Get the question
        page_question = page.locator("#questiontext").text_content().strip()
        
        # Get all answer buttons from the page
        answer_buttons = page.query_selector_all(".col")
        know = False
        
        for q in questions:

            if q[0].lower() != page_question.lower(): continue
            
            # Found matching question!
            print("answer is:", q[1], "searching for button...")
            for button in answer_buttons:
                
                if not button.text_content().strip(): continue # blank space
                
                if button.text_content().strip().lower() == q[1].lower() or button.text_content() == "I don't know":
                    print("found it! clicking...")
                    know = True
                    
                    # Found the answer button, now click it!
                    box = button.bounding_box()
                    page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                    break
                
            break
        
        page.wait_for_timeout(1500)
        
        if not know: # question is not in csv
            print("dont know... :/ adding to csv")
            for btn in page.query_selector_all(".col"):
                if btn.text_content() == "I don't know":
                    box = btn.bounding_box()
                    page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)

            page.wait_for_timeout(1000)

            for a in page.query_selector_all(".btn-success"):
                if a.text_content().strip() == "Next Question": continue
                q = page.locator("#questiontext")
                # add it to the known questions and move on
                print(f"{q.text_content().strip()}|{a.text_content().strip()}")
                questions.append((q.text_content().strip(), a.text_content().strip()))
                

        page.wait_for_timeout(1000)
        
        # Now we have answered, press the next button
        next_box = page.locator("#lnkNext").bounding_box()
        page.mouse.click(next_box["x"] + next_box["width"] / 2, next_box["y"] + next_box["height"] / 2)

        # Wait a moment for the page to load
        page.wait_for_timeout(1000)
        
        # Rinse and repeat...

write_csv(CSV_PATH, questions)
    