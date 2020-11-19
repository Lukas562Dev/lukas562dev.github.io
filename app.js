// app.js
console.log('Hello World!');
console.log('Lukas\'s Website!');
console.log('Example project generated using SmartCLI');

var test = (a, b, c) => a + b + c;
console.log(test('1', '2', '3')); // 123?


var projectsListEl = document.querySelector('.projectsList');


fetch('https://api.github.com/users/LukasDoesDev/repos')
  .then((res) => {
    return res.json();
  })
  .then((repos) => {
    projectsListEl.innerHTML = '';
    for (let i = 0; i < repos.length; i++) {
      const repo = repos[i];
      // create item(s)
      projectsListEl.innerHTML += makeRepoEl(repo);
    }
  })
  .catch((err) => {
    console.error(err);
  })


function makeRepoEl(repo) {
  return `
        <div class="project">

          <div class="projectUpper">
            <h3 class="projectTitle">${DOMPurify.sanitize(repo.name)}</h3>
            <span class="projectDesc">${DOMPurify.sanitize(repo.description)}</span>
          </div>

          <div class="projectLower">
            <div class="projectLinks">
              <a href="${DOMPurify.sanitize(repo.html_url)}">Github</a>
            </div>
          </div>

        </div>`
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