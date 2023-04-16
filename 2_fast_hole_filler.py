import asyncio
from pyppeteer import launch
from pyppeteer.errors import TimeoutError

#hole_list = [1X,4X,39,49X,51X,53X,62,87X,94,95,98,105,109,123,145,150,164,166,175]
hole_list = [98]

with open('key_words_sorted.txt', 'r') as file:
    word_list_sorted = [line.strip() for line in file]

async def submit_answer(page, answer):
    # find the input field on the website and enter the answer string
    await page.waitForSelector('input[name="guess"]')
    input_field = await page.querySelector('input[name="guess"]')
    await input_field.click()
    await input_field.focus()
    await input_field.type(answer)
    await page.click('html body div.backgroundImage div#guessBox.guessBox center form input#checkGuess')


    # wait for the results to load


    try:
        await page.waitForSelector('div.backgroundImage div#messageBox.guessBox', visible=True)
        message_text = await page.querySelectorEval('div.backgroundImage div#messageBox.guessBox h1, div.backgroundImage div#messageBox.guessBox h3', 'e => e.textContent')
        return message_text.strip()
    except TimeoutError:
        return None

async def generate_combinations(page, start_word, end_word):
    if len(start_word) != len(end_word):
        return None

    current_word = list(start_word)
    end_word = list(end_word)
    combinations = []

    while current_word <= end_word:
        combinations.append(''.join(current_word))

        i = len(current_word) - 1
        while i >= 0 and current_word[i] == 'z':
            current_word[i] = 'a'
            i -= 1

        if i == -1:
            break

        current_word[i] = chr(ord(current_word[i]) + 1)

    return combinations

async def main():
    # launch the browser
    browser = await launch(headless=True)

    # create a new page
    page = await browser.newPage()

    # navigate to the website
    await page.goto('http://sixsilversaturns.space/rotateSaturn.php')
    # click on the login link
    await page.click('a[onclick="loginOption()"]')

    # login
    await page.type('input[name="username"]', "Pieaxeman")
    await page.type('input[name="password"]', "helloWERLD10!")
    await page.click('input#loginButton[value=Login]')
    counter = 0
    for number in hole_list:
        six_letter_words = []
        print(word_list_sorted[number-1])
        print(word_list_sorted[number])
        six_letter_words = await generate_combinations(page, word_list_sorted[number-1],word_list_sorted[number])
        #six_letter_words = await generate_combinations(page, 'haaaaa',word_list_sorted[number])
        for word in six_letter_words:
            counter += 1
            message = await submit_answer(page, word)
            if message == "Great job.":
                print("Found keyword:", word)
                break
            if counter % 1000 == 0:
                print(word)

    # close the browser
    await browser.close()

asyncio.run(main())
