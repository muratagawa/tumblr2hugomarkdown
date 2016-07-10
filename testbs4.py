from bs4 import BeautifulSoup

soup = BeautifulSoup('<iframe width="500" height="281"  id="youtube_iframe" src="https://www.youtube.com/embed/AdymCQ5PXrs?feature=oembed&amp;enablejsapi=1&amp;origin=http://safe.txmblr.com&amp;wmode=opaque" frameborder="0" allowfullscreen></iframe>', "html.parser")
sources=soup.findAll('iframe',{"src":True})

for source in sources:
    print source['src']
