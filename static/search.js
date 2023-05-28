function search() {
    formData = {
        "query": $("#search").val()
    }
    // send post request to server with search text
    $.post("/search", formData)
    .done(function(data) {
        // update table
        $("#table-content").html(data);
    });
  }
