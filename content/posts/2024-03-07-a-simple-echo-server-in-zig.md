---
categories:
    - code
    - zig
date: 2024-03-07 14:58:19.578261-08:00
title: A Simple Echo Server in Zig
---

Recently I've been trying to hone my low-level programming skills.
[Zig](https://ziglang.org/) is cool and it's less painful than Rust.

Eventually I'd like to implement a HTTP server. We'll see if I get
there. As a baby step, here is a simple echo server written in Zig:

<!--more-->

```zig
const std = @import("std");

pub fn main() !void {
    std.debug.print("Starting server\n", .{});
    const self_addr = try std.net.Address.resolveIp("127.0.0.1", 42069);
    var listener = try self_addr.listen(.{ .reuse_address = true });
    std.debug.print("Listening on {}\n", .{self_addr});

    while (listener.accept()) |conn| {
        std.debug.print("Accepted connection from: {}\n", .{conn.address});
        _ = try conn.stream.write("Welcome to my server.\n");
        var buffer: [4096]u8 = undefined;
        while (true) {
            const bytes_recv = try conn.stream.read(&buffer);
            const chunk = buffer[0..bytes_recv];
            if (chunk.len == 0) break;
            std.debug.print("message: {s}", .{chunk});
            _ = try conn.stream.writer().print("No u {s}", .{chunk});
        }
    } else |err| {
        std.debug.print("error in accept: {}\n", .{err});
    }
}
```

Here's what happens when you `telnet 127.0.0.1 42069`
and enter "Learn Zig":

```
❯❯❯ telnet 127.0.0.1 42069
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
Welcome to my server.
Learn Zig!
No u Learn Zig!
```

Note this compiles and runs on Zig version 0.12-dev.
It doesn't even run on 0.11. So YMMV if you are here from the future.
