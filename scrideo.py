import requests
from bs4 import BeautifulSoup
import ffmpeg
import os
import requests
import argparse


CLI=argparse.ArgumentParser()
CLI.add_argument(
  "urls",  # name on the CLI - drop the `--` for positional/required parameters
  nargs="*",  # 0 or more values expected => creates a list
  type=str,
  default=[
    'https://stackoverflow.com/questions/27792934/get-video-fps-using-ffprobe'
, 'https://stackoverflow.com/questions/394809/does-python-have-a-ternary-conditional-operator'
, 'https://hsm.stackexchange.com/questions/15008/how-were-sailing-warships-maneuvered-in-battle-who-coordinated-the-actions-of'
]  # default if nothing is provided
)
urls = CLI.parse_args().urls
urlResponseHtmls = [requests.get(url).content for url in urls]


CONTENT_TYPE_DICT = {
    'soQA': {
        'findAllTag': 'title'
        , 'parentTag': 'head'
    }
}

VIDEO_SETTINGS_DICT = {
    'default': {
        'videoDuration': '30'
        , 'slideColor': 'teal'
        , 'width': '1920'
        , 'height': '1080'
        , 'fontSize': '30'
        , 'fontColor': 'white'
        }
        }

class content:
    _contents = {
        'contentType': None
        , 'html': None
        , 'headTitle': None
        , 'topic': None
        , 'soQuestionTitle': None
        , 'soQuestion': None
        , 'ask': None
        , 'posts': None
    }
    _searchParameters = {
        'findAllTag': None
        , 'parentTag': None
    }    
    
    def __init__(self, html, contentType):
        self._contents['html'] = html
        self._contents['contentType'] = contentType
        #self._findAllTag = 'title'
        #self._parentTag = 'head'
        self._parseContent(html)

    def _parseContent(self, html):
        # parse and filter text, takes filter params
        soup = BeautifulSoup(html, "html.parser")
        # parse stack overflow question title and topic
        if self._contents['contentType'] == 'soQA':
            self._searchParameters['findAllTag'] = 'title'
            self._searchParameters['parentTag'] = 'head'
        self._contents['headTitle'] = [el.text for el in soup.findAll(self._searchParameters['findAllTag']) if el.parent.name == self._searchParameters['parentTag']][0]
        self._topic, self._contents['soQuestionTitle'] = self._contents['headTitle'].split(' - ')[:2]

        # parse question/answer content
        posts = soup.find_all("div", class_="s-prose js-post-body")
        self._contents['posts'] = [post.get_text().replace('\n\n', '\n').replace('\r\n', '\n') for post in posts] #separator='\n'
        # add newline every 135 characters
        n=135
        # make this a regex search instead so that it doesnt add a linebreak where i=100 is just whitespace before or after a linebreak 
        self._contents['posts'] = ['\n'.join([post[i:i+n] for i in range(0, len(post), n)]) for post in self._contents['posts']]
        return self._contents['posts']
        # down the line might be better to join all posts and apply height & width logic to all posts. 


    #### def html to image
    # make each post an  image rendered from html 
    #def _imgFromHtml():


class buildVideo:
    _settings = {
        'videoDuration': None# '12'
        , 'slideColor': None#'teal'
        , 'width': None#'1920'
        , 'height': None#'1080'
        , 'fontSize': None#'30'
        , 'fontColor': None#'white'
    }

    _contentSettings = {
        'text': ''''''
        , 'x': '35'#'(2*n)-text_w'#'(w-text_w)/2' # need to reorganize these attributes so can be updated from the type dict above 
        , 'y': '10'#'(2*n)-text_h' #'(h-text_h)/2'
        , 'outputPath': None #'output4.mp4'
        , 'allContent': None #['Test Slide 1', 'Test Slide 2']
        , 'slideDuration': 5# None #5
        , 'textStart': 0
        , 'textEnd': None
    }

    _content = {}

    def __init__(self, settings, content): 
        self._settings = settings
        self._content = content
        self._contentSettings['allContent'] = content['posts']
        self._contentSettings['textEnd'] = self._contentSettings['textStart'] + self._contentSettings['slideDuration']
        self._build()
        
    def _build(self):
        self._settings['videoDuration'] = self._contentSettings['slideDuration'] * len(self._contentSettings['allContent'])
        textStart, textEnd = [0,self._contentSettings['slideDuration']]
        vf = ''
        for i,content in enumerate(self._contentSettings['allContent']):
            fPath = '{}text{}.txt'.format(self._content['soQuestionTitle'],i)
            with open(fPath, 'w') as f:
                f.write(content)                
            vf += "drawtext=fontfile='/System/Library/Fonts/Supplemental/Arial.ttf':textfile={}:fontsize={}:fontcolor={}:x={}:y={}:enable='between(t,{},{})',".format(
                    fPath
                    , self._settings['fontSize']
                    , self._settings['fontColor']
                    , self._contentSettings['x']
                    , self._contentSettings['y']
                    , textStart
                    , textEnd
                    )
            textStart += self._contentSettings['slideDuration']
            textEnd += self._contentSettings['slideDuration']
        vf = vf[:-1]
        vf += '[out]'
        print('vf filter param:\n', vf)
        
        input = ffmpeg.input(
            "color=c={}:s={}x{}".format(self._settings['slideColor'], self._settings['width'], self._settings['height'])
            , f = "lavfi"
            , t = self._settings['videoDuration']
            )
        
        #filename with incrementing (TODO: move this to a handler class later)
        i = 0
        global os
        while os.path.exists("svo%s.mp4" % i):
            i += 1
        self._contentSettings['outputPath'] = "svo%s.mp4" % i

        output = ffmpeg.output(
            input
            , self._contentSettings['outputPath']
            , vcodec='libx264'
            , vf = vf
            ,  loglevel="quiet" # remove line to see ffmpeg stdout logs 
            )
        output.run()


def main():
    for html in urlResponseHtmls:
        buildVideo(VIDEO_SETTINGS_DICT['default'], content(html,'soQA')._contents)

if __name__ == "__main__":
    main()