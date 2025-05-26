import sys
from lib.tools.utils import clear, banner

def remove_duplicate_lines(input_file, output_file):
    try:
        total_lines = sum(1 for _ in open(input_file, 'r', encoding='utf-8'))
        with open(input_file, 'r', encoding='utf-8') as result:
            uniqlines = set(result.readlines())
            with open(output_file, 'w', encoding='utf-8') as kontol:
                processed_lines = 0
                for line in uniqlines:
                    kontol.write(line)
                    processed_lines += 1
                    progress = processed_lines / total_lines
                    print_progress_bar(progress)
        print(f'\nDuplicates removed and saved to {output_file}')
    except FileNotFoundError:
        print('Input file not found')

def print_progress_bar(progress):
    bar_length = 40
    block = int(round(bar_length * progress))
    progress_percent = progress * 100
    bar = '\033[32m' + '=' * block + '\033[0m' + '-' * (bar_length - block)
    sys.stdout.write(f'\r[{bar}] {progress_percent:.1f}%')
    sys.stdout.flush()

def xontol():
    clear()
    print(banner)
    print("\033[97m[\033[92m+\033[97m] URL Cleaner \n")
    list_file = input('\033[97m[\033[92m+\033[97m] List: ')
    output_file = list_file.replace('.txt', '_clean.txt')
    remove_duplicate_lines(list_file, output_file)

if __name__ == "__main__":
    xontol()