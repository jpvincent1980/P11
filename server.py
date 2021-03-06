import json
import datetime

from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    """
    Function that retrieves the list of clubs from clubs.json file.

    Returns a list of dictionaries
    """
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    """
    Function that retrieves the list of competitions from competitions.json
    file.

    Returns a list of dictionaries
    """
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    """
    Route to index page where users can login.
    """
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    """
    Route to showSummary page where competitions are displayed.
    """
    # Debug bug/Entering-a-unknown-email-crashes-the-app
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions)
    except IndexError:
        message = "Sorry, that email wasn't found."
        flash(message, 'error')
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition, club):
    """
    Route to book page where users can book places for competitions.
    """
    try:
        foundClub = [c for c in clubs if c['name'] == club][0]
    except IndexError:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club,
                               competitions=competitions)
    try:
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
    except IndexError:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club,
                               competitions=competitions)
    return render_template('booking.html', club=foundClub, competition=foundCompetition)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    """
    Route to purchasePlaces page where users can book places for competitions.
    """
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    # Debug bug/Clubs-should-not-be-able-to-use-more-points-than-allowed
    availablePoints = int(club.get('points', None))
    competitionDate = datetime.datetime.strptime(competition['date'],
                                                 '%Y-%m-%d %H:%M:%S')
    # Fonctionnalite -> 1 place = 3 points
    if (placesRequired*3) > availablePoints:
        message = f"You don't have enough points to book {placesRequired} places."
        flash(message, 'error')
        return render_template('welcome.html', club=club, competitions=competitions)
    # Debug bug/Clubs-shouldnt-be-able-to-book-more-than-12-places-per-competition
    elif placesRequired > 12:
        message = "You can't book more than 12 places per competition."
        flash(message, 'error')
        return render_template('welcome.html', club=club, competitions=competitions)
    # Debug bug/Booking-places-in-past-competitions
    elif competitionDate < datetime.datetime.now():
        message = "You can't book places for a competition that is past."
        flash(message, 'error')
        return render_template('welcome.html', club=club,
                               competitions=competitions)
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    # Debug bug/Point-updates-are-not-reflected
    # Fonctionnalite -> 1 place = 3 points
    club['points'] = int(club['points'])-(placesRequired*3)
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions, availablePoints=availablePoints)


@app.route('/displayClubsPoints')
def displayClubsPoints():
    """
    Route to displayClubsPoints page where users can see clubs points.
    """
    return render_template('display_clubs_points.html', clubs=clubs, competitions=competitions)


@app.route('/logout')
def logout():
    """
    Route for users to logout
    """
    return redirect(url_for('index'))
