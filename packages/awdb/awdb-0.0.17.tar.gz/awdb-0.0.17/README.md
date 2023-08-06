Awesome Web Debugger
====================

How to use
==========

Run the command `awdb-server` to start a server for debugging. The webserver runs on port 8080 by
default. It will listen for websocket connections on path /ws.

In order to use the debugger, you can use the 

Breakpoints using environment variables:
=======================================

The `set_trace` method can be defined in PYTHONBREAKPOINT environment variable as such

    PYTHONBREAKPOINT=awdb.set_trace

Then in the code you can invoke the debugger using the `breakpoint` native method.

    print(1)
    breakpoint()
    call_method()

Invoke a breakpoint using `set_trace`
=====================================

Like usual debugger in python, you can invoke it using the following code snippet.

    import awdb; awdb.set_trace()


Information about debugger
==========================

The debugger creates a thread with an async loop to communicate with the websocket
server. So the python application must be able to connect to the debugger server.

For each thread being debugged, a thread will be spawned with a websocket client.
Each thread can send asynchronuously messages to the server on their individual message loop.

The communication with the main thread is achieved using Queues.

When connected to the server, the Websocket client more or less act as a slave and wait for messages.

The control of the process start in the thread where it can be configured then moves into the frame trace
method. It will block the thread in a loop that send/receives messages from the async thread.

The design allow us to continue debugging while being able to eventually interrupt the debugging session.
Without having to reuse a breakpoint or even place any breakpoint.


Debugging an application
========================

Debugging can be achieved by using the awdb-client program. it will connect to the server and provide a simple
terminal user interface. There are few commands such as

- auto: auto subscribe to all new session but doesn't set them as active sessions
- w: show where we are
- up/down: move in the stack 
- (-)break event line file: add a breakpoint for certain event/file/line each of those parameters can be defined as "any" for anything.
- inspect: display the current stack frame with locals/globals and current code being executed
- (un)subscribe uuid: subscribe to a debugging session. It will display the messages received from any subscribed session
- use uuid: set the uuid session as the current session
- kill: kills the current active session
- continue: continue without breaking until it reaches a breakpoint
- interrupt: interrupt a session that continues (can be used to break out of an infinite loop)
- step: step to the next thing
- stop: stop debugging (remove set_trace as tracing method)
- list: show all sessions with their tags.
- set name value: set a value in the current stack frame
- eval [code...]: execute code in the current stack frame
- eval+: opens an editor defined with the environment variable _editor_ then sends the code to the debugger

Since it's using websocket, it's technically possible to run the client directly in the browser in a single page application.
The websocket protocol is the only requirement to be able to debug an application.



Environment variables
=====================

Those are environment variables useful to configure the servers/client/traced app

- AWDB_TAGS_[X]: Define tags in coma separated list used to display with the started sessions.
- AWDB_URL: Url of the AWDB server
- AWDB_ADMIN_TOKEN: Initial token for authentication
- editor: The editor to use
