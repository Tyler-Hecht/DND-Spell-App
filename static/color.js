function darkify(color_string) {
    //make r,g, and b values integers
    var r = parseInt(color_string.substring(1,3), 16);
    var g = parseInt(color_string.substring(3,5), 16);
    var b = parseInt(color_string.substring(5,7), 16);
    //make r,g, and b values darker by 16
    r = Math.max(0, r - 16);
    g = Math.max(0, g - 16);
    b = Math.max(0, b - 16);
    // make sure r,g, and b values are 2 digits long
    if (r.toString(16).length == 1) {
        r = "0" + r.toString(16);
    } else {
        r = r.toString(16);
    }
    if (g.toString(16).length == 1) {
        g = "0" + g.toString(16);
    } else {
        g = g.toString(16);
    }
    if (b.toString(16).length == 1) {
        b = "0" + b.toString(16);
    } else {
        b = b.toString(16);
    }
    //return new hex color as a string #rrggbb
    hex = "#" + r.toString(16) + g.toString(16) + b.toString(16);
    return hex;
}
// 0 = light gray
// 1 = light green
// 2 = light yellow
// 3 = light orange
// 4 = light red
// 5 = light purple
// 6 = light blue
// 7 = light cyan
// 8 = gray
// 9 = light white
var colors = ["#d8d9da", "#d4edda", "#fff3cd", "#ffe0c0", "#f8d7da", "#d1c4e9", "#cff4fc", "#94ffea", "#a6a8ab", "#ffb6c1"];
var rows = document.getElementsByTagName("tr");
// when cursor hovers over a row, change its color to the corresponding color in colorsDarker
// when cursor leaves a row, change its color back to the corresponding color in colors
// if header row is hovered over, do nothing
opacityHex = "a4";
for (var i = 1; i < rows.length; i++) {
    // default
    rows[i].style.backgroundColor = colors[rows[i].cells[0].innerHTML] + opacityHex;
    // hover
    rows[i].addEventListener("mouseover", function() {
        console.log(this.cells[0].innerHTML);
        this.style.backgroundColor = darkify(colors[this.cells[0].innerHTML]) + opacityHex;
    });
    rows[i].addEventListener("mouseout", function() {
        this.style.backgroundColor = colors[this.cells[0].innerHTML] + opacityHex;
    });
}
    