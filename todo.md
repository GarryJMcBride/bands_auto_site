## Generic

* [ ] Add these todos to the wnd - they will go towards the how to design a website checklist or process

* [ ] Implement TypeScript - Use and explorer Vite for the bundle
* [ ] Create JavaScript API Call for form data to backend
* [ ] Consider replacing JQuery? Its rather static and we will be using JavaScript for backend functionality like API Requests to python
    * [ ] or just have static JS/JQuery files and then have TS/JS seperate for backend logic
* [ ] Currently the linkes from the HTML to JS and CSS files are `../../` as its local
    * [ ] Since we are using FASTAPI, They need to be mounted in `app.py` - need to fix all paths to work when FASTAPI takes control. *See chatGPT `relative paths in fastapi` and `understanding the browser 1 and 2`
    * [ ] Get process together for firing up server for development as using VS Code Live server is ok for jumping back REPOS, but not whenever we start fully integrating with FASTAPI
* [ ] Create `main()` for uvicorn in a `main()`
* [ ] Install ruff and pylance
* [ ] Move `/images` on T-X into Static as its in `.gitignore` and on T-X its one folder above
* [ ] Remove CSS bloat - Rename classes to new names for their purpose
    * [ ] They are fine just now due to them not being ready high priorty and they work





-------------------
Feature: Get vehicle info from REGI
- Brian wants a contact form that will sent him an email with the clients info as well as the vehicles info
- The Customer will only add their regi as asking for all of the other information is too much *See email images from Brian for example of what he recieves
- We need to use an API on the server to gather the information about the car and then send it to Brians email address
- The information will need to be secure as its details about the car
    - Anyone can type a regi into a website though and generate the information
*See emails template in `Takmadoon/B&S Autos/Template from Book my Mechanic`
*See chatgpt chat B&S Autos - `Initial look at new features`




-------------------
Feature: Allow testimonials to be added by user
- Without adding a backend that allows users to log in (too large of a feature)
    - People can add reviews to Brians site and they are stored in a database, either accetped or rejected
- Need to consider if this website will scrape or request the reviews from `book my garage` to then be mirrored on this site
*See chatgpt chat B&S Autos - `Initial look at new features`






-----------
CCS and UI
* [ ] Understand how the CSS is implemented... the variables and the settings for different styles pages from the template
* [ ] Remove CSS bloat - Rename classes to new names for their purpose
    * [ ] They are fine just now due to them not being ready high priorty and they work
* [ ] Look at how SCSS is set up
* [ ] Understand the use of Jquery for the UI and others 
* [ ] Understand Bootstrap implementation
* [ ] Understand the fades and transitions (things that move)









## Typescript installation TODO

- Get commands for running compiler to js seperatly
- Get it to compile to the right folders
- Move JQuery to a jquery folder and use js as the target for typescript compiler
- Get Uvicorn ro run the typescript compiler when the fastapi server is launched
- Find out more about what part Vite has to play
- Summarise Claude pages for Development_jounral.md
    - Vite and the bundler regarding typescript - no need to hard code into html
    - What to do about static JQuery files and if they need updates?



### Typescript Paths TODO
* Decide on TypeScript import strategy: use `baseUrl` and optional path aliases instead of deep relative paths
* Update `tsconfig.json`:

  * Set `"baseUrl": "./src"`
  * Add optional `"paths": { "@/*": ["*"] }` for clean absolute imports
* Refactor all TypeScript imports to use baseUrl/alias or simple relative paths
* Check that compiled output in `dist/` resolves correctly for Node/FastAPI
* Introduce a bundler (esbuild or webpack) to handle:

  * Path alias resolution
  * Outputting clean browser-ready files to `dist/`
* Ensure HTML references (`<script>` / `<link>`) point to the correct bundled/dist files
* Test end-to-end: TypeScript build → FastAPI → browser to confirm no broken imports or missing assets








## Deployment on VPS (Configuration to have multiple sites running on server)

- Separate FastAPI apps per site
- Check were all folders are mounted to by FastAPI?
    - Will different sites mix these files if they all mount?
    - Do FastAPI examples state to mount to static/ because they dont know context that another site is running on the same server?
- Can/Should multiple sites share the same database?
- Can/Should multiple sites share the same port (443)?
- Consider using Core FASTAPI set up that can update mutliple sites when infrastructure improves of code 








## Client side validation - Frontend JavaScript

- Add max lengths to forms 
- What is Ajax 
- Should we have a call to the endpoint if the browser doesn’t support JavaScript ?
- Delete data on client side after passed 
- Error handling: the user should be told it’s been successful.
- Read custom script. Js
- Find out why that form is inheriting the validation 