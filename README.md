# Edexcel-Pseudocode
## ℹ About 
There's websites for compiling Cambridge IGCSEs pseudocode on the web (and even a PyPi package!; dudocode) but when you look one up for Pearson IGCSEs pseudocode, there's none?
Well, this is to help those who want to test and run their pseudocode written as per the appendix at:
https://tools.withcode.uk/ks4pseudo/media/edexcel_pseudocode.pdf

A Pearon International GCSEs pseudocode to Python transpiler!
## Information
If you take a look at the way of implementation, you might see a bizarre line by line translation instead of using tokens. That's because the pseudocode has some weird syntax. For example,
```
SEND "hello, world" TO DISPLAY
```
The syntax features inputs in between "functions", making the conventional token approach very hard
Though, the reason for me not having investigated tokens was because I hadn't done research either
## Future plans
Actually publishing this to pip, i hadn't had much time to do this.
Expanding to the Cambridge Pseudocode as well.
This repository should be wrapped up before May 2025.
## Notes
idk how to implement repeat
## TO DO
File handling
