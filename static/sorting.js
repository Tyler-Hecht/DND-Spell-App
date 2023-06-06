// this is broken for now

function lt_level(first, other) {
  return first < other;
}

function lt_casting_time(first, other) {
  // reaction < bonus action < action
  if (first == "1 Reaction") {
    return other != "1 Reaction";
  }
  if (other == "1 Reaction") {
    return false;
  }
  if (first == "1 Bonus Action") {
    return other != "1 Bonus Action";
  }
  if (other == "1 Bonus Action") {
    return false;
  }
  if (first == "1 Action") {
    return other != "1 Action";
  }
  if (other == "1 Action") {
    return false;
  }
  // if of form x minute(s), extract x and compare
  var self = parseInt(first.split(" ")[0]);
  var o = parseInt(other.split(" ")[0]);
  return self < o;
}

function extractFeet(range) {
  if (range.includes("feet")) {
    return parseInt(range.split(" ")[0]);
  }
  if (range.includes("foot")) {
    return parseInt(range.split("-")[0]);
  }
  if (range.includes("ft")) {
    return parseInt(range.split("ft")[0]);
  }
}

// Range class
function lt_range(first, other) {
  // self is always less than anything else
  if (first.includes("Self")) {
    if (other.includes("Self")) {
      if (first.includes("foot") && other.includes("foot")) {
        // if of form x ft., extract x and compare
        var foot_index_self = first.indexOf("-foot");
        // get number after ( but before "-foot"
        var self = parseInt(first.substring(0, foot_index_self).split("(")[1]);
        var foot_index_other = other.indexOf("-foot");
        var o = parseInt(other.substring(0, foot_index_other).split("(")[1]);
        return self < o;
      }
      return !first.includes("foot") && other.includes("foot");
    }
    return true;
  }
  // if other is self, self is greater
  if (other.includes("Self")) {
    return false;
  }
  // touch is less than anything except self
  if (first == "Touch") {
    return other != "Touch";
  }
  if (other == "Touch") {
    return false;
  }
  // if of form x ft., extract x and compare
  if (first.includes("feet") || first.includes("foot") || first.includes("ft")) {
    if (other.includes("feet") || other.includes("foot") || other.includes("ft")) {
      var self = extractFeet(first);
      var o = extractFeet(other);
      return self < o;
    }
    return true;
  }
  if (other.includes("feet") || other.includes("foot") || other.includes("ft")) {
    return false;
  }
  // if other is of form x miles, extract x and compare
  if (first.includes("mile")) {
    if (other.includes("mile")) {
      var self = parseInt(first.split(" ")[0]);
      var o = parseInt(other.split(" ")[0]);
      return self < o;
    }
    return true;
  }
  if (other.includes("mile")) {
    return false;
  }
  return first < other;
}

// Duration class
function lt_duration(first, other) {
  // instantaneous is less than anything else
  if (first == "Instantaneous") {
    return other != "Instantaneous";
  }
  if (other == "Instantaneous") {
    return false;
  }
  // detect "round"
  if (first.includes("round")) {
    // get the index of round
    var index_self = first.indexOf("round");
    // get the number of rounds
    var self_pre = first.substring(0, index_self - 1);
    // remove anything before the number of rounds (such as "up to")
    var self_rounds = parseInt(self_pre.substring(self_pre.lastIndexOf(" ") + 1));
    // same thing for other
    if (other.includes("round")) {
      var index_other = other.indexOf("round");
      var other_pre = other.substring(0, index_other - 1);
      var other_rounds = parseInt(other_pre.substring(other_pre.lastIndexOf(" ") + 1));
      if (self_rounds == other_rounds) {
        return !first.includes("Concentration") && other.includes("Concentration");
      }
      return self_rounds < other_rounds;
    } else {
      return true;
    }
  }
  if (other.includes("round")) {
    return false;
  }
  // detect "minute"
  if (first.includes("minute")) {
    // get the index of minute
    var index_self = first.indexOf("minute");
    // get the number of minutes
    var self_pre = first.substring(0, index_self - 1);
    // remove anything before the number of minutes (such as "up to")
    var self_minutes = parseInt(self_pre.substring(self_pre.lastIndexOf(" ") + 1));
    // same thing for other
    if (other.includes("minute")) {
      var index_other = other.indexOf("minute");
      var other_pre = other.substring(0, index_other - 1);
      var other_minutes = parseInt(other_pre.substring(other_pre.lastIndexOf(" ") + 1));
      if (self_minutes == other_minutes) {
        return !first.includes("Concentration") && other.includes("Concentration");
      }
      return self_minutes < other_minutes;
    } else {
      return true;
    }
  }
  if (other.includes("minute")) {
    return false;
  }
  // detect "hour"
  if (first.includes("hour")) {
    // get the index of hour
    var index_self = first.indexOf("hour");
    // get the number of hours
    var self_pre = first.substring(0, index_self - 1);
    // remove anything before the number of hours (such as "up to")
    var self_hours = parseInt(self_pre.substring(self_pre.lastIndexOf(" ") + 1));
    // same thing for other
    if (other.includes("hour")) {
      var index_other = other.indexOf("hour");
      var other_pre = other.substring(0, index_other - 1);
      var other_hours = parseInt(other_pre.substring(other_pre.lastIndexOf(" ") + 1));
      if (self_hours == other_hours) {
        return !first.includes("Concentration") && other.includes("Concentration");
      }
      return self_hours < other_hours;
    } else {
      return true;
    }
  }
  if (other.includes("hour")) {
    return false;
  }
  // detect "day"
  if (first.includes("day")) {
    // get the index of day
    var index_self = first.indexOf("day");
    // get the number of days
    var self_pre = first.substring(0, index_self - 1);
    // remove anything before the number of days (such as "up to")
    var self_days = parseInt(self_pre.substring(self_pre.lastIndexOf(" ") + 1));
    // same thing for other
    if (other.includes("day")) {
      var index_other = other.indexOf("day");
      var other_pre = other.substring(0, index_other - 1);
      var other_days = parseInt(other_pre.substring(other_pre.lastIndexOf(" ") + 1));
      if (self_days == other_days) {
        return !first.includes("Concentration") && other.includes("Concentration");
      }
      return self_days < other_days;
    } else {
      return true;
    }
  }
  if (other.includes("day")) {
    return false;
  }
  return self < other;
}

