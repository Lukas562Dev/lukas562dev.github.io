// app.js
console.log('Hello World!');
console.log('Lukas\'s Website!');
console.log('Source code at https://github.com/LukasDoesDev/lukasdoesdev.github.io');


var projectsListEl = document.querySelector('.projectsList') || document.querySelector('.square-container');


fetch('https://api.github.com/users/LukasDoesDev/repos')
  .then((res) => {
    return res.json();
  })
  .then((repos) => {
    projectsListEl.innerHTML = '';
    for (let i = 0; i < repos.length; i++) {
      const repo = repos[i];
      // create item(s)
      makeRepoEl(repo, projectsListEl);
    }
  })
  .catch((err) => {
    console.error(err);
  })


function makeRepoEl(repo, element) {

  cssnames = {
    project: ['project'],
    projectContent: ['projectContent'],
    projectTitle: ['projectTitle'],
    projectDesc: ['projectDesc'],
    projectLink: ['link'],
  }

  var projectDiv = document.createElement('div');
  projectDiv.classList.add(cssnames.project);

  var projectContent = document.createElement('div');
  projectContent.classList.add(cssnames.projectContent);
  projectDiv.appendChild(projectContent);

  var projectTitle = document.createElement('h3');
  projectTitle.classList.add(cssnames.projectTitle);
  projectTitle.textContent = repo.name;
  projectContent.appendChild(projectTitle);

  var projectDesc = document.createElement('span');
  projectDesc.classList.add(cssnames.projectDesc);
  projectDesc.textContent = repo.description;
  projectContent.appendChild(projectDesc);

  projectContent.appendChild(document.createElement('br'));
  projectContent.appendChild(document.createElement('br'));

  var githubLink = document.createElement('a');
  githubLink.classList.add(cssnames.projectLink);
  githubLink.setAttribute('href', repo.html_url);
  githubLink.textContent = 'Github';
  projectContent.appendChild(githubLink);

  element.appendChild(projectDiv);
}


/*
  <div class="project">

    <div class="projectUpper">
      <h3 class="projectTitle">Exaple Project</h3>
      <span class="projectDesc">This is an Example Project. Lorem ipsum dolor sit amet, consectetur adipiscing elit,
        sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</span>
    </div>

    <div class="projectLower">
      <div class="projectLinks">
        <a href="https://github.com/LukasDoesDev/example">Github</a>
      </div>
    </div>

  </div>
 */
