import pandas
import imgurpython
import praw
import time
import datetime
import argparse
from imgurpython.helpers.error import ImgurClientError

from app import db, app
from app.models import Post
from sqlalchemy.exc import IntegrityError


def check_image(image_url):
    
    pos = image_url.rfind('/')
    temp = image_url[pos+1:]
    
    #indicates the url has an extension
    if temp.find('.') != -1:
        image_id = temp[:temp.find('.')]
        has_extension = True
    else:
        image_id = temp
        has_extension = False
    
    if has_extension == True:
        try:
            image = client.get_image(image_id)
        except ImgurClientError as e:
            return None
    else:
        try:
            album = client.get_album(image_id)
            is_gallery = True
        except:
            is_gallery = False

        if is_gallery == True:
            return None
        
        try:
            image = client.get_image(image_id)
        except ImgurClientError as e:
            return None
    
    if image is None:
        return None
    
    if image.nsfw == True:
        return None
    
    if image.type == 'image/gif':
        return None
    
    return image.link

def add_from_csv(datafile, sample_size=1000):
    num_processed = 0 
    df = pandas.read_csv(datafile)
    for row in df.sample(sample_size).iterrows():
        data = row[1]
        insert_into_db(data.url, data.title, data.score, data.id, data.subreddit, data.year, data.month)

def add_from_subreddit(subreddit, sample_size=100):
    num_processed = 0
    current_unix = int( time.time() - 16070400 )
    two_years_ago_unix = current_unix - 48211200
    r = praw.Reddit(user_agent="virality_prediction_game")
    last_id = None
    while num_processed < sample_size:
        i=0
        period = "%d..%d" % (two_years_ago_unix,current_unix)
        results = r.search('site:imgur.com', subreddit=subreddit, sort='new', syntax=None, period=period)
        for x in results:
            i+=1
            submission_time = datetime.datetime.fromtimestamp(int(x.created_utc))
            if insert_into_db(x.url, x.title, int(x.score), x.id, subreddit, submission_time.year, submission_time.month):
                num_processed +=1
                print "Processed %d new posts" % num_processed
                if i+num_processed >= sample_size:
                    break
        current_unix = int(x.created_utc)
        if x.id==last_id or i==0:
            print "Unable to add anymore posts. Aborting"
            break
        last_id=x.id

def insert_into_db(imgur_url,title,score,id,subreddit,year,month):
    if Post.query.filter(Post.reddit_id == id).count() == 0:
        new_link = check_image(imgur_url)
        if new_link is not None:
            p = Post(new_link, title, score, id, subreddit, year, month)
            try:
                db.session.add(p)
                db.session.commit()
                return True
            except IntegrityError as e:
                print "WOAH! Error adding to the DB. Rolling back"
                print e
                db.session.rollback()
                return False
        else:
            print "%s is an invalid link" % imgur_url
            return False
    else:
        print "t3_%s is already in the db" % id
        return False

if __name__=='__main__':
    imgur_client_id     = app.config['IMGUR_ID']
    imgur_client_secret = app.config['IMGUR_SECRET']
    client = imgurpython.ImgurClient(imgur_client_id, imgur_client_secret)

    parser = argparse.ArgumentParser(description='Add images to the DB')
    parser.add_argument('--csv',         help='CSV File to be parsed')
    parser.add_argument('--subreddit',   help='Subreddit to be scraped')
    parser.add_argument('--sample_size', help='How many samples to import', type=int, default=25)
    args = parser.parse_args()

    if args.csv is not None:
        add_from_csv(args.csv, sample_size=args.sample_size)
    elif args.subreddit is not None:
        add_from_subreddit(args.subreddit, sample_size=args.sample_size)
    else:
        parser.print_help()
        print("You must pass either a --csv or --subreddit argument")

