# EdgeMerge

A simple blender add-on to make life easier when cleaning up after knife and/or boolean operations.

# Usecases, basics of the algorithm

When working with boolean and knife operations, no matter if your workflow is destructive or non-destructive, there is good chance you are going to be left with extra vertices. And in most cases, you are going to want to remove them - they add unnecessary data to store, waste processing power when you want to do something with the model and also often ruin shading.

And while they can look like this and take just a few seconds to get rid of,
![image](https://user-images.githubusercontent.com/84248577/127743330-96bf635f-b858-491a-8b32-f87ad5a17507.png)

they can also look like this, in which case it isn't a whole lot of fun to remove them.
![image](https://user-images.githubusercontent.com/84248577/127743325-1aaecfb4-e4bb-4125-960e-b66bb04d877a.png)


The second case is the one for which EdgeMerge is designed for. It works for both open and closed loops. On an oversimplified level, the algorithm looks for vertices that do not actually "hold" the shape and merges them to the closest "holding" vertex. For example, the middle vertex on the first picture **is not** going to be removed, because it is required to keep the shape. However on the second picture, we only need the two edge vertices to keep the shape and therefore the middle vertex **is** going to be removed.

![image](https://user-images.githubusercontent.com/84248577/127743554-85c7f84f-4b62-444f-a4f1-de0f47414cf9.png)

![image](https://user-images.githubusercontent.com/84248577/127743524-7282b2d4-f3af-43c3-bc10-84bc6fa5119a.png)

# Usage

The add-on is installed just like any other blender add-ons from a python file. After installing and enabling it, you can use it from the object context menu of a mesh while you are in edit mode and have vertices selected. 

![image](https://user-images.githubusercontent.com/84248577/127743805-fcd72036-4f39-446e-a088-56d706cda0fe.png)

# Limitations

Unfortunately, the add-on is not just "magic" and therefore basically only works on a **single loop at a time**. Below are some examples of what it **does not** work on:

![image](https://user-images.githubusercontent.com/84248577/127744132-2ce1f03e-9104-408f-82dc-c814295204d8.png)
![image](https://user-images.githubusercontent.com/84248577/127744153-b561a920-2862-4417-828c-cdd638a03ab7.png)
![image](https://user-images.githubusercontent.com/84248577/127744191-89c3b864-c905-4e7e-a3ec-93ad5e4e0a4f.png)
![image](https://user-images.githubusercontent.com/84248577/127744212-f171584d-94d2-4af1-acf4-2b0942250673.png)
