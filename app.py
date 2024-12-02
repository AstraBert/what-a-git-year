import gradio as gr
import pandas as pd
from repos import get_repo_info
from scrape import fetch_contribution_details, parse_contribution_details
from plotly_im import plot_to_html, plot_pie_chart

def reply(username: str, token: str):
    base_str = f"<h2 align='center'>What a git-year, {username}!🥂🎉</h2>\n\n<br>\n\n<div align='center'><img src='https://logos-world.net/wp-content/uploads/2020/11/GitHub-Logo.png' alt='GitHub Logo' width=150></div>\n\n\n"
    contributions = fetch_contribution_details(username, token)
    contrib_str = parse_contribution_details(contributions)
    repocount, gained_stars, gained_forks, top_10_topics, top_10_languages = get_repo_info(username, token)
    gainings_string = f"### ✅ This year's achievements\n\n- 📁 You created **{repocount} repositories**\n- ⭐ You gained **{gained_stars} new stars**\n- 🍴 You gained **{gained_forks} new forks**\n\n### 🪛 This year's contributions\n\n"
    base_str+=gainings_string
    base_str+=contrib_str
    top_10_tops = [f"- `{el[0]}` was used in {el[1]} of your repositories" for el in top_10_topics]
    top_10_langs = [f"- **{k}** accounted for **{top_10_languages[k]}%** of your code this year" for k in top_10_languages]
    tops_and_langs = "### 📓 Your Top 10 Topics This Year\n\n" + "\n".join(top_10_tops) + "\n\n" + "### 💻 Your Top 5 Languages This Year \n\n" + "\n".join(top_10_langs) + "\n\n"
    base_str+=tops_and_langs
    top_10_tops_df = pd.DataFrame.from_dict({"TOPIC": [el[0] for el in top_10_topics], "COUNT": [el[1] for el in top_10_topics]})
    top_10_langs_df = pd.DataFrame.from_dict({"LANGUAGE": list
    (top_10_languages.keys())+["Other"], "PERCENTAGE": list(top_10_languages.values())+[100-sum(list(top_10_languages.values()))]})
    top_10_tops_img = plot_to_html(top_10_tops_df, x="TOPIC", y="COUNT", y_label="Count", title="Your Top 10 Topics This Year", labels={"TOPIC": "TOPIC", "COUNT": "COUNT"},  color_based_on="COUNT", filepath="topics")
    top_10_langs_img = plot_pie_chart(
    df=top_10_langs_df,
    names="LANGUAGE",
    values="PERCENTAGE",
    labels={"LANGUAGE": "Language", "PERCENTAGE": "Percentage"},
    title="Your Top 5 Languages This Year",
    filepath="language_usage"
)

    return base_str, top_10_tops_img, top_10_langs_img


mytheme = gr.themes.Monochrome(font=gr.themes.Font("sans-serif"))

iface = gr.Interface(fn=reply, inputs=[gr.Textbox(label="GitHub Username", info="Insert your username here"), gr.Textbox(type="password", label="GitHub Token", info="Insert a GitHub token with repository-level access (<a href='https://github.com/settings/tokens'>find/create yours here</a>)")], outputs=[gr.Markdown(label="Your output will be displayed here"), gr.Image(label="Topics"), gr.Image(label="Languages")], title="<h1 align='center'>What A Git-Year!🥳</h1>\n<h2 align='center'>Find out about your contributions on GitHub in the last year📆</h2>\n<br>", theme=mytheme)

iface.launch(server_name="0.0.0.0", server_port=7860)






