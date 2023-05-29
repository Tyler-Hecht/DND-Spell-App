// This file is really messy right now, will clean up later

// Generic property class
class OtherDDD {
  constructor(value) {
    this.value = value;
  }
  // less than operator
  lt(other) {
    return this.value < other.value;
  }
}

// Casting time class
class CastingTime {
  constructor(castingTime) {
    this.castingTime = castingTime;
  }
  // less than operator
  lt(other) {
    // reaction < bonus action < action
    if (this.castingTime == "1 Reaction") {
      return other.castingTime != "1 Reaction";
    }
    if (other.castingTime == "1 Reaction") {
      return false;
    }
    if (this.castingTime == "1 Bonus Action") {
      return other.castingTime != "1 Bonus Action";
    }
    if (other.castingTime == "1 Bonus Action") {
      return false;
    }
    if (this.castingTime == "1 Action") {
      return other.castingTime != "1 Action";
    }
    if (other.castingTime == "1 Action") {
      return false;
    }
    // if of form x minute(s), extract x and compare
    var self = parseInt(this.castingTime.split(" ")[0]);
    var o = parseInt(other.castingTime.split(" ")[0]);
    return self < o;
  }
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
class Range {
  constructor(range) {
    this.range = range;
    if (range == "Sight") {
      this.range = "2 miles";
    }
  }
  // less than operator
  lt(other) {
    // self is always less than anything else
    if (this.range.includes("Self")) {
      if (other.range.includes("Self")) {
        if (this.range.includes("foot") && other.range.includes("foot")) {
          // if of form x ft., extract x and compare
          var foot_index_self = this.range.indexOf("-foot");
          // get number after ( but before "-foot"
          var self = parseInt(this.range.substring(0, foot_index_self).split("(")[1]);
          var foot_index_other = other.range.indexOf("-foot");
          var o = parseInt(other.range.substring(0, foot_index_other).split("(")[1]);
          return self < o;
        }
        return !this.range.includes("foot") && other.range.includes("foot");
      }
      return true;
    }
    // if other is self, self is greater
    if (other.range.includes("Self")) {
      return false;
    }
    // touch is less than anything except self
    if (this.range == "Touch") {
      return other.range != "Touch";
    }
    if (other.range == "Touch") {
      return false;
    }
    // if of form x ft., extract x and compare
    if (this.range.includes("feet") || this.range.includes("foot") || this.range.includes("ft")) {
      if (other.range.includes("feet") || other.range.includes("foot") || other.range.includes("ft")) {
        var self = extractFeet(this.range);
        var o = extractFeet(other.range);
        return self < o;
      }
      return true;
    }
    if (other.range.includes("feet") || other.range.includes("foot") || other.range.includes("ft")) {
      return false;
    }
    // if other is of form x miles, extract x and compare
    if (this.range.includes("mile")) {
      if (other.range.includes("mile")) {
        var self = parseInt(this.range.split(" ")[0]);
        var o = parseInt(other.range.split(" ")[0]);
        return self < o;
      }
      return true;
    }
    if (other.range.includes("mile")) {
      return false;
    }
    return this.range < other.range;

  }
}

// Duration class
class Duration {
  constructor(duration) {
    this.duration = duration;
  }
  // less than operator
  lt(other) {
    // instantaneous is less than anything else
    if (this.duration == "Instantaneous") {
      return other.duration != "Instantaneous";
    }
    if (other.duration == "Instantaneous") {
      return false;
    }
    // detect "round"
    if (this.duration.includes("round")) {
      // get the index of round
      var index_self = this.duration.indexOf("round");
      // get the number of rounds
      var self_pre = this.duration.substring(0, index_self - 1);
      // remove anything before the number of rounds (such as "up to")
      var self_rounds = parseInt(self_pre.substring(self_pre.lastIndexOf(" ") + 1));
      // same thing for other
      if (other.duration.includes("round")) {
        var index_other = other.duration.indexOf("round");
        var other_pre = other.duration.substring(0, index_other - 1);
        var other_rounds = parseInt(other_pre.substring(other_pre.lastIndexOf(" ") + 1));
        if (self_rounds == other_rounds) {
          return !this.duration.includes("Concentration") && other.duration.includes("Concentration");
        }
        return self_rounds < other_rounds;
      } else {
        return true;
      }
    }
    if (other.duration.includes("round")) {
      return false;
    }
    // detect "minute"
    if (this.duration.includes("minute")) {
      // get the index of minute
      var index_self = this.duration.indexOf("minute");
      // get the number of minutes
      var self_pre = this.duration.substring(0, index_self - 1);
      // remove anything before the number of minutes (such as "up to")
      var self_minutes = parseInt(self_pre.substring(self_pre.lastIndexOf(" ") + 1));
      // same thing for other
      if (other.duration.includes("minute")) {
        var index_other = other.duration.indexOf("minute");
        var other_pre = other.duration.substring(0, index_other - 1);
        var other_minutes = parseInt(other_pre.substring(other_pre.lastIndexOf(" ") + 1));
        if (self_minutes == other_minutes) {
          return !this.duration.includes("Concentration") && other.duration.includes("Concentration");
        }
        return self_minutes < other_minutes;
      } else {
        return true;
      }
    }
    if (other.duration.includes("minute")) {
      return false;
    }
    // detect "hour"
    if (this.duration.includes("hour")) {
      // get the index of hour
      var index_self = this.duration.indexOf("hour");
      // get the number of hours
      var self_pre = this.duration.substring(0, index_self - 1);
      // remove anything before the number of hours (such as "up to")
      var self_hours = parseInt(self_pre.substring(self_pre.lastIndexOf(" ") + 1));
      // same thing for other
      if (other.duration.includes("hour")) {
        var index_other = other.duration.indexOf("hour");
        var other_pre = other.duration.substring(0, index_other - 1);
        var other_hours = parseInt(other_pre.substring(other_pre.lastIndexOf(" ") + 1));
        if (self_hours == other_hours) {
          return !this.duration.includes("Concentration") && other.duration.includes("Concentration");
        }
        return self_hours < other_hours;
      } else {
        return true;
      }
    }
    if (other.duration.includes("hour")) {
      return false;
    }
    // detect "day"
    if (this.duration.includes("day")) {
      // get the index of day
      var index_self = this.duration.indexOf("day");
      // get the number of days
      var self_pre = this.duration.substring(0, index_self - 1);
      // remove anything before the number of days (such as "up to")
      var self_days = parseInt(self_pre.substring(self_pre.lastIndexOf(" ") + 1));
      // same thing for other
      if (other.duration.includes("day")) {
        var index_other = other.duration.indexOf("day");
        var other_pre = other.duration.substring(0, index_other - 1);
        var other_days = parseInt(other_pre.substring(other_pre.lastIndexOf(" ") + 1));
        if (self_days == other_days) {
          return !this.duration.includes("Concentration") && other.duration.includes("Concentration");
        }
        return self_days < other_days;
      } else {
        return true;
      }
    }
    if (other.duration.includes("day")) {
      return false;
    }
    return self < other;
  }
}

// compares two rows, first by the primary sort column, then by the level column
function compare(a_primary, b_primary, a_level, b_level, headerName) {
    if (headerName == "Range") {
      a_primary = new Range(a_primary);
      b_primary = new Range(b_primary);
    } else if (headerName == "Casting Time") {
      a_primary = new CastingTime(a_primary);
      b_primary = new CastingTime(b_primary);
    } else if (headerName == "Duration") {
      a_primary = new Duration(a_primary);
      b_primary = new Duration(b_primary);
    } else {
      a_primary = new OtherDDD(a_primary);
      b_primary = new OtherDDD(b_primary);
    }
    if (a_primary.lt(b_primary)) {
      return -1;
    } else if (b_primary.lt(a_primary)) {
      return 1;
    }
    if (a_level < b_level) {
      return -1;
    }
    if (b_level < a_level) {
      return 1;
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
