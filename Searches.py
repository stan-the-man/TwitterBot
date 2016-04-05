# for experimenting with search terms.


# test of searching twitter. doesn't work yet
# search formatting is messed up somehow...cant search for anything more than a single type of term.
# raw_query = "q=like%20follow%20retweet%20for%20a%20chance%20to%20win"
# results = api.GetSearch(raw_query)

# its annoying that this doesn't work because it's taken directly from the documentation online
# results = api.GetSearch(raw_query="q=twitter%20&result_type=recent&since=2014-07-19&count=100")

#results = api.GetSearch("q=Dubs%20lang%3Aen")
#print([s.text for s in results])
# results = api.GetSearch("q=like%20follow%20retweet%20chance%20win%20lang%3Aen")
# print([s.text for s in results])
# results = api.GetSearch("q=%22like%20follow%20and%20retweet%20for%20a%20chance%20to%20win%22")
# print([s.text for s in results])

# limit results by location in SF. this totally works.
#results = api.GetSearch(geocode=[37.781157, -122.398720, "1mi"])
#print([s.text for s in results])

# comma delineation doesn't work...
#results = api.GetSearch("Warriors", "Clippers")
#print([s.text for s in results])

#results = api.GetSearch("Warriors+Clippers") # warriors+clippers works, but warriors+clippers&count=100 doesnt...
#print([s.text for s in results])

#raw_query="q=twitter%20&result_type=recent&since=2014-07-19&count=100"
#results = api.GetSearch(raw_query="q=twitter%20&result_type=recent&since=2014-07-19&count=100")
#print([s.text for s in results])
