# youtube_synopsis

Youtube Synopsis downloads and generates a colored "summary" of a Youtube video.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install youtube_synopsis.

```bash
pip install youtube-synopsis
```

## Usage

```python
import youtube_synopsis as yts

# yts takes in a search phrase, the number of stripes, and the format
args = []
args.append( 'bbibbi iu' ) # search phrase
args.append( 100 )         # Number of stripes
args.append( 'rec' )       # Format, takes "square", "sqr", "rectangle", or "rec"

yts.youtube_synopsis.main( args ) # Returns path to the synopsis
```