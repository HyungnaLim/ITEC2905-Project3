from flask import Flask, render_template, request  # NOT the same as requests
# from github_api import get_github_user
#TODO - Add APIs here to import

app = Flask(__name__)

@app.route('/') # home page - this is returning "index.html"
def homepage():
    return render_template('index.html')

@app.route('/get_artist') # don't forget the /
def get_user_info():
    # get user info from an API (figure out which one)
    print('form data is', request.args)
    # this will read the artist that is being searched for
    artistname = request.args.get('artist_name')
    #TODO - call the funciton from the API's
    # this will call the function from github_api.py in the video
    #user_info, error message = get_github_user(username) from video or]
    # if error_message:
    #     return render_template('error.html,', error=error_message)
    # else:
    #     return render_template('github.html', user_info=user_info)
    artist_info, error message = get_artist_name(artist_name)
    if error_message:
        return render_template('error.html,', error=error_message)
    else:
        return render_template('github.html', artist_info=artist_info) #TODO change github.html

    #return render_template('API.html', artist_info=artist_info)
    # using parameters, this will go to 'API_html' above and search the artist's name
    return render_template('API.html', music_name=artistname)
    # return
    # TODO - this will call the user_info


if __name__ == '__main__':
    app.run()