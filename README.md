# NOS liveblog tracker

The NOS liveblog tracker is a headline tracker for the Dutch national tv. This tracker will grep the url of an existing liveblog on the [NOS website](https://nos.nl). If there are no liveblogs, the script will display a notice that there are no liveblogs.

## Installation

```bash
git clone https://github.com/hvanderlaan/nos-liveblog-tracker
cd nos-liveblog-tracker
pip install -r requirements.txt
./nos-liveblog-tracker.py [-u/--url <url to livelog>]
```
