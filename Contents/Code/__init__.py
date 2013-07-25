####################################################################################################

PREFIX = "/video/surftv"

NAME = "Surfing Movies"

ART = 'art-default.jpg'
ICON = 'icon-default.png'

VIDS_PER_PAGE = 20

####################################################################################################

# This function is initially called by the PMS framework to initialize the plugin. This includes
# setting up the Plugin static instance along with the displayed artwork.
def Start():    
    Plugin.AddViewGroup("List", viewMode = "List", mediaType = "items")
    # Plugin.AddViewGroup("VidList", viewMode = "List", mediaType = "videos")
    # Plugin.AddViewGroup("InfoList", viewMode = "InfoList", mediaType = "items")

    # Setup the artwork associated with the plugin
    ObjectContainer.art = R(ART)
    ObjectContainer.title1 = NAME
    # ObjectContainer.view_group = "List"
    ObjectContainer.content = ContainerContent.GenericVideos
    DirectoryObject.thumb = R(ICON)
    #VideoClipObject.thumb  = R(ICON)

# This main function will setup the displayed items.
@handler(PREFIX, NAME, ICON, ART)
def MainMenu():
    oc = GetPageOfVideos() #default is to get page 1
    return oc

def GetPageOfVideos(page=1):    
    oc = ObjectContainer(objects=[], view_group="List")
    
    if page == 1: 
        start_index = 1
    else:
        oc.title2 = "Page "+str(page)
        start_index = ( (page-1) * VIDS_PER_PAGE)+1        
    
    end_index = page * VIDS_PER_PAGE
    
    Log("start> "+str(start_index))
    Log("end> "+str(end_index))
    
    search_page = HTML.ElementFromURL("http://www.freesurfmovies.org/p/movies-liste.html")
    total_links = len(search_page.xpath("//div[@class='post-body entry-content']//div[@dir='ltr']//a"))
    # The XPath query will return a list of all items which match the query.
    links = search_page.xpath("//div[@class='post-body entry-content']//div[@dir='ltr']//a[position() >= "+str(start_index)+" and position() <= "+str(end_index)+"]")

    Log("len(links)> "+str(len(links)))

    for x in range(0,len(links)):
        link = links[x]
        
        title = link.xpath("text()")[0]
        url = link.get("href")
        if url.find("facebook") == -1:            
            video = GetVideoObject(title,url);
            if video is not None:                
                oc.add(video)
    
    if end_index <= total_links:
        oc.add(NextPageObject(key=Callback(GetPageOfVideos, page=page+1), title=L('More >>')))
    
    Log("Num of Items in container: "+str(len(oc)))
    return oc

def GetVideoObject(title, url):
    movie_page = HTML.ElementFromURL(url)
    param = movie_page.xpath("//object/param[@name='movie']")
    video = None
    if param is not None and len(param) > 0:        
        video_url = param[0].get('value');
        
        video = VideoClipObject(
            title = title,        
            url = video_url
        )
    return video
