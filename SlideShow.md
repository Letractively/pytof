# Introduction #

Having a one click nice slideshow would be a good enhancement to the user experience. This has probably to be done on the client side and javascript would be a good fit.

## Changes ##

### Python ###

We would have to embed some js (callbacks) inside the HTML pages

### Java Script ###

The whole thing would be done in a separate bunch of JS scripts, located somewhere inside the generated directory. Here is an example of a slidewhow code can be fetched from [here](http://www.robertnyman.com/jas/). They hard-code the pictures files. We would have to have this done dynamically by js, or off-line by python.

```
        imagePath : "pictures/",
        images : [
                ["1.jpg", "Bat bridge in Austin", "Bridge"],
                ["2.jpg", "Blossoming tree", "Tree"],
                ["3.jpg", "Bat bridge from below", "Bridge"],
                ["4.jpg", "Birds", "Birds"],
                ["5.jpg", "Stevie Ray Vaughan Memorial", "Memorial"],
                ["6.jpg", "Me in river park", "River park"],
                ["7.jpg", "Woode Wood playing guitar", "Woode Wood, River park"], // Separate multiple tags by a comma
                ["8.jpg", "Woode's sign", "Woode Wood"],
                ["9.jpg", "Meeting room", "Texas Capitol"],
                ["10.jpg", "Nice painting", "Texas Capitol"],
                ["11.jpg", "Bigger meeting room", "Texas Capitol"],
                ["12.jpg", "Great name tag!", "Texas Capitol"]
        ],

```