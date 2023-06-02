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

        var paladin_color = "#f5dab1"
        var sorcerer_color = "#b1d9f5"
        var bard_color = "#d9b1f5"

        // hide sidebar when class is changed
        $("#close-sidebar").attr("hidden", true);
        $("#sidebar-text").attr("hidden", true);
        $("#spell-title").attr("hidden", true);
        $("#sidebar").attr("hidden", true);

        if (selected == "Select Class") {
            $("#sidebar").attr("hidden", true);
            $("#table-content").attr("hidden", true);
            $("#default-text").removeAttr("hidden");
            $("#filters").attr("hidden", true);
            $("body").css("background-color", "#f9f7ed");
        } else {
            $("#sidebar").removeAttr("hidden");
            $("#sidebar-text").attr("hidden", true);
            $("#sidebar-default-text").removeAttr("hidden");
            $("#table-content").removeAttr("hidden");
            $("#default-text").attr("hidden", true);
            $("#filters").removeAttr("hidden");
            if (selected == "Paladin") {
                document.getElementsByClassName("scrollit")[0].id = "paladin";
                $("#fullCaster").attr("hidden", true);
                $("body").css("background-color", paladin_color);
            } else if (selected == "Sorcerer") {  
                document.getElementsByClassName("scrollit")[0].id = "sorcerer";
                $("#fullCaster").removeAttr("hidden");
                $("body").css("background-color", sorcerer_color);
            } else if (selected == "Bard") {
                document.getElementsByClassName("scrollit")[0].id = "bard";
                $("#fullCaster").removeAttr("hidden");
                $("body").css("background-color", bard_color);
            }
        }
    });
}
