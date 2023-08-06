# HeaderBreakdown
flattens a collection of HTTP headers into a JSON structure for automated analysis

### Example Usage
```
from headerbreakdown import HeaderBreakdown
import json

#
# SAMPLE HEADERS
#
# header with multiple Host and User-Agent values
H1 = "GET /?gws_rd=ssl HTTP/1.1\r\nHost: www.google.com\r\nHost: www.bing.com\r\nHost: www.yahoo.com\r\nConnection: keep-alive\r\nAccept-Encoding: gzip, deflate\r\nAccept: */*\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/99.0\r\nCookie: 1P_JAR=2021-03-13-04"
# single header as a plain string (with no \r\n)
H2 = "Set-Cookie: k1=v1;k2=v2"
# normal header examples that terminate with \r\n\r\n
H3 = "HTTP/1.1 302 Found\r\nLocation: https://www.google.com/?gws_rd=ssl\r\nCache-Control: private\r\nContent-Type: text/html; charset=UTF-8\r\nDate: Sat, 13 Mar 2021 04:15:44 GMT\r\nServer: gws\r\nContent-Length: 231\r\nX-XSS-Protection: 0\r\nX-Frame-Options: SAMEORIGIN\r\nSet-Cookie: 1P_JAR=2021-03-13-04; expires=Mon, 12-Apr-2021 04:15:44 GMT; path=/; domain=.google.com; Secure; SameSite=none\r\n\r\n"
H4 = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nSet-Cookie: k1=v1;k2=v2\r\n\r\n"
H5 = "GET / HTTP/1.1\r\nHost: google.com\r\nUser-Agent: BLAHBLAH\r\nAccept: text/plain\r\n\r\n"

#
# USAGE
#
h = HeaderBreakdown(H1)
print(h.output) # dictionary
print(h.json) # string
print(h.summary)
# etc
```
### Available Attributes (all except summary included in output and json)
```
# dictionaries
	output
	nested_output
# lists
	notices
# strings
	json
	nested_json
	direction
	http_version
	method
	host
	path
	user_agent
	response_code
	response_phrase
	summary
```

### Releases and Updates
- 2021-03-23
	- minor edits, added summary and nested_output/nested_json attributes
- 2021-03-13
	- first release
