---
categories:
    - code
    - zig
date: 2024-03-16 23:21:45.066943-07:00
title: Writing a HTTP Server in Zig
---

I continue my Zig adventure by following up [an echo server](/2024/03/a-simple-echo-server-in-zig/)
with a [HTTP server](https://github.com/Fingel/zig-http-server/tree/main).

I've been doing web development the majority of my career. Yet I never really thought too much about
HTTP servers, much less what it would take to implement one. So it made perfect sense for me when I
started to learn Zig to build one. The problem space is a nice mix of socket programming and
string handling.

The source is available [on Github](https://github.com/Fingel/zig-http-server/tree/main).

To start the server:

```
zig run http.zig
```

I'm not super confident that any of the following code is "good Zig" but here it is anyways.

### Constants: Errors and Mime-Types

I defined program-wide custom errors at the top where they are easy to reference. As well
as an anonymous struct of structs that maps file extensions to mime-type strings. This is
important later.

```zig
const std = @import("std");
const net = std.net;
const fs = std.fs;
const mem = std.mem;
const expect = std.testing.expect;

pub const ServeFileError = error{
    HeaderMalformed,
    MethodNotSupported,
    ProtoNotSupported,
    UnknownMimeType,
};

const mimeTypes = .{
    .{ ".html", "text/html" },
    .{ ".css", "text/css" },
    .{ ".png", "image/png" },
    .{ ".jpg", "image/jpeg" },
    .{ ".gif", "image/gif" },
};
```

I really do like how Zig does error handling. The error-tuples reminds me of Golang, but without
the annoying need to handle them explicitly every time they are returned.

### The Main Loop

This is the main loop off the program. I probably could have factored it more.

It starts off with some pretty standard socket programming: listening on an address
and then setting up a loop to listen for data on that address. The Zig standard library
seems well designed here.

I also encountered my first browser behavioral peculiarity. It would seem that (at least Firefox)
attempts to open a connect to the remote server of the target of an anchor tag when the user
hovers over it with their mouse. Presumably this is to optimize load speed in anticipation of
a click. However no data is actually sent until the user clicks, and will time out after about 10
seconds. This required a special case in this code.

The majority of the rest of the code is string parsing/formatting, followed by sending the
result down the socket to the browser.

```zig
pub fn main() !void {
    std.debug.print("Starting server\n", .{});
    const self_addr = try net.Address.resolveIp("0.0.0.0", 4206);
    var listener = try self_addr.listen(.{ .reuse_address = true });
    std.debug.print("Listening on {}\n", .{self_addr});

    while (listener.accept()) |conn| {
        std.debug.print("Accepted connection from: {}\n", .{conn.address});
        var recv_buf: [4096]u8 = undefined;
        var recv_total: usize = 0;
        while (conn.stream.read(recv_buf[recv_total..])) |recv_len| {
            if (recv_len == 0) break;
            recv_total += recv_len;
            if (mem.containsAtLeast(u8, recv_buf[0..recv_total], 1, "\r\n\r\n")) {
                break;
            }
        } else |read_err| {
            return read_err;
        }
        const recv_data = recv_buf[0..recv_total];
        if (recv_data.len == 0) {
            // Browsers (or firefox?) attempt to optimize for speed
            // by opening a connection to the server once a user highlights
            // a link, but doesn't start sending the request until it's
            // clicked. The request eventually times out so we just
            // go agane.
            std.debug.print("Got connection but no header!\n", .{});
            continue;
        }
        const header = try parseHeader(recv_data);
        const path = try parsePath(header.requestLine);
        const mime = mimeForPath(path);
        const buf = openLocalFile(path) catch |err| {
            if (err == error.FileNotFound) {
                _ = try conn.stream.writer().write(http404());
                continue;
            } else {
                return err;
            }
        };
        std.debug.print("SENDING----\n", .{});
        const httpHead =
            "HTTP/1.1 200 OK \r\n" ++
            "Connection: close\r\n" ++
            "Content-Type: {s}\r\n" ++
            "Content-Length: {}\r\n" ++
            "\r\n";
        _ = try conn.stream.writer().print(httpHead, .{ mime, buf.len });
        _ = try conn.stream.writer().write(buf);
    } else |err| {
        std.debug.print("error in accept: {}\n", .{err});
    }
}
```

### Parsing the header

This is straight string parsing. While the std library has some nice inclusions, coming
from Python this still seems verbose and difficult. But perhaps that's not a fair comparison.

I used structs here to give some structure to the return type of the `parseHeader` function.

```zig
const HeaderNames = enum {
    Host,
    @"User-Agent",
};

const HTTPHeader = struct {
    requestLine: []const u8,
    host: []const u8,
    userAgent: []const u8,

    pub fn print(self: HTTPHeader) void {
        std.debug.print("{s} - {s}\n", .{
            self.requestLine,
            self.host,
        });
    }
};

pub fn parseHeader(header: []const u8) !HTTPHeader {
    var headerStruct = HTTPHeader{
        .requestLine = undefined,
        .host = undefined,
        .userAgent = undefined,
    };
    var headerIter = mem.tokenizeSequence(u8, header, "\r\n");
    headerStruct.requestLine = headerIter.next() orelse return ServeFileError.HeaderMalformed;
    while (headerIter.next()) |line| {
        const nameSlice = mem.sliceTo(line, ':');
        if (nameSlice.len == line.len) return ServeFileError.HeaderMalformed;
        const headerName = std.meta.stringToEnum(HeaderNames, nameSlice) orelse continue;
        const headerValue = mem.trimLeft(u8, line[nameSlice.len + 1 ..], " ");
        switch (headerName) {
            .Host => headerStruct.host = headerValue,
            .@"User-Agent" => headerStruct.userAgent = headerValue,
        }
    }
    return headerStruct;
}
```

At least we have slices!

### Parsing the Request Path

Again, this is normal string parsing. We do ensure that the browser is only performing a
GET over HTTP/1.1

```zig
pub fn parsePath(requestLine: []const u8) ![]const u8 {
    var requestLineIter = mem.tokenizeScalar(u8, requestLine, ' ');
    const method = requestLineIter.next().?;
    if (!mem.eql(u8, method, "GET")) return ServeFileError.MethodNotSupported;
    const path = requestLineIter.next().?;
    if (path.len <= 0) return error.NoPath;
    const proto = requestLineIter.next().?;
    if (!mem.eql(u8, proto, "HTTP/1.1")) return ServeFileError.ProtoNotSupported;
    if (mem.eql(u8, path, "/")) {
        return "/index.html";
    }
    return path;
}
```

### Reading the Local File

The File API seems to be well thought out in Zig. Here we translate the requested
path into a local file - or else return an `error.FileNotFound` which we can easily
translate into a 404 status higher up the call stack.

```zig
pub fn openLocalFile(path: []const u8) ![]u8 {
    const localPath = path[1..];
    const file = fs.cwd().openFile(localPath, .{}) catch |err| switch (err) {
        error.FileNotFound => {
            std.debug.print("File not found: {s}\n", .{localPath});
            return error.FileNotFound;
        },
        else => return err,
    };
    defer file.close();
    std.debug.print("file: {}\n", .{file});
    const memory = std.heap.page_allocator;
    const maxSize = std.math.maxInt(usize);
    return try file.readToEndAlloc(memory, maxSize);
}
```

Speaking of 404s, this is what that looks like:

```zig
pub fn http404() []const u8 {
    return "HTTP/1.1 404 NOT FOUND \r\n" ++
        "Connection: close\r\n" ++
        "Content-Type: text/html; charset=utf8\r\n" ++
        "Content-Length: 9\r\n" ++
        "\r\n" ++
        "NOT FOUND";
}
```

### Detecting the mime-type.

Nothing too interesting here, but necessary:

```zig
pub fn mimeForPath(path: []const u8) []const u8 {
    const extension = std.fs.path.extension(path);
    inline for (mimeTypes) |kv| {
        if (mem.eql(u8, extension, kv[0])) {
            return kv[1];
        }
    }
    return "application/octet-stream";
}
```

### Testing

Originally I was writing tests inline adjacent to the functions they were testing. I think
I might like doing that, for smaller files with a focused purpose. But for this project I moved
the files out to `test_http.zig` for clarity. They can be run with `zig test test_http.zig`.

### Final Thoughts

This was an extremely fun exercise to lean more Zig. The cool thing about an HTTP
server is that there is so much to implement but a lot of it isn't very complex. However,
I think I'm going to leave this one here.
