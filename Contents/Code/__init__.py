####################################################################################################

PREFIX = "/video/example"

NAME = "Surf TV"

ART = 'art-default.jpg'
ICON = 'icon-default.png'

####################################################################################################

# This function is initially called by the PMS framework to initialize the plugin. This includes
# setting up the Plugin static instance along with the displayed artwork.
def Start():    
    Plugin.AddViewGroup("List", viewMode = "List", mediaType = "items")
    Plugin.AddViewGroup("InfoList", viewMode = "InfoList", mediaType = "items")

    # Setup the artwork associated with the plugin
    ObjectContainer.art = R(ART)
    ObjectContainer.title1 = NAME
    ObjectContainer.view_group = "List"
    DirectoryObject.thumb = R(ICON)

# This main function will setup the displayed items.
@handler(PREFIX, NAME, ICON, ART)
def MainMenu():
    oc = ObjectContainer()
    # oc = ObjectContainer(
    #     objects = [
    #         DirectoryObject(
    #             key = Callback(SecondMenu),
    #             title = "Example Directory"
    #         )
    #     ]
    # )
    search_page = HTML.ElementFromURL("http://www.freesurfmovies.org/p/movies-liste.html")

    # The XPath query will return a list of all items which match the query.
    links = search_page.xpath("//div[@class='post-body entry-content']//div[@dir='ltr']//a")
    for link in links:
        title = link.xpath("text()")[0]
        url = link.get("href")
        oc.add(DirectoryObject(key=Callback(SecondMenu, title=title, url=url), title=title, summary="Movie",thumb=R(ICON)))

    return oc

def SecondMenu(title, url):
    movie_page = HTML.ElementFromURL(url)

    param = movie_page.xpath("//object/param[@name='movie']")[0]

    Log("<<><><><><><><><><><>>")
    Log(param.get('value'))
    Log("<<><><><><><><><><><>>")
    video_url = param.get('value');

    oc = ObjectContainer(objects=[])

    # oc.add(DirectoryObject(key=Callback(test), title=url, summary=url))

    video = VideoClipObject(
        title = title,        
        url = video_url
    )
    oc.add(video)

    return oc

def test():
    pass