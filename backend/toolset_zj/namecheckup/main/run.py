#!/usr/bin/env python
# encoding:utf-8
import os

from asgiref.sync import sync_to_async
from lxml import etree
import requests
from loguru import logger


class NameCheckUp:
    def __init__(self):
        self.init_data_all = {'facebook': {'name': 'Facebook', 'href': 'https://www.facebook.com'},
                              'twitter': {'name': 'Twitter', 'href': 'https://twitter.com'},
                              'youtube': {'name': 'Youtube', 'href': 'https://www.youtube.com'},
                              'tiktok': {'name': 'TikTok', 'href': 'https://www.tiktok.com/'},
                              'pinterest': {'name': 'Pinterest', 'href': 'https://www.pinterest.com'},
                              'medium': {'name': 'Medium', 'href': 'https://medium.com'},
                              'twitch': {'name': 'Twitch', 'href': 'https://www.twitch.tv'},
                              'tumblr': {'name': 'Tumblr', 'href': 'https://www.tumblr.com'},
                              'github': {'name': 'Github', 'href': 'https://github.com'},
                              'disqus': {'name': 'Disqus', 'href': 'https://disqus.com'},
                              'aboutme': {'name': 'About.me', 'href': 'https://www.about.me'},
                              'meetup': {'name': 'Meetup', 'href': 'https://www.meetup.com'},
                              'periscope': {'name': 'Periscope', 'href': 'https://www.pscp.tv/'},
                              'patreon': {'name': 'Patreon', 'href': 'https://www.patreon.com'},
                              'behance': {'name': 'Behance', 'href': 'https://www.behance.net'},
                              'livejournal': {'name': 'LiveJournal', 'href': 'https://www.livejournal.com'},
                              'buzzfeed': {'name': 'Buzzfeed', 'href': 'https://www.buzzfeed.com'},
                              'vk': {'name': 'Vk', 'href': 'https://www.vk.com'},
                              'blogger': {'name': 'Blogger', 'href': 'https://www.blogger.com'},
                              'wordpress': {'name': 'Wordpress', 'href': 'https://www.wordpress.com'},
                              'spotify': {'name': 'Spotify', 'href': 'https://open.spotify.com'},
                              'gravatar': {'name': 'Gravatar', 'href': 'https://www.gravatar.com'},
                              'bitbucket': {'name': 'Bitbucket', 'href': 'https://bitbucket.org'},
                              'id99designs': {'name': '99Designs', 'href': 'https://99designs.com'},
                              'ifttt': {'name': 'IFTTT', 'href': 'https://ifttt.com'},
                              'slideshare': {'name': 'SlideShare', 'href': 'https://www.slideshare.net'},
                              'deviantart': {'name': 'DeviantArt', 'href': 'https://www.deviantart.com'},
                              'cnet': {'name': 'CNET', 'href': 'https://www.cnet.com'},
                              'shopify': {'name': 'Shopify', 'href': 'https://www.shopify.com'},
                              'askfm': {'name': 'Ask.FM', 'href': 'https://ask.fm'},
                              'sourceforge': {'name': 'SourceForge', 'href': 'https://sourceforge.net'},
                              'soundcloud': {'name': 'SoundCloud', 'href': 'https://soundcloud.com'},
                              'etsy': {'name': 'Etsy', 'href': 'https://www.etsy.com'},
                              'shutterstock': {'name': 'Shutterstock', 'href': 'https://www.shutterstock.com'},
                              'okru': {'name': 'OK.RU', 'href': 'https://ok.ru'},
                              'lastfm': {'name': 'Last.FM', 'href': 'https://www.last.fm'},
                              'vimeo': {'name': 'Vimeo', 'href': 'https://vimeo.com'},
                              'dribble': {'name': '', 'href': 'https://dribbble.com'},
                              'myspace': {'name': 'MySpace', 'href': 'https://myspace.com'},
                              'slack': {'name': 'Slack', 'href': 'https://slack.com'},
                              'quora': {'name': 'Quora', 'href': 'https://www.quora.com'},
                              'wikipedia': {'name': 'Wikipedia', 'href': 'https://wikipedia.org'},
                              'dailymotion': {'name': 'Dailymotion', 'href': 'https://www.dailymotion.com'},
                              'goodreads': {'name': 'Goodreads', 'href': 'https://www.goodreads.com'},
                              'indiegogo': {'name': 'Indiegogo', 'href': 'https://www.indiegogo.com'},
                              'taskrabbit': {'name': 'TaskRabbit', 'href': 'https://www.taskrabbit.com'},
                              'devto': {'name': 'Dev.to', 'href': 'https://dev.to'},
                              'id9gag': {'name': '9gag', 'href': 'https://9gag.com'},
                              'houzz': {'name': 'Houzz', 'href': 'https://www.houzz.com'},
                              'gitlab': {'name': 'GitLab', 'href': 'https://gitlab.com'},
                              'mastodon': {'name': 'Mastodon', 'href': 'https://mastodon.social'},
                              'imageshack': {'name': 'ImageShack', 'href': 'https://imageshack.com'},
                              'steamcommunity': {'name': 'Steam', 'href': 'http://steamcommunity.com'},
                              'hackernoon': {'name': 'Hacker Noon', 'href': 'https://hackernoon.com/'},
                              'wikihow': {'name': 'WikiHow', 'href': 'https://www.wikihow.com/'},
                              'discord': {'name': 'Discord', 'href': 'https://discord.io'},
                              'telegram': {'name': 'Telegram', 'href': 'https://telegram.org'},
                              'ebay': {'name': 'Ebay', 'href': 'https://www.ebay.com'},
                              'producthunt': {'name': 'Product Hunt', 'href': 'https://www.producthunt.com'},
                              'donationalerts': {'name': 'DonationAlerts', 'href': 'https://www.donationalerts.com'},
                              'linktree': {'name': 'Linktree', 'href': 'https://linktr.ee'},
                              'photobucket': {'name': 'Photobucket', 'href': 'https://www.photobucket.com'},
                              'roblox': {'name': 'Roblox', 'href': 'https://www.roblox.com'},
                              'ign': {'name': 'IGN', 'href': 'https://ign.com'},
                              'basecamp': {'name': 'Basecamp', 'href': 'https://basecamp.com/'},
                              'quizlet': {'name': 'Quizlet', 'href': 'https://quizlet.com/'},
                              'genius': {'name': 'Genius', 'href': 'https://genius.com'},
                              'steemit': {'name': 'Steemit', 'href': 'https://www.steemit.com'},
                              'fandom': {'name': 'Fandom', 'href': 'https://www.fandom.com'},
                              'smugmug': {'name': 'SmugMug', 'href': 'https://smugmug.com'},
                              'gumroad': {'name': 'Gumroad', 'href': 'https://gumroad.com'},
                              'eyeem': {'name': 'EyeEm', 'href': 'https://www.eyeem.com'},
                              'wowhead': {'name': 'Wowhead', 'href': 'https://www.wowhead.com'},
                              'scribd': {'name': 'Scribd', 'href': 'https://scribd.com'},
                              'pixiv': {'name': 'Pixiv', 'href': 'https://pixiv.net'},
                              'fanpop': {'name': 'Fanpop', 'href': 'http://www.fanpop.com'},
                              'coderwall': {'name': 'Coderwall', 'href': 'https://coderwall.com'},
                              'kongregate': {'name': 'Kongregate', 'href': 'https://www.kongregate.com'},
                              'pastebin': {'name': 'Pastebin', 'href': 'https://pastebin.com'},
                              'tripit': {'name': 'TripIt', 'href': 'https://www.tripit.com'},
                              'zenfolio': {'name': 'Zenfolio', 'href': 'https://zenfolio.com'},
                              'flipboard': {'name': 'Flipboard', 'href': 'https://flipboard.com'},
                              'designspiration': {'name': 'Designspiration', 'href': 'https://www.designspiration.net'},
                              'mix': {'name': 'Mix', 'href': 'https://mix.com'},
                              'newgrounds': {'name': 'Newgrounds', 'href': 'https://newgrounds.com'},
                              'younow': {'name': 'YouNow', 'href': 'https://www.younow.com/'},
                              'wattpad': {'name': 'Wattpad', 'href': 'https://www.wattpad.com'},
                              'reverbnation': {'name': 'ReverbNation', 'href': 'https://www.reverbnation.com'},
                              'bandcamp': {'name': 'Bandcamp', 'href': 'https://bandcamp.com'},
                              'myportfolio': {'name': 'Adobe Portfolio', 'href': 'https://myportfolio.com'},
                              'venmo': {'name': 'Venmo', 'href': 'https://venmo.com'},
                              'hubpages': {'name': 'HubPages', 'href': 'https://hubpages.com'},
                              'contently': {'name': 'Contently', 'href': 'https://contently.com'},
                              'ello': {'name': 'Ello', 'href': 'https://ello.co'},
                              'codementor': {'name': 'Codementor', 'href': 'https://www.codementor.io'},
                              'trakt': {'name': 'Trakt', 'href': 'https://trakt.tv'},
                              'stocksnap': {'name': 'StockSnap', 'href': 'https://stocksnap.io'},
                              'letterboxd': {'name': 'Letterboxd', 'href': 'https://letterboxd.com'},
                              'keybase': {'name': 'Keybase', 'href': 'https://keybase.io'},
                              'imgbin': {'name': 'Imgbin', 'href': 'https://imgbin.com'},
                              'unsplash': {'name': 'Unsplash', 'href': 'https://unsplash.com'},
                              'alamy': {'name': 'Alamy', 'href': 'https://www.alamy.com'},
                              'codecademy': {'name': 'Codecademy', 'href': 'https://www.codecademy.com'},
                              'shutterfly': {'name': 'Shutterfly', 'href': 'https://shutterfly.com'},
                              'sketchfab': {'name': 'Sketchfab', 'href': 'https://sketchfab.com'},
                              'journoportfolio': {'name': 'Journo Portfolio', 'href': 'https://journoportfolio.com'},
                              'portfoliobox': {'name': 'Portfoliobox', 'href': 'https://portfoliobox.net'},
                              'cargo': {'name': 'Cargo', 'href': 'https://cargo.site'},
                              'lifeofpix': {'name': 'Life of Pix', 'href': 'https://www.lifeofpix.com'},
                              'burst': {'name': 'Burst', 'href': 'https://burst.shopify.com'},
                              'kaboompics': {'name': 'Kaboompics', 'href': 'https://kaboompics.com'},
                              'zillow': {'name': 'Zillow', 'href': 'https://www.zillow.com'},
                              'ulule': {'name': 'Ulule', 'href': 'https://www.ulule.com'},
                              'strava': {'name': 'Strava', 'href': 'http://strava.com'},
                              'gamespot': {'name': 'GameSpot', 'href': 'https://www.gamespot.com'},
                              'ultguitar': {'name': 'Ultimate Guitar', 'href': 'https://www.ultimate-guitar.com'},
                              'discogs': {'name': 'Discogs', 'href': 'https://www.discogs.com'},
                              'jimdo': {'name': 'Jimdo', 'href': 'https://jimdo.com'},
                              'metacritic': {'name': 'Metacritic', 'href': 'http://www.metacritic.com'},
                              'redbubble': {'name': 'Redbubble', 'href': 'https://www.redbubble.com'},
                              'flightaware': {'name': 'Flightaware', 'href': 'https://flightaware.com'},
                              'fool': {'name': 'The Motley Fool', 'href': 'https://fool.com'},
                              'weebly': {'name': 'Weebly', 'href': 'https://weebly.com'},
                              'moddb': {'name': 'Mod DB', 'href': 'http://www.moddb.com'},
                              'cracked': {'name': 'Cracked', 'href': 'https://www.cracked.com'},
                              'plurk': {'name': 'Plurk', 'href': 'https://www.plurk.com'},
                              'toluna': {'name': 'Toluna', 'href': 'https://toluna.com'},
                              'issuu': {'name': 'Issuu', 'href': 'https://issuu.com'},
                              'weheartit': {'name': 'We Heart It', 'href': 'https://weheartit.com'},
                              'dzone': {'name': 'DZone', 'href': 'https://dzone.com'},
                              'cheezburger': {'name': 'CHEEZburger', 'href': 'https://www.cheezburger.com'},
                              'hi5': {'name': 'Hi5', 'href': 'https://www.hi5.com'},
                              'armorgames': {'name': 'Armor Games', 'href': 'http://armorgames.com'},
                              'slashdot': {'name': 'Slashdot', 'href': 'https://slashdot.org'},
                              'netvibes': {'name': 'Netvibes', 'href': 'https://www.netvibes.com'},
                              'fark': {'name': 'Fark', 'href': 'https://www.fark.com'},
                              'wonderhowto': {'name': 'Wonder How To', 'href': 'https://wonderhowto.com'},
                              'skyrock': {'name': 'Skyrock', 'href': 'https://skyrock.com'},
                              'fatsecret': {'name': 'FatSecret', 'href': 'https://www.fatsecret.com'},
                              'proboards': {'name': 'ProBoards', 'href': 'https://www.proboards.com'},
                              'spreaker': {'name': 'Spreaker', 'href': 'https://www.spreaker.com'},
                              'mouthshut': {'name': 'MouthShut', 'href': 'https://www.mouthshut.com'},
                              'biggerpockets': {'name': 'BiggerPockets', 'href': 'https://www.biggerpockets.com'},
                              'spectrum': {'name': 'Spectrum', 'href': 'https://spectrum.chat'},
                              'sparkpeople': {'name': 'SparkPeople', 'href': 'https://www.sparkpeople.com'},
                              'dreamstime': {'name': 'Dreamstime', 'href': 'https://www.dreamstime.com'},
                              'ebaumsworld': {'name': "eBaum's World", 'href': 'https://www.ebaumsworld.com'},
                              'listal': {'name': 'Listal', 'href': 'https://listal.com'},
                              'udemy': {'name': 'Udemy', 'href': 'https://www.udemy.com '},
                              'chess': {'name': 'Chess', 'href': 'https://www.chess.com'},
                              'fodors': {'name': 'Fodors Travel', 'href': 'https://www.fodors.com'},
                              'techsupportalert': {'name': "Gizmo's Freeware",
                                                   'href': 'https://www.techsupportalert.com'},
                              'audiojungle': {'name': 'AudioJungle', 'href': 'https://audiojungle.net'},
                              'datpiff': {'name': 'DatPiff', 'href': 'https://www.datpiff.com'},
                              'diigo': {'name': 'Diigo', 'href': 'https://diigo.com'},
                              'shockwave': {'name': 'Shockwave', 'href': 'http://www.shockwave.com'},
                              'metacafe': {'name': 'Metacafe', 'href': 'https://www.metacafe.com'},
                              'feedburner': {'name': 'FeedBurner', 'href': 'http://feedburner.com'},
                              'slideserve': {'name': 'SlideServe', 'href': 'https://www.slideserve.com'},
                              'blogtalkradio': {'name': 'BlogTalkRadio', 'href': 'https://www.blogtalkradio.com'},
                              'awwwards': {'name': 'Awwwards', 'href': 'https://www.awwwards.com'},
                              'techdirt': {'name': 'Techdirt', 'href': 'https://www.techdirt.com'},
                              'bitly': {'name': 'BitLy', 'href': 'https://bit.ly'},
                              'trendhunter': {'name': 'TrendHunter', 'href': 'https://www.trendhunter.com'},
                              'mapmyrun': {'name': 'MapMyRun', 'href': 'https://www.mapmyrun.com'},
                              'carbonmade': {'name': 'Carbonmade', 'href': 'https://carbonmade.com'},
                              'blurb': {'name': 'Blurb', 'href': 'https://www.blurb.com'},
                              'programmableweb': {'name': 'ProgrammableWeb', 'href': 'https://www.programmableweb.com'},
                              'photoshelter': {'name': 'PhotoShelter', 'href': 'https://photoshelter.com'},
                              'fmylife': {'name': 'FMyLife', 'href': 'https://www.fmylife.com'},
                              'codecanyon': {'name': 'CodeCanyon ', 'href': 'https://codecanyon.net'},
                              'pluralsight': {'name': 'Pluralsight ', 'href': 'https://pluralsight.com'},
                              'geeksforgeeks': {'name': 'GeeksforGeeks ', 'href': 'https://geeksforgeeks.org'},
                              'instapaper': {'name': 'Instapaper ', 'href': 'https://www.instapaper.com'},
                              'meneame': {'name': 'Meneame ', 'href': 'https://www.meneame.net'},
                              'xing': {'name': 'XING ', 'href': 'https://www.xing.com'},
                              'typepad': {'name': 'Typepad ', 'href': 'https://typepad.com'},
                              'theverge': {'name': 'The Verge ', 'href': 'https://www.theverge.com'},
                              'kinja': {'name': 'Kinja ', 'href': 'https://kinja.com'},
                              'npmjs': {'name': 'npm', 'href': 'https://www.npmjs.com'},
                              'ecwid': {'name': 'Ecwid', 'href': 'https://ecwid.com'},
                              'symbaloo': {'name': 'Symbaloo', 'href': 'https://www.symbaloo.com'},
                              'wykop': {'name': 'Wykop', 'href': 'https://www.wykop.pl'},
                              'bigstockphoto': {'name': 'Bigstock', 'href': 'https://www.bigstockphoto.com'},
                              'artsy': {'name': 'Artsy', 'href': 'https://www.artsy.net'},
                              'screencast': {'name': 'Screencast', 'href': 'https://www.screencast.com'},
                              'teamtreehouse': {'name': 'Treehouse', 'href': 'https://teamtreehouse.com'},
                              'saatchiart': {'name': 'Saatchi Art', 'href': 'http://www.saatchiart.com'},
                              'artfinder': {'name': 'Artfinder', 'href': 'https://www.artfinder.com'},
                              'society6': {'name': 'Society6', 'href': 'https://society6.com'},
                              'wish': {'name': 'Wish', 'href': 'https://www.wish.com'},
                              'storenvy': {'name': 'Storenvy', 'href': 'https://www.storenvy.com'},
                              'bigcartel': {'name': 'Big Cartel', 'href': 'https://bigcartel.com'},
                              'sellfy': {'name': 'Sellfy', 'href': 'https://sellfy.com'},
                              'premiumbeat': {'name': 'PremiumBeat', 'href': 'https://www.premiumbeat.com'},
                              'bloglovin': {'name': "Bloglovin'", 'href': 'https://www.bloglovin.com'},
                              'calendly': {'name': 'Calendly', 'href': 'https://calendly.com'},
                              'coub': {'name': 'Coub', 'href': 'https://coub.com'},
                              'couchsurfing': {'name': 'Couchsurfing', 'href': 'https://www.couchsurfing.com/'},
                              'dailykos': {'name': 'Daily Kos', 'href': 'https://www.dailykos.com'},
                              'd3': {'name': 'D3.ru', 'href': 'https://d3.ru'},
                              'dwell': {'name': 'Dwell', 'href': 'https://www.dwell.com'},
                              'themeforest': {'name': 'Themeforest', 'href': 'https://themeforest.net/'},
                              'graphicriver': {'name': 'GraphicRiver', 'href': 'https://graphicriver.net'},
                              'videohive': {'name': 'VideoHive', 'href': 'https://videohive.net'},
                              'elementsenvato': {'name': 'Envato Elements', 'href': 'https://elements.envato.com'},
                              'tutsplus': {'name': 'TutsPlus', 'href': 'https://tutsplus.com'},
                              'studioenvato': {'name': 'Envato Studio', 'href': 'https://studio.envato.com/'},
                              'epicurious': {'name': 'Epicurious', 'href': 'https://www.epicurious.com'},
                              'eurogamer': {'name': 'Eurogamer', 'href': 'https://www.eurogamer.net'},
                              'filmow': {'name': 'Filmow', 'href': 'https://filmow.com/'},
                              'flyertalk': {'name': 'FlyerTalk', 'href': 'https://www.flyertalk.com'},
                              'freepik': {'name': 'Freepik', 'href': 'https://www.freepik.com'},
                              'giantbomb': {'name': 'Giant Bomb', 'href': 'https://www.giantbomb.com'},
                              'gfycat': {'name': 'Gfycat', 'href': 'https://gfycat.com'},
                              'giphy': {'name': 'Giphy', 'href': 'https://giphy.com'},
                              'zotero': {'name': 'Zotero', 'href': 'https://www.zotero.org'},
                              'wireclub': {'name': 'Wireclub', 'href': 'https://www.wireclub.com'},
                              'untappd': {'name': 'Untappd', 'href': 'https://untappd.com'},
                              'hackster': {'name': 'Hackster', 'href': 'https://www.hackster.io'},
                              'hypebeast': {'name': 'Hypebeast', 'href': 'https://hypebeast.com'},
                              'instructables': {'name': 'Instructables', 'href': 'https://www.instructables.com'},
                              'teletypein': {'name': 'Teletype', 'href': 'https://teletype.in'},
                              'boosty': {'name': 'Boosty.to', 'href': 'https://boosty.to'}}
        self.init_data = {'facebook': {'name': 'Facebook', 'href': 'https://www.facebook.com'},
                          'twitter': {'name': 'Twitter', 'href': 'https://twitter.com'},
                          'youtube': {'name': 'Youtube', 'href': 'https://www.youtube.com'},
                          'tiktok': {'name': 'TikTok', 'href': 'https://www.tiktok.com/'},
                          'pinterest': {'name': 'Pinterest', 'href': 'https://www.pinterest.com'},
                          'medium': {'name': 'Medium', 'href': 'https://medium.com'},
                          'twitch': {'name': 'Twitch', 'href': 'https://www.twitch.tv'},
                          'tumblr': {'name': 'Tumblr', 'href': 'https://www.tumblr.com'},
                          'github': {'name': 'Github', 'href': 'https://github.com'},
                          'disqus': {'name': 'Disqus', 'href': 'https://disqus.com'},
                          'aboutme': {'name': 'About.me', 'href': 'https://www.about.me'},
                          'meetup': {'name': 'Meetup', 'href': 'https://www.meetup.com'},
                          'periscope': {'name': 'Periscope', 'href': 'https://www.pscp.tv/'},
                          'patreon': {'name': 'Patreon', 'href': 'https://www.patreon.com'},
                          'behance': {'name': 'Behance', 'href': 'https://www.behance.net'},
                          'livejournal': {'name': 'LiveJournal', 'href': 'https://www.livejournal.com'},
                          'buzzfeed': {'name': 'Buzzfeed', 'href': 'https://www.buzzfeed.com'},
                          'vk': {'name': 'Vk', 'href': 'https://www.vk.com'},
                          'blogger': {'name': 'Blogger', 'href': 'https://www.blogger.com'},
                          'wordpress': {'name': 'Wordpress', 'href': 'https://www.wordpress.com'},
                          'spotify': {'name': 'Spotify', 'href': 'https://open.spotify.com'},
                          'gravatar': {'name': 'Gravatar', 'href': 'https://www.gravatar.com'},
                          'bitbucket': {'name': 'Bitbucket', 'href': 'https://bitbucket.org'},
                          'id99designs': {'name': '99Designs', 'href': 'https://99designs.com'},
                          'ifttt': {'name': 'IFTTT', 'href': 'https://ifttt.com'},
                          'slideshare': {'name': 'SlideShare', 'href': 'https://www.slideshare.net'},
                          'deviantart': {'name': 'DeviantArt', 'href': 'https://www.deviantart.com'},
                          'cnet': {'name': 'CNET', 'href': 'https://www.cnet.com'},
                          'shopify': {'name': 'Shopify', 'href': 'https://www.shopify.com'},
                          'askfm': {'name': 'Ask.FM', 'href': 'https://ask.fm'},
                          'sourceforge': {'name': 'SourceForge', 'href': 'https://sourceforge.net'},
                          'soundcloud': {'name': 'SoundCloud', 'href': 'https://soundcloud.com'},
                          'etsy': {'name': 'Etsy', 'href': 'https://www.etsy.com'},
                          'shutterstock': {'name': 'Shutterstock', 'href': 'https://www.shutterstock.com'},
                          'okru': {'name': 'OK.RU', 'href': 'https://ok.ru'},
                          'lastfm': {'name': 'Last.FM', 'href': 'https://www.last.fm'},
                          'vimeo': {'name': 'Vimeo', 'href': 'https://vimeo.com'},
                          'dribble': {'name': '', 'href': 'https://dribbble.com'},
                          'myspace': {'name': 'MySpace', 'href': 'https://myspace.com'},
                          'slack': {'name': 'Slack', 'href': 'https://slack.com'},
                          'quora': {'name': 'Quora', 'href': 'https://www.quora.com'},
                          'wikipedia': {'name': 'Wikipedia', 'href': 'https://wikipedia.org'},
                          'dailymotion': {'name': 'Dailymotion', 'href': 'https://www.dailymotion.com'},
                          'goodreads': {'name': 'Goodreads', 'href': 'https://www.goodreads.com'},
                          'indiegogo': {'name': 'Indiegogo', 'href': 'https://www.indiegogo.com'},
                          'taskrabbit': {'name': 'TaskRabbit', 'href': 'https://www.taskrabbit.com'},
                          'devto': {'name': 'Dev.to', 'href': 'https://dev.to'},
                          'id9gag': {'name': '9gag', 'href': 'https://9gag.com'},
                          'houzz': {'name': 'Houzz', 'href': 'https://www.houzz.com'},
                          'gitlab': {'name': 'GitLab', 'href': 'https://gitlab.com'},
                          'mastodon': {'name': 'Mastodon', 'href': 'https://mastodon.social'},
                          'imageshack': {'name': 'ImageShack', 'href': 'https://imageshack.com'},
                          'steamcommunity': {'name': 'Steam', 'href': 'http://steamcommunity.com'},
                          'hackernoon': {'name': 'Hacker Noon', 'href': 'https://hackernoon.com/'},
                          'wikihow': {'name': 'WikiHow', 'href': 'https://www.wikihow.com/'},
                          'discord': {'name': 'Discord', 'href': 'https://discord.io'},
                          'telegram': {'name': 'Telegram', 'href': 'https://telegram.org'},
                          'ebay': {'name': 'Ebay', 'href': 'https://www.ebay.com'},
                          'producthunt': {'name': 'Product Hunt', 'href': 'https://www.producthunt.com'},
                          'donationalerts': {'name': 'DonationAlerts', 'href': 'https://www.donationalerts.com'},
                          'linktree': {'name': 'Linktree', 'href': 'https://linktr.ee'},
                          'photobucket': {'name': 'Photobucket', 'href': 'https://www.photobucket.com'},
                          'roblox': {'name': 'Roblox', 'href': 'https://www.roblox.com'},
                          'ign': {'name': 'IGN', 'href': 'https://ign.com'},
                          'basecamp': {'name': 'Basecamp', 'href': 'https://basecamp.com/'},
                          'quizlet': {'name': 'Quizlet', 'href': 'https://quizlet.com/'},
                          'genius': {'name': 'Genius', 'href': 'https://genius.com'},
                          'steemit': {'name': 'Steemit', 'href': 'https://www.steemit.com'},
                          'fandom': {'name': 'Fandom', 'href': 'https://www.fandom.com'}}

    def single_username_list(self):
        # response = requests.get("https://namecheckup.com/full")
        response = requests.get("https://namecheckup.com")
        root = etree.HTML(response.text)
        username_list = root.xpath('//div[contains(@class,"single_username_list")]')
        print(len(username_list))
        result = {}
        for u in username_list:
            un = u.xpath('a/span/text()')
            href = u.xpath('a/@href')
            id = u.xpath('a/@id')
            img = u.xpath('a/img/@src')
            name = un[0] if un else ''
            href = href[0] if href else ''
            id = id[0] if id else ''
            img = img[0] if img else ''
            print(id, name, href, img)
            result[id] = {'name': name, 'href': href}

            # if img:
            #     self.down_svg(img)
        print(result)

    def down_svg(self, img):
        url = "https://namecheckup.com" + img
        img_name = os.path.basename(img)
        response = requests.get(url)
        with open(os.path.join("../images", img_name), "wb") as code:
            code.write(response.content)

    def check(self, name, media):
        url = "https://namecheckup.com/api/v1/media/check"
        payload = f'data%5Bname%5D={name}&data%5Bmedia%5D={media}&data%5Btx%5D=2'
        headers = {
            'referer': 'https://namecheckup.com/',
            'referrer': '/',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()['data']


async def search_extranet(query, key):
    n = NameCheckUp()
    d = await sync_to_async(n.check)(name=query, media=key)
    data = {'query': query, 'key': key, "info": n.init_data[d['media']], "available": d['available'], "tx": d['tx']}

    logger.info("[检索全网网络ID] APP 执行参数为: {query}", query=query)
    return {"status": 0, "result": data}


async def infos(all=False):
    n = NameCheckUp()
    logger.info("[检索全网网络ID] APP 执行参数为: {all}", all=all)

    if all:
        return {"status": 0, "result": n.init_data_all}
    else:
        return {"status": 0, "result": n.init_data}


if __name__ == '__main__':
    n = NameCheckUp()
    n.single_username_list()
    # a = n.check("facksxx")
    # print(a)
