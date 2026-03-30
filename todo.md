- Look at how SCSS is set up
- Implement TypeScript - Use and explorer Vite for the bundle
- Create JavaScript API Call for form data to backend
- Consider replacing JQuery? Its rather static and we will be using JavaScript for backend functionality like API Requests to python
    - or just have static JS/JQuery files and then have TS/JS seperate for backend logic
- Currently the linkes from the HTML to JS and CSS files are `../../` as its local
    - Since we are using FASTAPI, They need to be mounted in `app.py` - need to fix all paths to work when FASTAPI takes control. *See chatGPT `relative paths in fastapi` and `understanding the browser 1 and 2`
    - Get process together for firing up server for development as using VS Code Live server is ok for jumping back REPOS, but not whenever we start fully integrating with FASTAPI
- Create `main()` for uvicorn in a `main()`
- Install ruff and pylance
- Move `/images` on T-X into Static as its in `.gitignore` and on T-X its one folder above
- Remove CSS bloat - Rename classes to new names for their purpose
    - They are fine just now due to them not being ready high priorty and they work
- Add workers to Uvicorn



--------
Typescript installation TODO

- Get commands for running compiler to js seperatly
- Get it to compile to the right folders
- Move JQuery to a jquery folder and use js as the target for typescript compiler
- Get Uvicorn ro run the typescript compiler when the fastapi server is launched
- Find out more about what part Vite has to play
- Summarise Claude pages for Development_jounral.md
    - Vite and the bundler regarding typescript - no need to hard code into html
    - What to do about static JQuery files and if they need updates?




------------
Deployment on VPS (Configuration to have multiple sites running on server)

- Separate FastAPI apps per site
- Check were all folders are mounted to by FastAPI?
    - Will different sites mix these files if they all mount?
    - Do FastAPI examples state to mount to static/ because they dont know context that another site is running on the same server?
- Can/Should multiple sites share the same database?
- Can/Should multiple sites share the same port (443)?
- Consider using Core FASTAPI set up that can update mutliple sites when infrastructure improves of code 