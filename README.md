## Credits
Forked from [tumblr2markdown](https://github.com/jaanus/tumblr2markdown).

## The Goal
The goal of this script is to let you completely export your content hosted on Tumblr to plain Markdown files suitable for [Hugo](https://gohugo.io).

It downloads and converts “text”~~, “photo”, “video”, “link”, and “quote”~~ post bodies. It optionally also downloads images from Tumblr into your local storage. I have built and tested it to migrate from Tumblr to ~~Octopress~~Hugo, but it may have other uses as well.

I found [tumblr2markdown](https://github.com/jaanus/tumblr2markdown), but the end result still required changing/adding front matter for Hugo, as well as removing a fair bit of HTML and converting them to Markdown. Combining it with [html2text](https://github.com/Alir3z4/html2text) allowed me to quickly add in functionality to make the final output more Hugo-friendly. Thanks to the respective authors for their work, otherwise this would have taken a lot more time and effort.

This was used in the migration of my blog from Tumblr to the current Hugo-based one at https://yc.sg.

## Prerequisites
Requires [py2tumblr](https://github.com/tumblr/pytumblr) and [html2text](https://github.com/Alir3z4/html2text).

## How to Use
Just run it with -h switch.

	ycsoh-mbp:tumblr2hugomarkdown ycsoh$ ./tumblr2hugomarkdown.py -h
	usage: tumblr2hugomarkdown.py [-h] --apikey APIKEY --host HOST
                              [--posts-path POSTSPATH] [--download-images]
                              [--images-path IMAGESPATH]
                              [--images-url-path IMAGESURLPATH]
                              [--no-image-folders] [--use-draft-mode]

	Tumblr to Hugo Markdown downloader

	Tumblr to Hugo Markdown downloader

	optional arguments:
	  -h, --help            show this help message and exit
	  --apikey APIKEY       Tumblr API key
	  --host HOST           Tumblr site host, e.g example.tumblr.com
	  --posts-path POSTSPATH
	                        Output path for posts, by default
	                        “output/content/posts”
	  --download-images     Whether to download images hosted on Tumblr into a
	                        local folder, and replace their URLs in posts
	  --images-path IMAGESPATH
	                        If downloading images, store them to this local path,
	                        by default “output/static/img”
	  --images-url-path IMAGESURLPATH
	                        If downloading images, this is the URL path where they
	                        are stored at, by default “/img”
	  --no-image-folders    The images will be sorted into individual folders with
	                        the folder names set to the matching Mardown file
	                        names by default. Specify this argument if you do not
	                        want them to be sorted.
	  --use-draft-mode      The created Hugo Markdown files will be set to
	                        draft=false by default. Specify this argument if you
	                        want to create them in draft mode.

	This app downloads all your Tumblr content into Markdown files that are
	suitable for processing with Hugo. Optionally also downloads the images hosted
	on Tumblr and replaces their URLs with locally hosted versions.

You will need a Tumblr API key, which you can get by [registering a Tumblr application.](http://www.tumblr.com/oauth/apps) Get the value called called “OAuth Consumer Key”.
