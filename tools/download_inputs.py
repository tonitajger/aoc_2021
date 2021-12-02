from http.cookiejar import MozillaCookieJar
from datetime import date

import requests

CHRISTMAS_DATE = date(2021, 12, 25)

def main():
    cookies = MozillaCookieJar('/users/tony.liu/cookies/cookies-adventofcode-com.txt')
    cookies.load()
    headers = {'User-Agent': 'Mozilla/5.0'}

    end_day = date.today()
    if end_day > CHRISTMAS_DATE:
        end_day = CHRISTMAS_DATE

    for day in range(1, end_day.day + 1):
        response = requests.get(f'https://adventofcode.com/2021/day/{day}/input', cookies=cookies, headers=headers)
    
        if response.status_code == 200:
            input_file_path = f'input_files/day{day}'
            with open(input_file_path, 'w') as f:
                f.write(response.text)
            print(f'Successfully wrote input for day {day} to {input_file_path}\n')
        else:
            print(f'Failed to get input file for day {day}!\nStatus code: {response.status_code}\nMessage: {response.text}\nBailing!')
            return

if __name__ == '__main__':
    main()
