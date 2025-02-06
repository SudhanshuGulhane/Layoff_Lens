import praw
import prawcore
import json
import time
import os

def save_data_to_json(file_path, data):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)
    file_size = os.path.getsize(file_path) / (1024 * 1024)
    print(f"Updated JSON file. Current size: {file_size:.2f} MB")

def get_comment_replies(comment):
    replies = []
    for reply in comment.replies:
        if isinstance(reply, praw.models.MoreComments):
            continue
        reply_dict = {
            "id": reply.id,
            "author": str(reply.author) if reply.author else "Deleted",
            "body": reply.body,
            "replies": get_comment_replies(reply)
        }
        replies.append(reply_dict)
    return replies

def fetch_subreddit_data():
    
    reddit = praw.Reddit(
        client_id='MIgE_4hYfPDUGVk3rcH68A',
        client_secret='3IH1-U_WQpCih4_9lVAwx7d6VxmgIw',
        user_agent='data_scraper/0.1 by ThorinOaken_Shield',
        username='ThorinOaken_Shield',
        password='Password@123'
    )

    subreddit_list = ['Layoffs','breakinglayoffs', 'jobs', 'LayoffNews', 'jobsearchhacks',
                    'jobsearch', 'jobsearchadvice', 'jobsearchtips', 'jobsearchresources', 'jobsearchstrategies', 'jobsearchsupport', 'jobsearchtools',
                    'jobsearchadvice', 'jobsearchtips', 'jobsearchresources', 'jobsearchstrategies', 'jobsearchsupport', 'jobsearchtools',  
                    'lost-job', 'jobsearchhacks', 'jobsearchadvice', 'jobsearchtips', 'jobsearchresources', 'jobsearchstrategies', 'jobsearchsupport', 'jobsearchtools',
                    'layoff news today', 'microsoft layoffs', 'amazon layoffs', 'layoff stories', 'How to cope up with Layoffs', 'How to get job during layoffs',
                    'layoffs','breakinglayoffs', 'jobs', 'LayoffNews', 'jobsearchhacks','Netflix layoffs', 'Twitter layoffs', 'Meta layoffs', ''
                    'career', 'layoff', 'layoff news today', 'microsoft layoffs', 'amazon layoffs', 'layoff stories', 'How to cope up with Layoffs', 'How to get job during layoffs',
                    'microsoft layoffs', 'amazon layoffs', 'layoff stories', 'How to cope up with Layoffs', 'How to get job during layoffs',
                    'layoffs causing unemployement', 'google layoffs', 'industry with high job loss rate', 'industry with high layoff rate', 'industry with high unemployment rate', 'industry with high jobless rate', 'industry with high jobless claims',
                    'major layoffs this week', 'reasons of layoff in 2023', 'future predictions for job market and layoffs', 'job market after layoffs', 'job market after covid', 'job market after pandemic', 'job market after recession', 'job market after economic crisis',
                    'case studies on large scale layoffs', 'case studies on mass layoffs', 'case studies on layoffs', 'case studies on job loss', 'case studies on jobless rate', 'case studies on jobless claims', 'case studies on unemployment', 'case studies on job cuts',
                    'mental peace during layoffs', 'mental health during layoffs', 'mental health after layoffs', 'mental health after job loss', 'mental health after job cuts', 'mental health after unemployment', 'mental health after jobless rate', 'mental health after jobless claims',
                    'layoff support services', 'layoff support groups', 'layoff support organizations', 'layoff support resources', 'layoff support helpline', 'layoff support hotline', 'layoff support chat', 'layoff support forum', 'layoff support website',
                    'impact of layoffs on the economy', 'impact of layoffs on the job market', 'impact of layoffs on the unemployment rate', 'impact of layoffs on the jobless rate', 'impact of layoffs on the jobless claims', 'impact of layoffs on the job cuts', 'impact of layoffs on the job loss', 'impact of layoffs on the job search',
                    'layoff survival guide', 'layoff survival tips', 'layoff survival advice', 'layoff survival help', 'layoff survival resources', 'layoff survival strategies', 'layoff survival support', 'layoff survival tools', 'layoff survival techniques',
                    'mental peace during layoffs', 'mental health during layoffs', 'mental health after layoffs', 'mental health after job loss', 'mental health after job cuts', 'mental health after unemployment', 'mental health after jobless rate', 'mental health after jobless claims',
                    'layoff support services', 'layoff support groups', 'layoff support organizations', 'layoff support resources', 'layoff support helpline', 'layoff support hotline', 'layoff support chat', 'layoff support forum', 'layoff support website',
                    'job market after layoffs', 'job market after covid', 'job market after pandemic', 'job market after recession', 'job market after economic crisis',
                    'market crash layoffs', 'market crash job loss', 'market crash job cuts', 'market crash jobless rate', 'market crash jobless claims', 'market crash unemployment', 'market crash job search',
                    'job market after layoffs', 'job market after covid', 'job market after pandemic', 'job market after recession', 'job market after economic crisis',
                    'recession layoffs', 'recession job loss', 'recession job cuts', 'recession jobless rate', 'recession jobless claims', 'recession unemployment', 'recession job search',
                    'economic crisis layoffs', 'economic crisis job loss', 'economic crisis job cuts', 'economic crisis jobless rate', 'economic crisis jobless claims', 'economic crisis unemployment', 'economic crisis job search',
                    'pandemic layoffs', 'pandemic job loss', 'pandemic job cuts', 'pandemic jobless rate', 'pandemic jobless claims', 'pandemic unemployment', 'pandemic job search',
                    'covid layoffs', 'covid job loss', 'covid job cuts', 'covid jobless rate', 'covid jobless claims', 'covid unemployment', 'covid job search',
                    'job market after layoffs', 'job market after covid', 'job market after pandemic', 'job market after recession', 'job market after economic crisis',
                    'crash layoffs', 'crash job loss', 'crash job cuts', 'crash jobless rate', 'crash jobless claims', 'crash unemployment', 'crash job search'
                    ]

    total_content = list()

    for subreddit_itr in subreddit_list:
        attempt = 0
        while attempt < 5:
            try:
                current_subreddit = reddit.subreddit(subreddit_itr)
                for post in current_subreddit.hot(limit=None):
                    ID = post.id
                    Title = post.title
                    Body = post.selftext
                    Post_URL = post.permalink
                    Upvotes = post.score
                    Number_Of_Comments = post.num_comments
                    Publish_Date = post.created
                    Image_URL = post.url
                    Upvote_ratio = post.upvote_ratio
                    Username = str(post.author)
                    Downvotes = Upvotes - int(Upvotes * Upvote_ratio)

                    comments = list()
                    post.comments.replace_more(limit=None)
                    for comment in post.comments.list():
                        comment_dict = {
                            "id": comment.id,
                            "author": str(comment.author),
                            "body": str(comment.body),
                            "replies": get_comment_replies(comment)
                        }
                        comments.append(comment_dict)

                    data_set = {"ID": ID,"Title":Title,"Body": Body, "Post_URL": Post_URL, "Upvotes":Upvotes,"Username": Username,"Downvotes": Downvotes,
                                "Number_Of_Comments":Number_Of_Comments,"Publish_Date":Publish_Date,"Image URL":Image_URL,
                                "Upvote Ratio": Upvote_ratio, "Comments": comments}
                    total_content.append(data_set)
                    save_data_to_json("data.json", total_content)
                    print('post:{', ID, "} added successfully")
                    time.sleep(1)
                break
            except prawcore.exceptions.TooManyRequests as e:
                wait = 10 * (attempt + 1)
                print(f"Rate limit exceeded. Retrying in {wait} seconds.")
                time.sleep(wait)
                attempt += 1
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                break

def main():
    fetch_subreddit_data()

if __name__ == "__main__":
    main()
 