*\* clone/pull directory to view EDA html reports \**

`EDA.Rmd` is the main data cleaning script. Also includes: 

 - adds tidy timepoints for 'over time' visualisations
 - adds centroid coordianates of coutries (origin/notified)
 - generates random coordinates within-country polygons to create dot plots/density maps

Other EDA scripts look at specific hazards (using tidy output file from the main script)

`EDA_EU.Rmd` cleans up EU/non-EU labels and explores data_source categories (e.g. RASFF vs UK sources)

`EDA_allergens.Rmd` explores hazards from allergens; created new variable with tidy labels and summarised similar entries

`EDA_plastic.Rmd` explore hazards from various foreign bodies (plastic, glass, metal, insects). Finds these hazards in other categories (not just the predefined "foreign bodies" category); visualises them over time;


[interactive version of the map](content/kepler_notifications_about_UK_by_UK.html) 

[interactive version of the map](https://github.com/mvab/JGI-food-hazards-viz-challenge/content/kepler_notifications_about_UK_by_UK.html) 

[interactive version of the map](https://github.com/mvab/JGI-food-hazards-viz-challenge/docs/content/kepler_notifications_about_UK_by_UK.html) 

[interactive version of the map](https://github.com/mvab/JGI-food-hazards-viz-challenge/marina-working-dir/EDA.html) 
