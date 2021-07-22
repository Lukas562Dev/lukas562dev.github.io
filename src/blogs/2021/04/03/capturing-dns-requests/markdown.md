How to capture DNS requests in Linux using the `tcpdump` utility.

**Warning: There is a dot after the domain, this is intended output from tcpdump**

The command is:
```sh
sudo tcpdump -l port 53 2>/dev/null | grep --line-buffered ' A? ' | cut -d' ' -f8
```

Let me break it down:
### `sudo tcpdump -l port 53 2>/dev/null`
`sudo` - We can't use tcpdump without root permissions.<br/>
`tcpdump -l` - Run tcpdump with the `-l` flag, which means that it will make stdout line buffered.<br/>
`port 53` - DNS requests go through port 53 so we'll want to capture that<br/>
`2>/dev/null` - Send stderr to `/dev/null`.<br/>
### `grep --line-buffered ' A? '`
`grep --line-buffered` - Run grep with the `--line-buffered` flag, which means that grep will use line buffering.<br/>
`' A? '` - search for <code>&nbsp;A?&nbsp;</code> and only return lines that match.<br/>
### `cut -d' ' -f8`
`cut` - Run the cut utility<br/>
`-d' '` - Use a space as the delimeter<br/>
`-f8` - Get the eigth column<br/>
