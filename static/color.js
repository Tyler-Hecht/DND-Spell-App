// 1 = light green
// 2 = light yellow
// 3 = light orange
// 4 = light red
// 5 = light purple
// 6 = light blue
// 7 = light cyan
// 8 = light gray
// 9 = light white
function darkify(color_string) {
    //make r,g, and b values integers
    var r = parseInt(color_string.substring(4, color_string.indexOf(",")));
    var g = parseInt(color_string.substring(color_string.indexOf(",") + 2, color_string.lastIndexOf(",")));
    var b = parseInt(color_string.substring(color_string.lastIndexOf(",") + 2, color_string.indexOf(")")));
    //make r,g, and b values darker by 16
    r = Math.max(0, r - 16);
    g = Math.max(0, g - 16);
    b = Math.max(0, b - 16);
    //return new color string
    return "rgb(" + r + ", " + g + ", " + b + ")";
    }
    var colors = ["#d4edda", "#fff3cd", "#ffe0c0", "#f8d7da", "#d1c4e9", "#d1ecf1", "#cff4fc", "#d6d8db", "#f8f9fa"];
    var rows = document.getElementsByTagName("tr");
    // when cursor hovers over a row, change its color to the corresponding color in colorsDarker
    // when cursor leaves a row, change its color back to the corresponding color in colors
    // if header row is hovered over, do nothing
    for (var i = 0; i < rows.length; i++) {
        // default
        rows[i].style.backgroundColor = colors[rows[i].cells[0].innerHTML - 1];
        // hover
        rows[i].addEventListener("mouseover", function() {
            this.style.backgroundColor = darkify(this.style.backgroundColor);
        });
        rows[i].addEventListener("mouseout", function() {
            this.style.backgroundColor = colors[this.cells[0].innerHTML - 1];
        });
    }
    