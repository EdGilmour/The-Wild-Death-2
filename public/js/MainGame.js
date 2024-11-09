// FOR TESTING: pushd index.html; python3 -m http.server 9999; popd;
import { AsciiArt } from "./AsciiArt.js";
const asciiContainer = document.getElementById("ascii_art");
let asciiArt = AsciiArt.dalevilleWest;
asciiContainer.innerHTML = '<pre>' + asciiArt + '</pre>';
