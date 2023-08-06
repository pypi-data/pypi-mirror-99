Vidify - convert img tags to html5 video tags
================================================================================

Vidify is a plugin for Python's Markdown that allows you to embed html5 video
into your document. It's inteneded for Python 3.6 + but is _probably_
back-compatible with 2.7.

Vidifiy works by detecting `<img>` tags pointing at a file with an extension of
.webm, .mp4, or .ogg and replacing them with `<video>` tags.

Installing
---
Simply install from PyPi:
```
pip install markdown-vidify
```

Usage
================================================================================
Simply import the package and then pass it to the extensions parameter of
markdown!
```python
import markdown
import markdown_vidify

# ...

ouptut = markdown.markdown(input, extensions=[
    markdown_vidify.VidifyExtension(
        autoplay=False,
        controls=True,
        loop=False,
        mute=False,
    )
])
```

Options
--------------------------------------------------------------------------------
All default to false:

* autoplay - Autoplay the video once page is loaded
* controls - Display player controls below the video
* loop - Loop the video
* muted - Video is muted by default

Extra Hints!
--------------------------------------------------------------------------------
Consider using the Attribute List plugin that comes with markdown to set the
html5 poster attribute. This will be an image that displays in-place of your
video while it is downloading or until the user hits the play button!

```
![alt](/path/to/video.webm){: poster="/path/to/image.png"}
```

Weird Caveat
--------------------------------------------------------------------------------
Since html5 video doesn't have an alt-text, the body of the [] is entirely
ignored. Other plugins may still use it however. I am aware of how -janky- this
is. I considered using it for the poster tag but that still feels janky and it
would also interfere with other markdown plugins. If you feel you haev a good
usgesstion feel free to post it as an issue.

Boring Stuff
================================================================================
vidify was written by Jason Hamilton-Smith `<hs.jason@gmail.com>`, my website is
[zchfvy.com](https://zchfvy.com).

This project is licensed under the GPL v3.0 license. See the `LICENSE` file for
details.
