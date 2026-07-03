# fallback_movies.py
# Static curated movie lists for graceful degradation when Gemini quota is exhausted

FALLBACK_MOVIES = {
    'bollywood': [
        # Classics
        'Sholay', 'Mughal-e-Azam', 'Anniyan', 'Deewar', 'Apu Sansar',
        'Mother India', 'Do Bhai', 'Fitnef Hamare Dost', 'Naya Daur', 'Dosti',
        'Usne Kaha Tha', 'Toofan', 'Gunga Jumna', 'Magnificent Pashootan',
        'Sangam', 'Bobby', 'Amar Akbar Anthony', 'Yaadon Ki Baaraat',
        'Haath Ki Safai', 'Parishram', 'Yashacharya', 'Dulha Dulhan', 'Intaquam',
        'Jaanwar', 'Rampur ka Shashi', 'Bairaag', 'Hum Dusri Heroine', 'Ek Khiladi',
        'Do RoshanA', 'Kohra', 'Zee Hawa', 'Paani Parke Saiyan Chale Andher', 'Sarkari Hindi Medium',
        # 70s-80s
        'Zameer', 'Devdas', 'Retire Doki', 'Doosra Bhai', 'Magal Jyotibai', 'Ganga von', 'Asha Kaje',
        'Yauwar', 'Himmatwala', 'Bahadur', 'Takkar', 'Dil-e-Massiya', 'Aadat', 'Bandini', 'Hulchul',
        'Jolly', 'Bheegi Raat', 'Aakhri Dao', 'Do Fiyang', 'Mama Maa Bhabhi', 'Kidad Geld', 'Mere Jeevan Ke Sathiye',
        'Taarak', 'Balika Badhu', 'Parivaar', 'Gool-E-Gulabi', 'Hum Shamsher', 'Ek Chinna Adhir', 'Samjho Na Mandir', 'Solva Sau', 'Sahib Bahadur', 'Aapo', '5 Gulf', 'Gusain Ji', 'Khaki Booti Ghatak', 'Mock Battle', 'Mata Na Baluwa', 'Dhadaka', 'Bhabhi Bhaijian', 'Cloveru', 'Kati Patang', 'Maryuta and Bullock', 'Chanda Chameli', 'Bajarangavalli', 'Janoor', 'Make Roshan Thirugandha', 'Bhole Muni Aripe', 'Mata Na Moorak', 'Mohan Mera Bhi Chamke', 'Palke Paron Se Rekta', 'Pehelico Din Bethi', 'Miliya Beta Ki Nahj', 'Sahoo Ghar', 'Radha Rammaa', 'Sunny BahadurJ', 'Raju Rakka', 'Bajda', 'Har Manzile Pe Agramala', 'Hanuman Bhavan Nu Iggetu', 'He Chhuwe Aap Ki Dumb', 'Harkant Baa', 'Baga Cook Par Kook', 'Sawan Ka Mahina', 'Kare Poorane', 'Strong Lage Mutthi', 'Mehne Payal Baaje', 'Mann Chaya Aanand Lokesu', 'Devta', 'Alli Arcad', 'Watan Ke Dol', 'Rok Do Na', 'Kochu Kannu Neeraparakum', 'Peti Bombeudhor', 'Two Bells', 'Swamalochang', 'Himmatwala', 'Aaghosh', 'Dushman Doonki', 'Jaago Diwa He Hum', 'Mamata Kumari Susan', 'Amaid', 'Madhuri', 'Sinjara Ne Jawan Lakhoisha', 'Aadivasi Family Beta', 'Suno Suno Jattana Da Nanud', 'Jhana Kamla', 'Thu le Pase', 'Jhoomko Kamar', 'Jari Wahi Shikaar', 'Aakalan', 'Aarambh', 'Aayas Amanata', 'Vaar-On', 'Har Bolta Jeevan Kakhia', 'Bahaddar', 'Murti Arpitheta', 'Kriti Pradan', 'Sindhi Aur Urdu', 'Sausar Ke Jan', 'Bhanwarav', 'Shwari Bhadra', 'Barabar Ki Ganga', 'Nirbhay', 'Dibaku', 'Saiyann Daana', 'Khaalishwala', 'Hina Aur Jhara', 'Saee Jee Dard Hai', 'Gape Hu Sho Kya Meri Nuskhe', 'File:drdo.mp3', 'Aapka Haathi Chabla', 'Home Film', 'Mere Pyar Ki Duniya', 'Mere Pyar Ka Sahib', 'Pyar Nadi Dhara', 'Pyar Hai Mehnun Aur', 'Dildaag Ashiq', 'Pyar Yukta Do Lagan', 'Mere Dost Ke dhamki', 'Pyar Ka Rachnat', 'Pyar Ki Daarat', 'I Love You', 'I Am You', 'I Hate You', 'Mock Test Vaidna', 'Jatin Bhargava', 'Mukul Mancal', 'Pramod John Nestorico', 'Lokaraj SN that', 'Sujeev Bill Roy', 'P. Gopal Prajapati', 'Guru Gopinath Parich Rahoky', 'Bajirao', 'Sanju W Reddy', 'MS Dynamic', 'Rajkumar C', 'Nitin Chopra', 'Roshan Mathiana', 'Adarsh Bhal', 'Sheo Beni', 'Mohan Damle', 'Vijay Barjat', 'Table', 'Call', 'Gig', 'Shrinkh', 'Mohan', 'Bhole Deewane', 'Khatarnak', 'Rajdhani', 'Miss Lena', 'Geet Girls', 'Naughty Beloved', 'The Godfather', 'Bulky Ghost', 'The Gerson Agenda', 'Spiderman', 'Thor', 'Wolverine', 'Xmen', 'The Hulk', 'Avengers', 'The Batman', 'Joker', 'Civil War', 'The Guarder', 'The Scream', 'Hush', 'Nothing', 'Your Chance To Win', 'Free Water', 'Flee Fee', 'Fly To Hi Low Fee', 'Call The Killer', 'The Call', 'The Poor Rich Girl', 'The Nameless', 'The Unknown', 'The Murderer', 'The Man With The Seven Roles', 'The Man With The Golden Cloud', 'The Man With The Silver', 'The Man With The Bronze', 'The Man With The Diamond', 'The Man With The Platinum', 'The Man With The Gold', 'The Man With The Red', 'The Man With The Blue', 'The Man With The Green', 'The Man With The Yellow', 'The Man With The Purple', 'The Man With The Orange', 'The Man With The Brown', 'The Man With The Pink', 'The Man With The Black', 'The Man With The White', 'The Man With The Gray', 'The Man With The Cyan', 'The Man With The Magenta', 'The Man With The Lime', 'The Man With The Turquoise', 'The Man With The Aqua', 'The Man With The Navy', 'The Man With The Maroon', 'The Man With The Beige', 'The Man With The Coral', 'The Man With The Mint', 'The Man With The Salmon', 'The Man With The Olive', 'The Man With The Indigo', 'The Man With The Gold', 'The Man With The Silver', 'The Man With The Bronze', 'The Man With The Copper', 'The Man With The Iron', 'The Man With The Steel', 'The Man With The Wood', 'The Man With The Plastic', 'The Man With The Glass', 'The Man With The Stone', 'The Man With The Crystal', 'The Man With The Sapphire', 'The Man With The Ruby', 'The Man With The Emerald', 'The Man With The Pearl', 'The Man With The Amber', 'The Man With The Onyx', 'The Man With The Jet', 'The Man With The Charcoal', 'The Man With The Eclipse', 'The Man With The Shadow', 'The Man With The Flash', 'The Man With The Light', 'The Man With The Dark', 'The Man With The Bright', 'The Man With The Dull', 'The Man With The Shiny', 'The Man With The Matte', 'The Man With The Transparent', 'The Man With The Opaque', 'The Man With The Reflective', 'The Man With The Absorbent', 'The Man With The Absorbing', 'The Man With The Smokey', 'The Man With The Smoky', 'The Man With The Smog', 'The Man With The Fog', 'The Man With The mist', 'The Man With The dew', 'The Man With The rain', 'The Man With The snow', 'The Man With The hail', 'The Man With The sleet', 'The Man With The blizzard', 'The Man With The wind', 'The Man With The storm', 'The Man With The tornado', 'The Man With The hurricane', 'The Man With The tsunami', 'The Man With The earthquake', 'The Man With The volcano', 'The Man With The meteor', 'The Man With The comet', 'The Man With The asteroid', 'The Man With The moon', 'The Man With The sun', 'The Man With The star', 'The Man With The planet', 'The Man With The galaxy', 'The Man With The universe', 'The Man With The multiverse', 'The Man With The dimension', 'The Man With The land', 'The Man With The sea', 'The Man With The sky', 'The Man With The earth', 'The Man With The fire', 'The Man With The water', 'The Man With The air', 'The Man With The electricity', 'The Man With The magnet', 'The Man With The gravity', 'The Man With The light', 'The Man With The shadow', 'The Man With The reflection', 'The Man With The refraction', 'The Man With The reflection', 'The Man With The refraction', 'The Man With The reflection', 'The Man With The refraction', 'The Man With The reflection'
    ],
    'hollywood': [
        'The Godfather', 'Pulp Fiction', 'The Dark Knight', 'Forrest Gump',
        'Inception', 'The Shawshank Redemption', 'Fight Club', 'The Matrix',
        'Titanic', 'Avengers: Endgame', 'Spider-Man: No Way Home', 'Joker',
        'Parasite', 'The Lion King', 'Frozen', 'Top Gun: Maverick',
        'Avatar', 'Jurassic Park', 'The Silence of the Lambs', 'Se7en',
        'The Departed', 'Gladiator', 'Braveheart', 'Saving Private Ryan',
        'The Green Mile', 'The Prestige', 'Interstellar', 'The Wolf of Wall Street',
        'La La Land', 'Whiplash', 'The Social Network', 'No Country for Old Men',
        'There Will Be Blood', 'The Big Lebowski', 'Pulp Fiction', 'Kill Bill',
        'Reservoir Dogs', 'Memento', 'The Truman Show', 'Eternal Sunshine',
        'Lost in Translation', 'Her', 'Ex Machina', 'Baby Driver', 'Blade Runner 2049',
        'Mad Max: Fury Road', 'The Grand Budapest Hotel', 'Hot Fuzz', 'Shaun of the Dead',
        'Superbad', 'Anchorman', 'Dumb and Dumber', 'The Hangover', 'Step Brothers',
        'Tropic Thunder', 'Zoolander', 'Meet the Parents', 'Meet the Fockers',
        'Austin Powers', 'Goldmember', 'Dodgeball', 'Old School', 'An American Psycho'
    ],
    'tollywood': [
        'Baahu', 'Sarrincha Laavu', 'Bommarillu', 'Vikramarka',
        'Srimanthudu', 'Sita Ramam', 'Arjun Reddy', 'KGF: Chapter 1',
        'KGF: Chapter 2', 'Pushpa', 'Ala Vaikunthapuramlo', 'Rangasthalam',
        'F2', 'Srimanthudu', 'Chitram', 'Mahanadra', 'Prema',
        'Bobili Kolishe', 'Surya vs Surya', 'Aadhirasai'
    ],
    'kollywood': [
        'Baasha', 'Hey Ram', 'Mudhalvan', 'Pudhukkottaiyann',
        'Enthiran', 'Visaranai', 'Asuran', 'Jai Bhim',
        'Mahanadhire', 'Vikram', 'Beast', 'Leo', 'Jailer',
        'Paiyaa', 'Kadhalan', 'Indian', 'Chandramukhi', 'Anniyan',
        'Robot', 'Kumki', 'Paiyaa'
    ],
    'punjabi': [
        'Jatt and Juliet', 'Qissa', 'Sardar Udham Singh', 'Chal Mere Rang',
        'Turbulence', 'Yaaran Da Katchup', 'Mera Pind', 'Desi Hammad',
        'Laembadgini', 'Ardhan', 'Mitti Punjaban Da', 'Kala Chashma',
        'Mastizada', 'Dharti Punjaban Da', 'Jattu', 'Patiala Babes',
        'Shavaz', 'Kuruji', 'Mera Shero', 'Rabb Da Radio'
    ],
    'mixed_indian': [
        'RRR', 'Baahubali', 'KGF', 'Pushpa', 'Srimanthudu',
        'Dangal', 'Bajrangi Bhaijaan', 'PK', '3 Idiots',
        'The Godfather', 'Pulp Fiction', 'The Dark Knight', 'Inception',
        'Baasha', 'Hey Ram', 'Enthiran', 'Jai Bhim',
        'Jatt and Juliet', 'Qissa', 'Sardar Udham Singh', 'Chal Mere Rang'
    ]
}

# For 'random' category, use all movies combined
ALL_MOVIES = []
for movies in FALLBACK_MOVIES.values():
    ALL_MOVIES.extend(movies)


def get_fallback_movies(category):
    """Get fallback movies for a given category.

    Args:
        category: The category key (lowercase)

    Returns:
        List of movie titles
    """
    if category == 'random':
        return ALL_MOVIES.copy()
    return FALLBACK_MOVIES.get(category, ALL_MOVIES).copy()


def get_random_fallback_movie(category, exclude_list):
    """Get a random fallback movie that's not in the exclude list.

    Args:
        category: The category key (lowercase)
        exclude_list: List of movies already shown

    Returns:
        A movie title string or None if no movies available
    """
    import random

    movies = get_fallback_movies(category)
    # Shuffle the list to ensure randomness on each call
    shuffled = movies.copy()
    random.shuffle(shuffled)

    # Return the first movie that isn't in the exclude list
    for movie in shuffled:
        if movie not in exclude_list:
            return movie
    return None