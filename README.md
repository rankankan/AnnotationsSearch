# AnnotationsSearch
It searches for all annotation entries that contain the substring provided as a parameter.
It returns a list of all indices that contain that substring.

The program makes use of 'memcached' as the infrastructure behind:  an open source implementation of a client/server mechanism which allows for setting of timeouts, expiration dates, starting/stopping/cleaning the cache, etc. Python's interface to memcached is the pymcached package.

The code will be optimized once the format of the data that the cache stores is decided. 
Additional options are foreseen: relevance results list, regex support, tokenization.
