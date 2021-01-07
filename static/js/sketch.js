// adapted from: https://codeburst.io/sunsets-and-shooting-stars-in-p5-js-92244d238e2b
// p5.js sketch as background: https://www.youtube.com/watch?v=OIfEHD3KqCg

var stars = [];
var shootingStar;

// windowResized is a p5 global function
function windowResized() {
  resizeCanvas(windowWidth, windowHeight); // recreate canvas with new window width and window height
}

var canvas;
function setup() {
  canvas = createCanvas(windowWidth, windowHeight);
  canvas.position(0, 0);
  canvas.style('z-index', '-1'); // css function; z whether it is infront or behind
  frameRate(5); // how fast the stars will change
  for (var i = 0; i < 500; i++) { // push 500 stars to the array
      stars.push(new Star());
  }
}

function Star() {
  // windowWidth and windowHeight dynamically detect height and window of browser page
  this.x = random(windowWidth); // x position of star
  this.y = random(windowHeight); // y position of star, 200 pixels above horizon
  this.w = 1; // width of star
  this.h = 1; // height of star
}

Star.prototype.draw = function() {
  noStroke(); // no outline around the stars
  fill(255, 255, 255); // makes the stars white
  ellipse(this.x, this.y, this.w, this.h); // draw 2x2 pixel ellipse at random (x,y) loc
  var randomness = random(5);

  if (randomness < 2) {
    if (randomness > 0) {
      this.x = random(windowWidth);
      this.y = random(windowHeight);
    }
    this.w = random(2)
    this.h = random(2)
  }
}

function draw() {
  background(25, 25, 112);
  for (var i = 0; i < 500; i++) {
      stars[i].draw();
  }
}
