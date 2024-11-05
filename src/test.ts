const container: HTMLElement | any = document.getElementById("app");
let output: string = `
    <span class="card--id">#1</span>
    <h1 class="card--name">Name</h1>
    <span class="card--details">Details</span>
    `;
container.innerHTML += output;