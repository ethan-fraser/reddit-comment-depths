import praw
import os
import sys

# set up reddit instance
reddit = praw.Reddit(
    user_agent = "reddit comment depth analysis"
)

def get_subreddit_from_id(submission_id):
    return reddit.submission(id=submission_id).subreddit.display_name


def breadth_first_search(submission):
    comments = [[]]
    comment_queue = submission.comments[:]
    level_sizes = [len(comment_queue)]
    i = 0
    while comment_queue:
        if level_sizes[i] == 0:
            i += 1
            comments.append([])
        level_sizes[i] -= 1
        comment = comment_queue.pop(0)
        comments[i].append(comment)
        comment_queue.extend(comment.replies)
        # need to make a new level if we encounter one
        try:
            level_sizes[i+1] += len(comment.replies)
        except IndexError:
            level_sizes.append(len(comment.replies))
    return comments


def dfs_aux(comment):
    result = []
    for reply in comment.replies:
        result.extend(dfs_aux(reply))
    return result

def depth_first_search(submission):
    comments = []
    for i, comment in enumerate(submission.comments):
        comments.append([comment])
        comments[i].extend(dfs_aux(comment))
    return comments


def calculate_averages(comments):
    avg_scores = []
    for i in range(len(comments)):
        total = sum([comment.score for comment in comments[i]])
        avg_scores.append(total//len(comments[i]))
    return avg_scores


if __name__ == "__main__":
    subreddit_name = input("Enter the name of the target subreddit: ").strip()
    output_file = input("Enter the name of the output file: ").strip()
    if not os.path.exists(output_file):
        print(f"Error: {output_file}: no such file exists")
        sys.exit(1)
    limit = input("Enter the number of posts you want to look at (default = 10): ").strip()
    if limit == "":
        print("Setting limit to defualt (10)")
        limit = 10
    else:
        limit = int(limit)

    subreddit = reddit.subreddit(subreddit_name)
    for submission in subreddit.top("all", limit=limit):
        print(f"{submission.title} ({submission.id})")

        # fully extend the comment tree for that post
        # have to do this otherwise not all the comments will be visible
        submission.comments.replace_more(limit=None)

        # perform a breadth-first-search on the comment tree
        bf_comments = breadth_first_search(submission)
        df_comments = depth_first_search(submission)

        # get an average score for each level
        bf_averages = calculate_averages(bf_comments)
        df_averages = calculate_averages(df_comments)

        print(f"bf: {bf_averages}\ndf: {df_averages}")
        with open(output_file, "a") as avgs_file:
            avgs_file.write(f"{submission.id}:{bf_averages}:{df_averages}\n")

