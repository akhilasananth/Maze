# I'm pausing work on this branch: "extensible"

Why?
Because I feel like I am adding more and abstraction, just in case I'll extend the program in the future. 
I am losing sight of actually making the project better, and this constant refactoring feels like a waste of time.
It might not be a waste of time in the long term, but right now it is.
I have no plans to extend at the moment, and this is outside my scope at the moment.
This code is not tested, and I'm pretty sure that it will not run, but I am not moving forward.
I have decided to just work on improving the mvp that I initially built. 
I spent almost 3 days refactoring this for extensibility.
I came across this article and it kind of opened my eyes: [article](https://programmingisterrible.com/post/139222674273/write-code-that-is-easy-to-delete-not-easy-to)

- Every line of code written comes at a price: maintenance. 
- The problem with code re-use is that it gets in the way of changing your mind later on.

This also ties in with my problem of accumulating a lot of things in life. As I have been solo traveling for the past 
year, I have learnt the importance of valuing the items that actually use. I pay in luggage at the airport for every 
item that I keep "just in case." I need to trust that everything will be provided for and more importantly, I need to 
trust myself. I need to trust that I don't need to add "just in case" padding for the future. I will manage any situation
just fine. In fact, those "just in case" items add to my cognitive load every day and "it gets in the way of 
changing your mind later on." As the article states.

I just found it interesting how I do one thing translated to pretty much everything in life.


This [article](https://programmingisterrible.com/post/139222674273/write-code-that-is-easy-to-delete-not-easy-to) 
talks about writing code that is straightforward to delete.

Repeat yourself to avoid creating dependencies, but don’t repeat yourself to manage them. 
- A little redundancy is healthy. It’s good to copy-paste code a couple of times, just to get a handle on how it will be used.
- This is completely the opposite of what I learnt in school
- BUT: When you’ve copied and pasted something enough times, maybe it’s time to pull it up to a function. 
These functions go in a utils directory or a utils file. 

Layer your code too: build simple-to-use APIs out of simpler-to-implement but clumsy-to-use parts. 
Split your code: isolate the hard-to-write and the likely-to-change parts from the rest of the code, and each other. 

`"Instead of breaking code into parts with common functionality, we break code apart by what it does not share with the 
rest. We isolate the most frustrating parts to write, maintain, or delete away from each other."`

Don’t hard-code every choice, and maybe allow changing a few at runtime. 
Don’t try to do all of these things at the same time, and maybe don’t write so much code in the first place.

**Love this**: Good code isn’t about getting it right the first time. 
Good code is just legacy code that doesn’t get in the way. Good code is easy to delete. 

While commiting this massacre, I deleted all the methods used only in tests and abstractions. 
Magically, things seem way clearer!