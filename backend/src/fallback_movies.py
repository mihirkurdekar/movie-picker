# fallback_movies.py
# Static curated movie lists for graceful degradation when Gemini quota is exhausted

FALLBACK_MOVIES = {
    'bollywood': [
        '3 Idiots', 'Dangal', 'PK', 'Queen', 'Andhadhun', 'Drishyam',
        'Dilwale Dulhania Le Jayenge', 'Kabhi Khushi Kabhie Gham', 'Chennai Express',
        'Bajrangi Bhaijaan', 'OMG 2', 'The Lunchbox', 'Badla', 'Article 15',
        'Jawan', 'Pathaan', 'Animal', 'Rocky Aur Rani Kii Prem Kahaani',
        'Sholay', 'Lagaan', 'Dil Chahta Hai', 'Zindagi Na Milegi Dobara',
        'Gangs of Wasseypur', 'Paan Singh Tomar', 'Barfi', 'Kahaani',
        'Talaash', 'Special 26', 'A Wednesday', 'Rang De Basanti',
        'Guru', 'Wake Up Sid', 'Rocket Singh', 'Band Baaja Baaraat',
        'Zoya Factor', 'Thappad', 'Sir', 'Piku', 'Tamasha', 'Dear Zindagi',
        'Raazi', 'Gully Boy', 'Article 15', 'Super 30', 'Chhichhore',
        'Bala', 'Dream Girl', 'Good Newwz', 'Tanhaji', 'Angrezi Medium',
        'Coolie No 1', 'Bell Bottom', 'Sooryavanshi', '83', 'Jersey'
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
    available = [m for m in movies if m not in exclude_list]

    if available:
        return random.choice(available)
    return None