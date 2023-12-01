# Song Filter Program
# Maceo Parker
# 11-25-23
# This Program loads a song database from file, prompts user for filtering options, and returns result that matches requested parameter.
# I will be taking the following College level Computer Programming at Seattle Central College classes prior to Highschool Graduation;
#   CSC 110 (Intro to Computer Programming) - Winter Quarter
#   CSC 142 (Computer Programming I) - Spring Quarter

import pandas as pd
df = pd.read_csv('Song_List.txt', dtype={'Year': str})


print()
print("Hello, welcome to Maceo's Song Filter Program!")

search_choice = 99

# Main Loop
while search_choice != 0:
    print()
    print('Search for your next favorite song.')
    print()
    print('1 = Filter by Year')
    print('2 = Filter by Key')
    print('3 = Filter by BPM')
    print('4 = Generate Random Song')
    print()

    search_choice = int(input('How would you like to search? Enter desired filter here: '))

# Parameter 1
    if search_choice == 1:
        year_choice = input('   Enter a year from 1958-2000: ')
        song_year = df[(df['Year'] == year_choice)]
        if int(year_choice) > 2000 or int(year_choice) < 1958:
            print()
            print("   Oops, there aren't any songs of that year in the database.")
            print()
        else:
            print()
            print('Here are some great songs from the year ' + year_choice + '!')
            print()
            print(song_year.to_string(index=False))
            print()

# Parameter 2
    if search_choice == 2:
        print()
        key_choice = input('''Major = M, Minor = m
Use #s instead of flats
Example; CM, A#m
    
    Enter a song key Here: ''')

        if key_choice == 'Bm':
            print()
            print("    Oops, there aren't any songs that use that key in the database.")
            print()

        else:
            print()
            print('Here are some great songs in the key of ' + key_choice + '!')
            print()
            song_key = df[(df['Key'] == key_choice)]
            print(song_key.to_string(index=False))
            print()

# Parameter 3
    if search_choice == 3:
        BPM_choice = input('Enter a BPM: ')
        BPM = df[(df['BPM'] == BPM_choice)]

        print()
        print('Here are some great songs that have ' + BPM_choice + ' BPM!')
        print()
        print(BPM.to_string(index=False))
        print()

# Parameter 4
    if search_choice == 4:
        rand = df.sample()
        print()
        print('Here is a song picked at random!')
        print()
        print(rand.to_string(index=False))
        print()

    search_choice = int(input('''Would you like to use another filter? Enter 9 to continue, or 0 to quit: '''))
    print()
    print('__________________________________________________________________________')
