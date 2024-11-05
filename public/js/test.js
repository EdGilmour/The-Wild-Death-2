"use strict";
const container = document.getElementById("app");
let output = `
<div class="card">
    <span class="card--id">#1</span>
    <h1 class="card--name">Name</h1>
    <span class="card--details">Details</span>
</div>`;
container.innerHTML += output;
