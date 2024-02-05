run("8-bit");
run("Duplicate...", " ");
run("Enhance Contrast...", "saturated=35 equalize");
run("Subtract Background...", "rolling=150 light");
setAutoThreshold("Default dark no-reset");
setOption("BlackBackground", true);
run("Convert to Mask");
run("Invert");
run("Fill Holes");
getDimensions(width, height, channels, slices, frames);
median_radius = height/(20);
run("Median", "radius=median_radius");
//Assuming squareish image, wand tool selects center
doWand(width/2, height/2);
setBackgroundColor(0, 0, 0);
run("Clear Outside");
run("Close-")
run("Median", "radius=median_radius");
run("Close-")
run("Select None");
run("Outline");
//Adjust number of iterations based on desired thickness of the outline.
//Must be an integer
num_iterations = 1
run("Options...", "iterations=num_iterations count=1 black do=Dilate");
run("Invert");