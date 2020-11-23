## Reddit Comment Depths

A tool to analyse the number of votes comments get in popular subreddits. In particular looking at how the number of votes changes depending on the depth in the comment tree and the height of the comment beneath its post.

### Setup

#### 1. Clone repository
In the target directory:
`git clone https://github.com/ethan-fraser/reddit-comment-depths.git`

#### 2. Install dependencies
Using python 3.8 or greater:
`pip install praw matplotlib numpy progress`

#### 3. Create a Reddit app
- Go to https://www.reddit.com/prefs/apps/
- Click *create another app...*
- Enter a name
- Select *script*
- Enter a redirect uri (use https://localhost:5000)
- Click *create app*

#### 4. Create praw.ini
Create a `praw.ini` file in the project folder with the following
```
client_id=<client-id>
client_secret=<client-secret>
```

#### 5. Run `python getavgs.py`
Follow the steps and repeat this process for as many subreddits as you please. Create a new output file for each subreddit that you process, e.g. `askreddit_output.txt`

#### 6. Run `python makeplot.py <filename(s)>`
Modify the `makeplot.py` script to work for you.

