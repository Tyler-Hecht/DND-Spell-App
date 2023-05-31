function classChange(select) {
    var selected = select.options[select.selectedIndex].value;
    $.get("/class/" + selected, function(data) {
        // Update the table content without changing the URL
        $("#table-content").html(data);
        // make sidebar visible
        if (selected != "Select Class") {
            $("#sidebar-text").removeAttr("hidden");
        } else {
            $("#sidebar-text").attr("hidden", true);
        }
        // change title
        if (selected != "Select Class") {
            $("#title").html("<h3>" + selected + " Spells</h3>");
        } else {
            $("#title").html("<h3>DND Spells</h3>");
        }

        // hide sidebar when class is changed
        $("#close-sidebar").attr("hidden", true);
        $("#sidebar-text").html("Click on a spell to see more information.");

        if (selected == "Select Class") {
            $("#table-content").attr("hidden", true);
            $("#default-text").removeAttr("hidden");
            $("#filters").attr("hidden", true);
            $("body").css("background-color", "#f9f7ed");
        } else {
            $("#table-content").removeAttr("hidden");
            $("#default-text").attr("hidden", true);
            $("#filters").removeAttr("hidden");
            if (selected == "Paladin") {
                document.getElementsByClassName("scrollit")[0].id = "paladin";
                $("#fullCaster").attr("hidden", true);
                $("body").css("background-color", "#f5dab1");
            } else if (selected == "Sorcerer") {  
                document.getElementsByClassName("scrollit")[0].id = "sorcerer";
                $("#fullCaster").removeAttr("hidden");
                $("body").css("background-color", "#b1d9f5");
            } else if (selected == "Bard") {
                document.getElementsByClassName("scrollit")[0].id = "bard";
                $("#fullCaster").removeAttr("hidden");
                $("body").css("background-color", "#d9b1f5");
            }
        }
    });
}
