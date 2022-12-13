# scrideo
Generate video from scraped content

- scrapes stack exchange content 
- parses and shapes text in content class. 
- builds video from scraped post text using ffmpeg and draw text filter. outputs an mp4 per scraped stack over overflow article. 

# usage
This can be used from the CLI like so: 
`python3 scrideo.py url1 url2 …`

The following example creates 5 videos out of scraped content from stackexchange posts:
`python3 scrideo.py https://softwareengineering.stackexchange.com/questions/442777/accessing-enemies-locations-quickly-in-a-2d-game https://softwareengineering.stackexchange.com/questions/271567/how-can-i-avoid-tight-coupling-when-practically-every-decision-logic-has-to-chec https://softwareengineering.stackexchange.com/questions/365060/using-observer-pattern-to-selectively-act-on-events https://softwareengineering.stackexchange.com/questions/322448/vba-outlook-quickly-find-subfolder https://hermeneutics.stackexchange.com/questions/80322/did-jesus-correctly-state-the-shema-in-`

# to do / wip
- cleanup text formatting: add h/w text wrapping logic that approximates pixels based on font size and video dimensions, chunk long posts to multiple slides 
- add formatting (title slide text from question, label first post as OP and subsequent slides as answers from community)
- extract actual question title from html into contents obj
- add features for directly converting html to an image to construct slides or building html templates to preformat everything. 
