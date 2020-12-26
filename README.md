# FTCLegends
A website that contains a list of the teams that have partcipated in the elimination rounds of the FIRST Tech Challenge World Championship.

## Contributing
If there's something you would like to change please create a [pull request](https://github.com/jspspike/ftclegends/compare). If you don't know what this is you can read about them [here](https://guides.github.com/activities/hello-world/#pr). If you're lazy you can create an [issue](https://github.com/jspspike/ftclegends/issues/new/choose) or email me at jspspike@gmail.com but be warned I am also very lazy.

All of the info thats displayed on the site is contained in `data.json` so this is where you can update placements for future events.

If you would like to add/update a team logo you can place the image in `public/img/teams` with the image name being `[team number].png`.

Finally if you would like to make further changes `index.template.html` contains the actual template for the website and `generate.py` parses `data.json` and generates the site from the template.
