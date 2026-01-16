# Image-augmentation - Hassle free way to increase Dataset size
Demo link - https://www.youtube.com/watch?v=6JQuTVdgvY4
### Requirements specified by SAMSUNG R&D India
## Inspiration
Came up with the idea when playing with filters in snapchat as filter can be added and swapped out without needing to capture the entire image again with a new filter.
## What it does
The idea is that when training models with small data set there is a sure chance of the model overfitting to the data. Project aims to prevent it by adding noises that are realistic. That occur in nature like blurs when taking manual photography. 
## How we built it
This is build using Python and Scrum methodology for project management.
## Challenges we ran into
The challenges are listed as follows
- unsure about the threshold of noise to add, so we had to rectroactively find out a way to handle sliders for each noise that turned out to be a huge issue with handling requests from the frontend. This turned out to cause lot of false triggers.
- performance degradation when adding noise to video.
- UI componenet were not reactive to different window sizes, so there was a need to research to make it reactive.
## Accomplishments that we're proud of
Fully completing a working prototype within the given timeline, and also recieved Excellence award.
## What we learned
A lot actually from Learning to use PyQT5, Concurrency, image manipulation using OpenCV, bundling the python code to exe and to project management.
## What's next for Image Augmentation by adding noises
To add a slider to adjust how much noise is being added to image.


