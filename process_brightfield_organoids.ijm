run("Enhance Contrast...", "saturated=35 equalize");
run("Subtract Background...", "rolling=150 light");
setAutoThreshold("Default dark no-reset");
setOption("BlackBackground", true);
run("Convert to Mask");
run("Invert");
run("Fill Holes");
run("Median", "radius=20");
getDimensions(width, height, channels, slices, frames);
doWand(width/2, height/2);
setBackgroundColor(0, 0, 0);
run("Clear Outside");
run("Close-")
run("Median", "radius=20");
run("Close-")
run("Select None");
run("Outline");
run("Options...", "iterations=4 count=1 black do=Dilate");
save()