""" Author EAHT, use for educational purposes ONLY.
Always credit owner """

from camoufox.sync_api import Camoufox
from dotenv import load_dotenv
import os

from csvreader import read_csv

# Small csv reader utility (csvreader.py)
questions = read_csv("questions.csv")
load_dotenv()

custom_fonts = ["Arial", "Helvetica", "Times New Roman"]
with Camoufox(os="macos", fonts=custom_fonts, humanize=True, window=(2360, 1640)) as browser:
    page = browser.new_page()
    page.set_extra_http_headers({"Accept-Encoding": "identity"})
    page.goto("https://smartrevise.online")
    
    # Wait for page to download and for all assests to be downloaded
    page.wait_for_load_state(state="domcontentloaded")
    page.wait_for_load_state('networkidle')
    
    # Click on 'Log in'
    page.mouse.click(550, 350)
    page.wait_for_timeout(2000)
    
    # Click on 'Microsoft'
    page.mouse.click(600, 245)
    page.wait_for_timeout(2500)
    
    # Get microsoft email input
    email_selector = "input[name='loginfmt']"
    page.wait_for_selector(email_selector)
    
    # Type ed.haig-thomas2024@radley.org.uk and go
    page.type(email_selector, os.environ.get("MICROSOFT_EMAIL"), delay=100)
    page.keyboard.press("Enter")
    page.wait_for_timeout(2500)
    
    # Get microsoft password input
    password_selector = "input[name='passwd']"
    page.wait_for_selector(email_selector)
    
    # Enter password
    page.type(password_selector, os.environ.get("MICROSOFT_PASSWD"), delay=100)
    page.keyboard.press("Enter")
    
    # Press stay signed in
    page.wait_for_timeout(7000)
    page.keyboard.press("Enter")
    
    # Wait for Smart revise to load
    page.wait_for_timeout(2000)
    
    # Click on the computer science course
    page.mouse.click(90, 340)
    page.wait_for_timeout(1000)
    
    # Scroll down so revise comes into view and click
    page.mouse.wheel(0, 200)
    page.mouse.click(90, 550)
    
    """ In the question page """
    page.mouse.wheel(0, -50)
    
    for i in range(50):
        page_question = page.locator("#questiontext").text_content().strip()
        
        # Get all answer buttons from the page
        answer_buttons = page.query_selector_all(".col")
        
        for q in questions:
            qt = tuple(q)
            
            if qt[0].lower() != page_question.lower(): continue
            
            # Found matching question!
            print("answer is:", qt[1], "searching for button...")
            
            for button in answer_buttons:
                
                if not button.text_content().strip(): continue # blank space
                
                print(button.text_content().strip(), end="\n" if button.text_content() else "")
                
                if button.text_content().strip().lower() == qt[1].lower() or button.text_content() == "I don't know":
                    print("found it / dont know! clicking...")
                    
                    # Found the answer button, now click it!
                    box = button.bounding_box()
                    print(box)
                    page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                    
                    break
            
            break
        
        page.wait_for_timeout(1000)
        
        page.mouse.wheel(0, -100)
        
        # Now we have answered, press the next button
        next_box = page.locator("#lnkNext").bounding_box()
        page.mouse.click(next_box["x"] + next_box["width"] / 2, next_box["y"] + next_box["height"] / 2)

        # Wait a moment for the page to load
        page.wait_for_timeout(1000)
        
        # Rinse and repeat...

    page.wait_for_timeout(12500)