// compares two rows, first by the primary sort column, then by the level column
function compare(a_primary, b_primary, a_level, b_level, headerName) {
    // return 1 if a should be before b
    // return -1 if b should be before a
    // return 0 if they are equal
    if (headerName == "Range") {
      var comp_range = lt_range(a_primary, b_primary);
      if (comp_range != 0) {
        return comp_range;
      }
    } else if (headerName == "Duration") {
      var comp_duration = lt_duration(a_primary, b_primary);
      if (comp_duration != 0) {
        return comp_duration;
      }
    } else if (headerName == "Casting Time") {
      var comp_casting_time = lt_casting_time(a_primary, b_primary);
      if (comp_casting_time != 0) {
        return comp_casting_time;
      }
    }
    var comp_level = lt_level(a_level, b_level);
    if (comp_level != 0) {
      return comp_level;
    }
    return 0;
  }

// sorts the table by the given column
// uses level as a secondary sort column
function sort(column, direction) {
  var table, rows, switching, i, x, y, shouldSwitch;
  table = document.getElementById("data");
  switching = true;
  while (switching) {
    switching = false;
    rows = table.getElementsByTagName("tr");
    for (i = 1; i < (rows.length - 1); i++) {
      shouldSwitch = false;
      x = rows[i].getElementsByTagName("td")[column];
      y = rows[i + 1].getElementsByTagName("td")[column];
      if (direction == "asc") {
        var headerName = rows[0].getElementsByTagName("th")[column].innerHTML;
        if (compare(x.innerHTML, y.innerHTML, rows[i].getElementsByTagName("td")[0].innerHTML, rows[i + 1].getElementsByTagName("td")[0].innerHTML, headerName) == 1) {
          shouldSwitch = true;
          break;
        }
      } else if (direction == "desc") {
        var headerName = rows[0].getElementsByTagName("th")[column].innerHTML;
        if (compare(x.innerHTML, y.innerHTML, rows[i].getElementsByTagName("td")[0].innerHTML, rows[i + 1].getElementsByTagName("td")[0].innerHTML, headerName) == -1) {
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
    }
  }
}

// when a column header is clicked, sort the table by that column
// if the column is already sorted, reverse the sort
// if the column is not sorted, sort ascending
var table = document.getElementById("data");
var headers = table.getElementsByTagName("th");
for (i = 0; i < headers.length; i++) {
  headers[i].addEventListener("click", function() {
    var column = this.cellIndex;
    var direction = this.getAttribute("data-direction");
    if (direction == "asc") {
      this.setAttribute("data-direction", "desc");
      sort(column, "desc");
    } else if (direction == "desc") {
      this.setAttribute("data-direction", "asc");
      sort(column, "asc");
    } else {
      this.setAttribute("data-direction", "asc");
      sort(column, "asc");
    }
  });
}
