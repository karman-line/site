This repo was forked entirely from [Jonathan Soma](https://github.com/jsoma)'s, and all the back-end pages for my website [www.kaarnam.com](www.kaarnam.com) live here.

This repo helps publish a portfolio from Google Docs *without touching a single iota of programming.* You can do it all clickity-clickity-click through GitHub and Google Drive. It'll make a website [like this](https://jsoma.github.io/portfolio-autopublish/).

## Part 0: Make a project or ten

Make some projects using Google Docs. They should be formatted [using ArchieML](http://archieml.org/). You can more or less just use my template for this.

You can have the following filled in:

|key|meaning|
|---|---|
|`headline`|the headline|
|`author`|your name|
|`kicker`|the [kicker](https://www.merriam-webster.com/words-at-play/kicker-definition-meaning) *optional*|
|`intro`|an intro listed at the top of the story as well as on your homepage|
|`slug`|the project's name in the url, e.g. `covid-project`|
|`content`|the body of your story (text, charts, embeds, etc)|
|`github_repo`|where your code for this project lives *optional*|
|`theme`|theme options - by default there are `light`, `dark` and `beige` *optional*|
|`text_color`|text color *optional*|
|`bg_color`|page background color *optional*|
|`css`|custom CSS *optional*|

Most of these are on a single line, but `content:` ends at the `:end`. If you kept the template intact you'll probably be okay!

#### Notes about text

* Links will automatically become links, lists will automatically become lists
* Using Heading 1 and 2 in Google Docs will automatically make headers
* For bold etc you'll need to use doing markdown. Reference here: https://guides.github.com/features/mastering-markdown/

#### Notes about Datawrapper

* Links to Datawrapper will automatically be converted into embedded charts
* Datawrapper isn't too hot with the dark theme

#### Notes about images

* Images will automatically be embedded in the page
* You can use tables to put images side-by-side, but it doesn't really work with Datawrapper charts.
* Use the text option **Heading 3** to provide a title for a graphic. The line of text following it will automatically be styled as a subhead.
* The text immediately after an image will be treated as a caption. Use it for notes, credit, etc. 

## Part 1: Make your projects public

> If you're doing this from a corporate account (e.g. Columbia), you won't be able to make your projects public. As a result you'll need to **make a new Google Docs document from a personal Google account**. Just open up the old one and cut and paste it all into a new document you've made on your personal account.

1. Open your project in Google Docs. If it's in a corporate account (e.g. Columbia), you'll need to create a new one on a personal Google Docs account (see above).
2. Click the **Share** button in the upper right-hand corner of the page.
3. Under **Get link**, change it to be *Anyone on the internet with this link can view*. If this option doesn't appear, it's because you need to create the file from a non-corporate account.
4. Copy this link. You'll need it for **Part 2**.

## Part 2: Get the setup done

1. Visit [my repository](https://github.com/jsoma/portfolio-autopublish). Or yours, if you've already cloned it!
1. Click the **Fork** button in the upper right-hand corner of this page. This will create a copy of my repository just for you.
2. Once it's done copying over, click the file `details.yaml` (on your forked version of the repo, not on mine!). This file contains all of the details about your website.
3. Now you should be looking at the contents of `details.yaml`. Click the **pencil icon** on the right-hand side of the page to edit the file.
4. Change everything! Name, bio, links, all of that. Feel free to add and remove links and projects. Make sure you pay attention to how things are indented, and where `-` are. Each project should point to the **shared URL**.
5. Scroll to the bottom, click **Commit changes** to save.

## Part 3: Publish your projects

1. Click the **Actions** link at the top of the repository
2. On the right, click **Build site** under **All workflows**.
3. Click **Run workflow** on the right, then the green **Run workflow** button.
4. A new "Build site" action will show up! It'll turn yellow, then hopefully green. If it turns **red**, there was an error (If that happens, click it and scroll down to see what happened). If it turns **green**, you're all set.

## Part 4: Make your website

1. Click the **Settings** link at the top of the repository.
2. Change the name of your repository! `portfolio-autopublish` is a pretty awful name.
3. After you rename the repo, keep scrolling down until you see the **GitHub Pages** header. Change the `None` dropdown to `master` or `main`. Then the new dropdown that shows up should be `docs` to publish the site from the `docs` folder. Click **Save**.
4. Eventually you'll (hopefully?) get a **Your site is published at...** notice and you can click it. You have a website!!

## Republishing

Do Step 3 again and it'll automatically republish.

## Customizing your page

Take a look in `templates/` and `style/`. If you know what those files are, you're welcome to change them!

Note that while templates are kind of HTML, they're also this templating language called [Jinja](https://jinja.palletsprojects.com/en/2.11.x/) (that's all the conditionals etc).
