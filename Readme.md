# Wix Server Entry Level Exam

Hi there!  
In this exam you will build a ticketing system.
The task's main purpose is to test your ability to learn new topics and deliver high quality digital products. 

## Tasks

The exam is split into 2 parts. The first part is about creating a basic server. Implement this in *any* language you feel comfortable with. The second part is about creating a usable server.

### Part 1 - Create a simple API that returns the tickets from the database

Take a look at the attached `data.json` file - it contains 200 tickets. We would like you to create a simple API with a `GET` endpoint at `/tickets`. 

### Part 2 - Filtering functionality 

Imagine that the database could have millions of tickets eventually. We need the ability to filter the returning requests on the server side.

a. Our product manager has asked to implement a search bar in the product that returns only tickets that match. Implement this functionality so that only tickets matching this text in the title will return.

b. Another useful filter is by time. Implement a filter that can receive `from`, `to` or both and return tickets that match this criteria.

c. Turns out that the search you implemented in section `a` is great, but sometimes it would be even better to search in all the text fields! (`title`, `content` and `email`). Please implement this filter.

## General notes
- Test your work well. Think of edge cases. Think of how users will use it, and make sure your work is of high quality
- Stick to the best practices of the libraries used as much as possible
- If you have any questions regarding the task itself or its environment, feel free to ask in the exam's e-mail. For general coding / technology questions, please consult stack overflow, forums and other sources of your choice.


## Submitting

1. Zip *all* the files that are needed to run this code *without* the binaries.
2. Send this Zip as an attachment link using Google drive, WeTransfer or any other attachment you feel comfortable with. Take notice, ZIP attachments to emails will be rejected and we won't get a notification!