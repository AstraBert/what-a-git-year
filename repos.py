from github import Github
from collections import Counter
from date import date_is_within_one_year

def top_ten_strings(strings):
    """
    Counts occurrences of strings in a list and returns the top ten by count.

    :param strings: List of strings to count.
    :return: List of tuples containing the string and its count, sorted by count in descending order.
    """
    # Count the occurrences of each string
    string_counts = Counter(strings)

    # Get the top 10 most common strings
    top_ten = string_counts.most_common(10)

    return top_ten

def sort_dict_by_value(d):
    """
    Sorts a dictionary by its integer values in descending order and returns up to the first 10 items.
    :param d: Dictionary with string keys and integer values.
    :return: List of tuples containing the key and value, sorted by value in descending order.
    """
    # Sort the dictionary by its values in descending order and take the first 10 items
    sorted_items = sorted(d.items(), key=lambda item: item[1], reverse=True)[:5]
    sorted_items = {el[0]: el[1] for el in sorted_items}
    return sorted_items

def get_repo_info(username,token):
    gh = Github(token)
    user = gh.get_user(username)
    repos = user.get_repos()
    repocount = 0
    gained_stars = 0
    gained_forks = 0
    topics = []
    languages = {}
    for repo in repos:
        if date_is_within_one_year(repo.created_at):
            repocount+=1
            rep_topics = repo.get_topics()
            gained_stars += repo.stargazers_count
            gained_forks += repo.forks_count
            for topic in rep_topics:
                topics.append(topic)
            langss = repo.get_languages()
            for lang in langss:
                if lang in languages:
                    languages[lang]+=langss[lang]
                else:
                    languages.update({lang: langss[lang]})
    top_10_topics = top_ten_strings(topics)
    top_10_langs_abs = sort_dict_by_value(languages)
    sum_langs = sum(list(languages.values()))
    top_10_langs = {l: f"{round(top_10_langs_abs[l]*100/sum_langs,2)}%" for l in top_10_langs_abs}
    return repocount, gained_stars, gained_forks, top_10_topics, top_10_langs


